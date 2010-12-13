from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

from collective.geo.contentlocations.interfaces import IGeoManager

class IProjectView(Interface):
    """
    Project view interface
    """


class ProjectView(BrowserView):
    """
    Project browser view
    """
    implements(IProjectView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    subfolder_template = ViewPageTemplateFile("listing.pt")
    def render_subfolder_listing(self,folder=None):
        """ Render a listing of folder
        @return: Resulting HTML code as Python string
        """
        obj = None
        listing = None
        type_filter = {"portal_type" : ["Folder", "File", "Image", "Link",
                                        "NewsItem", "Event", "Document",
                                        "Topic", "FeedFeederItem",
                                        "FeedfeederFolder"]}
        if folder == None:
            obj = folder = self.context
        if folder.portal_type in ["Folder","Project", "FeedfeederFolder", "Topic"]:
            if not obj:
                obj = folder.getObject()
            listing = obj.getFolderContents(contentFilter=type_filter)
        return self.subfolder_template(listing=listing)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def is_geo_referenced(self):
        geo = IGeoManager(self.context)
        if geo.isGeoreferenceable():
            pass
            return True
        else:
            return False
