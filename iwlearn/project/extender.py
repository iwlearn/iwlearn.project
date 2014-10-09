""" Extend some types with geo- fields
"""

import logging

#from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface 

from Products.CMFCore.interfaces import ISiteRoot

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATImage

from Products.Archetypes import atapi

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from iwlearn.project import vocabulary

from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import IProject

logger = logging.getLogger('iwlearn.project')

class _ExtensionComputedField(ExtensionField, atapi.ComputedField): pass
class _ExtensionImageField(ExtensionField, atapi.ImageField): pass
class _ExtensionLinesField(ExtensionField, atapi.LinesField): pass
class _ExtensionReferenceField(ExtensionField, atapi.ReferenceField): pass
class _ExtensionStringField(ExtensionField, atapi.StringField): pass

class GeoFieldsExtender(object):
    """ Group Region/Basin/Country fields
    """
    implements(ISchemaExtender)

    fields = [

        _ExtensionComputedField('region',
            schemata='geodata',
            required=True,
            searchable=True,
            expression='context.restrictedTraverse("@@geo_view")._computeRegions()',
            widget=atapi.ComputedWidget(
                label=_(u"Geographic Region"),
                description=_(u"Geographic Region in which the project operates"),
            ),
        ),

        _ExtensionComputedField('subregion',
            schemata='geodata',
            required=False,
            searchable=True,
            expression='context.restrictedTraverse("@@geo_view")._computeSubregions()',
            widget=atapi.ComputedWidget(
                label=_(u"Geographic Sub Region"),
                description=_(u"Geographic Sub Region in which the project operates"),
            ),
        ),

        _ExtensionLinesField('country',
            schemata='geodata',
            required=False,
            searchable=True,
            vocabulary=vocabulary.get_countries(),
            widget=atapi.InAndOutWidget(
                label=_(u"Countries"),
                description=_(u"Countries"),
            ),
        ),

        _ExtensionReferenceField('basins',
            schemata='geodata',
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

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields



class ProjectFieldsExtender(object):
    """ Add 'Project Type' field
    """
    implements(ISchemaExtender)

    fields = [
        _ExtensionLinesField(
            "document_type",
            searchable=True,
            vocabulary = vocabulary.DOCUMENT_TYPE,
            widget = atapi.SelectionWidget(
                label=u"Document Type",
                description=u"Classification of the document type",
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


from plone.indexer import indexer


@indexer(IATFile)
@indexer(IATImage)
@indexer(IATDocument)
def document_type_indexer(context):
    document_type = context.getField('document_type').get(context)
    #DBG logger.info('document_type_indexer: %s' % document_type)
    return document_type


@indexer(IATFile)
@indexer(IATImage)
@indexer(IProject)
@indexer(IATDocument)
def country_indexer(context):
    countries = _find_first(context, 'country')
    #DBG logger.info('country_indexer: %s' % `countries`)
    return countries


@indexer(IATFile)
@indexer(IATImage)
@indexer(IProject)
@indexer(IATDocument)
def country_code_indexer(context):
    countries = _find_first(context, 'country')
    ccs = []
    for k,v in vocabulary.my_countrylist.iteritems():
        if v['name'] in countries:
            ccs.append(k)
    #DBG logger.info('country_code_indexer: %s' % `ccs`)
    return ccs


@indexer(IATFile)
@indexer(IATImage)
@indexer(IProject)
@indexer(IATDocument)
def basin_indexer(context):
    basins = _find_first(context, 'basins')
    titles = []
    for basin in basins:
        if basin is not None:
             titles.append(basin.Title())
    #DBG logger.info('basin_indexer: %s' % `titles`)
    return titles


@indexer(IATFile)
def subregion_indexer(context):
    countries = _find_first(context, 'country')
    if context.getProject_scale():
        scale = [context.getProject_scale(), ]
    else:
        scale = []
    if countries:
        sr = vocabulary.get_subregions(countries=countries)
        r = vocabulary.get_regions(countries=countries)
        subregions = scale + r + sr
        #DBG logger.info('subregion_indexer: %s' % `subregions`)
        return subregions
    else:
        if context.getGlobalproject():
            subregions = [u'Global',]
            #DBG logger.info('subregion_indexer: %s' % `subregions`)
            return subregions
        else:
            logger.info('no regions found for %s' % '/'.join(
                context.getPhysicalPath()))
            subregions = scale + ['???',]
            #DBG logger.info('subregion_indexer: %s' % `subregions`)
            return subregions


class IGeoTags(Interface):
    """ For content that knows where it is
    """

    def _computeRegions():
        """Compute regions"""

    def _computeSubregions():
        """Compute sub regions"""


def _find_first(context, fieldname):
    context = context.aq_inner
    while not ISiteRoot.providedBy(context):
        field_getter = getattr(context, 'getField', None)
        if field_getter:
            field = field_getter(fieldname)
            if field:
                value = field.get(context)
                if value:
                    return value
        context = context.aq_parent

class GeoTags(object):
    implements(IGeoTags)

    def _computeRegions(self):
        context = self.context
        countries = _find_first(context, 'country')

        if context.getGlobalproject():
            regions = ', '.join(
                    vocabulary.get_regions(
                        countries=countries,
                        regions=[u'Global']))
        else:
            regions = ', '.join(vocabulary.get_regions(countries=countries))

        #DBG logger.info('_computeRegions: %s' % `regions`)
        return regions 

    def _computeSubregions(self):
        context = self.context
        subregions = ', '.join(
                vocabulary.get_subregions(
                        countries=_find_first(context, 'country')))
        #DBG logger.info('_computeSubregions: %s' % `subregions`)
        return subregions
