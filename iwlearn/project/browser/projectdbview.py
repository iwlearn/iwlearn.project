from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import vocabulary
from iwlearn.project.browser.utils import get_query

#from collective.geo.mapwidget.interfaces import IMapView

from collective.geo.kml.interfaces import IKMLOpenLayersView

class IProjectDBView(IKMLOpenLayersView):
    """
    ProjectDB view interface
    """



class ProjectDBView(BrowserView):
    """
    ProjectDB browser view
    """
    implements(IProjectDBView)

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def get_js(self):
        js = """
 $(document).ready(function() {
   $("#projectsearchform").find("select").each(function(i) {
     $(this).change(function( objEvent ){
         $('#flexiprojects').flexOptions({newp: 1}).flexReload();
        }) ;
   });
 });



    $("#flexiprojects").flexigrid
            (
            {
            url: '@@flexijson_view',
            dataType: 'json',
            colModel : [
                {display: 'Title', name : 'Title', width : 220, sortable : true, align: 'left'},
                {display: 'Project type', name : 'getProject_type', width : 100, sortable : true, align: 'left'},
                {display: 'Implementing agencies', name : 'getAgencies', width : 220, sortable : true, align: 'left'},
                {display: 'Region', name : 'getSubRegions', width : 200, sortable : true, align: 'left'},
                {display: 'Status', name : 'getProject_status', width : 100, sortable : true, align: 'left'},
                {display: 'URL', name : 'getRemoteUrl', width : 100, sortable : false, align: 'left', hide: true}
                ],
            sortname: "Title",
            sortorder: "asc",
            usepager: true,
            title: 'Projects',
            useRp: true,
            rp: 15,
            showTableToggleBtn: true,
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
            qs = qs + field.name + '=' + field.value + "&";
            params[field.name] = field.value;
        });
        var map = cgmap.config['default-cgmap'].map;
        var kmls = map.getLayersByClass('OpenLayers.Layer.GML');
        layer = kmls[0];
        layer.setVisibility(false);
        layer.loaded = false;
        layer.setUrl('%s/@@projectdbkml_view' + qs);
        layer.refresh({ force: true, params: params });
        layer.setVisibility(true);

        return true;
    }


$('#projectsearchform').submit
(
    function ()
        {
            $('#flexiprojects').flexOptions({newp: 1}).flexReload();
            return false;
        }
);
        """ % self.context.absolute_url()
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

    def _get_index_values(self, idx):
        items = list(self.portal_catalog.Indexes[
                idx].uniqueValues())
        selected = self.request.get(idx,None)
        items.sort()
        item_list =  [{'name': _('All'), 'value':'',
                'disabled':None,
                'selected':self._sel(None,selected)}]
        for item in items:
            item_list.append({'name': item, 'value':item,
                    'disabled': None,
                    'selected':self._sel(item,selected)})
        return item_list

    def get_projecttype(self):
        return self._get_index_values('getProject_type')

    def get_agency(self):
        return self._get_index_values('getAgencies')

    def get_status(self):
        return self._get_index_values('getProject_status')

    def get_basin(self):
        return self._get_index_values('getBasin')

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

        region_subregions = [{'name': 'All', 'value':'',
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
        is_search = len(form)!=0
        if not is_search:
            return None
        batch_size = form.get('b_size', 20)
        batch_start = form.get('b_start', 0)
        query = get_query(form)
        results = self.portal_catalog(**query)

        return {'results': results, 'size': batch_size, 'start': batch_start}

