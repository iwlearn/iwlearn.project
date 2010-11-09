"""Definition of the Project content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.AddRemoveWidget import AddRemoveWidget
from Products.ATExtensions.widget.url import UrlWidget



from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IProject
from iwlearn.project.config import PROJECTNAME
from iwlearn.project import vocabulary

ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


    # overview

    atapi.StringField(
        'gef_project_id',
        required=False,
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"GEF Project Id"),
            description=_(u"GEF Project Id"),
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
        vocabulary = vocabulary.BASINS,
        widget=atapi.SelectionWidget(
            label=_(u"Basin"),
            description=_(u"Basin"),
        ),
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

    atapi.LinesField(
        'strategic_priority',
        required=False,
        searchable=True,
        vocabulary = vocabulary.STRATEGIC_PRIORITIES,
        widget=atapi.InAndOutWidget(
            label=_(u"GEF Strategic Priority"),
            description=_(u"GEF Strategic Priority"),
        ),
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
        vocabulary = vocabulary.OPERATIONAL_PROGRAMMES,
        widget=atapi.InAndOutWidget(
            label=_(u"GEF Operational Programme"),
            description=_(u"GEF Operational Programme"),
        ),
    ),

    atapi.FixedPointField(
        'gef_project_allocation',
        widget=atapi.DecimalWidget(
            label=_(u"GEF Allocation to project"),
            description=_(u"GEF Allocation to project"),
        ),
        validators=('isDecimal'),
    ),

    atapi.FixedPointField(
        'total_cost',
        widget=atapi.DecimalWidget(
            label=_(u"Total Cost"),
            description=_(u"Total Cost"),
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
            base_query={'Subject':'Executing Agency'},
            allow_browse=True,
            allow_sorting=True,
        ),
        relationship='executing_agency_project',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    # geographical info

    atapi.FloatField(
        'longitude',
        widget=atapi.DecimalWidget(
            label=_(u"Longitude of an marker on map"),
            description=_(u"Longitude of an marker on map"),
        ),
        validators=('isDecimal'),
    ),


    atapi.FloatField(
        'latitude',
        widget=atapi.DecimalWidget(
            label=_(u"Latitude of an marker on map"),
            description=_(u"Latitude of an marker on map"),
        ),
        validators=('isDecimal'),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)


class Project(folder.ATFolder):
    """GEF IW Project"""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    def _computeRegions(self):
        if self.getGlobalproject():
            return vocabulary.get_regions(countries=self.getCountry(),
                regions=[u'Global'])
        else:
             return vocabulary.get_regions(countries=self.getCountry())

    def _computeSubregions(self):
        return vocabulary.get_subregions(countries=self.getCountry())


    def getSubRegions(self):
        """ get region + subregion for indexing """
        return self._computeRegions() + self._computeSubregions()

    def getAgencies(self):
        """ Returns the implementing + lead agencies of the project """
        agencies = []
        for ia in self.getOther_implementing_agency():
            agencies.append(ia.Title())
        agencies.append(self.getLeadagency().Title())
        return agencies
    # -*- Your ATSchema to Python Property Bridges Here ... -*-



atapi.registerType(Project, PROJECTNAME)
