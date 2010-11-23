from zope.interface import implements, Interface, Attribute

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

# config for the projectmap viewlet with google maps
PROPERTY_SHEET = 'projectmap_properties'
PROPERTY_GOOGLE_KEYS_FIELD = 'map_google_api_keys'


class IProjectmapConfigView(Interface):
    """
    projectmap_config view interface
    """

    def googlemaps_key(self):
        """ returns google maps api key for a website"""

class ProjectmapConfigView(BrowserView):
    """
    projectmap_config browser view
    """
    implements(IProjectmapConfigView)

    def __init__(self, context, request):
        """ init view """
        self.context = context
        self.request = request
        portal_props = getToolByName(context, 'portal_properties')
        self.properties = getattr(portal_props, PROPERTY_SHEET, None)


    def _search_key(self, property_id):
        if self.properties is None:
            return None
        keys_list = getattr(self.properties, property_id, None)
        if keys_list is None:
            return None
        keys = {}
        for key in keys_list:
            url, key = key.split('|')
            url = url.strip()
            # remove trailing slashes
            url = url.strip('/')
            key = key.strip()
            keys[url] = key
        portal_url_tool = getToolByName(self.context, 'portal_url')
        portal_url = portal_url_tool()
        portal_url = portal_url.split('/')
        while len(portal_url) > 2:
            url = '/'.join(portal_url)
            if keys.has_key(url):
                return keys[url]
            portal_url = portal_url[:-1]
        return None

    def googlemaps_key(self):
        return self._search_key(PROPERTY_GOOGLE_KEYS_FIELD)
