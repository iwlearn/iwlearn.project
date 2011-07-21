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

class CountryPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, country, projects):
        super(CountryPlacemark, self).__init__(context, request, document)
        self.country = country
        self.projects = []
        if country == 'Global':
            for project in projects:
                if project.getSubRegions:
                    if self.country in project.getSubRegions:
                        self.projects.append(project)
        else:
            for project in projects:
                if project.getCountry:
                    if self.country in project.getCountry:
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
        return self.context.Title + ' - %i Projects' % len(self.projects)

    @property
    def description(self):
        desc = '<ul>'
        try:
            for project in self.projects:
                desc += '<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                                cgi.escape(project.Title),
                                cgi.escape(project.Title[:32] + '...'))
        except Exception, err:
            desc += str(err)
        desc += '</ul>'
        return desc



class ProjectDbKmlCountryView(ProjectDbKmlView):

    @property
    def features(self):
        #bbox = self.request.form.get('bbox')
        #import ipdb; ipdb.set_trace()
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
        countries = self.portal_catalog(portal_type = 'Image', path='iwlearn/images/countries/')
        country_names = []
        geo_annotated_countries =[]
        for country in countries:
            if ((country.Title in project_countries) and
                country.zgeo_geometry):
                geo_annotated_countries.append(country.Title)
                if country.Title in country_names:
                    logger.info('skipped: %s : %s' % (country.getId, country.Title ))
                    continue
                else:
                    yield CountryPlacemark(country, self.request, self,
                                country.Title, projects )
                country_names.append(country.Title)
        for c in project_countries:
            if c in geo_annotated_countries:
                continue
            else:
                logger.critical('country %s not in database some projects will not be shown' % c)
