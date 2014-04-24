from zope.component import adapts
from zope.interface import implements

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATImage

from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import StringField

from Products.Archetypes.public import ComputedWidget
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from iwlearn.project import vocabulary

class _ExtensionImageField(ExtensionField, ImageField): pass
class _ExtensionStringField(ExtensionField, StringField): pass
# class _ExtensionCountryField(ExtensionField, LinesField): pass
class _ExtensionRegionField(ExtensionField, LinesField):pass
class _ExtensionBasinField(ExtensionField, ReferenceField):pass
class _ExtensionDocumentTypeField(ExtensionField, LinesField):pass

_fields = [
    _ExtensionDocumentTypeField(
        "document_type",
        searchable=True,
        vocabulary = vocabulary.DOCUMENT_TYPE,
        widget = SelectionWidget(
            label=u"Document Type",
            description=u"Classification of the document type",
        ),
    ),
]

class ProjectFieldsExtender(object):
    """ Add 'Project Type' field
    """
    #adapts(IATFile,IATImage)
    implements(ISchemaExtender)

    fields = _fields

    def __init__(self, context):
        self.context = context

    # def _computeSubregions(self):
    #     return ','.join(vocabulary.get_subregions(
    #             countries=self.getCountry()))

    def getFields(self):
        return self.fields


class ImageAndFileExtender(ProjectFieldsExtender):
    """ Additionally add image fields
    """

    fields = [
	    _ExtensionImageField(
		"folderimage",
		    widget = ImageWidget(
		    label=u"Folder Image",
		    description=u"Image to display with the folder",
		),
	    ),
	    _ExtensionStringField(
		"folderimagetitle",
		widget = StringWidget(
		    label=u"Image Title",
		    description=u"Title of image to display with the folder",
		),
	    ),
        ] + _fields

from plone.indexer import indexer

@indexer(IATDocument)
def document_type_doc_indexer(context):
    return context.getField('document_type').get(context)

@indexer(IATFile)
def document_type_file_indexer(context):
    return context.getField('document_type').get(context)
