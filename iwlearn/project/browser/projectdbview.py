from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import vocabulary

class IProjectDBView(Interface):
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
        catalog = self.portal_catalog
        ptitle = form.get('Title', None)
        ptype = form.get('getProject_type', None)
        pagency = form.get('getAgencies', None)
        pstatus = form.get('getProject_status', None)
        pbasin = form.get('getBasin', None)
        pregion = form.get('getSubRegions', None)

        batch_size = form.get('b_size', 20)
        batch_start = form.get('b_start', 0)
        is_search = len(form)!=0

        results = catalog(SearchableText=self.search_term,
                        portal_type='Project',
                        Title=ptitle,
                        getProject_type=ptype,
                        getAgencies=pagency,
                        getProject_status=pstatus,
                        getBasin=pbasin,
                        getSubRegions=pregion)

        return {'results': results, 'size': batch_size, 'start': batch_start}
