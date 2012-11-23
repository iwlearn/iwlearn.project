"""Definition of the Project content type
"""
import logging

from zope.interface import implements


from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATExtensions.widget.url import UrlWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget



from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IProject
from iwlearn.project.config import PROJECTNAME
from iwlearn.project import vocabulary


logger = logging.getLogger('iwlearn.project')

ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((


    atapi.ImageField('logo_image',
        max_size = (64, 64),
        widget=atapi.ImageWidget(label=_(u'Logo'),
                        description=_(u'The project logo')),
        validators=('isNonEmptyFile'),
    ),

    atapi.ImageField('project_header_image',
        widget=atapi.ImageWidget(label=_(u'Header Image'),
                        description=_(u'The project header image')),
        validators=('isNonEmptyFile'),
    ),




    atapi.StringField(
        'gef_project_id',
        required=True,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"GEF Project Id"),
            description=_(u"GEF Project Id"),
        ),
        validators=('isInt',)
    ),


    atapi.StringField(
        'wb_project_id',
        required=False,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"IBRD PO ID"),
            description=_(u"Worldbank Project Id"),
        ),
         validators=('isInt',)
    ),



    atapi.StringField(
        'remote_url',
        required=False,
        searchable=False,
        widget= UrlWidget(
            label=_(u"Project Website"),
            description=_(u"Website of the project"),
        ),
        validators=('isURL'),
        accessor='getRemoteUrl',
    ),

    atapi.BooleanField(
        'globalproject',
        required=False,
        searchable=True,
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u"Global"),
            description=_(u"Indicate if the project has a global scope"),
        ),

    ),


    atapi.ComputedField(
        'region',
        required=True,
        searchable=True,
        expression = 'context._computeRegions()',
        widget=atapi.ComputedWidget(
            label=_(u"Geographic Region"),
            description=_(u"Geographic Region in which the project operates"),
        ),

    ),

    atapi.ComputedField(
        'subregion',
        required=False,
        searchable=True,
        expression = 'context._computeSubregions()',
        widget=atapi.ComputedWidget(
            label=_(u"Geographic Sub Region"),
            description=_(u"Geographic Sub Region in which the project operates"),
        ),
    ),

    atapi.LinesField(
        'country',
        required=False,
        searchable=True,
        vocabulary = vocabulary.get_countries(),
        widget=atapi.InAndOutWidget(
            label=_(u"Countries"),
            description=_(u"Countries"),
        ),
    ),


    atapi.LinesField(
        'basin',
        required=False,
        searchable=True,
        vocabulary_factory = u"iwlearn.project.basins",
        widget=AddRemoveWidget(
            label=_(u"Basin"),
            description=_(u"Basin"),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
    ),



    atapi.ReferenceField(
        'basins',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Basins"),
            description=_(u"Basins"),
            allow_sorting=True,
        ),
        relationship='basins_projects',
        allowed_types=('Basin',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'project_contacts',
        widget=ReferenceBrowserWidget(
            label=_(u"Project Contacts"),
            description=_(u"Select Project Contacts"),
        ),
        relationship='persons_project_contacts',
        allowed_types=('ContactPerson',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

    atapi.TextField(
        'project_summary',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Project Description"),
            description=_(u"Project Description"),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    #   General Information

    atapi.StringField(
        'project_type',
        required=False,
        searchable=True,
        vocabulary = vocabulary.PROJECT_TYPES,
        widget=atapi.SelectionWidget(
            label=_(u"Project Type"),
            description=_(u"Project Type"),
        ),
    ),


    atapi.StringField(
        'project_status',
        required=False,
        searchable=True,
        vocabulary = vocabulary.PROJECT_STATUS,
        widget=atapi.SelectionWidget(
            label=_(u"Project Status"),
            description=_(u"Project Status"),
        ),
    ),

    atapi.DateTimeField(
        'start_date',
        widget=atapi.CalendarWidget(
            label=_(u"Start Date"),
            description=_(u"Start Date"),
            show_hm=False,
        ),
        validators=('isValidDate'),
    ),

   atapi.DateTimeField(
        'end_date',
        widget=atapi.CalendarWidget(
            label=_(u"End date"),
            description=_(u"End date"),
            show_hm=False,
        ),
        validators=('isValidDate'),
    ),


    # GEF characteristic

    atapi.StringField(
        'gef_phase',
        required=True,
        searchable=False,
        default=u'GEF-5',
        vocabulary = vocabulary.GEF_PHASE,
        widget=atapi.SelectionWidget(
            label=_(u"GEF Phase"),
            description=_(u"GEF replenishment phase"),
        ),
    ),


    atapi.LinesField(
        'strategic_priority',
        required=False,
        searchable=True,
        #vocabulary = vocabulary.STRATEGIC_PRIORITIES,
        #widget=atapi.InAndOutWidget(
        #    label=_(u"GEF Strategic Priority"),
        #    description=_(u"GEF Strategic Priority"),
        #),
    ),

    atapi.LinesField(
        'focal_area',
        required=False,
        searchable=True,
        vocabulary = vocabulary.FOCAL_AREAS,
        widget=atapi.MultiSelectionWidget(
            label=_(u"Focal Areas"),
            description=_(u"Focal Areas"),
            format = 'checkbox',
        ),
    ),


    atapi.LinesField(
        'operational_programme',
        required=False,
        searchable=True,
        #vocabulary = vocabulary.OPERATIONAL_PROGRAMMES,
        #widget=atapi.InAndOutWidget(
        #    label=_(u"GEF Operational Programme"),
        #    description=_(u"GEF Operational Programme"),
        #),
    ),

    atapi.FixedPointField(
        'gef_project_allocation',
        widget=atapi.DecimalWidget(
            label=_(u"GEF Allocation to project"),
            description=_(u"GEF Allocation to project in Million $US"),
        ),
        validators=('isDecimal'),
    ),

    atapi.FixedPointField(
        'total_cost',
        widget=atapi.DecimalWidget(
            label=_(u"Total Cost"),
            description=_(u"Total Cost in Million $US"),
        ),
        validators=('isDecimal'),
    ),


    # Partners


    atapi.ReferenceField(
        'leadagency',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Lead Implementing Agency"),
            description=_(u"Lead Implementing Agency"),
            base_query={'Subject':'Lead Implementing Agency'},
        ),
        relationship='leadagency_project',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),

    atapi.ReferenceField(
        'other_implementing_agency',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Other Implementing Agencies"),
            description=_(u"Other Implementing Agencies"),
            base_query={'Subject':'Implementing Agency'},
            allow_sorting=True,
        ),
        relationship='other_implementing_project',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'executing_agency',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Executing Agencies"),
            description=_(u"Executing Agencies"),
            #base_query={'Subject':'Executing Agency'},
            allow_browse=True,
            allow_sorting=True,
        ),
        relationship='executing_agency_project',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'other_partners',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Other Partners"),
            description=_(u"Other agencies or institutions involved in the project"),
            allow_browse=True,
            allow_sorting=True,
        ),
        relationship='other_partner_project',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),



    atapi.IntegerField( 'iprating',
        required = False,
        vocabulary_factory = u"iwlearn.project.ratings",
        widget = atapi.SelectionWidget(
            label = u'IP Rating',
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isInt',)
    ),


    atapi.IntegerField( 'dorating',
        required = False,
        vocabulary_factory = u"iwlearn.project.ratings",
        widget = atapi.SelectionWidget(
            label = u'DO Rating',
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isInt',)
    ),

    # geographical info only for historical reasons - replaced with collective.geo

    atapi.FloatField(
        'longitude',
        widget=atapi.DecimalWidget(
            label=_(u"Longitude"),
            description=_(u"Longitude of an marker on map"),
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
        validators=('isDecimal'),
    ),


    atapi.FloatField(
        'latitude',
        widget=atapi.DecimalWidget(
            label=_(u"Latitude"),
            description=_(u"Latitude of an marker on map"),
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
        validators=('isDecimal'),
    ),

# project result ratings:

    atapi.IntegerField( 'csim_committees',
        label=_(u"Establishment of country-specific inter-ministerial committees"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),

    atapi.IntegerField( 'regional_frameworks',
        label=_(u"Regional legal agreements and cooperation frameworks"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),
    atapi.IntegerField( 'rmis',
        label=_(u"Regional Management Institutions"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),
    atapi.IntegerField( 'reforms',
        label=_(u"National/Local reforms"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),
    atapi.IntegerField( 'tda_priorities',
        label=_(u"Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),

    atapi.IntegerField( 'sap_devel',
        label=_(u"Development of Strategic Action Plan (SAP)"),
        description=_(u""),
        required = False,
        validators=('isInt',)
    ),



))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)

ProjectSchema['relatedItems'].widget.visible['edit'] = 'visible'

class Project(folder.ATFolder):
    """GEF IW Project"""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    def _computeRegions(self):
        if self.getGlobalproject():
            return ','.join(vocabulary.get_regions(
                    countries=self.getCountry(),
                    regions=[u'Global']))
        else:
             return ','.join(vocabulary.get_regions(
                    countries=self.getCountry()))

    def _computeSubregions(self):
        return ','.join(vocabulary.get_subregions(
                countries=self.getCountry()))


    def getSubRegions(self):
        """ get region + subregion for indexing """
        countries=self.getCountry()
        if countries:
            sr = vocabulary.get_subregions(countries=countries)
            if self.getGlobalproject():
                r = vocabulary.get_regions(countries=countries,
                        regions=[u'Global'])
                return r + sr
            else:
                r = vocabulary.get_regions(countries=countries)
                return r + sr
        else:
            if self.getGlobalproject():
                return [u'Global',]
            else:
                logger.info('no regions found for %s' % '/'.join(
                    self.getPhysicalPath()))
                return []

    def getAgencies(self):
        """ Returns the implementing + lead agencies of the project """
        agencies = []
        la = self.getLeadagency()
        if la:
            agencies.append(la.Title())
        ias = self.getOther_implementing_agency()
        if ias:
            for ia in ias:
                agencies.append(ia.Title())
        return agencies

    def getGefRatings(self):
        """ Returns IP and DO Ratings as a tuple """
        return (self.getDorating(), self.getIprating())


    def getBasin(self):
        basins = self.getBasins()
        titles = []
        for basin in basins:
            if basin is not None:
                 titles.append(basin.Title())
        return titles

    def get_normalized_ratings(self):
        def norm4ratings(rating):
            if rating != None:
                return ((float(rating) + 1.0) / 4.0) * 10
            else:
                return None

        ratings = []
        if self.getDorating() != None:
            ratings.append(((float(self.getDorating()) + 1.0) / 6.0) * 10.0)
        else:
            ratings.append(None)
        if self.getIprating() != None:
            ratings.append(((float(self.getIprating()) + 1.0) / 6.0) * 10.0)
        else:
            ratings.append(None)

        ratings.append(norm4ratings(self.getCsim_committees()))
        ratings.append(norm4ratings(self.getRegional_frameworks()))
        ratings.append(norm4ratings(self.getRmis()))
        ratings.append(norm4ratings(self.getReforms()))
        ratings.append(norm4ratings(self.getTda_priorities()))
        ratings.append(norm4ratings(self.getSap_devel()))
        return ratings


    # -*- Your ATSchema to Python Property Bridges Here ... -*-

def reindexProjectDocuments(context, event):
    """ Project documents acquire some project attributes: project_type
        region/subregion lead/agency project_status.  This part takes
        care about reindex all project documents.
    """
    logger.info('reindexProjectDocuments')
    # Reindex project documents
    cat = getToolByName(context, 'portal_catalog')
    brains = cat.searchResults(portal_type='File',
        path='/'.join(context.getPhysicalPath()))
    for brain in brains:
        obj = brain.getObject()
        logger.info('reindex: %s' % '/'.join(obj.getPhysicalPath()))
        obj.reindexObject(idxs=['getSubRegions',
            'getAgencies', 'getBasin','getCountry',
            'getProject_status', 'getProject_type'])

    basins = context.getBasins()
    for basin in basins:
        basin.reindexObject()


atapi.registerType(Project, PROJECTNAME)
