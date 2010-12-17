from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark
from iwlearn.project.browser.utils import get_query

class IProjectDbKmlView(Interface):
    """
    ProjectDbKml view interface
    """


class ProjectDbKmlView(KMLBaseDocument):
    """
    ProjectDbKml browser view
    """
    implements(IProjectDbKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    @property
    def features(self):
        query = get_query(self.request.form)
        results = self.portal_catalog(**query)
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)
