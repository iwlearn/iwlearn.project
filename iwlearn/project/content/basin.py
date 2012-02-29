"""Definition of the Basin content type
"""

from zope.interface import implements

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import ATDocumentSchema

from Products.ATBackRef import backref

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IBasin
from iwlearn.project.config import PROJECTNAME
from iwlearn.project import vocabulary


BasinSchema = ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'basin_type',
        required=False,
        searchable=True,
        vocabulary = vocabulary.BASIN_TYPE,
        widget=atapi.SelectionWidget(
            label=_(u"Basin Type"),
            description=_(u"Type of Basin"),
        ),
    ),

    backref.BackReferenceField(
        'projects',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Projects"),
            description=_(u"Projects in this basin"),
            allow_search =True,
            allow_sorting = True,
            allow_browse =True,
            hide_inaccessible=True,
            show_review_state=True,
            history_length=3,
        ),
        relationship='basins_projects',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'frameworks',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Frameworks"),
            description=_(u"Legal and Institutional Frameworks"),
            #base_query={'Subject':'Executing Agency'},
            #startup_directory_method='_getProjectsDirectory',
            allow_browse=True,
            allow_sorting=True,
        ),
        relationship='basin_framework',
        allowed_types=('Document',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


))



schemata.finalizeATCTSchema(BasinSchema, moveDiscussion=False)


class Basin(base.ATCTContent):
    """Basins for projects and legal frameworks"""
    implements(IBasin)

    meta_type = "Basin"
    schema = BasinSchema




atapi.registerType(Basin, PROJECTNAME)
