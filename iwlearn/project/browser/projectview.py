import random

import pygal
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
            return True
        else:
            return False


    def rnd_picture(self):
        results = self.portal_catalog(portal_type=['Image'],
                        path='/'.join(self.context.getPhysicalPath()),
                        review_state=['published',])
        if results:
            return random.choice(results)


    def get_rating_chart(self):
        chart = pygal.Bar(width=400, height=200,
                    explicit_size=True,
                    disable_xml_declaration=True,
                    show_legend=True)
        ratings = self.context.get_normalized_ratings()
        chart.add('Rating', ratings)
        notapplicable =[None, None]
        for rating in ratings[2:]:
            if rating == 0:
               notapplicable.append(5)
            else:
                notapplicable.append(None)
        chart.add('N/A', notapplicable)
        #chart.range = [0, 10]
        chart.x_labels = ['DO', 'IP', 'IMC', 'RF', 'RMI', 'LR', 'TDA', 'SAP']
        return chart.render()




