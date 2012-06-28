"""Definition of the Project Database content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IProjectDatabase
from iwlearn.project.config import PROJECTNAME

ProjectDatabaseSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.LinesField(
        'exclude_ids',
        widget=atapi.LinesWidget(
            label=_(u"Exclude Project Ids"),
            description=_(u"Project ids not to be harvested from gefonline (multifocal projects with no IW components)"),
        ),
    ),

    atapi.StringField( 'country_fill',
        title=u"Country Fillcolor",
        description=u"",
        default =u"7fff00cc",
        required=True),

    atapi.StringField( 'country_border',
        title=u"Country Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),


    atapi.StringField('oo_fill',
        title=u"Oceans Fillcolor",
        description=u"",
        default =u"ff0000cc",
        required=True),

    atapi.StringField('oo_border',
        title=u"Oceans Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),

    atapi.StringField('lme_fill',
        title=u"LME Fillcolor",
        description=u"",
        default =u"0000bfcc",
        required=True),

    atapi.StringField('lme_border',
        title=u"LME Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),

    atapi.StringField('lake_fill',
        title=u"Lake Fillcolor",
        description=u"",
        default =u"2c80d3cc",
        required=True),

    atapi.StringField('lake_border',
        title=u"Lake Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),

    atapi.StringField('river_fill',
        title=u"River Fillcolor",
        description=u"",
        default =u"56ffffcc",
        required=True),

    atapi.StringField('river_border',
        title=u"River Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),

    atapi.StringField('gw_fill',
        title=u"Aquifer Fillcolor",
        description=u"c1742ccc",
        default =u"",
        required=True),

    atapi.StringField('gw_border',
        title=u"Aquifer Outline Color",
        description=u"",
        default =u"ff0000cc",
        required=True),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.


schemata.finalizeATCTSchema(
    ProjectDatabaseSchema,
    folderish=True,
    moveDiscussion=False
)


class ProjectDatabase(folder.ATFolder):
    """Database for GEF IW projects"""
    implements(IProjectDatabase)

    meta_type = "Project Database"
    schema = ProjectDatabaseSchema


    # -*- Your ATSchema to Python Property Bridges Here ... -*-



atapi.registerType(ProjectDatabase, PROJECTNAME)
