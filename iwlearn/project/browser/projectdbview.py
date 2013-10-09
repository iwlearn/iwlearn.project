import cgi
import pygal
from time import time
from zope.interface import implements, Interface

from plone.memoize import ram

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import vocabulary
from iwlearn.project.browser.utils import get_query, get_color

from collective.geo.kml.interfaces import IKMLOpenLayersView

class IProjectDBView(IKMLOpenLayersView):
    """
    ProjectDB view interface
    """

#recalculate chartdata every 10 minutes only
def _chartdata_cachekey(context, fun, form):
    ckey = [form, time() // (600)]
    return ckey


class ProjectDBBaseView(BrowserView):
    """
    ProjectDB browser view
    """


    def __init__(self, context, request):
        self.context = context
        self.request = request

    js_template = """
/*<![CDATA[*/
 $(document).ready(function() {
   $("#projectsearchform").find("select").each(function(i) {
     $(this).change(function( objEvent ){
         $('#flexiprojects').flexOptions({newp: 1}).flexReload();
        }) ;
   });
    $("#projectsearchform").find("input:checkbox").each(function(i) {
     $(this).change(function( objEvent ){
         $('#flexiprojects').flexOptions({newp: 1}).flexReload();
        }) ;
   });
 });



    $("#flexiprojects").flexigrid
            (
            {
            url: '%(url)s/@@flexijson_view',
            dataType: 'json',
            colModel : [
                {display: 'Title', name : 'Title', width : 440, sortable : true, align: 'left', hide: false},
                {display: 'Type', name : 'getProject_type', width : 30, sortable : true, align: 'left', hide: false},
                {display: 'Implementing agencies', name : 'getAgencies', width : 220, sortable : true, align: 'left', hide: false},
                {display: 'Region', name : 'getSubRegions', width : 200, sortable : true, align: 'left', hide: false},
                {display: 'Status', name : 'getProject_status', width : 100, sortable : true, align: 'left', hide: false},
                {display: 'URL', name : 'getRemoteUrl', width : 100, sortable : false, align: 'left', hide: true}
                ],
            sortname: "Title",
            sortorder: "asc",
            usepager: true,
            title: 'Projects',
            useRp: true,
            rp: 15,
            showTableToggleBtn: false,
            width: 900,
            onSubmit: addFormData,
            height: 200
            }
            );


    /*This function adds paramaters to the post of flexigrid.
    You can add a verification as well by return to false if
    you don't want flexigrid to submit function addFormData() */
    function addFormData() {
        /*passing a form object to serializeArray will get the valid data
        from all the objects, but, if the you pass a non-form object,
        you have to specify the input elements that the data will come from */
        var dt = $('#projectsearchform').serializeArray();
        $("#flexiprojects").flexOptions({params: dt});
        var qs = '';
        var params = {};
        jQuery.each(dt, function(i, field){
                qs = qs + field.name + '=' + field.value + "&";
                params[field.name] = field.value;
        });

        charts_url =  '%(url)s/@@chart_view.html?' + qs;
        jQuery.get(charts_url,
                function(data) {
                  $('#projectdbcharts').html(data);
            });

        var xp_url = '%(url)s/@@export.csv?' + qs;
        jQuery("a#excelexportlink").attr('href', xp_url);
        return true;
        };


$('#projectsearchform').submit
(
    function ()
        {
            $('#flexiprojects').flexOptions({newp: 1}).flexReload();
            return false;
        }
);
/*]]>*/
        """

    def get_js(self):
        js =  self.js_template % {'url': self.context.absolute_url()}
        return js


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def updated_projects(self):
        return self.portal_catalog(portal_type ='Project',
                review_state='published', sort_on='modified',
                sort_order='descending', sort_limt=4)[:4]

    def new_projects(self):
        return self.portal_catalog(portal_type ='Project',
                review_state='published', sort_on='created',
                sort_order='descending', sort_limt=4)[:4]



    def _sel(self, item, selected):
        if item == selected:
            return 'selected'
        else:
            return None

    def _get_index_values(self, idx, name):
        items = list(self.portal_catalog.Indexes[
                idx].uniqueValues())
        selected = self.request.get(idx,None)
        items.sort()
        item_list =  [{'name': _('Select %s' % name), 'value':'',
                'disabled':None,
                'selected':self._sel(None,selected)}]
        for item in items:
            item_list.append({'name': cgi.escape(item),
                    'value':cgi.escape(item),
                    'disabled': None,
                    'selected':self._sel(item,selected)})
        return item_list

    def get_projecttype(self):
        return self._get_index_values('getProject_type', "Project Type")

    def get_agency(self):
        return self._get_index_values('getAgencies', "Agency")

    def get_status(self):
        return self._get_index_values('getProject_status', "Project Status")

    def get_basin(self):
        return self._get_index_values('getBasin', "Basin")

    def get_country(self):
        return self._get_index_values('getCountry', "Country")


    def get_region(self):
        """ Returns regions/subregions select """
        def disable(region):
            if region in active_regions:
                return None
            else:
                return 'disabled'

        active_regions = self.portal_catalog.Indexes[
                'getSubRegions'].uniqueValues()
        selected = self.request.get('getSubRegions',None)

        region_subregions = [{'name': 'Select Region', 'value':'',
                'disabled':None,
                'selected':self._sel(None,selected)}]
        regions = vocabulary.get_regions()
        for region in regions:
            disabled = disable(region)
            region_subregions.append({'name': region, 'value':region,
                    'disabled': disabled,
                    'selected':self._sel(region,selected)})
            if disabled:
                continue
            else:
                subregions = vocabulary.get_subregions([region,])
                for subregion in subregions:
                    disabled = disable(subregion)
                    region_subregions.append({'name': ' - ' + subregion,
                            'value': subregion,
                            'disabled': disabled,
                            'selected':self._sel(subregion,selected)})
        return region_subregions


    @property
    def search_term(self):
        return self.request.form.get('SearchableText', '')

    def search_results(self):
        form = self.request.form
        batch_size = form.get('b_size', 20)
        batch_start = form.get('b_start', 0)
        query = get_query(form)
        results = self.portal_catalog(**query)

        return {'results': results, 'size': batch_size, 'start': batch_start}


    def init_ratings(self):
        rl = [['NA', 0], ['HU', 0], ['U', 0], ['MU', 0], ['MS', 0], ['S', 0],
                ['HS', 0]]
        return rl

    def acronym(self, agency):
        if agency.find('(') > -1:
            return agency[agency.find('(') +1 : agency.find(')')]
        else:
            return agency

    #@ram.cache(_chartdata_cachekey)
    def get_chart_data(self, form):
        countries = {}
        agencies = {}
        for a in list(self.portal_catalog.Indexes['getAgencies'].uniqueValues()):
           agencies[a] = 0
        doRating = self.init_ratings()
        ipRating = self.init_ratings()
        outcomeRating = self.init_ratings()
        results = self.search_results()
        regions = vocabulary.get_regions()
        regionsd = {}
        for r in regions:
            regionsd[r] = 0
        if results:
            for project in results['results']:
                for country in project.getCountry:
                    ci = countries.get(country, 0)
                    countries[country] = ci + 1
                for agency in project.getAgencies:
                    ca = agencies.get(agency, 0)
                    agencies[agency]= ca + 1
                if project.getGefRatings:
                    if project.getGefRatings[0] == None:
                        doRating[0][1] = doRating[0][1] + 1
                    else:
                        dor = project.getGefRatings[0]
                        doRating[dor+1][1] = doRating[dor+1][1] + 1

                    if project.getGefRatings[1] == None:
                        ipRating[0][1] = ipRating[0][1] + 1
                    else:
                        ipr = project.getGefRatings[1]
                        ipRating[ipr+1][1] = ipRating[ipr+1][1] + 1

                    if project.getGefRatings[2] == None:
                        outcomeRating[0][1] = outcomeRating[0][1] + 1
                    else:
                        opr = project.getGefRatings[2]
                        outcomeRating[opr+1][1] = outcomeRating[opr+1][1] + 1
                if project.getSubRegions:
                    for rsr in project.getSubRegions:
                        if rsr in regions:
                            cr = regionsd.get(rsr, 0)
                            regionsd[rsr] = cr + 1

        return {'do': doRating,
                'ip': ipRating,
                'outcome': outcomeRating,
                'countries': countries,
                'regions': regionsd,
                'agencies': agencies}

    def get_chart(self):
        desc = u''

        chartdata = self.get_chart_data(self.request.form)
        doRating = chartdata['do']
        ipRating = chartdata['ip']
        outcomeRating = chartdata['outcome']
        countries = chartdata['countries']
        regionsd = chartdata['regions']
        agencies = chartdata['agencies']

                    #na        hu        u          mu
        colors = ['#565656', '#FF0000', '#FF7F00', '#FFFF00',
                    #ms         s       hs
                    '#00FFFF', '#00FF7F', '#00FF00', '#FF007F',
                    '#0011FF']

        style = pygal.style.Style(colors=colors)

        chart = pygal.Pie(width=160, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'DO Rating'
        values = doRating
        for value in values:
            chart.add(value[0], value[1])
        desc += chart.render()

        chart = pygal.Pie(width=160, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'IP Rating'
        values = ipRating
        for value in values:
            chart.add(value[0], value[1])
        desc += chart.render()

        chart = pygal.Pie(width=160, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'TE Rating'
        values = outcomeRating
        for value in values:
            chart.add(value[0], value[1])
        desc += chart.render()


        chart = pygal.Pie(width=220, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'Regions'
        values = regionsd.items()
        values.sort()
        chart.x_labels =[]
        for value in values:
            url = self.context.absolute_url() + '?getSubRegions=' + value[0]
            chart.add(value[0], [{'value': value[1], 'label': value[0],
                    'xlink': {'href': url, 'target': '_top'}}])
            #chart.x_labels.append(value[0])
        desc += chart.render()


        chart = pygal.Pie(width=180, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'Agencies'
        values = agencies.items()
        values.sort()
        for value in values:
            url = self.context.absolute_url() + '?getAgencies=' + value[0]
            chart.add(self.acronym(value[0]),
                    [{'value': value[1], 'label': self.acronym(value[0]),
                    'xlink': {'href': url, 'target': '_top'}}])
        desc += chart.render()
        return desc


    def dorating_chart(self):
        doRating = self.init_ratings()
        results = self.search_results()
        if results:
            for project in results['results']:
                if project.getGefRatings:
                    if project.getGefRatings[0] == None:
                        doRating[0][1] = doRating[0][1] + 1
                    else:
                        dor = project.getGefRatings[0]
                        doRating[dor+1][1] = doRating[dor+1][1] + 1
        colors = ['#565656', '#FF0000', '#FF7F00', '#FFFF00',
                '#00FFFF', '#00FF7F', '#00FF00', '#FF007F',
                '#0011FF']

        style = pygal.style.Style(colors=colors)

        chart = pygal.Pie(width=160, height=240,
                explicit_size=True,
                style=style,
                disable_xml_declaration=True,
                show_legend=True)
        chart.title = 'DO Rating'
        values = doRating
        for value in values:
            chart.add(value[0], value[1])
        return chart.render()


class ProjectDBView(ProjectDBBaseView):
    implements(IProjectDBView)


class ProjectDBChartView(ProjectDBView):

    def __call__(self):
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        return self.get_chart()


class IProjectDBCountryView(IKMLOpenLayersView):
    """
    ProjectDB country view interface
    """

class ProjectDBCountryView(ProjectDBBaseView):
    implements(IProjectDBCountryView)

    def get_js(self):
        refresh_js = """
        var kmls = map.getLayersByClass('OpenLayers.Layer.GML');
        var kml_url = '%s' + qs;
        layer = kmls[0];
        layer.setVisibility(false);
        layer.loaded = false;
        layer.setUrl(kml_url);
        layer.refresh({ force: true, params: params });
        layer.setVisibility(true);
        """ % (self.context.absolute_url() + '/@@projectdbcountry_view.kml')

        js =  self.js_template % (self.context.absolute_url(), refresh_js)

        return js

    def color_style(self, n):
        color = get_color(n)
        return 'background: %s; padding: 0.5em' % color


class ProjectDBBasinView(ProjectDBBaseView):
    implements(IProjectDBCountryView)

    js_template = """
/*<![CDATA[*/
 $(document).ready(function() {
   $("#projectsearchform").find("select").each(function(i) {
     $(this).change(function( objEvent ){
         $('#flexiprojects').flexOptions({newp: 1}).flexReload();
        }) ;
   });
    $("#projectsearchform").find("input:checkbox").each(function(i) {
     $(this).change(function( objEvent ){
         $('#flexiprojects').flexOptions({newp: 1}).flexReload();
        }) ;
   });
 });



    $("#flexiprojects").flexigrid
            (
            {
            url: '%s/@@flexijson_view',
            dataType: 'json',
            colModel : [
                {display: 'Title', name : 'Title', width : 220, sortable : true, align: 'left', hide: false},
                {display: 'Project type', name : 'getProject_type', width : 100, sortable : true, align: 'left', hide: false},
                {display: 'Implementing agencies', name : 'getAgencies', width : 220, sortable : true, align: 'left', hide: false},
                {display: 'Region', name : 'getSubRegions', width : 200, sortable : true, align: 'left', hide: false},
                {display: 'Status', name : 'getProject_status', width : 100, sortable : true, align: 'left', hide: false},
                {display: 'URL', name : 'getRemoteUrl', width : 100, sortable : false, align: 'left', hide: true}
                ],
            sortname: "Title",
            sortorder: "asc",
            usepager: true,
            title: 'Projects',
            useRp: true,
            rp: 15,
            showTableToggleBtn: false,
            width: 900,
            onSubmit: addFormData,
            height: 200
            }
            );


    /*This function adds paramaters to the post of flexigrid.
    You can add a verification as well by return to false if
    you don't want flexigrid to submit function addFormData() */
    function addFormData() {
        /*passing a form object to serializeArray will get the valid data
        from all the objects, but, if the you pass a non-form object,
        you have to specify the input elements that the data will come from */
        var dt = $('#projectsearchform').serializeArray();
        $("#flexiprojects").flexOptions({params: dt});
        // refresh map
        var qs = '?';
        var params = {};
        jQuery.each(dt, function(i, field){
            if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                qs = qs + field.name + '=' + field.value + "&";
                params[field.name] = field.value;
            };
        });
        try {
            var map = $('#default-cgmap').data('collectivegeo').mapwidget.map;
        } catch(e) {
            var map = null;
        };
        if (map != null) {
            try {
            %s
            } catch (e) {

                alert("An exception occurred. Error name: " + e.name
                + ". Error message: " + e.message); };
            jQuery("a#projectkmlurl").attr('href', kml_url);
            };
        return true;
        };


$('#projectsearchform').submit
(
    function ()
        {
            $('#flexiprojects').flexOptions({newp: 1}).flexReload();
            return false;
        }
);
/*]]>*/
        """



    def get_js(self):
        refresh_js = """
        var kmls = map.getLayersByName('Basin Cluster');
        layer = kmls[0];
        kml_url = '%s' + qs;
        layer.refresh({url: kml_url});
        var kmls = map.getLayersByName('Basin Detail');
        layer = kmls[0];
        kml_url = '%s' + qs;
        layer.refresh({url: kml_url});
        kml_url = '%s' + qs;
        """ % ( self.context.absolute_url() + '/@@projectbasincluster_view.kml',
                self.context.absolute_url() + '/@@projectbasindetail_view.kml',
                self.context.absolute_url() + '/@@projectbasin_view.kml')

        js =  self.js_template % (self.context.absolute_url(), refresh_js)

        return js

class ProjectDBMapView(ProjectDBBaseView):
    implements(IProjectDBCountryView)

    box_ = '''<div style="border: 3px solid #%s; background-color: #%s;
            width: 16px; height: 16px; display: inline-block;">&nbsp;</div>'''


    def ocean_box(self):
        bc = self.context.getOo_border()
        fc = self.context.getOo_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def lme_box(self):
        bc = self.context.getLme_border()
        fc = self.context.getLme_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def river_box(self):
        bc = self.context.getRiver_border()
        fc = self.context.getRiver_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def lake_box(self):
        bc = self.context.getLake_border()
        fc = self.context.getLake_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def gw_box(self):
        bc = self.context.getGw_border()
        fc = self.context.getGw_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def country_box(self):
        bc = self.context.getCountry_border()
        fc = self.context.getCountry_fill()
        return  self.box_ % (bc[:6].upper(), fc[:6].upper())

    def get_js(self):
        refresh_js = """
        function onLayerOptionsChange(event) {
            // refresh map
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            try {
                var map = $('#default-cgmap').data('collectivegeo').mapwidget.map;
            } catch(e) {
                var map = null;
            };
            if ( map != null){
                var kmls = map.getLayersByName('Countries');
                var kml_url = '%(url)s/@@projectdbcountry_view.kml' + qs;
                layer = kmls[0];
                layer.refresh({url: kml_url});
                var kmls = map.getLayersByName('Project management offices');
                layer = kmls[0];
                kml_url = '%(url)s/@@projectdbpmo_view.kml' + qs;
                layer.refresh({url: kml_url});
            };

            onBasinLayerOptionsChange(event);
            return true;

        };

        function onBasinLayerOptionsChange(event) {
            // refresh map
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            try {
                var map = $('#default-cgmap').data('collectivegeo').mapwidget.map;
            } catch(e) {
                var map = null;
            };
            var kmls = map.getLayersByName('Basin Cluster');
            layer = kmls[0];
            kml_url = '%(url)s/@@projectbasincluster_view.kml' + qs;
            layer.refresh({url: kml_url});
            var kmls = map.getLayersByName('Basin Detail');
            layer = kmls[0];
            kml_url = '%(url)s/@@projectbasindetail_view.kml' + qs;
            layer.refresh({url: kml_url});
            refreshDownloadKmlUrl(event);
            return true;
        };

        function refreshDownloadKmlUrl(event) {
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            kml_url = '%(url)s/@@projectdblinkall_view.kml' + qs;
            jQuery("a#projectdballkmlurl").attr('href', kml_url);
        };

        function refreshFeatureDetails(layerName, featureName) {
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            if (layerName == "Countries") {
                qs = qs + 'getCountry=' + featureName
            }
            if (layerName == "Basin Detail") {
                qs = qs + 'getBasin=' + featureName
            }
            var url = '%(url)s/@@project-list-view.html' + qs;
            jQuery.get(url,
                function(data) {
                  jQuery('#featureprojectdetails').html(data);
            });
        };
        """ % {'url': self.context.absolute_url()}
        return refresh_js


class ProjectDBResultMapView(ProjectDBMapView):

    def get_js(self):
        refresh_js = """
        function onPraLayerOptionsChange(event) {
            // refresh map
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            try {
                var map = $('#default-cgmap').data('collectivegeo').mapwidget.map;
            } catch(e) {
                var map = null;
            };
            var kmls = map.getLayersByName('National Results');
            layer = kmls[0];
            kml_url = '%(url)s/@@projectdbnationalresults_view.kml' + qs;
            layer.refresh({url: kml_url});
            var kmls = map.getLayersByName('Regional Results');
            layer = kmls[0];
            kml_url = '%(url)s/@@projectdbregionalresults_view.kml' + qs;
            layer.refresh({url: kml_url});
            return true;

        };


        function refreshDownloadKmlUrl(event) {
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            kml_url = '%(url)s/@@projectdblinkall_view.kml' + qs;
            jQuery("a#projectdballkmlurl").attr('href', kml_url);
        };

    function refreshFeatureDetails(layerName, featureName) {
            var dt = $('#projectmapform').serializeArray();
            var qs = '?';
            var params = {};
            jQuery.each(dt, function(i, field){
                if (field.name.substring(0,25) != 'cgmap_state.default-cgmap') {
                    qs = qs + field.name + '=' + field.value + "&";
                    params[field.name] = field.value;
                };
            });
            if (layerName == "National Results") {
                qs = qs + 'getCountry=' + featureName
            };
            if (layerName == "Regional Results") {
                qs = qs + 'getBasin=' + featureName
            };
            var url = '%(url)s/@@project-list-view.html' + qs;
            jQuery.get(url,
                function(data) {
                  jQuery('#featureprojectdetails').html(data);
            });
        };



        """ % {'url': self.context.absolute_url()}
        return refresh_js



class IProjectDBListView(Interface):
    """ Marker Interface """

class ProjectDBListView(BrowserView):
    """ Returns html snippet for project map view when a feature
    is clicked"""
    implements(IProjectDBListView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def search_results(self):
        form = self.request.form
        if 'getCountry' in form:
            if form['getCountry'] == 'Global':
                form.pop('getCountry')
                form['getSubRegions'] = 'Global'

        query = get_query(form)
        query['sort_on'] = 'start'
        query['sort_order'] = 'reverse'
        results = self.portal_catalog(**query)
        return results

    def feature_name(self):
        form = self.request.form
        if 'getCountry' in form:
            return form['getCountry']
        elif 'getBasin' in form:
            return form['getBasin']
        elif 'getSubRegions' in form:
            return form['getSubRegions']
        else:
            return 'N/A'

