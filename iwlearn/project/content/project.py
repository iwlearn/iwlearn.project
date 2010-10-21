"""Definition of the Project content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IProject
from iwlearn.project.config import PROJECTNAME

ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


	# overview
	
    atapi.StringField(
        'gef_project_id',
        required=False,
		searchable=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"GEF Project Id"),
            description=_(u"GEF Project Id"),
        ),
    ),
	
    atapi.StringField(
        'remote_url',
        required=False,
		searchable=False,        
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Project Website"),
            description=_(u"Website of the project"),
        ),
    ),
		
    atapi.LinesField(
        'region',
        required=True,
		searchable=True,  
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Geographic Region"),
            description=_(u"Geographic Region in which the project operates"),
        ),
    ),

    atapi.LinesField(
        'subregion',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.PickListWidget(
            label=_(u"Geographic Sub Region"),
            description=_(u"Geographic Sub Region in which the project operates"),
        ),
    ),
        	
    atapi.LinesField(
        'basin',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.PickListWidget(
            label=_(u"Basin"),
            description=_(u"Field description"),
        ),
    ),


    atapi.ReferenceField(
        'project_contacts',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceBrowserWidget(
            label=_(u"Project Contacts"),
            description=_(u"Select Project Contacts"),
        ),
        relationship='project_project_contacts',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

    atapi.TextField(
        'project_summary',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
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
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Project Type"),
            description=_(u"Project Type"),
        ),
    ),


    atapi.StringField(
        'project_status',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.SellectionWidget(
            label=_(u"Project Status"),
            description=_(u"Project Status"),
        ),
    ),

    atapi.DateTimeField(
        'start_date',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Date"),
            description=_(u"Start Date"),
        ),
        validators=('isValidDate'),
    ),

   atapi.DateTimeField(
        'end_date',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"End date"),
            description=_(u"End date"),
        ),
        validators=('isValidDate'),
    ),


	# GEF characteristic

    atapi.LinesField(
        'strategic_priority',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.PickListWidget(
            label=_(u"GEF Strategic Priority"),
            description=_(u"GEF Strategic Priority"),
        ),
    ),

    atapi.StringField(
        'focal_area',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Focal Areas"),
            description=_(u"Focal Areas"),
        ),
    ),


    atapi.LinesField(
        'operational_programme',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.PickListWidget(
            label=_(u"GEF Operational Programme"),
            description=_(u"GEF Operational Programme"),
        ),
    ),
    
    atapi.FixedPointField(
        'gef_project_allocation',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"GEF Allocation to project"),
            description=_(u"GEF Allocation to project"),
        ),
        validators=('isDecimal'),
    ),

    atapi.FixedPointField(
        'total_cost',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Total Cost"),
            description=_(u"Total Cost"),
        ),
        validators=('isDecimal'),
    ),
    
    
    # Partners

    atapi.LinesField(
        'country',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.PickListWidget(
            label=_(u"Countries"),
            description=_(u"Countries"),
        ),
    ),


    atapi.StringField(
        'leadagency',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Lead Implementing Agency"),
            description=_(u"Lead Implementing Agency"),
        ),
    ),

    atapi.LinesField(
        'other_implementing_agency',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Other Implementing Agencies"),
            description=_(u"Other Implementing Agencies"),
        ),
    ),


    atapi.LinesField(
        'executing_agency',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Executing Agencies"),
            description=_(u"Executing Agencies"),
        ),
    ),



  atapi.LinesField(
        'other_partners',
        required=False,
		searchable=True, 
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Other Partners"),
            description=_(u"Other Partners"),
        ),
    ),

    # geographical info

    atapi.FloatField(
        'longitude',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Longitude of an marker on map"),
            description=_(u"Longitude of an marker on map"),
        ),
        validators=('isDecimal'),
    ),


    atapi.FloatField(
        'latitude',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Latitude of an marker on map"),
            description=_(u"Latitude of an marker on map"),
        ),
        validators=('isDecimal'),
    ),

	# other stuff - seems to be unused

    atapi.StringField(
        'gef_project_stage',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"New Field"),
            description=_(u"GEF Project Stage"),
        ),
    ),


    atapi.StringField(
        'evaluator_name',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Name of Evaluator"),
            description=_(u"Field description"),
        ),
    ),


    atapi.DateTimeField(
        'terminal_evaluation_date',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Terminal Evaluation Date"),
            description=_(u"Terminal Evaluation Date"),
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'consultant_name',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Name of Consultant"),
            description=_(u"Name of Consultant"),
        ),
    ),


    atapi.DateTimeField(
        'evaluation_report_date',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Evaluation Report Date"),
            description=_(u"Evaluation Report Date"),
        ),
        validators=('isValidDate'),
    ),


    atapi.TextField(
        'project_results',        
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Project Results"),
            description=_(u"Project Results"),
        ),
		validators=('isTidyHtmlWithCleanup',),
    ),






))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProjectSchema['title'].storage = atapi.AnnotationStorage()
ProjectSchema['description'].storage = atapi.AnnotationStorage()

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

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    longitude = atapi.ATFieldProperty('longitude')

    latitude = atapi.ATFieldProperty('latitude')

    evaluator_name = atapi.ATFieldProperty('evaluator_name')

    terminal_evaluation_date = atapi.ATFieldProperty('terminal_evaluation_date')

    consultant_name = atapi.ATFieldProperty('consultant_name')

    evaluation_report_date = atapi.ATFieldProperty('evaluation_report_date')

    project_results = atapi.ATFieldProperty('project_results')

    total_cost = atapi.ATFieldProperty('total_cost')

    gef_project_allocation = atapi.ATFieldProperty('gef_project_allocation')

    gef_project_stage = atapi.ATFieldProperty('gef_project_stage')

    project_type = atapi.ATFieldProperty('project_type')

    gef_project_id = atapi.ATFieldProperty('gef_project_id')

    focal_area = atapi.ATFieldProperty('focal_area')

    operational_programme = atapi.ATFieldProperty('operational_programme')

    strategic_priority = atapi.ATFieldProperty('strategic_priority')

    project_summary = atapi.ATFieldProperty('project_summary')

    end_date = atapi.ATFieldProperty('end_date')

    start_date = atapi.ATFieldProperty('start_date')

    project_status = atapi.ATFieldProperty('project_status')

    other_partners = atapi.ATFieldProperty('other_partners')

    executing_agency = atapi.ATFieldProperty('executing_agency')

    other_implementing_agency = atapi.ATFieldProperty('other_implementing_agency')

    leadagency = atapi.ATFieldProperty('leadagency')

    country = atapi.ATFieldProperty('country')

    basin = atapi.ATFieldProperty('basin')

    subregion = atapi.ATFieldProperty('subregion')

    region = atapi.ATFieldProperty('region')

    project_contacts = atapi.ATReferenceFieldProperty('project_contacts')

    remote_url = atapi.ATFieldProperty('remote_url')


atapi.registerType(Project, PROJECTNAME)
