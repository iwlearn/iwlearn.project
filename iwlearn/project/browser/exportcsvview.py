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
            'Agency',
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
            'Executing Agency']


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
            pd['Agency']= '; '.join([self.acronym(e) for e in obj.getAgencies()])
            pd['Country']= '; '.join(obj.getCountry())
            pd['Type']= obj.getProject_type()
            pd['Project Name']= obj.Title()
            pd['Region']= obj.getRegion()
            pd['Subregion']= obj.getSubregion()
            pd['Basin']= '; '.join(obj.getBasin())
            pd['Project Status']=obj.getProject_status()
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
            pd['Phase']= obj.getGef_phase()
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
            writer.writerow(pd)
        output.seek(0)
        self.request.RESPONSE.setHeader('Content-Type','text/csv; charset=utf-8')
        filename = datetime.now().strftime('IWLEARN_Projects_%Y-%m-%d.csv')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s"' % filename)
        return output.read()



