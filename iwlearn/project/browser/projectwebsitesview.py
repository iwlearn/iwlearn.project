from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

from projectdbview import ProjectDBView
from iwlearn.project.browser.utils import get_query

class IProjectWebsitesView(Interface):
    """
    ProjectWebsites view interface
    """


class ProjectWebsitesView(ProjectDBView):
    """
    ProjectWebsites browser view
    """
    implements(IProjectWebsitesView)

    def get_websites(self):
        form = self.request.form
        results = []
        query = get_query(form)
        for brain in self.portal_catalog(**query):
            if brain.getRemoteUrl:
                results.append(brain)
        return results
