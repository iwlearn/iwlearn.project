"""Definition of the Basin content type
"""

import logging
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

logger = logging.getLogger('iwlearn.project')


class UpdatingBackReferenceField(backref.BackReferenceField):
    """ An backreference field that takes care of the reference
    """

    def set(self, instance, value, **kwargs):
        old_refs = self.get(instance, aslist=True)
        super(UpdatingBackReferenceField, self).set(instance, value, **kwargs)
        new_refs = self.get(instance, aslist=True)
        refs = set(old_refs + new_refs)
        for ref in refs:
            #TODO: ref.reindexObject(idxs=...)
            #DBG logger.info('UpdatingBackReferenceField: %s' % ref.id) 
            ref.reindexObject()


BasinSchema = ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'basin_type',
        required=True,
        searchable=True,
        vocabulary=vocabulary.BASIN_TYPE,
        widget=atapi.SelectionWidget(
            label=_(u"Basin Type"),
            description=_(u"Type of Basin"),
        ),
    ),

    UpdatingBackReferenceField(
        'projects',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Projects"),
            description=_(u"Projects in this basin"),
            allow_search=True,
            allow_sorting=True,
            allow_browse=True,
            hide_inaccessible=True,
            show_review_state=True,
            history_length=3,
        ),
        relationship='basins_projects',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    backref.BackReferenceField(
        'frameworks',
        required=False,
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Frameworks"),
            description=_(u"Legal and Institutional Frameworks"),
            allow_browse=True,
            allow_sorting=True,
            allow_search=True,
        ),
        relationship='basin_framework',
        allowed_types=('LegalFW',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


))



schemata.finalizeATCTSchema(BasinSchema, moveDiscussion=False)


class Basin(base.ATCTContent):
    """Basins for projects and legal frameworks"""
    implements(IBasin)

    meta_type = "Basin"
    schema = BasinSchema

    def getEcosystem(self):
        bt = self.getBasin_type()
        if bt == 'Ocean':
            bt = 'Sea'
        elif bt == 'Aquifer':
            bt = 'Groundwater'
        return bt

atapi.registerType(Basin, PROJECTNAME)
