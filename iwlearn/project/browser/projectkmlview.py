from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark

class IProjectKMLView(Interface):
    """
    ProjectKML view interface
    """


class ProjectKMLView(KMLBaseDocument):
    """
    ProjectKML browser view
    """
    implements(IProjectKMLView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    @property
    def features(self):
        path = '/'.join(self.context.getPhysicalPath())
        portal_catalog = self.portal_catalog
        results = portal_catalog(path=path, Subject='map-layer')
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)


class ProjectCountryKMLView(ProjectKMLView):

    @property
    def features(self):
        project = self.context
        project_countries=[]
        if project.getCountry():
            project_countries = project.getCountry()
        countries = self.portal_catalog(portal_type = 'Image',
                        path='iwlearn/images/countries/')
        for country in countries:
            if ((country.Title in project_countries) and
                country.zgeo_geometry):
                yield BrainPlacemark(country, self.request, self)
