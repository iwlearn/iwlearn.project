from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _


class IProjectWebsitesView(Interface):
    """
    ProjectWebsites view interface
    """


class ProjectWebsitesView(BrowserView):
    """
    ProjectWebsites browser view
    """
    implements(IProjectWebsitesView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_websites(self):
        portal_catalog = self.portal_catalog
        path = path = '/'.join(self.context.getPhysicalPath())
        results = []
        for brain in portal_catalog(path=path, portal_type='Project',
                review_state='published', sort_on='sortable_title'):
            if brain.getRemoteUrl:
                results.append(brain)
        return results
