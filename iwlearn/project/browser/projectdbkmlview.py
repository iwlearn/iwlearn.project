import cgi
import logging
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view, ram, instance
from time import time

from iwlearn.project import projectMessageFactory as _
from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark, NullGeometry
from collective.geo.kml.utils import web2kmlcolor


from iwlearn.project.browser.utils import get_query, get_color
from shapely.geometry import MultiPoint
from shapely.geometry import asShape

logger = logging.getLogger('iwlearn.project')
logger.setLevel(logging.DEBUG)

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

    def get_results(self, query):
        print query
        return self.portal_catalog(**query)


    @property
    def features(self):
        query = get_query(self.request.form)
        results = self.get_results(query)
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)

class BasinPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, basin, projects):
        self.context = context
        self.request = request
        shape = { 'type': context.zgeo_geometry['type'],
                'coordinates': context.zgeo_geometry['coordinates']}
        self.geom = NullGeometry()
        self.geom.type = shape['type']
        self.geom.coordinates = shape['coordinates']
        try:
            self.styles = self.context.collective_geo_styles
        except:
            self.styles = None
        self.basin = basin
        self.projects = []
        for project in projects:
            if self.basin in project['basin']:
                self.projects.append(project)

    @property
    def description(self):
        if self.projects:
            desc = u'<ul>'
            for project in self.projects:
                title = project['title'].decode('utf-8', 'ignore')
                desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (
                        project['url'],
                        cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                        cgi.escape(title[:32].encode(
                            'ascii', 'xmlcharrefreplace') + u'...')
                        )
            desc += u'</ul>'
        else:
            desc = u"<p><strong>No Gef projects involved in this basin</strong></p>"
        return desc

    # Avoid getObject

    def lead_image(self, scale='thumb', css_class="tileImage"):
        return None



# do not compute the centeroid of a shape every time cache it
def _centeroid_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

class ClusteredBasinPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, basin, projects):
        super(ClusteredBasinPlacemark, self).__init__(context, request, document, basin, [])
        shape = { 'type': context.zgeo_geometry['type'],
                'coordinates': context.zgeo_geometry['coordinates']}
        geom = self._get_simplified_geometry(shape)
        self.geom = NullGeometry()
        self.geom.type = geom.__geo_interface__['type']
        self.geom.coordinates = geom.__geo_interface__['coordinates']

    @ram.cache(_centeroid_cachekey)
    def _get_simplified_geometry(self, shape):
        logger.debug( 'center of: %s' % shape['type'])
        return asShape(shape).centroid

    @property
    def description(self):
        return u""

    @property
    def name(self):
        return u""

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
        return cgi.escape(title) + u' - %i Projects' % len(self.projects)

    @property
    def description(self):
        desc = u'<ul>'
        for project in self.projects:
            title = project.Title.decode('utf-8', 'ignore')
            desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                            cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                            cgi.escape(title[:32].encode(
                            'ascii', 'xmlcharrefreplace') + u'...'))
        desc += u'</ul>'
        return desc


# do not compute the area of a shape every time cache it
def _area_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

# fetch projects once only
def _projects_cachekey(context, fun, query):
    ckey = [query]
    return ckey



class ProjectDbKmlBasinView(ProjectDbKmlView):

    @ram.cache(_area_cachekey)
    def  _get_basin_area(self, shape):
        logger.debug('area of: %s' % shape['type'] )
        return asShape(shape).envelope.area

    @ram.cache(_projects_cachekey)
    def get_projects_basins(self, query):
        logger.debug('get projects')
        brains = self.get_results(query)
        basins = []
        projects = []
        for brain in brains:
            if brain.getBasin:
                basins += brain.getBasin
                projects.append({'title': brain.Title.decode('utf-8', 'ignore'),
                                'basin':brain.getBasin,
                                'url': brain.getURL()})
        basins = list(set(basins))
        return projects, basins

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', ['with', 'without'])
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        project, project_basins = self.get_projects_basins(query)
        path = []
        if basin_types:
            for basin_type in basin_types:
                path.append('iwlearn/iw-projects/basins/' + basin_type)
        else:
            path='iwlearn/iw-projects/basins/'
        basin_query = {'portal_type': 'Document', 'path': path}
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                if 'with' in show_gef_basins:
                    if basin.Title in project_basins:
                        yield BasinPlacemark(basin, self.request, self,
                                basin.Title, projects)
                        continue
                if 'without' in show_gef_basins:
                    if not(basin.Title in project_basins):
                        yield BasinPlacemark(basin, self.request, self,
                                basin.Title, [])

SHOW_BBOX_RATIO = 2048

class ProjectDbKmlBasinClusterView(ProjectDbKmlBasinView):


    @property
    def features(self):
        if int(self.request.form.get('zoomfactor','0')) > 5:
            return
        sbbox = self.request.form.get('bbox','-180,-90,180,90')
        bbox = [float(c) for c in sbbox.split(',')]
        bbox_area = MultiPoint([bbox[:2],bbox[2:]]).envelope.area
        show_gef_basins = self.request.form.get('showgefbasins', ['with', 'without'])
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        projects, project_basins = self.get_projects_basins(query)
        path = []
        if basin_types:
            for basin_type in basin_types:
                path.append('iwlearn/iw-projects/basins/' + basin_type)
        else:
            path='iwlearn/iw-projects/basins/'
        if sbbox != '-180,-90,180,90':
            basin_query = {'portal_type':'Document',
                    'path': path, 'zgeo_geometry': {
                    'geometry_operator': 'intersects', 'query': sbbox}}
        else:
            basin_query = {'portal_type':'Document', 'path': path}
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                shape = { 'type': basin.zgeo_geometry['type'],
                            'coordinates': basin.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area < bbox_area/SHOW_BBOX_RATIO:
                    if 'with' in show_gef_basins:
                        if basin.Title in project_basins:
                            yield ClusteredBasinPlacemark(basin, self.request, self,
                                    basin.Title, projects)
                            continue
                    if 'without' in show_gef_basins:
                        if not(basin.Title in project_basins):
                            yield ClusteredBasinPlacemark(basin, self.request, self,
                                    basin.Title, [])

class ProjectDbKmlBasinDetailView(ProjectDbKmlBasinView):


    @property
    def features(self):
        sbbox = self.request.form.get('bbox','-180,-90,180,90')
        bbox = [float(c) for c in sbbox.split(',')]
        bbox_area = MultiPoint([bbox[:2],bbox[2:]]).envelope.area
        show_gef_basins = self.request.form.get('showgefbasins', ['with', 'without'])
        #map_state= self.request.form.get('cgmap_state.default-cgmap', {'zoom': '0'})
        #if int(map_state.get('zoom', '0')) > 5:
        #    bbox_area = 1
        if int(self.request.form.get('zoomfactor','0')) > 5:
             bbox_area = 1
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        projects, project_basins = self.get_projects_basins(query)
        path = []
        if basin_types:
            for basin_type in basin_types:
                path.append('iwlearn/iw-projects/basins/' + basin_type)
        else:
            path='iwlearn/iw-projects/basins/'
        if sbbox != '-180,-90,180,90':
            basin_query = {'portal_type':'Document',
                    'path': path, 'zgeo_geometry': {
                    'geometry_operator': 'intersects', 'query': sbbox}}
        else:
            basin_query = {'portal_type':'Document', 'path': path}
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                shape = { 'type': basin.zgeo_geometry['type'],
                        'coordinates': basin.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area >= bbox_area/SHOW_BBOX_RATIO:
                    if 'with' in show_gef_basins:
                        if basin.Title in project_basins:
                            yield BasinPlacemark(basin, self.request, self,
                                    basin.Title, projects)
                            continue
                    if 'without' in show_gef_basins:
                        if not(basin.Title in project_basins):
                            yield BasinPlacemark(basin, self.request, self,
                                    basin.Title, [])

class ProjectDbKmlCountryView(ProjectDbKmlView):


    @property
    def features(self):
        query = get_query(self.request.form)
        projects = self.get_results(query)
        project_countries = []
        for project in projects:
            if project.getCountry:
                project_countries += project.getCountry
            if project.getSubRegions:
                if 'Global' in project.getSubRegions:
                    project_countries.append('Global')
        project_countries = list(set(project_countries))
        cquery = {'portal_type': 'Image',
                'path': 'iwlearn/images/countries/'}
        countries = self.get_results(cquery)
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
