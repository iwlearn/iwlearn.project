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
            project.setGef_phase(data['Phase'])
            #pd['Project Type #1']= None
            #pd['Project Type #2']= None
            #pd['Project Type #3']= None
            #pd['Prog App']= None
            #pd['Multi FA']= None
            #pd['SAP']= None
            #pd['Keywords']= '; '.join(obj.Subject())
            logger.info('Updating project %s' % data['ID'] )


    @form.action('Submit')
    def actionSubmit(self, action, data):
        f = StringIO.StringIO(data['csvupload'])
        reader = csv.DictReader(f)
        pdict = {}
        for row in reader:
            try:
                pdict[int(row['ID'])] = row
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




