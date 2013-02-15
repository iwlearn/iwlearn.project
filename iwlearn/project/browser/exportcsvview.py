#
import logging
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import csv
from datetime import datetime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _


logger = logging.getLogger('iwlearn.project')

CSV_FIELDS= ['ID',
            "GEF Project ShortName",
            'Agency',
            'IBRD ID',
            'Country',
            'Type',
            'Project Name',
            'Region',
            'Subregion',
            'Basin',
            'Status',
            'FOCAL AREA',
            'Approval Date',
            'Start',
            'End',
            'FY',
            'Staff',
            'GEFAmount',
            'Cofin Amt',
            'Fee Total',
            'Project Cost',
            'CEO Endorsement Date',
            'Phase',
            'Project Type #1',
            'Project Type #2',
            'Project Type #3',
            'Prog App',
            'Multi FA',
            'SAP',
            'Keywords',
            'Url',
            'Strategic Program',
            'Operational Program',
            'Executing Agency',
            "Information Sources",
            "Key Lessons Learned from Project",
            "Key Project Results",
            "Catalytic Impacts",
            "Establishment of country-specific inter-ministerial committees",
            "Qualification: Establishment of country-specific inter-ministerial committees",
            "Regional legal agreements and cooperation frameworks",
            "Qualification: Regional legal agreements and cooperation frameworks",
            "Regional Management Institutions",
            "Qualification: Regional Management Institutions",
            "National/Local reforms",
            "Qualification: National/Local reforms",
            "Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes",
            "Qualification: Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes",
            "Development of Strategic Action Plan (SAP)",
            "Qualification: Development of Strategic Action Plan (SAP)",
            "Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)",
            "Qualification: Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)",
            "Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations",
            "Qualification: Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations",
            "TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities",
            "Qualification: TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities",
            "Proportion of Countries that have adopted SAP",
            "Qualification: Proportion of Countries that have adopted SAP",
            "Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)",
            "Qualification: Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)",
            "Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc",
            "Qualification: Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc",
            "Other Key Process Results",
            ]


class IExportCSVView(Interface):
    """
    ExportCSV view interface
    """



class ExportCSVView(BrowserView):
    """
    ExportCSV browser view
    """
    implements(IExportCSVView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def acronym(self, agency):
        if agency.find('(') > -1:
            return agency[agency.find('(') +1 : agency.find(')')]
        else:
            return agency


    def __call__(self):
        """
        return a CSV Representation of the data in the projectdb
        """
        output = StringIO()
        fieldnames = CSV_FIELDS
        writer = csv.DictWriter(output, fieldnames)
        brains = self.portal_catalog(portal_type = 'Project')

        #writer.writeheader()
        pd = {}
        for field in fieldnames:
            pd[field] = field
        writer.writerow(pd)

        for brain in brains:
            pd = {}
            obj = brain.getObject()
            pd['ID']= int(obj.getGef_project_id())
            pd['Project Name']= obj.Title()
            pd['GEF Project ShortName']=obj.getProject_shortname()
            pd['Agency']= '; '.join([self.acronym(e) for e in obj.getAgencies()])
            pd['IBRD ID']= obj.getWb_project_id()
            pd['Country']= '; '.join(obj.getCountry())
            pd['Type']= obj.getProject_type()
            pd['Region']= obj.getRegion()
            pd['Subregion']= obj.getSubregion()
            pd['Basin']= '; '.join(obj.getBasin())
            pd['Status']=obj.getProject_status()
            pd['FOCAL AREA']='; '.join(obj.getFocal_area())
            pd['Approval Date']= None
            start = end = None
            if obj.getStart_date():
                start = obj.getStart_date().strftime('%Y-%m-%d')
            if obj.getEnd_date():
                end = obj.getEnd_date().strftime('%Y-%m-%d')
            pd['Start']= start
            pd['End']= end
            pd['FY']= None
            pd['Staff']= '; '.join([s.Title() for s in obj.getProject_contacts()])
            pd['GEFAmount']= obj.getGef_project_allocation()
            pd['Cofin Amt']= None
            pd['Fee Total']= None
            pd['Project Cost']= obj.getTotal_cost()
            pd['CEO Endorsement Date']= None
            if obj.getGef_phase() == '0':
                pd['Phase']= 'Pilot'
            else:
                pd['Phase']= 'GEF - ' + str(obj.getGef_phase())
            pd['Project Type #1']= None
            pd['Project Type #2']= None
            pd['Project Type #3']= None
            pd['Prog App']= None
            pd['Multi FA']= None
            pd['SAP']= None
            pd['Keywords']= '; '.join(obj.Subject())
            pd['Url']= obj.getRemoteUrl()
            pd['Strategic Program']= '; '.join(obj.getStrategic_priority())
            pd['Operational Program']= '; '.join(obj.getOperational_programme())
            pd['Executing Agency']= '; '.join([e.Title() for e in obj.getExecuting_agency()])
            pd["Information Sources"]=obj.getPra_sources()
            pd["Key Lessons Learned from Project"]=obj.getLessons()
            pd["Key Project Results"]=obj.getKey_results()
            pd["Catalytic Impacts"]=obj.getImpacts()
            pd["Establishment of country-specific inter-ministerial committees"]=obj.getImcs()
            pd["Qualification: Establishment of country-specific inter-ministerial committees"]=obj.getImcs_desc()
            pd["Regional legal agreements and cooperation frameworks"]=obj.getRegional_frameworks()
            pd["Qualification: Regional legal agreements and cooperation frameworks"]=obj.getRegional_frameworks_desc()
            pd["Regional Management Institutions"]=obj.getRmis()
            pd["Qualification: Regional Management Institutions"]=obj.getRmis_desc()
            pd["National/Local reforms"]=obj.getReforms()
            pd["Qualification: National/Local reforms"]=obj.getReforms_desc()
            pd["Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"]=obj.getTda_priorities()
            pd["Qualification: Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes"]=obj.getTda_priorities_desc()
            pd["Development of Strategic Action Plan (SAP)"]=obj.getSap_devel()
            pd["Qualification: Development of Strategic Action Plan (SAP)"]=obj.getSap_devel_desc()
            pd["Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"]=obj.getAbnj_rmi()
            pd["Qualification: Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)"]=obj.getAbnj_rmi_desc()
            pd["Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"]=obj.getTdasap_cc()
            pd["Qualification: Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations"]=obj.getTdasap_cc_desc()
            pd["TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"]=obj.getTda_mnits()
            pd["Qualification: TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities"]=obj.getTda_mnits_desc()
            pd["Proportion of Countries that have adopted SAP"]=obj.getSap_adopted()
            pd["Qualification: Proportion of Countries that have adopted SAP"]=obj.getSap_adopted_desc()
            pd["Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"]=obj.getSap_implementing()
            pd["Qualification: Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)"]=obj.getSap_implementing_desc()
            pd["Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"]=obj.getSap_inc()
            pd["Qualification: Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc"]=obj.getSap_inc_desc()
            pd["Other Key Process Results"]=obj.getKey_process_results()
            writer.writerow(pd)
            try:
                obj.r4imcs()
            except:
                logger.error('pid: %s r4imcs: %s' % (obj.getGef_project_id(), obj.imcs))
            try:
                obj.r4regional_frameworks()
            except:
                logger.error('pid: %s r4regional_frameworks: %s' % (obj.getGef_project_id(),
                obj.regional_frameworks))
            try:
                obj.r4rmis()
            except:
                logger.error('pid: %s r4rmis: %s' % (obj.getGef_project_id(), obj.rmis))
            try:
                obj.r4reforms()
            except:
                logger.error('pid: %s r4reforms: %s' % (obj.getGef_project_id(), obj.reforms))
            try:
                obj.r4tda_priorities()
            except:
                logger.error('pid: %s r4tda_priorities: %s' % (obj.getGef_project_id(), obj.tda_priorities))
            try:
                obj.r4sap_devel()
            except:
                logger.error('pid: %s r4sap_devel: %s' % (obj.getGef_project_id(), obj.sap_devel))
            try:
                obj.r4abnj_rmi()
            except:
                logger.error('pid: %s r4abnj_rmi: %s' % (obj.getGef_project_id(), obj.abnj_rmi))
            try:
                obj.r4tdasap_cc()
            except:
                logger.error('pid: %s r4tdasap_cc: %s' % (obj.getGef_project_id(), obj.tdasap_cc))
            try:
                obj.r4tda_mnits()
            except:
                logger.error('pid: %s r4tda_mnits: %s' % (obj.getGef_project_id(), obj.tda_mnits))
            try:
                obj.r4sap_adopted()
            except:
                logger.error('pid: %s r4sap_adopted: %s' % (obj.getGef_project_id(), obj.sap_adopted))
            try:
                obj.r4sap_implementing()
            except:
                logger.error('pid: %s r4sap_implementing: %s' % (obj.getGef_project_id(), obj.sap_implementing))
            try:
                obj.r4sap_inc()
            except:
                logger.error('pid: %s r4sap_inc: %s' % (obj.getGef_project_id(), obj.sap_inc))




        output.seek(0)
        self.request.RESPONSE.setHeader('Content-Type','text/csv; charset=utf-8')
        filename = datetime.now().strftime('IWLEARN_Projects_%Y-%m-%d.csv')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s"' % filename)
        return output.read()



