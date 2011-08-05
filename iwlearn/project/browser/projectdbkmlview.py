import cgi
import logging
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view

from iwlearn.project import projectMessageFactory as _
from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark
from collective.geo.kml.utils import web2kmlcolor

from iwlearn.project.browser.utils import get_query, get_color


logger = logging.getLogger('iwlearn.project')

def get_related_countries_uids(country):
    for c in country.getObject().getRelatedItems():
        yield c.UID()

class IProjectDbKmlView(Interface):
    """
    ProjectDbKml view interface
    """


class ProjectDbKmlView(KMLBaseDocument):
    """
    ProjectDbKml browser view
    """
    implements(IProjectDbKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    @property
    @view.memoize
    def features(self):
        query = get_query(self.request.form)
        results = self.portal_catalog(**query)
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)

class BasinPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, basin, projects):
        super(BasinPlacemark, self).__init__(context, request, document)
        self.basin = basin
        self.projects = []
        for project in projects:
            if project.getBasin:
                if self.basin in project.getBasin:
                    self.projects.append(project)

    @property
    def description(self):
        if self.projects:
            desc = u'<ul>'
            for project in self.projects:
                title = project.Title.decode('utf-8', 'ignore').encode(
                                            'ascii', 'xmlcharrefreplace')
                desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                                cgi.escape(title),
                                cgi.escape(title[:32] + '...'))
            desc += u'</ul>'
        else:
            desc = u"<p><strong>No Gef projects involved in this basin</strong></p>"
        return desc




class CountryPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, country, projects, substitute_for=None):
        super(CountryPlacemark, self).__init__(context, request, document)
        self.projects = []
        if country == 'Global':
            for project in projects:
                if project.getSubRegions:
                    if country in project.getSubRegions:
                        self.projects.append(project)
        else:
            for project in projects:
                if project.getCountry:
                    if country in project.getCountry:
                        self.projects.append(project)
                    elif substitute_for:
                        if substitute_for in project.getCountry:
                            self.projects.append(project)
    @property
    def polygoncolor(self):
        color = get_color(len(self.projects))
        return web2kmlcolor(color.upper())

    @property
    def use_custom_styles(self):
        return True


    @property
    def name(self):
        if callable(self.context.Title):
            title = self.context.Title()
        else:
            title = self.context.Title
        return cgi.escape(title) + ' - %i Projects' % len(self.projects)

    @property
    def description(self):
        desc = '<ul>'
        for project in self.projects:
            desc += '<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                            cgi.escape(project.Title),
                            cgi.escape(project.Title[:32] + '...'))
        desc += '</ul>'
        return desc



class ProjectDbKmlBasinView(ProjectDbKmlView):
    @property
    def features(self):
        #bbox = self.request.form.get('bbox')
        #import ipdb; ipdb.set_trace()
        show_gef_basins = self.request.form.get('showgefbasins', [])
        basin_types = self.request.form.get('basintype', [])
        print show_gef_basins, basin_types
        query = get_query(self.request.form)
        projects = self.portal_catalog(**query)
        project_basins = []
        for project in projects:
            if project.getBasin:
                project_basins += project.getBasin
        project_basins = list(set(project_basins))
        path = []
        if basin_types:
            for basin_type in basin_types:
                path.append('iwlearn/iw-projects/basins/' + basin_type)
        else:
            path='iwlearn/iw-projects/basins'
        basins = self.portal_catalog(portal_type = 'Document',
                path = path)
        for basin in basins:
            if basin.zgeo_geometry:
                if 'with' in show_gef_basins:
                    if basin.Title in project_basins:
                        yield BasinPlacemark(basin, self.request, self,
                                basin.Title, projects)
                if 'without' in show_gef_basins:
                    if not(basin.Title in project_basins):
                        yield BasinPlacemark(basin, self.request, self,
                                basin.Title, projects)

class ProjectDbKmlCountryView(ProjectDbKmlView):

    @property
    def features(self):
        query = get_query(self.request.form)
        projects = self.portal_catalog(**query)
        project_countries = []
        for project in projects:
            if project.getCountry:
                project_countries += project.getCountry
            if project.getSubRegions:
                if 'Global' in project.getSubRegions:
                    project_countries.append('Global')
        project_countries = list(set(project_countries))
        countries = self.portal_catalog(portal_type = 'Image',
                    path='iwlearn/images/countries/')
        geo_annotated_countries =[]
        for country in countries:
            if ((country.Title in project_countries) and
                country.zgeo_geometry):
                if country.zgeo_geometry['coordinates']:
                    geo_annotated_countries.append(country.Title)
                    yield CountryPlacemark(country, self.request, self,
                                    country.Title, projects )
                else:
                    # the country is there but has no coordinates => cs
                    related_countries = list(get_related_countries_uids(country))
                    logger.debug('Country %s is not geoannotated' % country.Title)
                    for rel_country in self.portal_catalog(portal_type = 'Image',
                                path='iwlearn/images/countries/',
                                UID = related_countries):
                        geo_annotated_countries.append(rel_country.Title)
                        geo_annotated_countries.append(country.Title)
                        logger.debug('replacing with %s' % rel_country.Title)
                        yield CountryPlacemark(rel_country, self.request, self,
                                rel_country.Title, projects, country.Title)
            elif country.Title in project_countries:
                logger.critical('Country %s is not geoannotated and has no related items' % country.Title)

        for c in project_countries:
            if c in geo_annotated_countries:
                continue
            else:
                logger.critical('country %s not in database some projects will not be shown' % c)
