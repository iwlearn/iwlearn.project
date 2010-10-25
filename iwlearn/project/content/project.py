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
        widget=atapi.StringWidget(
            label=_(u"GEF Project Id"),
            description=_(u"GEF Project Id"),
        ),
    ),
	
    atapi.StringField(
        'remote_url',
        required=False,
		searchable=False,        
        widget=atapi.StringWidget(
            label=_(u"Project Website"),
            description=_(u"Website of the project"),
        ),
        validators=('isURL'),
    ),
		
    atapi.LinesField(
        'region',
        required=True,
		searchable=True,  
        widget=atapi.SelectionWidget(
            label=_(u"Geographic Region"),
            description=_(u"Geographic Region in which the project operates"),
        ),
    ),

    atapi.LinesField(
        'subregion',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
            label=_(u"Geographic Sub Region"),
            description=_(u"Geographic Sub Region in which the project operates"),
        ),
    ),

    atapi.LinesField(
        'country',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
            label=_(u"Countries"),
            description=_(u"Countries"),
        ),
    ),

        	
    atapi.LinesField(
        'basin',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
            label=_(u"Basin"),
            description=_(u"Basin"),
        ),
    ),


    atapi.ReferenceField(
        'project_contacts',
        widget=atapi.ReferenceWidget(
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
        widget=atapi.SelectionWidget(
            label=_(u"Project Type"),
            description=_(u"Project Type"),
        ),
    ),


    atapi.StringField(
        'project_status',
        required=False,
		searchable=True, 
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
        ),
        validators=('isValidDate'),
    ),

   atapi.DateTimeField(
        'end_date',
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
        widget=atapi.SelectionWidget(
            label=_(u"GEF Strategic Priority"),
            description=_(u"GEF Strategic Priority"),
        ),
    ),
    
    atapi.LinesField(
        'focal_area',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
            label=_(u"Focal Areas"),
            description=_(u"Focal Areas"),
        ),
    ),


    atapi.LinesField(
        'operational_programme',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
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


    atapi.StringField(
        'leadagency',
        required=False,
		searchable=True, 
        widget=atapi.SelectionWidget(
            label=_(u"Lead Implementing Agency"),
            description=_(u"Lead Implementing Agency"),
        ),
    ),

    atapi.LinesField(
        'other_implementing_agency',
        required=False,
		searchable=True, 
        widget=atapi.LinesWidget(
            label=_(u"Other Implementing Agencies"),
            description=_(u"Other Implementing Agencies"),
        ),
    ),


    atapi.LinesField(
        'executing_agency',
        required=False,
		searchable=True, 
        widget=atapi.LinesWidget(
            label=_(u"Executing Agencies"),
            description=_(u"Executing Agencies"),
        ),
    ),



  atapi.LinesField(
        'other_partners',
        required=False,
		searchable=True, 
        widget=atapi.LinesWidget(
            label=_(u"Other Partners"),
            description=_(u"Other Partners"),
        ),
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

	# other stuff - seems to be unused

    atapi.StringField(
        'gef_project_stage',
        widget=atapi.SelectionWidget(
            label=_(u"GEF Project Stage"),
            description=_(u"GEF Project Stage"),
        ),
    ),


    atapi.StringField(
        'evaluator_name',
        widget=atapi.StringWidget(
            label=_(u"Name of Evaluator"),
            description=_(u"Field description"),
        ),
    ),


    atapi.DateTimeField(
        'terminal_evaluation_date',
        widget=atapi.CalendarWidget(
            label=_(u"Terminal Evaluation Date"),
            description=_(u"Terminal Evaluation Date"),
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'consultant_name',
        widget=atapi.StringWidget(
            label=_(u"Name of Consultant"),
            description=_(u"Name of Consultant"),
        ),
    ),


    atapi.DateTimeField(
        'evaluation_report_date',
        widget=atapi.CalendarWidget(
            label=_(u"Evaluation Report Date"),
            description=_(u"Evaluation Report Date"),
        ),
        validators=('isValidDate'),
    ),


    atapi.TextField(
        'project_results',        
        widget=atapi.RichWidget(
            label=_(u"Project Results"),
            description=_(u"Project Results"),
        ),
		validators=('isTidyHtmlWithCleanup',),
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



    # -*- Your ATSchema to Python Property Bridges Here ... -*-
 


atapi.registerType(Project, PROJECTNAME)
