from zope.interface import implements, Interface

try:
    import simplejson as json
except ImportError:
    import json

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _


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
        query = {}
        agencies = form.get('getAgencies',None)
        if agencies:
            query['getAgencies'] = agencies
        ptitle = form.get('Title',None)
        if ptitle:
            query['Title'] = ptitle
        status = form.get('getProject_status',None)
        if status:
            query['getProject_status'] = status
        regions = form.get('getSubRegions',None)
        if regions:
            query['getSubRegions'] = regions
        text = form.get('SearchableText',None)
        if text:
            query['SearchableText'] = text
        ptype = form.get('getProject_type', None)
        if ptype:
            query['getProject_type'] = ptype
        basin = form.get('getBasin',None)
        if basin:
            query['getBasin'] = basin
        query['portal_type'] = 'Project'
        sortorder = form.get('sortorder','asc')
        if sortorder=='asc':
            sort_order = 'ascending'
        else:
            sort_order = 'descending'
        query['sort_order'] = sort_order
        sort_on = form.get('sortname')
        if sort_on=='Title':
            sort_on = 'sortable_title'
        query['sort_on'] = sort_on
        results = self.portal_catalog(**query)
        json_result= {"page":form.get('page', '1') ,
            "total":len(results),
            "rows":[]}
        for result in results[start:end]:
            if result.getAgencies:
                agency = ', '.join(result.getAgencies)
            else:
                agency =''
            if result.getSubRegions:
                region = ', '.join(result.getSubRegions)
            else:
                region = ''
            a = u'<a href="%s">%s</a>'
            json_result['rows'].append(
                {"id":result.getId,"cell":[
                    a % (result.getURL(), result.Title.decode(
                                            'utf-8', 'ignore').encode(
                                            'ascii', 'xmlcharrefreplace')),
                    result.getProject_type ,
                    agency, region,
                    result.getProject_status,
                    a % (result.getRemoteUrl, result.getRemoteUrl)
                    ]})
        self.request.RESPONSE.setHeader('Content-Type','application/json; charset=utf-8')
        return json.dumps(json_result)


