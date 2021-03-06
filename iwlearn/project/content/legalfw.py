"""Definition of the LegalFW content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import folder
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from iwlearn.project import projectMessageFactory as _
from iwlearn.project import vocabulary
from iwlearn.project.interfaces import ILegalFW
from iwlearn.project.config import PROJECTNAME

LegalFWSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField(
        'basin_type',
        label=_(u"Basin Type"),
        description=_(u"Type of Basin"),
        required=False,
        searchable=True,
        vocabulary = vocabulary.BASIN_TYPE,
        widget=atapi.SelectionWidget(
            label=_(u"Basin Type"),
            description=_(u"Type of Basin"),
        ),
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
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),

    atapi.ComputedField(
        'region',
        required=True,
        searchable=True,
        expression = 'context._computeRegions()',
        widget=atapi.ComputedWidget(
            label=_(u"Geographic Region"),
            description=_(u"Geographic Region in which the project operates"),
        ),

    ),

    atapi.ComputedField(
        'subregion',
        required=False,
        searchable=True,
        expression = 'context._computeSubregions()',
        widget=atapi.ComputedWidget(
            label=_(u"Geographic Sub Region"),
            description=_(u"Geographic Sub Region in which the project operates"),
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
        'lfrelationships',
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



schemata.finalizeATCTSchema(LegalFWSchema, folderish=True, moveDiscussion=False)


class LegalFW(folder.ATFolder):
    """Legal Frameworks"""
    implements(ILegalFW)

    meta_type = "LegalFW"
    schema = LegalFWSchema

    # Moved to extender
    # def _computeRegions(self):
    #     return ','.join(vocabulary.get_regions(
    #                 countries=self.getCountry()))

    # def _computeSubregions(self):
    #     return ','.join(vocabulary.get_subregions(
    #             countries=self.getCountry()))

    # def getSubRegions(self):
    #     """ get region + subregion for indexing """
    #     countries=self.getCountry()
    #     if countries:
    #         sr = vocabulary.get_subregions(countries=countries)
    #         r = vocabulary.get_regions(countries=countries)
    #         return r + sr

    # def getBasin(self):
    #     basins = self.getBasins()
    #     titles = []
    #     for basin in basins:
    #         if basin is not None:
    #              titles.append(basin.Title())
    #     return titles

atapi.registerType(LegalFW, PROJECTNAME)
