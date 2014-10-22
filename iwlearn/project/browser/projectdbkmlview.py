#
import cgi
from copy import copy
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
from Products.CMFPlone.utils import safe_unicode
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


def get_ratings(obj, form):
    rt = form.get('result', None)
    if rt == 'rlacf':
        result ={'title': 'Regional legal agreements and cooperation frameworks'}
        rating = obj.r4regional_frameworks()
        rating['text'] = obj.getRegional_frameworks_desc()
    elif rt == "rmis":
        result ={'title': 'Regional Management Institutions'}
        rating = obj.r4rmis()
        rating['text'] = obj.getRmis_desc()
    elif rt == "tda":
        result ={'title': 'Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes'}
        rating = obj.r4tda_priorities()
        rating['text'] = obj.getTda_priorities_desc()
    elif rt == "sap":
        result ={'title': 'Development of Strategic Action Plan (SAP)'}
        rating = obj.r4sap_devel()
        rating['text'] = obj.getSap_devel_desc()
    else:
        rating = {'label': '???', 'description': '???', 'text': ''}
    return rating


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
        #form['bbox'] ='-180,-90,180,90'
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
        brains = self.get_results(query)
        for brain in brains:
            yield BrainPlacemark(brain, self.request, self)



class BasinPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, project_dicts):
        self.context = context
        self.request = request
        shape = {'type': context.zgeo_geometry['type'],
                'coordinates': context.zgeo_geometry['coordinates']}
        self.geom = NullGeometry()
        self.geom.type = shape['type']
        self.geom.coordinates = shape['coordinates']
        try:
            self.styles = copy(self.context.collective_geo_styles)
        except:
            self.styles = None
        self.project_dicts = []
        logger.debug("Projects for Basins %s" % str(context.getRawProjects))
        if context.getRawProjects:
            for project_uid in context.getRawProjects:
                if project_uid in project_dicts:
                    self.project_dicts.append(project_dicts[project_uid])
                else:
                    if project_dicts:
                        logger.debug('Project UID %s not found' % project_uid)
        self.project_dicts.sort(key=itemgetter('id'), reverse=True)

    @property
    def name(self):
        if callable(self.context.Title):
            title = self.context.Title() #.decode('utf-8', 'ignore')
        else:
            title = self.context.Title #.decode('utf-8', 'ignore')
        return cgi.escape(title) + '\t- %i Projects' % len(self.project_dicts)


    @property
    def description(self):

        if self.project_dicts:
            #desc = u'<ul>'
            #for project in self.project_dicts:
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
                        len(self.project_dicts))
        else:
            color = get_basin_color('#0022FF44',
                    len(self.project_dicts))
        return web2kmlcolor(color.upper())

    def display_properties(self, document):
        return []

    @property
    def item_url(self):
        return None

class BasinResultPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, project_dicts):
        super(BasinResultPlacemark, self).__init__(context, request, document, project_dicts)
        ref_cat = self.portal.reference_catalog
        for project_dict in self.project_dicts:
            obj = ref_cat.lookupObject(project_dict['uid'])
            project_dict['gefid'] = int(obj.getGef_project_id())
            project_dict['rlacf'] = obj.r4regional_frameworks()
            project_dict['rmi'] = obj.r4rmis()
            project_dict['tda'] = obj.r4tda_priorities()
            project_dict['sap'] = obj.r4sap_devel()
        self.project_dicts.sort(key=itemgetter('id'), reverse=True)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    @property
    def description(self):
        result_for = self.request.form.get('result', 'rlacf')
        desc = u''
        for project_dict in self.project_dicts:
            title = safe_unicode(project_dict['title'])
            basin = project_dict.get('basin', [])
            basin = [safe_unicode(b) for b in basin]
            basin = basin and '%s<br/>'%', '.join(basin) or ''
            result_label = project_dict[result_for]['label']
            rating = result_label and result_label+": " or ''
            rating += project_dict[result_for]['description']
            desc += u'''<h3><a href="%(url)s" title="%(alttitle)s">
                               %(title)s
                               </a></h3>
                    <p>%(basin)s
                    <em>Rating:</em> %(rating)s</p>''' % {
                    'url': '@@project-result-map-view.html#pid' + project_dict['uid'],
                    #title.encode(
                    #   'ascii', 'xmlcharrefreplace'),
                    'alttitle': "",
                    'title': title,
                    'basin': basin,
                    'rating': rating
                    }
        url = '@@project-result-map-view.html'
        desc +='<a href="%s#projectdetaillist">  More information below the map </a>' %url
        return desc.encode('ascii', 'xmlcharrefreplace')

    @property
    def polygoncolor(self):
        result_for = self.request.form.get('result', 'rlacf')
        value = self.project_dicts[0][result_for]['value']
        colors = {
            -1: '#ccddcca0',
            0: '#445544a0',
            1: '#ff0000a0',
            1.5: '#1122ffa0',
            2: '#ff7f00a0',
            3: '#ffff00a0',
            4: '#00ff00a0',
        }
        return web2kmlcolor(colors[value].upper())


# do not compute the centeroid of a shape every time cache it
def _centeroid_cachekey(context, fun, shape):
    ckey = [shape]
    return ckey

class ClusteredBasinPlacemark(BasinPlacemark):

    def __init__(self, context, request, document, project_dicts):
        super(ClusteredBasinPlacemark, self).__init__(context, request, document, project_dicts)
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
        logger.debug('center of: %s' % shape['type'])
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
                    '\t- %i Projects' % len(self.project_dicts))

    @property
    def use_custom_styles(self):
        return None

    def display_properties(self, document):
        return []


class CountryPlacemark(BrainPlacemark):

    def __init__(self, context, request, document, country, project_brains):
        self.context = context
        self.request = request
        self.geom = NullGeometry()
        self.geom.type =  context['geometry']['type']
        self.geom.coordinates =  context['geometry']['coordinates']
        self.country = country
        self.project_brains = []
        try:
            self.styles = copy(context['styles'])
        except:
            self.styles = None
        if country == 'Global':
            for brain in project_brains:
                if brain.getSubRegions:
                    if country in brain.getSubRegions:
                        self.project_brains.append(brain)
        else:
            for brain in project_brains:
                if brain.getCountry:
                    if country in brain.getCountry:
                        self.project_brains.append(brain)
                    for substitute_for in context.get('replaces', []):
                        if substitute_for in brain.getCountry:
                            logger.debug('%s in: "%s" assigned to "%s"'
                                % (brain.Title,
                                    substitute_for,
                                    country))
                            self.project_brains.append(brain)
        self.project_brains.sort(key=itemgetter('id'), reverse=True)

    @property
    def polygoncolor(self):
        if self.styles:
            color = get_color(self.styles['polygoncolor'], len(self.project_brains))
        else:
            color = get_color("#a52a2a3c", len(self.project_brains))
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
        return cgi.escape(self.country ) + '\t- %i Projects' % len(self.project_brains)

    @property
    def description(self):
        #desc = u'<ul>'
        #for brain in self.project_brains:
        #    title = brain.Title.decode('utf-8', 'ignore')
        #    desc += u'<li><a href="%s" title="%s" > %s </a></li>' % (brain.getURL(),
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

    def __init__(self, context, request, document, country, project_brains):
        super(CountryResultsPlacemark, self).__init__(
                context, request, document, country, project_brains)
        result_for = self.request.form.get('result', 'rlacf')
        tmp_project_brains =[]
        for brain in self.project_brains:
            project = brain.getObject()
            if result_for == 'rlacf':
                result = project.getRegional_frameworks()
                if result != 'nap':
                    tmp_project_brains.append(brain)
            if result_for == 'rmi':
                result = project.getRmis()
                if result != 'nap':
                    tmp_project_brains.append(brain)
            if result_for == 'tda':
                result = project.getTda_priorities()
                if result != 'nap':
                    tmp_project_brains.append(brain)
            if result_for == 'sap':
                result = project.getSap_devel()
                if result != 'nap':
                    tmp_project_brains.append(brain)
        if len(tmp_project_brains) == 0:
            self.geom = NullGeometry()
        self.project_brains = tmp_project_brains
        self.project_brains.sort(key=itemgetter('id'), reverse=True)

    @property
    def description(self):
        desc = u''
        for brain in self.project_brains:
            project = brain.getObject()
            if project.has_result_ratings():
                style = u"color: green;"
            else:
                style = u"color: red; text-decoration: line-through;"
            title = brain.Title.decode('utf-8', 'ignore')
            desc += u'<h3><a style="%s" href="%s" title="%s" > %s </a></h3>' % (
                    style,
                    '@@project-result-map-view.html#pid' + brain.UID,
                    cgi.escape(title.encode('ascii', 'xmlcharrefreplace')),
                    cgi.escape(title.encode('ascii', 'xmlcharrefreplace'))
                    )
            rating = get_ratings(project, self.request.form)
            desc += u'<br/><p>%(label)s : %(description)s</p>' % rating
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
        logger.debug(result_for)
        for brain in self.project_brains:
            project = brain.getObject()
            if result_for == 'rlacf':
                result = project.getRegional_frameworks()
                if result and result != 'nav':
                    i+=1
            if result_for == 'rmi':
                result = project.getRmis()
                if result and result != 'nav':
                    i+=1
            if result_for == 'tda':
                result = project.getTda_priorities()
                if result and result != 'nav':
                    i+=1
            if result_for == 'sap':
                result = project.getSap_devel()
                if result and result != 'nav':
                    i+=1
            #if project.has_result_ratings():
            #    i+= 1
            #else:
            #    continue
            logger.debug(result)
        if i == 0:
            ccolor = red
        elif i <  len(self.project_brains):
            ccolor = yellow
        else:
            ccolor = green
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

        project_dicts = {}
        for brain in brains:
            if brain.getBasin:
                project_dicts[brain.UID] = {
                                'title': brain.Title,
                                'uid': brain.UID,
                                'id': int(brain.id),
                                'basin': brain.getBasin,
                                'countries' : brain.getCountry,
                                'agencies': brain.getAgencies,
                                'ratings': brain.getGefRatings,
                                'url': brain.getURL()}
        return project_dicts

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
        query = get_query(self.request.form)
        project_dicts = self.get_projects(query)

        basin_query = {'portal_type': 'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types

        basin_brains = self.get_results(basin_query)
        for brain in basin_brains:
            if brain.zgeo_geometry and brain.zgeo_geometry['coordinates']:
                if 'with' in show_gef_basins:
                    if brain.getRawProjects:
                        show = False
                        for puid in brain.getRawProjects:
                            if puid in project_dicts:
                                show = True
                        if show:
                            yield BasinPlacemark(
                                    brain,
                                    self.request,
                                    self,
                                    project_dicts)
                            continue
                if 'without' in show_gef_basins:
                    has_projects = False
                    if brain.getRawProjects:
                        for puid in brain.getRawProjects:
                            if puid in project_dicts:
                                has_projects = True
                    if has_projects:
                            if 'with' in show_gef_basins:
                                yield BasinPlacemark(
                                        brain,
                                        self.request,
                                        self,
                                        project_dicts)
                    else:
                        yield BasinPlacemark(
                                brain,
                                self.request,
                                self,
                                {})

SHOW_BBOX_RATIO = 2048


class ProjectDbKmlBasinClusterView(ProjectDbKmlBasinView):

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
        query = get_query(self.request.form)
        logger.debug('Cluster basin view project query: %s' % str(query))
        project_dicts = self.get_projects(query)
        path = []

        basin_query = {'portal_type':'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types

        basin_brains = self.get_results(basin_query)
        for brain in basin_brains:
            if brain.zgeo_geometry and brain.zgeo_geometry['coordinates']:
                shape = {'type': brain.zgeo_geometry['type'],
                        'coordinates': brain.zgeo_geometry['coordinates']}
                basin_area = self._get_basin_area(shape)
                if basin_area < 15.0:
                    if 'with' in show_gef_basins:
                        if brain.getRawProjects:
                            show = False
                            for puid in brain.getRawProjects:
                                if puid in project_dicts:
                                    show = True
                            if show:
                                yield ClusteredBasinPlacemark(
                                        brain,
                                        self.request,
                                        self,
                                        project_dicts)
                                continue
                    if 'without' in show_gef_basins:
                        has_projects = False
                        if brain.getRawProjects:
                            for puid in brain.getRawProjects:
                                if puid in project_dicts:
                                    has_projects = True
                        if has_projects:
                            if 'with' in show_gef_basins:
                                yield ClusteredBasinPlacemark(
                                        brain,
                                        self.request,
                                        self,
                                        project_dicts)
                        else:
                            yield ClusteredBasinPlacemark(
                                    brain,
                                    self.request,
                                    self,
                                    {})


class ProjectDbKmlBasinDetailView(ProjectDbKmlBasinView):

    @property
    def features(self):
        show_gef_basins = self.request.form.get('showgefbasins', SHOW_BASINS)
        basin_types = self.request.form.get('basintype', DEFAULT_BASINS)
        query = get_query(self.request.form)
        logger.debug('detail basin view project query: %s' % str(query))
        project_dicts = self.get_projects(query)
        path = []

        basin_query = {'portal_type':'Basin'}
        if basin_types:
            basin_query['getBasin_type'] = basin_types

        basin_brains = self.get_results(basin_query)
        for brain in basin_brains:
            if brain.zgeo_geometry and brain.zgeo_geometry['coordinates']:
                if 'with' in show_gef_basins:
                    if brain.getRawProjects:
                        show = False
                        for puid in brain.getRawProjects:
                            if puid in project_dicts:
                                show = True
                        if show:
                            yield BasinPlacemark(
                                    brain,
                                    self.request,
                                    self,
                                    project_dicts)
                            continue
                if 'without' in show_gef_basins:
                    has_projects = False
                    if brain.getRawProjects:
                        for puid in brain.getRawProjects:
                            if puid in project_dicts:
                                has_projects = True
                    if has_projects:
                        if 'with' in show_gef_basins:
                            yield BasinPlacemark(
                                    brain,
                                    self.request,
                                    self,
                                    project_dicts)
                    else:
                        yield BasinPlacemark(
                                brain,
                                self.request,
                                self,
                                {})


# fetch projects once every hour only
def _country_cachekey(method, self, **args):
    ckey = [time() // (3600)]
    return ckey


class ProjectDbKmlCountryView(ProjectDbKmlView):

    @ram.cache(_country_cachekey)
    def get_countries(self):
        def _related_countries(country_brain):
            related_country_uids = list(get_related_countries_uids(country_brain))
            logger.debug('Country %s is not geoannotated' % country_brain.Title)
            is_related = False
            for related_country_b in self.portal_catalog(
                    UID=related_country_uids,
                    portal_type='Image',
                    path='iwlearn/images/countries/'):
                if related_country_b.Title in geo_annotated_countries:
                    replaces = geo_annotated_countries[
                            related_country_b.Title].get('replaces', [])
                else:
                    replaces = []
                replaces.append(country_brain.Title)
                geo_annotated_countries[related_country_b.Title] = {
                            'geometry': related_country_b.zgeo_geometry,
                            'styles': country_brain.collective_geo_styles,
                            'replaces': replaces,
                            'url': related_country_b.getURL()}
                is_related = True
                logger.debug('%s  replaces %s' % (related_country_b.Title, str(replaces)))
            return is_related
            # - end local functions -

        cquery = {'portal_type': 'Image',
                'path': 'iwlearn/images/countries/'}
        country_image_brains = self.get_results(cquery)
        geo_annotated_countries = {}
        for brain in country_image_brains:
            if brain.zgeo_geometry:
                if brain.zgeo_geometry['coordinates']:
                    if brain.Title in geo_annotated_countries:
                        replaces = geo_annotated_countries[
                                brain.Title].get('replaces', [])
                    else:
                        replaces = []
                    geo_annotated_countries[brain.Title] = {
                                    'geometry': brain.zgeo_geometry,
                                    'styles': brain.collective_geo_styles,
                                    'replaces': replaces,
                                    'url': brain.getURL() }
                    continue
                else:
                    # the country is there but has no coordinates => cs
                    if _related_countries(brain):
                        continue
            else:
                if _related_countries(brain):
                    continue
            logger.debug('Country %s is not geoannotated and has no related items' % brain.Title)

        return geo_annotated_countries


    def get_project_countries(self, project_brains):
        project_countries = []
        for brain in project_brains:
            if brain.getCountry:
                project_countries += brain.getCountry
            if brain.getSubRegions:
                if 'Global' in brain.getSubRegions:
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
        project_brains = self.get_results(query)
        countries, project_countries = self.get_project_countries(project_brains)
        processed_countries = []
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                processed_countries += cv['replaces']
            if (ct in project_countries) and cv.get('geometry', False):
                processed_countries.append(ct)
                yield CountryPlacemark(cv, self.request, self,
                                    ct, project_brains )
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
        query['getProject_category'] = self.request.form.get('getProject_category', 'Foundational')
        project_brains = self.get_results(query)
        countries, project_countries = self.get_project_countries(project_brains)
        processed_countries = []
        for ct, cv in countries.iteritems():
            if cv.get('replaces', False):
                processed_countries += cv['replaces']
            if (ct in project_countries) and cv.get('geometry', False):
                processed_countries.append(ct)
                yield CountryResultsPlacemark(
                        cv,
                        self.request,
                        self,
                        ct,
                        project_brains
                        )
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
        query['getProject_category'] = self.request.form.get('getProject_category', 'Foundational')
        logger.debug('detail basin view project query: %s' % str(query))
        project_dicts = self.get_projects(query)
        path = []
        basin_query = {'portal_type':'Basin'}
        basin_dicts = self.get_results(basin_query)
        for brain in basin_dicts:
            if brain.zgeo_geometry and brain.zgeo_geometry['coordinates']:
                if brain.getRawProjects:
                    for puid in brain.getRawProjects:
                        if puid in project_dicts:
                            yield BasinResultPlacemark(
                                    brain,
                                    self.request,
                                    self,
                                    project_dicts)

