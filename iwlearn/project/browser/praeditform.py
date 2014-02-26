from zope.interface import implements
from zope.interface import Interface
from z3c.form import form, field, button
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _


class IPraForm(Interface):

    iprating = schema.Int(
        required = False,
        title = _(u'IP Rating'),
        description=_(u""),
    )

    dorating = schema.Int(
        required = False,
        title = _(u'DO Rating'),
        description=_(u""),
    )

    outcomerating = schema.Int(
        required = False,
        title = _(u'TE Rating'),
        description=_(u""),
    )


# project result ratings:


    pra_sources = schema.TextLine(
        title=_(u'Information Sources'),
        description=_(u""),
        required = False,
        default=u"",
    )


    lessons = schema.Text(
        title=_(u"Key Lessons Learned from Project"),
        description=_(u""),
        required = False,
        default=u"",
    )

    key_results = schema.Text(
        title=_(u"Key Project Results"),
        description=_(u""),
        required = False,
        default=u"",
    )

    impacts = schema.Text(
        title=_(u"Catalytic Impacts"),
        description=_(u""),
        required = False,
        default=u"",
    )


    imcs = schema.TextLine(
        title=_(u"Establishment of country-specific inter-ministerial committees"),
        description=_(u"National Inter-Ministry Committees (IMCs)"),
        required = False,
        default=u"",
    )

    imcs_desc = schema.Text(
        title=_(u"Establishment of country-specific inter-ministerial committees"),
        description=_(u"National Inter-Ministry Committees (IMCs)"),
        required = False,
        default=u"",
    )

    regional_frameworks = schema.TextLine(
        title=_(u"Regional legal agreements and cooperation frameworks"),
        description=_(u""),
        required = False,
        default=u"",
    )

    regional_frameworks_desc = schema.Text(
        title=_(u"Regional legal agreements and cooperation frameworks"),
        description=_(u""),
        required = False,
        default=u"",
    )

    rmis = schema.TextLine(
        title=_(u"Regional Management Institutions"),
        description=_(u""),
        required = False,
        default=u"",
    )

    rmis_desc = schema.Text(
        title=_(u"Regional Management Institutions"),
        description=_(u""),
        required = False,
        default=u"",
    )

    reforms = schema.TextLine(
        title=_(u"National/Local reforms"),
        description=_(u""),
        required = False,
        default=u"",
    )

    reforms_desc = schema.Text(
        title=_(u"National/Local reforms"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tda_priorities = schema.TextLine(
        title=_(u"Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tda_priorities_desc = schema.Text(
        title=_(u"Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_devel = schema.TextLine(
        title=_(u"Development of Strategic Action Plan (SAP)"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_devel_desc = schema.Text(
        title=_(u"Development of Strategic Action Plan (SAP)"),
        description=_(u""),
        required = False,
        default=u"",
    )

    abnj_rmi = schema.TextLine(
        title=_(u"Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"),
        description=_(u""),
        required = False,
        default=u"",
    )

    abnj_rmi_desc = schema.Text(
        title=_(u"Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tdasap_cc = schema.TextLine(
        title=_(u"Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tdasap_cc_desc = schema.Text(
        title=_(u"Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tda_mnits = schema.TextLine(
        title=_(u"TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"),
        description=_(u""),
        required = False,
        default=u"",
    )

    tda_mnits_desc = schema.Text(
        title=_(u"TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_adopted = schema.TextLine(
        title=_(u"Proportion of Countries that have adopted SAP"),
        description=_(u"In %. 0 = None, 100=All"),
        required = False,
        default=u"",
    )

    sap_adopted_desc = schema.Text(
        title=_(u"Proportion of Countries that have adopted SAP"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_implementing = schema.TextLine(
        title=_(u"Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"),
        description=_(u"In %. 0 = None, 100=All"),
        required = False,
        default=u"",
    )

    sap_implementing_desc = schema.Text(
        title=_(u"Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_inc = schema.TextLine(
        title=_(u"Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"),
        description=_(u""),
        required = False,
        default=u"",
    )

    sap_inc_desc = schema.Text(
        title=_(u"Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"),
        description=_(u""),
        required = False,
        default=u"",
    )

    key_process_results = schema.Text(
        title=_(u"Other Key Process Results"),
        description=_(u""),
        required = False,
        default=u"",
    )

class PRA(object):
    implements(IPraForm)

    FIELDS = [ 'pra_sources', 'outcomerating', 'dorating', 'iprating',
        'imcs_desc', 'imcs', 'impacts', 'key_results', 'lessons',
        'rmis', 'regional_frameworks_desc', 'regional_frameworks',
        'tda_priorities', 'reforms_desc', 'reforms', 'rmis_desc',
        'abnj_rmi', 'sap_devel_desc', 'sap_devel', 'tda_priorities_desc',
        'abnj_rmi_desc', 'tdasap_cc', 'tdasap_cc_desc', 'tda_mnits',
        'tda_mnits_desc', 'sap_adopted', 'sap_adopted_desc', 'sap_implementing',
        'sap_implementing_desc', 'sap_inc', 'sap_inc_desc', 'key_process_results']

    def __init__(self, context):
        self.context = context
        for field in self.FIELDS:
            setattr(self, field, getattr(self.context, field))


class PraUpdateForm(form.Form):
    """form to update project results"""

    fields = field.Fields(IPraForm)
    RICH_TEXT_FIELDS = [
        'imcs_desc',  'impacts', 'key_results', 'lessons',
        'regional_frameworks_desc',
        'reforms_desc', 'rmis_desc',
        'sap_devel_desc', 'tda_priorities_desc',
        'abnj_rmi_desc', 'tdasap_cc_desc',
        'tda_mnits_desc', 'sap_adopted_desc',
        'sap_implementing_desc', 'sap_inc_desc', 'key_process_results']

    for field in RICH_TEXT_FIELDS:
        fields[field].widgetFactory = WysiwygFieldWidget



    def __init__(self, context, request):
        super(PraUpdateForm, self).__init__(context, request)
        self.request.set('disable_border', True)


    @button.buttonAndHandler(u'Save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            for k, v in data.iteritems():
                if (getattr(self.context, k) != v) and v:
                    setattr(self.context, k, v)
        self.request.response.redirect(self.context.absolute_url() + '/@@resultsview.html')
        return

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url() + '/@@resultsview.html')


UpdatePra = wrap_form(PraUpdateForm)
