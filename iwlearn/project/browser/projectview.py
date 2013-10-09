import random
import urllib2
import pygal
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

from collective.geo.contentlocations.interfaces import IGeoManager

import logging
logger = logging.getLogger('iwlearn.project.projectview')

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


    def get_pra_chart(self, disable_xml_declaration=True):
        ratings = [
        ('Establishment of country-specific inter-ministerial committees', [self.context.r4imcs()]),
        ('Regional legal agreements and cooperation frameworks', [self.context.r4regional_frameworks()]),
        ('Regional Management Institutions', [self.context.r4rmis()]),
        ('National/Local reforms', [self.context.r4reforms()]),
        ('Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes', [self.context.r4tda_priorities()]),
        ('Development of Strategic Action Plan', [self.context.r4sap_devel()]),
        ('Management measures in ABNJ incorporated in Global/Regional Management Organizations', [self.context.r4abnj_rmi()]),
        ('Revised TDA/ SAP including Climatic Variability and Change considerations', [self.context.r4tdasap_cc()]),
        ('TDA based on multi-national, interdisciplinary technical and scientific activities', [self.context.r4tda_mnits()]),
        ('Proportion of countries that have adopted SAP', [self.context.r4sap_adopted()]),
        ('Proportion of countries that are implementing specific measures from the SAP ', [self.context.r4sap_implementing()]),
        ('Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc.', [self.context.r4sap_inc()]),
        ]
        colors = []
        for rating in ratings:
            colors.append(rating[1][0]['style']['color'])

        config = pygal.Config()
        config.tooltip_font_size=10
        style = pygal.style.Style(
                        colors=colors,
                        background='white',
                        plot_background='rgba(0, 0, 255, 0.1)',
                        foreground='rgba(0, 0, 0, 0.7)',
                        foreground_light='rgba(0, 0, 0, 0.9)',
                        )

        chart = pygal.Bar(config, width=800, height=400,
                    explicit_size=True,
                    style=style,
                    disable_xml_declaration=disable_xml_declaration,
                    show_legend=True,
                    truncate_legend=30,)
        chart.range = [-1, 4]
        #chart.y_labels = [0, 1, 2, 3, 4]
        for rating in ratings:
            chart.add(rating[0], rating[1])
        return chart.render()


class ProjectResultView(ProjectView):
    ''' Display the project resultsarchive data '''


class ProjectResultChart(ProjectView):
    ''' Display the project resultsarchive chart as an svg file '''

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type',
            'image/svg+xml; charset=utf-8' )
        return self.get_pra_chart(False)


class GetProjectWebsiteCapture(ProjectView):

    def __call__(self):
        if self.context.getWebsite_thumb():
            self.request.RESPONSE.setHeader('Content-Type', 'image/jpg')
            return self.context.getWebsite_thumb().data
        else:
            if self.context.getRemoteUrl():
                api_url="http://api.snapito.com/web/9f423f1c3628556e3baffbd189a0fc14650d3a3b/mc?url=%s"
                try:
                    data = urllib2.urlopen(api_url % self.context.getRemoteUrl()).read()
                except Exception, e:
                    logger.error(str(e))
                    reason = "Upstream server returned: %s" % str(e)
                    self.request.RESPONSE.setHeader('Content-Type', 'text/plain')
                    self.request.RESPONSE.setStatus(500, reason)
                    return 'Could not get website screenshot: %s ' % reason
                self.context.setWebsite_thumb(data)
                self.request.RESPONSE.setHeader('Content-Type', 'image/jpg')
                return self.context.getWebsite_thumb().data




