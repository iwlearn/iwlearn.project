from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _


class ILegalFWView(Interface):
    """
    LegalFW view interface
    """


class LegalFWView(BrowserView):
    """
    LegalFW browser view
    """
    implements(ILegalFWView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def get_basin_projects(self):
        basins = self.context.getField('basin').get(context)
        projects = []
        brains = self.portal_catalog(portal_type='Project', getBasin=basins)
        for brain in brains:
            projects.append({'title': brain.Title, 'url': brain.getURL(), })
        return projects

    def get_country_projects(self):
        countries = self.context.getField('country').get(context)
        projects = []
        brains = self.portal_catalog(portal_type='Project', getCountry=countries)
        for brain in brains:
            projects.append({'title': brain.Title,
                        'url': brain.getURL(),
                        })
        return projects

class ILegalFWFolderView(Interface):
    """
    LegalFW view interface
    """


class LegalFWFolderView(BrowserView):
    """
    LegalFW browser view
    """
    implements(ILegalFWFolderView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


