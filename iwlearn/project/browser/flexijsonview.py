from zope.interface import implements, Interface

try:
    import simplejson as json
except ImportError:
    import json

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.browser.utils import get_query

class IFlexiJsonView(Interface):
    """
    FlexiJson view interface
    """

class FlexiJsonView(BrowserView):
    """
    FlexiJson browser view
    """
    implements(IFlexiJsonView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        """
        Return JSON for flexigrid, the query form looks like:
        {'getAgencies': '', 'rp': '15', 'sortname': 'Title', 'Title': '',
        'getProject_status': '', 'getSubRegions': '', 'SearchableText': '',
        'getProject_type': '', 'sortorder': 'asc', 'query': '',
        'getBasin': '', 'qtype': 'getSubRegions', 'page': '1'}
        """
        form = self.request.form
        limit = int(form.get('rp', '15'))
        start = (int(form.get('page', '1')) - 1) * limit
        end = start + limit + 1
        query = get_query(form)
        brains = self.portal_catalog(**query)
        json_result= {"page":form.get('page', '1') ,
            "total":len(brains),
            "rows":[]}
        for brain in brains[start:end]:
            if brain.getAgencies:
                agency = ', '.join(brain.getAgencies)
            else:
                agency =''
            if brain.getSubRegions:
                region = ', '.join(brain.getSubRegions)
            else:
                region = ''
            a = u'<a href="%s">%s</a>'
            json_result['rows'].append(
                {"id":brain.getId,"cell":[
                    a % (brain.getURL(), brain.Title.decode(
                                            'utf-8', 'ignore').encode(
                                            'ascii', 'xmlcharrefreplace')),
                    brain.getProject_type ,
                    agency, region,
                    brain.getBasin,
                    brain.getProject_status
                    ]})
        self.request.RESPONSE.setHeader('Content-Type','application/json; charset=utf-8')
        return json.dumps(json_result)


