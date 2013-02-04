import logging
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark

logger = logging.getLogger('iwlearn.project')

def get_related_countries_uids(country):
    for c in country.getObject().getRelatedItems():
        yield c.UID()


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
        path += '/maps_graphics'
        portal_catalog = self.portal_catalog
        results = portal_catalog(path=path)
        for brain in results:
            try:
                if brain.zgeo_geometry['coordinates']:
                    yield BrainPlacemark(brain, self.request, self)
            except:
                pass


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
                if country.zgeo_geometry['coordinates']:
                    yield BrainPlacemark(country, self.request, self)
                    continue
            if country.Title in project_countries:
                # the country is there but has no coordinates => cs
                related_countries = list(get_related_countries_uids(country))
                logger.debug('Country %s is not geoannotated' % country.Title)
                for rel_country in self.portal_catalog(portal_type = 'Image',
                            path='iwlearn/images/countries/',
                            UID = related_countries):
                    logger.debug('replacing with %s' % rel_country.Title)
                    yield  BrainPlacemark(rel_country, self.request, self)


class ProjectBasinKMLView(ProjectKMLView):

    @property
    def features(self):
        project = self.context
        project_countries = []
        project_basins = None
        if project.getBasin():
            project_basins = project.getRawBasins()
        if project_basins:
            basins = self.portal_catalog(UID=project_basins)
            for basin in basins:
                yield BrainPlacemark(basin, self.request, self)

