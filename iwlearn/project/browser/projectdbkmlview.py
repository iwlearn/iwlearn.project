import cgi
import logging
import ZTUtils
from time import time
from operator import itemgetter

try:
    from shapely.geometry import asShape
except ImportError:
    from pygeoif import as_shape as asShape

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view, ram, instance


from collective.geo.kml.browser.kmldocument import BrainPlacemark, NullGeometry
from collective.geo.fastkml.browser.kmldocument import FastKMLBaseDocument
from collective.geo.kml.utils import web2kmlcolor

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.browser.utils import get_query, get_color
from iwlearn.project.vocabulary import RATINGS



logger = logging.getLogger('iwlearn.project')
#logger.setLevel(logging.DEBUG)



def get_related_countries_uids(country):
    for c in country.getObject().getRelatedItems():
        yield c.UID()


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



class ProjectDbKmlView(FastKMLBaseDocument):
    """
    ProjectDbKml browser view
    """
    implements(IProjectDbKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_results(self, query):
        logger.debug('Query: %s' % str(query))
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
            title = self.context.Title() #.decode('utf-8', 'ignore')
        else:
            title = self.context.Title #.decode('utf-8', 'ignore')
        return cgi.escape(title) + '\t- %i Projects' % len(self.projects)


    @property
    def description(self):

        if self.projects:
            #desc = u'<ul>'
            #for project in self.projects:
            #    title = project['title'].decode('utf-8', 'ignore')
            #    desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (
            #            project['url'],
            #            cgi.escape(title.encode(
            #                'ascii', 'xmlcharrefreplace')),
            #            cgi.escape(title[:48].encode(
            #                'ascii', 'xmlcharrefreplace') + u'...')
            #            )
            #desc += u'</ul>'
            url = '@@project-map-view.html'
            desc ='<a href="%s#projectdetaillist">  More information below the map </a>' %url



        else:
            desc = "<p><strong>No Gef projects involved in this basin</strong></p>"
        return desc

    # Avoid getObject

    def lead_image(self, scale='thumb', css_class="tileImage"):
        return None

    @property
    def polygoncolor(self):
        if self.styles:
            color = get_color(self.styles['polygoncolor'],
                        len(self.projects))
        else:
            color = get_basin_color('#0022FF44',
                    len(self.projects))
        return web2kmlcolor(color.upper())

    def display_properties(self, document):
        return []

    @property
    def item_url(self):
        return None

class BasinResultPlacemark(BasinPlacemark):
    pass



# do not compute the centeroid of a shape every time cache it
def _centeroid_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

class ClusteredBasinPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, projects):
        super(ClusteredBasinPlacemark, self).__init__(context, request, document, [])
        shape = { 'type': context.zgeo_geometry['type'],
                'coordinates': context.zgeo_geometry['coordinates']}
        #geom = self._get_simplified_geometry(shape)
        self.geom = NullGeometry()
        #self.geom.type = geom.__geo_interface__['type']
        #self.geom.coordinates = geom.__geo_interface__['coordinates']
        self.geom.type = shape['type']
        self.geom.coordinates = shape['coordinates']

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
            title = self.context.Title() #.decode('utf-8', 'ignore')
        else:
            title = self.context.Title #.decode('utf-8', 'ignore')

        return cgi.escape(title +
                    '\t- %i Projects' % len(self.projects))

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
        try:
            self.styles = context['styles']
        except:
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
        if self.styles:
            color = get_color(self.styles['polygoncolor'], len(self.projects))
        else:
            color = get_color("#a52a2a3c", len(self.projects))
        return web2kmlcolor(color.upper())


    @property
    def marker_image(self):
        return self.context['url']

    @property
    def marker_image_size(self):
        return 0.7

    @property
    def use_custom_styles(self):
        return True

    @property
    def item_type(self):
        return 'Country'

    @property
    def item_url(self):
        #return self.context['url']
        return None

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
        return cgi.escape(self.country ) + '\t- %i Projects' % len(self.projects)

    @property
    def description(self):
        #desc = u'<ul>'
        #for project in self.projects:
        #    title = project.Title.decode('utf-8', 'ignore')
        #    desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (project.getURL(),
        #                    cgi.escape(title.encode(
        #                    'ascii', 'xmlcharrefreplace')),
        #                    cgi.escape(title[:48].encode(
        #                    'ascii', 'xmlcharrefreplace') + u'...'))
        #desc += u'</ul>'
        url = '@@project-map-view.html'
        desc ='<a href="%s#projectdetaillist">  More information below the map </a>' %url
        return desc

    def lead_image(self, scale='', css_class=''):
        return '''<img src="%s/image_thumb" alt="%s"
        class="tileImage" />''' %( self.context['url'], self.country)




class CountryResultsPlacemark(CountryPlacemark):

    def __init__(self, context, request, document, country, projects):
        super(CountryResultsPlacemark, self).__init__(context, request, document, country, projects)
        result_for = self.request.form.get('result', 'rlacf')
        tmp_projects =[]
        for project in self.projects:
            obj = project.getObject()
            if result_for == 'rlacf':
                result = obj.getRegional_frameworks()
                if result != 'nap':
                    tmp_projects.append(project)
            if result_for == 'rmi':
                result = obj.getRmis()
                if result != 'nap':
                    tmp_projects.append(project)
            if result_for == 'tda':
                result = obj.getTda_priorities()
                if result != 'nap':
                    tmp_projects.append(project)
            if result_for == 'sap':
                result = obj.getSap_devel()
                if result != 'nap':
                    tmp_projects.append(project)
        if len(tmp_projects) == 0:
            self.geom = NullGeometry()
        self.projects = tmp_projects



    @property
    def description(self):
        desc = u'<ul>'
        for project in self.projects:
            obj = project.getObject()
            if obj.has_result_ratings():
                style = u"color: green;"
            else:
                style = u"color: red; text-decoration: line-through;"
            title = project.Title.decode('utf-8', 'ignore')
            desc += u'<li><a style="%s" href="%s/@@resultsview.html" title="%s" > %s </a></li>' % (
                            style,
                            project.getURL(),
                            cgi.escape(title.encode(
                            'ascii', 'xmlcharrefreplace')),
                            cgi.escape(title[:48].encode(
                            'ascii', 'xmlcharrefreplace') + u'...'))
        desc += u'</ul>'
        url = u'@@project-result-map-view.html'
        desc +=u'<a href="%s#projectdetaillist">  More information below the map </a>' %url
        return desc.encode('ascii')


    @property
    def polygoncolor(self):
        green = '#00ff00b2'
        red = '#ff0000b2'
        yellow = '#ffff00b2'
        i = 0
        result_for = self.request.form.get('result', 'rlacf')
        logger.info(result_for)
        for project in self.projects:
            obj = project.getObject()
            if result_for == 'rlacf':
                result = obj.getRegional_frameworks()
                if result and result != 'nav':
                    i+=1
            if result_for == 'rmi':
                result = obj.getRmis()
                if result and result != 'nav':
                    i+=1
            if result_for == 'tda':
                result = obj.getTda_priorities()
                if result and result != 'nav':
                    i+=1
            if result_for == 'sap':
                result = obj.getSap_devel()
                if result and result != 'nav':
                    i+=1
            #if obj.has_result_ratings():
            #    i+= 1
            #else:
            #    continue
            logger.info(result)
        if i == 0:
            ccolor = red
        elif i <  len(self.projects):
            ccolor = yellow
        else:
            ccolor = green
        #color = get_color(ccolor, len(self.projects))
        return web2kmlcolor(ccolor.upper())



# do not compute the area of a shape every time cache it
def _area_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

# fetch projects once every 10 minutes only
def _projects_cachekey(context, fun, query):
    ckey = [query, time() // (600)]
    return ckey

SHOW_BASINS=['with',]
DEFAULT_BASINS=[
    'LME',
    'Lake',
    'River',
    'Aquifer',
    #'Ocean',
    ]



class ProjectDbKmlBasinView(ProjectDbKmlView):
    """ Produces the KML File """

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
                                    brain.Title,
                                'basin': brain.getBasin,
                                'countries' : brain.getCountry,
                                'agencies': brain.getAgencies,
                                'ratings': brain.getGefRatings,
                                'url': brain.getURL()}
        return projects

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
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
                    has_projects = False
                    if basin.getRawProjects:
                        for puid in basin.getRawProjects:
                            if puid in projects:
                                has_projects = True
                    if has_projects:
                            if 'with' in show_gef_basins:
                                yield BasinPlacemark(basin, self.request,
                                                    self, projects)
                    else:
                        yield BasinPlacemark(basin, self.request, self,
                                 {})

SHOW_BBOX_RATIO = 2048

class ProjectDbKmlBasinClusterView(ProjectDbKmlBasinView):


    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
        query = get_query(self.request.form)
        logger.debug('Cluster basin view project query: %s' % str(query))
        projects = self.get_projects(query)
        path = []
        basin_query = {'portal_type':'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                shape = { 'type': basin.zgeo_geometry['type'],
                            'coordinates': basin.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area < 15.0:
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
                        has_projects = False
                        if basin.getRawProjects:
                            for puid in basin.getRawProjects:
                                if puid in projects:
                                    has_projects = True
                        if has_projects:
                            if 'with' in show_gef_basins:
                                yield ClusteredBasinPlacemark(basin, self.request,
                                    self, projects)
                        else:
                            yield ClusteredBasinPlacemark(basin, self.request,
                                    self, {})

class ProjectDbKmlBasinDetailView(ProjectDbKmlBasinView):


    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
        query = get_query(self.request.form)
        logger.debug('detail basin view project query: %s' % str(query))
        projects = self.get_projects(query)
        path = []
        basin_query = {'portal_type':'Basin'}
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
                            yield BasinPlacemark(basin, self.request, self,
                                   projects)
                            continue
                if 'without' in show_gef_basins:
                    has_projects = False
                    if basin.getRawProjects:
                        for puid in basin.getRawProjects:
                            if puid in projects:
                                has_projects = True
                    if has_projects:
                        if 'with' in show_gef_basins:
                            yield BasinPlacemark(basin, self.request, self,
                               projects)
                    else:
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
                            'styles': country.collective_geo_styles,
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
                                    'styles': country.collective_geo_styles,
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


    def get_project_countries(self, projects):
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
        project_countries = list(set(project_countries))
        return  countries, project_countries

    @property
    def features(self):
        query = get_query(self.request.form)
        projects = self.get_results(query)
        countries, project_countries = self.get_project_countries(projects)
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



class ProjectDbKmlNationalResultsView(ProjectDbKmlCountryView):

    @property
    def features(self):
        query = get_query(self.request.form)
        query['getSubRegions'] = ['National']
        query['getProject_category'] = self.request.form.get('getProject_category', 'ABNJ')
        projects = self.get_results(query)
        countries, project_countries = self.get_project_countries(projects)
        processed_countries = []
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                processed_countries += cv['replaces']
            if (ct in project_countries) and cv.get('geometry', False):
                processed_countries.append(ct)
                yield CountryResultsPlacemark(cv, self.request, self,
                                    ct, projects )
            elif ct in project_countries:
                logger.critical('Country %s is not geoannotated and has no related items' % ct)

        for c in project_countries:
            if c in processed_countries:
                continue
            else:
                logger.error('country %s not in database some projects will not be shown' % c)

class ProjectDbKmlRegionalResultsView(ProjectDbKmlBasinView):


    @property
    def features(self):
        query = get_query(self.request.form)
        query['getSubRegions'] = ['Regional']
        logger.debug('detail basin view project query: %s' % str(query))
        projects = self.get_projects(query)
        path = []
        basin_query = {'portal_type':'Basin'}
        basins = self.get_results(basin_query)
        for basin in basins:
            if basin.zgeo_geometry and basin.zgeo_geometry['coordinates']:
                if basin.getRawProjects:
                    show = False
                    for puid in basin.getRawProjects:
                        if puid in projects:
                            show = True
                    if show:
                        yield BasinPlacemark(basin, self.request, self,
                               projects)
                        continue
