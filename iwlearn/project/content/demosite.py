from zope.interface import implements

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import ATDocumentSchema

from Products.ATBackRef import backref

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IDemoSite
from iwlearn.project.config import PROJECTNAME
from iwlearn.project import vocabulary


DemoSiteSchema = ATDocumentSchema.copy() + atapi.Schema((

# GEFID
# GEF Project Shortname
# Demo Site #
# Demo Site Title
# Indicator Type
# Stress Reduction Indicator
# Baseline
# Year
# Target
# Aggregate Result
# Result Description
# Year
# Cumulative Result
# Geographic Coordinates
# Brief
# Description
# Image/Video
# Other Notes/Results
# Reporting Date
# Data Source
))

schemata.finalizeATCTSchema(DemoSiteSchema, moveDiscussion=False)

class DemoSite(base.ATCTContent):
    """Demo Sites for projects"""
    implements(IDemoSite)

    meta_type = "DemoSite"
    schema = DemoSiteSchema

atapi.registerType(DemoSite, PROJECTNAME)
