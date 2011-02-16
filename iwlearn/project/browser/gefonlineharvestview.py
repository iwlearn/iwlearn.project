from zope.interface import implements, Interface
from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import harvest
from iwlearn.project.interfaces.projectdatabase import IProjectDatabase

class IsProjectDb(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_projectdb(self):
        return IProjectDatabase.providedBy(self.context)

class IGefOnlineHarvestView(Interface):
    """
    GefOnlineHarvest view interface
    """




class GefOnlineHarvestView(BrowserView):
    """
    GefOnlineHarvest browser view
    """
    implements(IGefOnlineHarvestView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def _create_project_folders(self, object):
        Id = "project_doc"
        title = 'Project Documents'
        description = 'project document, fact sheets, annexes...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = "links"
        title = 'Links'
        description = 'Links to further information about the project or project objectives'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'newsletters'
        title='Outreach materials'
        description="newsletters, brochures."
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)
        #newfolder.reindexObject()

        Id = 'reports'
        title='Technical Reports'
        description='TDAs, SAPs ...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)
        #object.manage_renameObject(id=Id, new_id= 'reports')

        Id = 'evaluations'
        title='Evaluations Reports'
        description='mid-term, final, appraisals...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)

        Id ='maps_graphics'
        title='Maps/Graphics'
        description='Maps and Graphics'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)


        Id = 'data_sets'
        title='Datasets'
        description='measurement, statistical data'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)

        Id = 'workshops'
        title='Workshops'
        description='presentations, participants list, meeting reports...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)
        #newfolder = getattr(object,Id)
        #newfolder.setTitle(title)
        #newfolder.setDescription(description)



    def create_project(self, pinfo, gpid):
        '''
        create a new project out of the data harvested from gefonline.
        unused attributes:
    ['', 'PDF A Amount', 'GEF Project Grant (CEO Appr.)',
    'PDF-B (Supplemental-2) Approval Date', 'Project Cancellation Date',
    'PPG Amount', 'Cofinancing Total (CEO Endo.)',
    'GEF Agency Fees (CEO Endo.)', 'UNDP PMIS ID', 'Funding Source',
     'PDF-C Approval Date',
    'GEF Project Grant', ,
    'PIF Approval Date', 'Cofinancing Total (CEO Appr.)',
    'PDF-A Approval Date', 'PPG Approval Date', 'PRIF Amount', ,
    'PDF-B Approval Date',
    'GEF Project Grant (CEO Endo.)', 'GEF Agency Fees', 'PDF B Amount',
    'PDF C Amount', 'CEO Endorsement Date',
    'GEF Agency', 'Pipeline Entry Date', 'Cofinancing Total',
    'PDF-B (Supplemental) Approval Date',
    'Strategic Program', 'Project Cost (CEO Appr.)', 'IBRD PO ID',
    'GEF Agency Approval Date', 'GEF Agency Fees (CEO Appr.)',
    'Project Cost (CEO Endo.)']
        '''
        portal_transforms = getToolByName(self, 'portal_transforms')
        portal_types = getToolByName(self, 'portal_types')
        wftool = getToolByName(self, 'portal_workflow')
        if gpid != int(pinfo['GEF Project ID'].strip()):
            return {'name': 'Error in GEF Project ID', 'url': ''}
        name = pinfo['Project Name']
        url = self.context.absolute_url() + '/' + pinfo['GEF Project ID']

        project_id = pinfo.get('GEF Project ID').strip()
        global_project = pinfo.get('Region', '').startswith('Global')
        countries= harvest.get_countries(pinfo.get('Country',''))
        #project_type =
        project_status = pinfo.get('Project Status', None)
        start_date = DateTime(pinfo.get('Approval Date',None))
        if pinfo.has_key('Project Completion Date'):
            end_date = DateTime(pinfo.get('Project Completion Date'))
        else:
            end_date = None
        focal_area = pinfo.get('Focal Area', None)
        operational_program = pinfo.get('Operational Program', None)
        project_allocation = harvest.convert_currency_to_millions(
                            pinfo.get('GEF Grant',None))
        total_cost = harvest.convert_currency_to_millions(
                            pinfo.get('Project Cost', None))

        description = ""
        if pinfo.has_key('GEF Agency'):
            description += "<h3>GEF Agency</h3> <p> %s </p>" % pinfo.get('GEF Agency')

        if pinfo.has_key('Executing Agency'):
            description += "<h3>Executing Agency</h3> <p> %s </p>" % pinfo.get('Executing Agency')
        if pinfo.has_key('Description'):
            html = portal_transforms.convert(
                'web_intelligent_plain_text_to_html',
                pinfo.get('Description')).getData()
            description += "<hr/><br/> %s" % html
        if pinfo.has_key('Implementation Status'):
            description += "<h3>Implementation Status</h3> <p> %s </p>" % pinfo.get('Implementation Status')

        #self.context.invokeFactory( 'Project', id= project_id, title=name)
        portal_types.constructContent('Project', self.context, project_id)

        new_project = getattr(self.context,project_id)
        #new_project.setTitle(name)
        #new_project.setGef_project_id(project_id)
        ##project.SetRemote_url
        #new_project.setGlobalproject(global_project)
        #new_project.setCountry(countries)
        ##project.SetProject_type
        #new_project.SetProject_status(project_status)
        #new_project.SetStart_date(start_date)
        #new_project.SetEnd_date(end_date)
        ##project.SetStrategic_priority
        #new_project.SetFocal_area(focal_area)

        #new_project.SetOperational_programme(operational_program)
        #new_project.SetGef_project_allocation(project_allocation)
        #new_project.SetTotal_cost(total_cost)
        #new_project.SetProject_summary(description)

        new_project.update(
                        title=name,
                        gef_project_id=project_id,
                        globalproject=global_project,
                        country=countries,
                        project_status=project_status,
                        start_date=start_date,
                        focal_area=focal_area,
                        operational_programme=operational_program,
                        gef_project_allocation=str(project_allocation),
                        total_cost=str(total_cost),
                        project_summary=description
                       )




        #new_project.Title = name
        #new_project.gef_project_id = project_id
        ##project.SetRemote_url
        #new_project.globalproject = global_project
        #new_project.country = countries
        ##project.SetProject_type
        #new_project.project_status =project_status
        #new_project.start_date = start_date
        #new_project.end_date =end_date
        ##project.SetStrategic_priority
        #new_project.focal_area = focal_area
        #new_project.operational_programme = operational_program
        #new_project.gef_project_allocation =project_allocation
        #new_project.total_cost = total_cost
        #new_project.project_summary =description



        self._create_project_folders(new_project)
        wftool.doActionFor(new_project, 'submit')
        return {'name': name, 'url': url, 'description': description}

    def harvest_projects(self):
        projects = self.portal_catalog(portal_type ='Project')
        project_ids=[]
        new_projects=[]
        for brain in projects:
            ob = brain.getObject()
            if ob.getGef_project_id():
                project_ids.append(int(ob.getGef_project_id().strip()))
        gef_project_ids = harvest.extract_gefids_from_page(
                harvest.get_gef_iw_project_page())
        for projectid in gef_project_ids:
            if projectid in project_ids:
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                new_projects.append(self.create_project(pinfo, projectid))
        return new_projects

