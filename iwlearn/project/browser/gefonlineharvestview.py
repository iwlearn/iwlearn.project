from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import harvest

class IGefOnlineHarvestView(Interface):
    """
    GefOnlineHarvest view interface
    """

    def test():
        """ test method"""


class GefOnlineHarvestView(BrowserView):
    """
    GefOnlineHarvest browser view
    """
    implements(IGefOnlineHarvestView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def harvest_projects(self):
        projects = self.portal_catalog(portal_type ='Project')
        project_ids=[]
        new_projects=[]
        for brain in projects:
            ob = brain.getObject()
            if ob.getGef_project_id():
                project_ids.append(int(ob.getGef_project_id().strip()))
        gef_project_ids = harvest.extract_gefids_from_page(
                harvest.get_gef_iw_project_page())
        for projectid in gef_project_ids:
            if projectid in project_ids:
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                new_projects.append(pinfo)
        return new_projects

