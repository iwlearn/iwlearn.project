import csv
import logging
import StringIO

from five.formlib import formbase
from iwlearn.project import projectMessageFactory as _
from iwlearn.project.vocabulary import my_countrylist as _countrylist
from Products.CMFCore.utils import getToolByName
from zope import interface, schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

logger = logging.getLogger(__name__)

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
            #pd['Region']= obj.getField('region').get(obj)
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

    plone_countries = [c['name'] for c in _countrylist.values()]

    def update_project(self, project, data):
            if data['GEF Project ShortName']:
                 project.setProject_shortname(data['GEF Project ShortName'])
            #project.setProject_type(data['Type'])
            #project.setTitle(data['GEF Project Full Title'])
            #XXX data['Associated Basin/Ecosystem']
            #project.setProject_status(data['Status'])
            #project.getField('country').set(project, [v.strip() for v in data['Country'].split(';') if v.strip() in self.plone_countries])
            project.setEcosystem(data['Ecosystem'])
            project.setProject_category([s.strip() for s in ','.join(data['Project Type'].split(';')).split(',')])
            project.setProject_scale(data['Project Scale'])
            project.setPra_sources(data['Information Sources'])
            project.setLessons(data['Key Lessons Learned from Project'])
            project.setKey_results(data['Key Project Results'])
            project.setImpacts(data['Catalytic Impacts'])
            project.setImcs_desc(data['Qualification: Establishment of country-specific inter-ministerial committees'])
            project.setImcs(data['Establishment of country-specific inter-ministerial committees'])
            project.setRegional_frameworks_desc(data['Qualification: Regional legal agreements and cooperation frameworks'])
            project.setRegional_frameworks(data['Regional legal agreements and cooperation frameworks'])
            project.setRmis_desc(data['Qualification: Regional Management Institutions'])
            project.setRmis(data['Regional Management Institutions'])
            project.setReforms_desc(data['Qualification: National/Local reforms'])
            project.setReforms(data['National/Local reforms'])
            project.setTda_priorities_desc(data['Qualification: Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes'])
            project.setTda_priorities(data['Transboundary Diagnostic Analysis: Agreement on transboundary priorities and root causes'])
            project.setSap_devel_desc(data['Qualification: Development of Strategic Action Plan (SAP)'])
            project.setSap_devel(data['Development of Strategic Action Plan (SAP)'])
            project.setAbnj_rmi_desc(data['Qualification: Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)'])
            project.setAbnj_rmi(data['Management measures in ABNJ incorporated in  Global/Regional Management Organizations (RMI)'])
            project.setTdasap_cc_desc(data['Qualification: Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations'])
            project.setTdasap_cc(data['Revised Transboundary Diagnostic Analysis (TDA)/Strategic Action Program (SAP) including Climatic Variability and Change considerations'])
            project.setTda_mnits_desc(data['Qualification: TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities'])
            project.setTda_mnits(data['TDA based on multi-national, interdisciplinary technical and scientific (MNITS) activities'])
            project.setSap_adopted_desc(data['Qualification: Proportion of Countries that have adopted SAP'])
            try:
                i = data['Proportion of Countries that have adopted SAP'].strip('%')
                if i:
                    if i == 'nap':
                        i = -1
                    elif i == 'nav':
                        i =0
                    sap_adopted= int(float(i))
                    project.setSap_adopted(sap_adopted)
                else:
                    project.setSap_adopted(None)
            except:
                logger.error('project %s has invalid data in: Proportion of Countries that have adopted SAP "%s"' % (
                    data[self.id_column], data['Proportion of Countries that have adopted SAP'] ))
                project.setSap_adopted(None)
            project.setSap_implementing_desc(data['Qualification: Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)'])
            try:
                i = data['Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)'].strip('%')
                if i:
                    if i == 'nap':
                        i = -1
                    elif i == 'nav':
                        i = 0
                    sap_implementing= int(float(i))
                    project.setSap_implementing(sap_implementing)
                else:
                    project.setSap_implementing(None)
            except:
                logger.error('project %s has invalid data in: Proportion of countries that are implementing specific measures from the SAP - "%s"' % (
                data[self.id_column], data['Proportion of countries that are implementing specific measures from the SAP (i.e. adopted national policies, laws, budgeted plans)']) )
                project.setSap_adopted(None)
            project.setSap_inc_desc(data['Qualification: Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc'])
            project.setSap_inc(data['Incorporation of (SAP, etc.) priorities with clear commitments and time frames into CAS, PRSPs, UN Frameworks, UNDAF, key agency strategic documents including financial commitments and time frames, etc'])
            project.setKey_process_results(data['Other Key Process Results'])

            logger.info('Updating project %s' % data[self.id_column] )
