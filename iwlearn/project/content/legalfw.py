"""Definition of the LegalFW content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import folder

# -*- Message Factory Imported Here -*-
from iwlearn.project import projectMessageFactory as _
from iwlearn.project.interfaces import ILegalFW
from iwlearn.project.config import PROJECTNAME

LegalFWSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.ReferenceField(
        'basins',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_(u"Basins"),
            description=_(u"Basins"),
            allow_sorting=True,
        ),
        relationship='basin_framework',
        allowed_types=('Basin',),
        multiValued=True,
    ),

    atapi.StringField(
        'basin_type',
        required=False,
        searchable=True,
        #vocabulary = vocabulary.BASIN_TYPE,
        #widget=atapi.SelectionWidget(
        #    label=_(u"Basin Type"),
        #    description=_(u"Type of Basin"),
        #),
    ),



    atapi.TextField(
        'legal_basis',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Legal Basis"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'member_states',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Member States"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
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


    atapi.TextField(
        'geographical_scope',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Geographical Scope"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'legal_personality',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Legal Personality"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'functions',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Functions"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'organizational_structure',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Organizational Structure"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'relationships',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Relationships"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'decision_making',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Decision Making"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'dispute_resolution',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Dispute Resolution"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'information_sharing',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Data Information Sharing, Exchange, and Harmonization"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'notifications',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Notifications"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'funding',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Funding and Financing"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'benefit_sharing',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Benefit Sharing"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'compliance_and_monitoring',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Compliance and Monitoring"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),


    atapi.TextField(
        'participation_and_stakeholders',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Participation and the Role of Multiple Stakeholders"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'dissolution_and_termination',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Dissolution and Termination"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'additional_remarks',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Additional Remarks"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    atapi.TextField(
        'references_urls',
        required=False,
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Websites and References"),
            description=_(u""),
        ),
        validators=('isTidyHtmlWithCleanup',),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

))



schemata.finalizeATCTSchema(LegalFWSchema, moveDiscussion=False)


class LegalFW(base.ATCTContent):
    """Legal Frameworks"""
    implements(ILegalFW)

    meta_type = "LegalFW"
    schema = LegalFWSchema


atapi.registerType(LegalFW, PROJECTNAME)
