import cgi
import logging
import ZTUtils
from time import time
from operator import itemgetter

from shapely.geometry import MultiPoint
from shapely.geometry import asShape
import pygal

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view, ram, instance


from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark, NullGeometry
from collective.geo.kml.utils import web2kmlcolor

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.browser.utils import get_query, get_color, get_basin_color
from iwlearn.project.vocabulary import RATINGS



logger = logging.getLogger('iwlearn.project')
logger.setLevel(logging.DEBUG)



def get_related_countries_uids(country):
    for c in country.getObject().getRelatedItems():
        yield c.UID()

def init_ratings():
    rl = [['NA', 0], ['HU', 0], ['U', 0], ['MU', 0], ['MS', 0], ['S', 0],
            ['HS', 0]]
    return rl


def acronym(agency):
    if agency.find('(') > -1:
        return agency[agency.find('(') +1 : agency.find(')')]
    else:
        return agency



class IProjectDbKmlView(Interface):
    """
    ProjectDbKml view interface
    """



class ProjectDBKMLLinkView(BrowserView):
    """ links pmo + basins + countries together"""
    implements(IProjectDbKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_name(self):
        return self.context.Title()

    def get_links(self):
        url = self.context.absolute_url()
        form = self.request.form
        form['bbox'] ='-180,-90,180,90'
        links = []
        qs = ZTUtils.make_query(form)
        if form.get('show-basins', None):
            links.append({'url': url + '/@@projectbasin_view.kml?' + qs,
                        'name': 'Transboundary water basins'})
        if form.get('show-pcu', None):
            links.append({'url': url + '/@@projectdbpmo_view.kml?' + qs,
                        'name': 'Location of project management offices'})
        if form.get('show-country', None):
            links.append({'url': url + '/@@projectdbcountry_view.kml?' + qs,
                        'name': 'Distribution of projects by partnering countries'})
        return links


class ProjectDbKmlView(KMLBaseDocument):
    """
    ProjectDbKml browser view
    """
    implements(IProjectDbKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_results(self, query):
        logger.info('Query: %s' % str(query))
        return self.portal_catalog(**query)


    @property
    def features(self):
        query = get_query(self.request.form)
        results = self.get_results(query)
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)

class BasinPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, projects):
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
        self.projects = []
        logger.debug("Projects for Basins %s" % str(context.getRawProjects))
        if context.getRawProjects:
            for project_uid in context.getRawProjects:
                if project_uid in projects:
                    self.projects.append(projects[project_uid])
                else:
                    if projects:
                        logger.debug('Project UID %s not found' % project_uid)

    @property
    def name(self):
        if callable(self.context.Title):
            title = self.context.Title().decode('utf-8', 'ignore')
        else:
            title = self.context.Title.decode('utf-8', 'ignore')
        return cgi.escape(title) + u' - %i Projects' % len(self.projects)


    @property
    def description(self):

        if self.projects:
            desc = u'<ul>'
            countries = {}
            agencies = {}
            doRating = init_ratings()
            ipRating = init_ratings()
            for project in self.projects:
                #for country in project['countries']:
                    #ci = countries.get(country, 0)
                    #countries[country] = ci + 1
                #for agency in project['agencies']:
                    #ca = agencies.get(agency, 0)
                    #agencies[agency]= ca + 1
                #if project['ratings'][0] == None:
                    #doRating[0][1] = doRating[0][1] + 1
                #else:
                    #dor = project['ratings'][0]
                    #doRating[dor+1][1] = doRating[dor+1][1] + 1

                #if project['ratings'][1] == None:
                    #ipRating[0][1] = ipRating[0][1] + 1
                #else:
                    #ipr = project['ratings'][1]
                    #ipRating[ipr+1][1] = ipRating[ipr+1][1] + 1


                title = project['title'].decode('utf-8', 'ignore')
                desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (
                        project['url'],
                        cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                        cgi.escape(title[:48].encode(
                            'ascii', 'xmlcharrefreplace') + u'...')
                        )
            desc += u'</ul>'

            #chart = pygal.Pie(width=150, height=180,
                    #explicit_size=True,
                    #disable_xml_declaration=True,
                    #show_legend=True)
            #chart.title = 'DO Rating'
            #values = doRating
            #for value in values:
                #chart.add(value[0], value[1])
            #desc += chart.render()

            #chart = pygal.Pie(width=150, height=180,
                    #explicit_size=True,
                    #disable_xml_declaration=True,
                    #show_legend=True)
            #chart.title = 'IP Rating'
            #values = ipRating
            #for value in values:
                #chart.add(value[0], value[1])
            #desc += chart.render()

            #desc += '<br />'

            #chart = pygal.Pie(width=150, height=150,
                    #explicit_size=True,
                    #disable_xml_declaration=True,
                    #show_legend=False)
            #chart.title = 'Countries'
            #values = countries.items()
            #values.sort()
            #for value in values:
                #chart.add(value[0], value[1])
            ##desc += chart.render()


            #chart = pygal.Pie(width=150, height=150,
                    #explicit_size=True,
                    #disable_xml_declaration=True,
                    #show_legend=True)
            #chart.title = 'Agencies'
            #values = agencies.items()
            #values.sort()
            #for value in values:
                #chart.add(acronym(value[0]), value[1])
            #desc += chart.render()


        else:
            desc = u"<p><strong>No Gef projects involved in this basin</strong></p>"
        return desc

    # Avoid getObject

    def lead_image(self, scale='thumb', css_class="tileImage"):
        return None

    @property
    def polygoncolor(self):
        if self.styles:
            color = get_basin_color(self.styles['polygoncolor'],
                        len(self.projects))
        else:
            color = get_basin_color('#0022FF44',
                    len(self.projects))
        return web2kmlcolor(color.upper())

# do not compute the centeroid of a shape every time cache it
def _centeroid_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

class ClusteredBasinPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, projects):
        super(ClusteredBasinPlacemark, self).__init__(context, request, document, [])
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
        return None


    @property
    def name(self):
        if callable(self.context.Title):
            title = self.context.Title().decode('utf-8', 'ignore')
        else:
            title = self.context.Title.decode('utf-8', 'ignore')

        return cgi.escape(title.encode('ascii','xmlcharrefreplace') +
                    u' - %i Projects' % len(self.projects))

    @property
    def use_custom_styles(self):
        return None

    def display_properties(self, document):
        return []


class CountryPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, country, projects):
        self.context = context
        self.request = request
        self.geom = NullGeometry()
        self.geom.type =  context['geometry']['type']
        self.geom.coordinates =  context['geometry']['coordinates']
        self.country = country
        self.projects = []
        self.styles = None
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
                    for substitute_for in context.get('replaces', []):
                        if substitute_for in project.getCountry:
                            logger.debug('%s in: "%s" assinged to "%s"'
                                % (project.Title,
                                    substitute_for, country))
                            self.projects.append(project)
    @property
    def polygoncolor(self):
        color = get_color(len(self.projects))
        return web2kmlcolor(color.upper())

    @property
    def use_custom_styles(self):
        return True

    @property
    def item_type(self):
        return 'Country'

    @property
    def item_url(self):
        return self.context['url']

    @property
    def author(self):
        return {
            'name': '',
            'uri': '',
            'email': ''}

    def display_properties(self, document):
        return []

    @property
    def name(self):
        return cgi.escape(self.country ) + u' - %i Projects' % len(self.projects)

    @property
    def description(self):
        desc = u'<ul>'
        for project in self.projects:
            title = project.Title.decode('utf-8', 'ignore')
            desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
                            cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                            cgi.escape(title[:48].encode(
                            'ascii', 'xmlcharrefreplace') + u'...'))
        desc += u'</ul>'
        return desc

    def lead_image(self, scale='', css_class=''):
        return '''<img src="%s/image_thumb" alt="%s"
        class="tileImage" />''' %( self.context['url'], self.country)



# do not compute the area of a shape every time cache it
def _area_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

# fetch projects once every 10 minutes only
def _projects_cachekey(context, fun, query):
    ckey = [query, time() // (600)]
    return ckey

SHOW_BASINS=['with',]

class ProjectDbKmlBasinView(ProjectDbKmlView):

    @ram.cache(_area_cachekey)
    def  _get_basin_area(self, shape):
        logger.debug('area of: %s' % shape['type'] )
        return asShape(shape).envelope.area

    @ram.cache(_projects_cachekey)
    def get_projects(self, query):
        logger.debug('get projects')
        brains = self.get_results(query)
        projects = {}
        for brain in brains:
            if brain.getBasin:
                projects[brain.UID] = {'title':
                                    brain.Title.decode('utf-8', 'ignore'
                                            ).encode('utf-8', 'ignore'),
                                'basin': brain.getBasin,
                                'countries' : brain.getCountry,
                                'agencies': brain.getAgencies,
                                'ratings': brain.getGefRatings,
                                'url': brain.getURL()}
        return projects

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        projects = self.get_projects(query)
        basin_query = {'portal_type': 'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                if 'with' in show_gef_basins:
                    if basin.getRawProjects:
                        show = False
                        for puid in basin.getRawProjects:
                            if puid in projects:
                                show = True
                        if show:
                            yield BasinPlacemark(basin, self.request,
                                self, projects)
                            continue
                if 'without' in show_gef_basins:
                    yield BasinPlacemark(basin, self.request, self,
                                 {})

SHOW_BBOX_RATIO = 2048

class ProjectDbKmlBasinClusterView(ProjectDbKmlBasinView):


    @property
    def features(self):
        if int(self.request.form.get('zoomfactor','0')) > 5:
            return
        sbbox = self.request.form.get('bbox','-180,-90,180,90')
        bbox = [float(c) for c in sbbox.split(',')]
        bbox_area = MultiPoint([bbox[:2],bbox[2:]]).envelope.area
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        logger.debug('Cluster basin view project query: %s' % str(query))
        projects = self.get_projects(query)
        path = []
        if sbbox != '-180,-90,180,90':
            basin_query = {'portal_type':'Basin',
                    'zgeo_geometry': {
                        'geometry_operator': 'intersects',
                            'query': sbbox}}
        else:
            basin_query = {'portal_type':'Basin'}

        if basin_types:
            basin_query['getBasin_type'] = basin_types
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                shape = { 'type': basin.zgeo_geometry['type'],
                            'coordinates': basin.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area < bbox_area/SHOW_BBOX_RATIO:
                    if 'with' in show_gef_basins:
                        if basin.getRawProjects:
                            show = False
                            for puid in basin.getRawProjects:
                                if puid in projects:
                                    show = True
                            if show:
                                yield ClusteredBasinPlacemark(basin,
                                    self.request, self, projects)
                                continue
                    if 'without' in show_gef_basins:
                        yield ClusteredBasinPlacemark(basin, self.request,
                                self, {})

class ProjectDbKmlBasinDetailView(ProjectDbKmlBasinView):


    @property
    def features(self):
        sbbox = self.request.form.get('bbox','-180,-90,180,90')
        bbox = [float(c) for c in sbbox.split(',')]
        bbox_area = MultiPoint([bbox[:2],bbox[2:]]).envelope.area
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        if int(self.request.form.get('zoomfactor','0')) > 5:
             bbox_area = 1
        basin_types = self.request.form.get('basintype', [])
        query = get_query(self.request.form)
        logger.debug('detail basin view project query: %s' % str(query))
        projects = self.get_projects(query)
        path = []
        if sbbox != '-180,-90,180,90':
            basin_query = {'portal_type':'Basin',
                    'zgeo_geometry': {
                        'geometry_operator': 'intersects',
                        'query': sbbox}}
        else:
            basin_query = {'portal_type':'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                shape = { 'type': basin.zgeo_geometry['type'],
                        'coordinates': basin.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area >= bbox_area/SHOW_BBOX_RATIO:
                    if 'with' in show_gef_basins:
                        if basin.getRawProjects:
                            show = False
                            for puid in basin.getRawProjects:
                                if puid in projects:
                                    show = True
                            if show:
                                yield BasinPlacemark(basin, self.request, self,
                                       projects)
                                continue
                    if 'without' in show_gef_basins:
                        yield BasinPlacemark(basin, self.request, self,
                                    {})

# fetch projects once every hour only
def _country_cachekey(method, self, **args):
    ckey = [time() // (3600)]
    return ckey

class ProjectDbKmlCountryView(ProjectDbKmlView):

    @ram.cache(_country_cachekey)
    def get_countries(self):
        def _related_countries():
            related_countries = list(get_related_countries_uids(country))
            logger.debug('Country %s is not geoannotated' % country.Title)
            is_related = False
            for rel_country in self.portal_catalog(UID = related_countries,
                            portal_type = 'Image',
                            path='iwlearn/images/countries/'):
                if rel_country.Title in geo_annotated_countries:
                    replaces = geo_annotated_countries[
                            rel_country.Title].get('replaces', [])
                else:
                    replaces = []
                replaces.append(country.Title)
                geo_annotated_countries[rel_country.Title] = {
                            'geometry': rel_country.zgeo_geometry,
                            'replaces': replaces,
                            'url': rel_country.getURL()}
                is_related = True
                logger.debug('%s  replaces %s' % (rel_country.Title, str(replaces)))
            return is_related
            # - end local functions -

        cquery = {'portal_type': 'Image',
                'path': 'iwlearn/images/countries/'}
        countries = self.get_results(cquery)
        geo_annotated_countries = {}
        for country in countries:
            if country.zgeo_geometry:
                if country.zgeo_geometry['coordinates']:
                    if country.Title in geo_annotated_countries:
                        replaces = geo_annotated_countries[
                                country.Title].get('replaces', [])
                    else:
                        replaces = []
                    geo_annotated_countries[country.Title] = {
                                    'geometry': country.zgeo_geometry,
                                    'replaces': replaces,
                                    'url': country.getURL() }
                    continue
                else:
                    # the country is there but has no coordinates => cs
                    if _related_countries():
                        continue
            else:
                if _related_countries():
                    continue
            logger.debug('Country %s is not geoannotated and has no related items' % country.Title)

        return geo_annotated_countries


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
        countries = self.get_countries()
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                for c in cv['replaces']:
                    if ((c in project_countries) and
                            (ct not in project_countries)):
                        project_countries.append(ct)


        processed_countries = []
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                processed_countries += cv['replaces']
            if (ct in project_countries) and cv.get('geometry', False):
                processed_countries.append(ct)
                yield CountryPlacemark(cv, self.request, self,
                                    ct, projects )
            elif ct in project_countries:
                logger.critical('Country %s is not geoannotated and has no related items' % ct)

        for c in project_countries:
            if c in processed_countries:
                continue
            else:
                logger.error('country %s not in database some projects will not be shown' % c)
