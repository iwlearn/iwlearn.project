import csv
import StringIO
import logging
from zope import interface, schema
from zope.formlib import form
from five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _

logger = logging.getLogger('iwlearn.project')

class IImportCSVSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    csvupload = schema.Bytes(
        title=_(u'CSV File'),
        description=_(u'CSV File to be uploaded'),
        required=True,
        readonly=False,
        default=None,
        )


class ImportCSV(formbase.PageForm):
    form_fields = form.FormFields(IImportCSVSchema)
    label = _(u'Import CSV')
    description = _(u'''Import a CSV file to add new projects to the
    Project DB and to update existing projects with data from the CSV''')

    id_column = 'ID'
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    def update_project(self, project, data):
            if data['Country']=="Global":
                 project.setGlobalproject(True)
            project.setProject_type(data['Type'])
            #pd['Project Name']= obj.Title()
            #pd['Region']= obj.getRegion()
            project.setProject_status(data['Status'])
            #pd['FOCAL AREA']='; '.join(obj.getFocal_area())
            #pd['Approval Date']= None
            start = end = None
            #pd['FY']= None
            #pd['Staff']= '; '.join([s.Title() for s in obj.getProject_contacts()])
            #pd['GEFAmount']= obj.getGef_project_allocation()
            #pd['Cofin Amt']= None
            #pd['Fee Total']= None
            #pd['Project Cost']= obj.getTotal_cost()
            #pd['CEO Endorsement Date']= None
            if data['Phase']:
                phase = data['Phase'].replace(' ', '').replace('-','').lower()
                if phase == 'pilot':
                    project.setGef_phase('0')
                elif phase.startswith('gef') and len(phase) == 4:
                    iphase = int(phase[3])
                    project.setGef_phase(str(iphase))
                else:
                    logger.warn('Invalid phase %s for  project %s' % (
                            data['Phase'], data[self.id_column]) )
            #pd['Project Type #1']= None
            #pd['Project Type #2']= None
            #pd['Project Type #3']= None
            #pd['Prog App']= None
            #pd['Multi FA']= None
            #pd['SAP']= None
            #pd['Keywords']= '; '.join(obj.Subject())
            logger.info('Updating project %s' % data[self.id_column] )


    @form.action('Submit')
    def actionSubmit(self, action, data):
        f = StringIO.StringIO(data['csvupload'])
        reader = csv.DictReader(f)
        pdict = {}
        for row in reader:
            try:
                pdict[int(row[self.id_column])] = row
            except:
                continue
        projects = self.portal_catalog(portal_type ='Project')
        for brain in projects:
            ob = brain.getObject()
            projectid = int(ob.getGef_project_id().strip())
            if projectid in pdict:
                self.update_project(ob, pdict.pop(projectid))
        include = list(self.context.getInclude_ids())
        include += [str(k) for k in pdict]
        include.sort()
        self.context.setInclude_ids(include)
        logger.info('Update complete')

class ImportRACSV(ImportCSV):

    description = _(u'''Import a CSV file to add the resultsarchive
                to the projectdb''')
    id_column = 'GEFID'

    def update_project(self, project, data):
            if data['GEF Project ShortName']:
                 project.setProject_shortname(data['GEF Project ShortName'])
            #project.setProject_type(data['Project Type'])
            #project.setTitle(data['GEF Project Full Title'])
            #XXX data['Associated Basin/Ecosystem']
            #project.setProject_status(data['Status'])
            project.setPra_sources(data['Information Sources'])
            project.setLessons(data['Key Lessons Learned from Project'])
            project.setKey_results(data['Key Project Results'])
            project.setImpacts(data['Catalytic Impacts'])
            project.setCsim_committees_desc(data['Establishment of country-specific inter-ministerial committees'])
            project.setCsim_committees(data['Establishment of country-specific inter-ministerial committees rating'])
            project.setRegional_frameworks_desc(data['Regional legal agreements and cooperation frameworks'])
            project.setRegional_frameworks(data['Regional legal agreements and cooperation frameworks rating'])
            project.setRmis_desc(data['Regional Management Institutions'])
            project.setRmis(data['Regional Management Institutions rating'])
            project.setReforms_desc(data['National/Local reforms'])
            project.setReforms(data['National/Local reforms rating'])
            project.setTda_priorities_desc(data['Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes'])
            project.setTda_priorities(data['Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes rating'])
            project.setSap_devel_desc(data['Development of Strategic Action Plan (SAP)'])
            project.setSap_devel(data['Development of Strategic Action Plan (SAP) rating'])
            project.setAbnj_rmi_desc(data['Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)'])
            project.setAbnj_rmi(data['Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI) rating'])
            project.setTdasap_cc_desc(data['Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations'])
            project.setTdasap_cc(data['Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations rating'])
            project.setTda_mnits_desc(data['TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities'])
            project.setTda_mnits(data['TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities rating'])
            project.setSap_adopted_desc(data['Proportion of Countries that have adopted SAP'])
            project.setSap_adopted(data['Proportion of Countries that have adopted SAP rating'])
            project.setSap_implementing_desc(data['Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)'])
            project.setSap_implementing(data['Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans) rating'])
            project.setSap_inc_desc(data['Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc'])
            project.setSap_inc(data['Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc rating'])
            project.setKey_process_results(data['Other Key Process Results'])

            logger.info('Updating project %s' % data[self.id_column] )