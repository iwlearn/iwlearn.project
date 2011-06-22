from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view

from iwlearn.project import projectMessageFactory as _
from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark
from collective.geo.kml.utils import web2kmlcolor

from iwlearn.project.browser.utils import get_query

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
        for project in projects:
            if project.getCountry:
                if self.country in project.getCountry:
                    self.projects.append(project)

    @property
    def polygoncolor(self):
        r = min(255, max(5 +(10 * len(self.projects)), 16))
        g = min(255, max(255 -r, 16))
        b = 64
        color = '#%x%x%x' % (r,g,b)
        print r, g, b
        print color
        print len(self.projects)
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
                desc += '<li><a href="%s" > %s </a></li>' % (project.getURL(),
                                project.Title)
        except Exception, err:
            desc += str(err)
        desc += '</ul>'
        return desc



class ProjectDbKmlCountryView(ProjectDbKmlView):

    @property
    def features(self):
        query = get_query(self.request.form)
        projects = self.portal_catalog(**query)
        project_countries = []
        for project in projects:
            if project.getCountry:
                project_countries += project.getCountry
        project_countries = list(set(project_countries))
        countries = self.portal_catalog(portal_type = 'Image', path='iwlearn/images/countries/')
        country_names = []
        for country in countries:
            if ((country.Title in project_countries) and
                country.zgeo_geometry):
                if country.Title in country_names:
                    continue
                else:
                    yield CountryPlacemark(country, self.request, self,
                                country.Title, projects )
                country_names.append(country.Title)
