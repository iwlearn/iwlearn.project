from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import vocabulary

class IProjectDBView(Interface):
    """
    ProjectDB view interface
    """

    def test():
        """ test method"""


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


    def get_region(self):
        """ Returns regions/subregions select """
        def sel(region):
            if selected_region == region:
                return 'selected'
            else:
                return None
        def disable(region):
            if region in active_regions:
                return None
            else:
                return 'disabled'

        active_regions = self.portal_catalog.Indexes[
                'getSubRegions'].uniqueValues()
        selected_region = self.request.get('getSubRegions',None)

        region_subregions = [{'name': 'All', 'value':'',
                'disabled':None,
                'selected':sel(None)}]
        regions = vocabulary.get_regions()
        for region in regions:
            disabled = disable(region)
            region_subregions.append({'name': region, 'value':region,
                    'disabled': disabled,
                    'selected':sel(region)})
            if disabled:
                continue
            else:
                subregions = vocabulary.get_subregions([region,])
                for subregion in subregions:
                    disabled = disable(subregion)
                    region_subregions.append({'name': ' - ' + subregion,
                            'value': subregion,
                            'disabled': disabled,
                            'selected':sel(subregion)})
        return region_subregions
