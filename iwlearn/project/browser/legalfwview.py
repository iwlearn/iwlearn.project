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


