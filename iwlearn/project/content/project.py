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

    atapi.StringField('project_shortname',
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u"Project short name"),
            description=_(u""),
        ),
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


    atapi.IntegerField(
        'wb_project_id',
        required=False,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"IBRD ID"),
            description=_(u"Worldbank Project Id"),
        ),
         validators=('isInt',)
    ),

    atapi.IntegerField(
        'unep_addis_project_id',
        required=False,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"UNEP ID"),
            description=_(u"Unep Addis Database Id"),
            visible={'edit': 'invisible'},

        ),
         validators=('isInt',)
    ),

    atapi.StringField(
        'unep_addis_url',
        widget=atapi.StringWidget(
            label=_(u"UNEP ADDIS URL"),
            description=_(u"Link to project in addis db"),
            visible={'edit': 'invisible'},
        ),
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

    atapi.ImageField('website_thumb',
        max_size = (160, 100),
        widget=atapi.ImageWidget(label=_(u'Website Thumbnail'),
                        description=_(u'Screenshot of the website')),
        validators=('isNonEmptyFile'),
    ),

    atapi.ComputedField(
        'globalproject',
        searchable=False,
        expression = 'context._isglobal()',
        widget=atapi.ComputedWidget(
        label=_(u"Global"),
            description=_(u"Indicate if the project has a global scope"),
        ),

    ),



    atapi.StringField(
        'project_scale',
        required=True,
        searchable=True,
        default=u"National",
        vocabulary = vocabulary.PROJECT_SCALE,
        widget=atapi.SelectionWidget(
            label=_(u"Project Scale"),
            description=_(u"Project Scale"),
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
        'ecosystem',
        required=False,
        searchable=True,
        vocabulary = vocabulary.ECOSYSTEM,
        widget=atapi.InAndOutWidget(
            label=_(u"Ecosystem"),
            description=_(u"Ecosystem"),
        ),
    ),

    atapi.LinesField(
        'project_category',
        required=False,
        searchable=True,
        vocabulary = vocabulary.PROJECT_CATEGORY,
        widget=atapi.InAndOutWidget(
            label=_(u"Project Category"),
            description=_(u"Project Category"),
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
        default=u'5',
        validators=('isInt',),
        vocabulary_factory = u"iwlearn.project.gef-phase",
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



    atapi.StringField( 'iprating',
        required = False,
        vocabulary_factory = u"iwlearn.project.ratings",
        widget = atapi.SelectionWidget(
            label = u'IP Rating',
            #visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isInt',),
        schemata = "ratings",
    ),


    atapi.StringField( 'dorating',
        required = False,
        vocabulary_factory = u"iwlearn.project.ratings",
        widget = atapi.SelectionWidget(
            label = u'DO Rating',
            #visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isInt',),
        schemata = "ratings",
    ),

    atapi.StringField( 'outcomerating',
        required = False,
        vocabulary_factory = u"iwlearn.project.ratings",
        widget = atapi.SelectionWidget(
            label = u'TE Rating',
            #visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isInt',),
        schemata = "ratings",
    ),


# project result ratings:


    atapi.StringField( 'pra_sources',
        widget=atapi.StringWidget(
            label=_(u'Information Sources'),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),


    atapi.TextField('lessons',
        widget=atapi.RichWidget(
            label=_(u"Key Lessons Learned from Project"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.TextField('key_results',
        widget=atapi.RichWidget(
            label=_(u"Key Project Results"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.TextField('impacts',
        widget=atapi.RichWidget(
            label=_(u"Catalytic Impacts"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'imcs',
        widget=atapi.StringWidget(
            label=_(u"Establishment of country-specific inter-ministerial committees"),
            description=_(u"National Inter-Ministry Committees (IMCs)"),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('imcs_desc',
        widget=atapi.RichWidget(
            label=_(u"Establishment of country-specific inter-ministerial committees"),
            description=_(u"National Inter-Ministry Committees (IMCs)"),
            #visible={'edit': 'invisible'},
        ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'regional_frameworks',
        widget=atapi.StringWidget(
            label=_(u"Regional legal agreements and cooperation frameworks"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('regional_frameworks_desc',
        widget=atapi.RichWidget(
            label=_(u"Regional legal agreements and cooperation frameworks"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'rmis',
        widget=atapi.StringWidget(
            label=_(u"Regional Management Institutions"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('rmis_desc',
        widget=atapi.RichWidget(
            label=_(u"Regional Management Institutions"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'reforms',
        widget=atapi.StringWidget(
            label=_(u"National/Local reforms"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),
    atapi.TextField('reforms_desc',
        widget=atapi.RichWidget(
            label=_(u"National/Local reforms"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'tda_priorities',
        widget=atapi.StringWidget(
            label=_(u"Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('tda_priorities_desc',
        widget=atapi.RichWidget(
            label=_(u"Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'sap_devel',
        widget=atapi.StringWidget(
            label=_(u"Development of Strategic Action Plan (SAP)"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('sap_devel_desc',
        widget=atapi.RichWidget(
            label=_(u"Development of Strategic Action Plan (SAP)"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'abnj_rmi',
        widget=atapi.StringWidget(
            label=_(u"Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('abnj_rmi_desc',
        widget=atapi.RichWidget(
            label=_(u"Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'tdasap_cc',
        widget=atapi.StringWidget(
            label=_(u"Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('tdasap_cc_desc',
        widget=atapi.RichWidget(
            label=_(u"Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'tda_mnits',
        widget=atapi.StringWidget(
            label=_(u"TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('tda_mnits_desc',
        widget=atapi.RichWidget(
            label=_(u"TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'sap_adopted',
        widget=atapi.StringWidget(
            label=_(u"Proportion of Countries that have adopted SAP"),
            description=_(u"In %. 0 = None, 100=All"),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        validators=('isInt',),
        schemata = "ratings",
    ),

    atapi.TextField('sap_adopted_desc',
        widget=atapi.RichWidget(
            label=_(u"Proportion of Countries that have adopted SAP"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'sap_implementing',
        widget=atapi.StringWidget(
            label=_(u"Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"),
            description=_(u"In %. 0 = None, 100=All"),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        validators=('isInt',),
        schemata = "ratings",
    ),

    atapi.TextField('sap_implementing_desc',
        widget=atapi.RichWidget(
            label=_(u"Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.StringField( 'sap_inc',
        widget=atapi.StringWidget(
            label=_(u"Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"),
            description=_(u""),
            #visible={'edit': 'invisible'},
        ),
        required = False,
        schemata = "ratings",
    ),

    atapi.TextField('sap_inc_desc',
        widget=atapi.RichWidget(
            label=_(u"Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
    ),

    atapi.TextField( 'key_process_results',
        widget=atapi.RichWidget(
            label=_(u"Other Key Process Results"),
            description=_(u""),
            #visible={'edit': 'invisible'},
            ),
        default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        allowable_content_types=('text/restructured', 'text/html', 'text/plain',),
        required = False,
        searchable=True,
        schemata = "ratings",
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

COLORS = {
        -1: 'white',
        0: 'grey',
        1: 'red',
        1.5: 'blue',
        2: 'orange',
        3: 'yellow',
        4: 'green'}


class Project(folder.ATFolder):
    """GEF IW Project"""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    ### values for computed fields ####

    def _isglobal(self):
        if self.getProject_scale() == 'Global':
            return True
        else:
            return False


    def _computeRegions(self):
        if self.getGlobalproject():
            return ', '.join(vocabulary.get_regions(
                    countries=self.getCountry(),
                    regions=[u'Global']))
        else:
             return ', '.join(vocabulary.get_regions(
                    countries=self.getCountry()))

    def _computeSubregions(self):
        return ', '.join(vocabulary.get_subregions(
                countries=self.getCountry()))

    ### indexed attributes ###

    def start(self):
        return self.getStart_date()

    def end(self):
        return self.getEnd_date()

    def getSubRegions(self):
        """ get region + subregion for indexing """
        countries=self.getCountry()
        if self.getProject_scale():
            scale = [self.getProject_scale(), ]
        else:
            scale = []
        if countries:
            sr = vocabulary.get_subregions(countries=countries)
            r = vocabulary.get_regions(countries=countries)
            return scale + r + sr
        else:
            if self.getGlobalproject():
                return [u'Global',]
            else:
                logger.info('no regions found for %s' % '/'.join(
                    self.getPhysicalPath()))
                return scale + ['???',]

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
        """ Returns IP, DO and TE Ratings as a tuple """
        return (self.getDorating(), self.getIprating(), self.getOutcomerating())


    def getBasin(self):
        basins = self.getBasins()
        titles = []
        for basin in basins:
            if basin is not None:
                 titles.append(basin.Title())
        return titles

    def start(self):
        return self.getStart_date()


    def end(self):
        return self.getEnd_date()

    def getCountryCode(self):
        ccs = []
        for k,v in vocabulary.my_countrylist.iteritems():
            if v['name'] in self.getCountry():
                ccs.append(k)
        return ccs

    ### Ratings ###

    def r4imcs(self):
        r = self.imcs
        dd = {'1': 'No IMCs established',
            '2': 'IMCs established and functioning, < 50% countries participating',
            '3': 'IMCs established and functioning, > 50% countries participating',
            '4': 'IMCs established, functioning and formalized thru legal and/or institutional arrangements, in most participating countries',
            'IV0': 'No IMCs established',
            'IV1': 'IMCs established with clear ToR but not functioning',
            'IV2': 'IMCs estbalished with clear ToR, functioning informally or for project purposes only',
            'IV3': 'IMCs established with clear ToR, functioning and formalized thru legal and/or institutional arrangements',
            'III0': 'No IMCs established',
            'III1': 'IMCs established but not functioning effectively or at all.',
            'III2': 'IMCs established and functioning on informal basis',
            'III3': 'IMCs established, functioning and formalized thru legal and/or institutional arrangements',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'IW1': '',
            'IW2': '',
            'IW3': '',
            'IW4': '',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            '': 'Not Avalable',
            None: 'Not Avalable',
            }

        if r in ['1', 'IV0', 'III0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'III1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'III2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III3', 'IW4']:
            ri = 4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4imcs: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-imcs'
        return {'value': ri, 'label': desc,
                'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#0090bd'}
                }

    def r4regional_frameworks(self):
        dd = {'1': 'No legal agreement/cooperation framework in place',
            '2': 'Regional legal agreement negotiated but not yet signed',
            '3': 'Countries signed legal agreement',
            '4': 'Legal agreement ratified and entered into force',
            'IV0': 'No legal agreement in place',
            'IV1': 'Legal agreement signed',
            'IV2': 'More than one country ratified legal agreement',
            'IV3': 'Legal agreement ratified by necessary quorum and in force',
            'III0': 'No legal agreement in place',
            'III1': 'Legal agreement signed and ratified by more than one country  ',
            'III2': '',
            'III3': 'Legal agreement ratified by necessary quorum and in force, Legal agreement  in force, ratified by all countries',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            #'IW0': 'Data Entry Error',
            'IW1': 'No legal agreement/cooperation framework in place (IWL Assessed)',
            'IW2': 'Regional legal agreement negotiated but not yet signed (IWL Assessed)',
            'IW3': 'Countries signed legal agreement (IWL Assessed)',
            'IW4': 'Legal agreement ratified and entered into force (IWL Assessed)',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        r = self.regional_frameworks
        if r in ['1', 'IV0', 'III0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'IV2', 'IW2']:
            ri = 2
        elif r in ['3', 'III1', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III2', 'III3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4regional_frameworks: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        #desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-frameworks'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#ff0000'}
                }

    def r4rmis(self):
        r = self.rmis
        dd = {'1': 'No RMI in place',
            '2': 'RMI established but functioning with limited effectiveness, < 50% countries contributing dues',
            '3': 'RMI established and functioning, >50% of countries contributing dues',
            '4': 'RMI in place, fully functioning and fully sustained by at or near 100% country contributions',
            'IV0': 'No TBW Institution in place',
            'IV1': 'TBW institution established but functioning with limited effectiveness due to lack of staff and  and  poor implementation of its work programme, countries contribution quite limited',
            'IV2': 'TBW institution established and functioning with moderate effectiveness, 50% of countries contributing dues',
            'IV3': 'TBW institution in place, fully functioning and fully sustained by at or near 100% country contributions',
            'III0': 'No TBW institution in place   ',
            'III1': 'TBW institution established but functioning with limited effectiveness; 50% or less of countries contributing dues',
            'III2': 'TBW institution established and functioning with moderate effectiveness, 50-75% of countries contributing dues',
            'III3': 'TBW institution in place, fully functioning and fully sustained by at or near 100% country contributions',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            #'IW0': 'Data Entry Error',
            'IW1': '',
            'IW2': '',
            'IW3': '',
            'IW4': '',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'III0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'III1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'III2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4rmis: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        #desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-rmis'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#ff6200'}
                }

    def r4reforms(self):
        r = self.reforms
        dd = {'1': 'No national/local reforms drafted',
            '2': 'National/ local reforms drafted but not yet adopted',
            '3': 'National/legal reform adopted with technical/enforcement mechanism in place',
            '4': 'National/ legal reforms implemented',
            'IV0': 'No progress',
            'IV1': '',
            'IV2': 'Less than 50% of countries committed to policy, legal and institutional reforms required to address agreed priority issues / 50-75% of countries committed to policy, legal and institutional reforms required to address agreed priority issues.',
            'IV3': 'Clear commitments in 90% or more of countries to policy, legal and institutional reforms required to address agreed priority issues.',
            'III0': 'Agreed reforms neither enacted nor implemented in majority of countries ',
            'III1': '',
            'III2': 'Most countries have enacted reforms but less than 50% are implementing, 50-80% of countries have enacted and are implementing reforms',
            'III3': '80% or more of countries have enacted and are implementing reforms',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'IW1': '',
            'IW2': '',
            'IW3': '',
            'IW4': '',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'III0', 'IW1']:
            ri = 1
        elif r in ['2', 'IW2']:
            ri = 2
        elif r in ['3', 'IV1', 'IV2', 'III1', 'III2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4reforms: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        #desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-reforms'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#fcfd00'}
                }

    def r4tda_priorities(self):
        r = self.tda_priorities
        dd = {'1': 'No progress on TDA',
            '2': 'Priority TB issues identified and agreed on but based on limited effect information; inadequate root cause analysis',
            '3': 'Priority TB issues agreed on based on solid baseline effect info; root cause analysis is inadequate',
            '4': 'Regional agreement on priority TB issues drawn from valid effect baseline, immediate and root causes properly determined',
            'IV0': 'No progress on TDA',
            'IV1': 'Priority TB issues identified and agreed but based on limited envir/socioecon impact information; none or inadequate root cause analysis',
            'IV2': 'Priority TB Issues agreed based on solid baseline of envir and socioecon impacts info; root cause analysis is inadequate',
            'IV3': 'Priority TB Issues agreed based on solid baseline of envir and socioecon impacts info; root cause analysis is adequate',
            'III0': 'No progress on TDA',
            'III1': 'TDA in progress, Priority TB issues identified and agreed but based on limited environmental/socioeconomic impact information; none or inadequate root cause analysis,',
            'III2': 'Priority TB Issues agreed based on solid baseline of envir and socioecon impacts info; root cause analysis is inadequate',
            'III3': 'Regional agreement on priority TB issues drawn from valid enviro/socioecon impacts baseline, immediate and root causes properly determined.',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            #'IW0': "Data Entry Error",
            'IW1': '',
            'IW2': '',
            'IW3': '',
            'IW4': '',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'III0', 'III1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'III2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4tda_priorities: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        #desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-tda-priorities'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#00147f'}
                }

    def r4sap_devel(self):
        r = self.sap_devel
        dd = {'1': 'No development of SAP',
            '2': 'SAP developed addressing key TB concerns spatially',
            '3': 'SAP developed and adopted by ministers ',
            '4': 'Adoption of SAP into National Action Plans (NAPs)',
            'IV0': 'No development of SAP',
            'IV1': 'SAP developed addressing key TB concerns spatially',
            'IV2': 'SAP developed and adopted by ministers ',
            'IV3': 'Adoption of SAP into National Action Plans (NAPs)',
            'III0': 'SAP neither developed, nor approved',
            'III1': 'SAP developed and agreed at highest technical level (e.g. project Steering Committee)',
            'III2': 'SAP developed and endorsed by minimum 50% 0f countries',
            'III3': 'SAP endorsed by all ministers of countries sharing the TB water body or adopted by relevant inter-governmental body',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            #'IW0': "Data Entry Error",
            'IW1': '',
            'IW2': '',
            'IW3': '',
            'IW4': '',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}
        if r in ['1', 'IV0', 'III0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'III1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'III2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'III3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4sap_devel: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        url = self.absolute_url() + '/@@resultsview.html' + '#pra-sap-devel'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#0a0034'}
                }

    def r4abnj_rmi(self):
        r = self.abnj_rmi
        dd = {'1': 'No management measures in ABNJ  in  (RMI) institutional/ management frameworks',
            '2': 'Management measures in ABNJ designed but not formally adopted by project participants',
            '3': 'Management measures in ABNJ  formally adopted by project participants but not incorporated in RMI institutional/management frameworks',
            '4': 'Management measures in ABNJ fully incorporated in  RMI institutional/ management frameworks',
            'IV0': 'No management measures in ABNJ  in  (RMI) institutional/ management frameworks',
            'IV1': 'Management measures in ABNJ designed but not formally adopted by project participants',
            'IV2': 'Management measures in ABNJ  formally adopted by project participants but not incorporated in RMI institutional/management frameworks',
            'IV3': 'Management measures in ABNJ fully incorporated in  RMI institutional/ management frameworks',
            'III0': '',
            'III1': '',
            'III2': '',
            'III3': '',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'IW1': 'No management measures in ABNJ  in  (RMI) institutional/ management frameworks',
            'IW2': 'Management measures in ABNJ designed but not formally adopted by project participants',
            'IW3': 'Management measures in ABNJ  formally adopted by project participants but not incorporated in RMI institutional/management frameworks',
            'IW4': 'Management measures in ABNJ fully incorporated in  RMI institutional/ management frameworks',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4abnj_rmi: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-abnj'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#003994'}
                }

    def r4tdasap_cc(self):
        r = self.tdasap_cc
        dd = {'1': 'No revised TDA or SAP',
            '2': 'TDA updated to incorporate climate variability and change',
            '3': 'Revised SAP prepared including Climatic Variability and Change',
            '4': 'SAP including Climatic Variability and Change adopted by all involved countries',
            'IV0': 'No revised TDA or SAP',
            'IV1': 'TDA updated to incorporate climate variability and change',
            'IV2': 'Revised SAP prepared including Climatic Variability and Change',
            'IV3': 'SAP including Climatic Variability and Change adopted by all involved countries',
            'III0': '',
            'III1': '',
            'III2': '',
            'III3': '',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'IW1': 'No revised TDA or SAP',
            'IW2': 'TDA updated to incorporate climate variability and change',
            'IW3': 'Revised SAP prepared including Climatic Variability and Change',
            'IW4': 'SAP including Climatic Variability and Change adopted by all involved countries',
            '': 'Not Avalable',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4tdasap_cc: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-tdasap-cc'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#491500'}
                }

    def r4tda_mnits(self):
        r = self.tda_mnits
        dd = {
            '1': 'TDA does not include technical annex based on MNITS activities',
            '2': 'MNITS committee established and contributed to TDA development',
            '3': 'TDA includes technical annex, documenting data and analysis being collected',
            '4': 'TDA includes technical annex posted IWLEARN and based on MNITS committee inputs',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            '': 'Not Avalable',
            None: 'Not Avalable',
            }

        if r in ['1']:
            ri = 1
        elif r in ['2']:
            ri = 2
        elif r in ['3']:
            ri = 3
        elif r in ['4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4tda_mnits: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-mnits'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#00821c'}
                }

    def r4sap_adopted(self):
        r = self.sap_adopted
        ri = 0
        desc = None
        if r:
            ri = int(r)
            desc = '%i %%' %ri
            rf = float(ri)/25.0
        else:
            rf = 0
            desc = ''
        color = COLORS[min(4,int(rf)+1)]
        if r in [-1,'nap']:
            rf = -1
            color = COLORS[rf]

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-sap-adopted'
        return {'value': rf, 'label': desc, 'description': '% of countries have adopted SAP',
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': color}
                #'style': {'color': '#003f17'}
                }

    def r4sap_implementing(self):
        desc = None
        r = self.sap_implementing
        ri = 0
        if r:
            ri = int(r)
            desc = '%i %%' %ri
            rf = float(ri)/25.0
        else:
            rf = 0
        color = COLORS[min(4,int(rf)+1)]
        if r in [-1,'nap']:
            rf = -1
            color = COLORS[rf]

        url = self.absolute_url() + '/@@resultsview.html' + '#pra-sap-implementing'
        return {'value': rf, 'label': desc, 'description': '% of countries implementing SAP',
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': color}
                #'style': {'color': '#000000'}
                }


    def r4sap_inc(self):
        r = self.sap_inc
        dd = {'1': 'No progress',
            '2': 'Limited progress, very generic with no specific agency/government(s) commitments',
            '3': 'Priorities specifically incorporated into some national development/assistance frameworks with clear agency/government(s) commitments and time frames for achievement',
            '4': 'Majority of national development/assistance frameworks have incorporated priorities with clear agency/government(s)  commitments and time frames for achievement',
            'IV0': 'No progress in incorporating priorities into national strategic planning frameworks',
            'IV1': 'Less than 25% of actions  incorporated  into national frameworks but very generic with no specific commitments',
            'IV2': 'Priorities specifically incorporated into some national frameworks with clear commitments and time frames for achievement',
            'IV3': 'Majority of national frameworks have incorporated priorities with clear commitments and time frames for achievement',
            'III0': '',
            'III1': '',
            'III2': '',
            'III3': '',
            'IWA': 'Some progress has occurred but cannot be ranked, please see the description for further details (IWL Assessed)',
            'IW1': 'No progress',
            'IW2': 'Limited progress, very generic with no specific agency/government(s) commitments',
            'IW3': 'Priorities specifically incorporated into some national development/assistance frameworks with clear agency/government(s) commitments and time frames for achievement',
            'IW4': 'Majority of national development/assistance frameworks have incorporated priorities with clear agency/government(s)  commitments and time frames for achievement',
            'nap': 'Not Applicable',
            'nav': 'Not Available',
            '': 'Not Avalable',
            None: 'Not Avalable',}

        if r in ['1', 'IV0', 'IW1']:
            ri = 1
        elif r in ['2', 'IV1', 'IW2']:
            ri = 2
        elif r in ['3', 'IV2', 'IW3']:
            ri = 3
        elif r in ['4', 'IV3', 'IW4']:
            ri =4
        elif r in ['IWA']:
            ri = 1.5
        elif r in ['nap']:
            ri = -1
        elif r in ['nav']:
            ri = 0
        elif r is None:
            ri = 0
        elif r.strip().lower() in ['n/a','']:
            ri = 0
        else:
            ri = 0
            logger.error('pid: %s r4sap_inc: "%s"' % (self.getGef_project_id(), r))
        if r:
            desc = r
        else:
            desc = ''
        url = self.absolute_url() + '/@@resultsview.html' + '#pra-r4sap-inc'
        return {'value': ri, 'label': desc, 'description':  dd[r],
                'xlink': {'href': url, 'target': '_top'},
                'style': {'color': COLORS[ri]},
                #'style': {'color': '#cb001d'}
                }



    def has_result_ratings(self):
        return ((bool(str(self.imcs)) and self.imcs is not None)  or
            (bool(str(self.regional_frameworks))  and self.regional_frameworks is not None) or
            (bool(str(self.rmis)) and self.rmis is not None)   or
            (bool(str(self.reforms))  and self.reforms is not None)  or
            (bool(str(self.tda_priorities)) and self.tda_priorities is not None)  or
            (bool(str(self.sap_devel)) and self.sap_devel is not None)  or
            (bool(str(self.abnj_rmi))   and self.abnj_rmi is not None) or
            (bool(str(self.tdasap_cc)) and self.tdasap_cc is not None)   or
            (bool(str(self.tda_mnits))  and self.tda_mnits is not None) or
            (bool(str(self.sap_adopted))   and self.sap_adopted is not None) or
            (bool(str(self.sap_implementing))   and self.sap_implementing is not None) or
            (bool(str(self.sap_inc)) and self.sap_inc is not None) )



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
            'getProject_status', 'getProject_type', 'getEcosystem'])

    basins = context.getBasins()
    for basin in basins:
        basin.reindexObject()


def get_default_logo(context, event):
    if not context.getLogo_image():
        la = context.getLeadagency()
        if la:
            logo = la.getRawLogo_image()
            if logo:
                context.setLogo_image(logo)
                logger.info('set logo: ' + '/'.join(context.getPhysicalPath()))
            else:
                logger.info( 'EA "%s" has no logo' % la.Title())


atapi.registerType(Project, PROJECTNAME)
