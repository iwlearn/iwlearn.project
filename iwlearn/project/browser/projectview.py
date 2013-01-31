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

    @property
    def get_wburl(self):
        wb_url = 'http://www.worldbank.org/projects/P%06d/gef-project?lang=en'
        try:
            wb_id = int(self.context.getWb_project_id())
        except:
            return None
        if wb_id:
            return wb_url % wb_id




    def rnd_picture(self):
        results = self.portal_catalog(portal_type=['Image'],
                        path='/'.join(self.context.getPhysicalPath()),
                        review_state=['published',])
        if results:
            return random.choice(results)


    #def get_rating_chart(self):
        #chart = pygal.Bar(width=400, height=200,
                    #explicit_size=True,
                    #disable_xml_declaration=True,
                    #show_legend=True)
        #ratings = self.context.get_normalized_ratings()
        #chart.add('Rating', ratings)
        #notapplicable =[None, None]
        #for rating in ratings[2:]:
            #if rating == 0:
               #notapplicable.append(5)
            #else:
                #notapplicable.append(None)
        #chart.add('N/A', notapplicable)
        #chart.range = [0, 10]
        #chart.x_labels = ['DO', 'IP', 'IMC', 'RF', 'RMI', 'LR', 'TDA', 'SAP']
        #return chart.render()


    def get_pra_chart(self):
        ratings = [
        ('IMC', [self.context.r4imcs()]),
        ('Frameworks', [self.context.r4regional_frameworks()]),
        ('RMI', [self.context.r4rmis()]),
        ('Reforms', [self.context.r4reforms()]),
        ('TDA', [self.context.r4tda_priorities()]),
        ('SAP', [self.context.r4sap_devel()]),
        ('ABNJ', [self.context.r4abnj_rmi()]),
        ('CC in TDA/SAP', [self.context.r4tdasap_cc()]),
        #('MNITS', [self.context.r4tda_mnits()]),
        ('SAP adopted', [self.context.r4sap_adopted()]),
        ('SAP implementing', [self.context.r4sap_implementing()]),
        ('SAP inc.', [self.context.r4sap_inc()]),
        ]
        colors = []
        for rating in ratings:
            colors.append(rating[1][0]['style']['color'])

        style = pygal.style.Style(colors=colors)

        chart = pygal.Bar(width=600, height=300,
                    explicit_size=True,
                    style=style,
                    disable_xml_declaration=True,
                    show_legend=True)
        chart.range = [0, 4]
        chart.y_labels = [0, 1, 2, 3, 4]
        #chart.x_labels = ['IMC', 'Frameworks', 'RMI', 'Reforms', 'TDA', 'SAP'
        #    'ABNJ', 'CC', 'SAP inc']
        for rating in ratings:
            chart.add(rating[0], rating[1])

        return chart.render()


class ProjectResultView(ProjectView):
    ''' Display the project resultsarchive data '''


