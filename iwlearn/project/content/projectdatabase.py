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

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProjectDatabaseSchema['title'].storage = atapi.AnnotationStorage()
ProjectDatabaseSchema['description'].storage = atapi.AnnotationStorage()

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

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ProjectDatabase, PROJECTNAME)
