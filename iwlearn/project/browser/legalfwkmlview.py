import cgi
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from .projectdbkmlview import ProjectDbKmlBasinView, ProjectDbKmlCountryView
from .projectdbkmlview import BasinPlacemark, CountryPlacemark

class ILegalFWKmlView(Interface):
    """
    LegalFWKml view interface
    """


class LegalFWKmlView(BrowserView):
    """
    LegalFWKml browser view
    """
    implements(ILegalFWKmlView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

class FWBasinPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, frameworks):
        super(FWBasinPlacemark, self).__init__(context, request, document, frameworks)
        obj = context.getObject()
        self.frameworks = []
        fw_uids = obj.getRawFrameworks()
        for fw in frameworks:
            if fw.UID in fw_uids:
                self.frameworks.append(fw)

    @property
    def name(self):
        if callable(self.context.Title):
            title = self.context.Title() #.decode('utf-8', 'ignore')
        else:
            title = self.context.Title #.decode('utf-8', 'ignore')
        return cgi.escape(title) + '\t- %i frameworks apply to this waterbody' % len(self.frameworks)

    @property
    def description(self):
        desc = u'<ul>'
        for framework in self.frameworks:
            title = framework.Title.decode('utf-8', 'ignore')
            if len(title) > 48:
                dots =u'...'
            else:
                dots = u''
            desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (
                    framework.getURL(),
                    cgi.escape(title.encode(
                        'ascii', 'xmlcharrefreplace')),
                    cgi.escape(title[:48].encode(
                        'ascii', 'xmlcharrefreplace') + dots)
                    )
        desc += u'</ul>'
        return desc.encode('utf-8')

class FWCountryPlacemark(CountryPlacemark):


    @property
    def name(self):
        return cgi.escape(self.country ) + '\tis member in %i frameworks' % len(self.project_brains)

    @property
    def description(self):
        desc = u'<ul>'
        for project in self.project_brains:
            title = project.Title.decode('utf-8', 'ignore')
            if len(title) > 48:
                dots =u'...'
            else:
                dots = u''
            desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                            cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                            cgi.escape(title[:48].encode(
                            'ascii', 'xmlcharrefreplace') + dots))
        desc += u'</ul>'

        return desc.encode('utf-8')

class LegalFWCountryView(ProjectDbKmlCountryView):
    implements(ILegalFWKmlView)

    @property
    def features(self):
        query = {}
        query['portal_type'] = 'LegalFW'
        frameworks = self.get_results(query)
        countries, fw_countries = self.get_project_countries(frameworks)
        processed_countries = []
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                processed_countries += cv['replaces']
            if (ct in fw_countries) and cv.get('geometry', False):
                processed_countries.append(ct)
                yield FWCountryPlacemark(cv, self.request, self,
                                    ct, frameworks)
            elif ct in fw_countries:
                logger.critical('Country %s is not geoannotated and has no related items' % ct)


class LegalFWBasinView(ProjectDbKmlBasinView):
    implements(ILegalFWKmlView)

    #XXX cache decorate this
    def get_basin_uids(self, brain):
        uids = []
        for fw in brain:
            obj = fw.getObject()
            uids += obj.getRawBasins()
        uids = list(set(uids))
        return uids

    @property
    def features(self):
        basin_types = self.request.form.get('basintype')
        query = {'portal_type': 'LegalFW'}
        frameworks = self.get_results(query)
        uids = self.get_basin_uids(frameworks)
        basin_query = {'portal_type': 'Basin', 'UID': uids}
        if basin_types:
            basin_query['getBasin_type'] = basin_types
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                yield FWBasinPlacemark(basin, self.request,
                    self, frameworks)

