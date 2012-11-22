import logging
from zope.interface import implements, Interface
from DateTime import DateTime
from htmllaundry import sanitize

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.project import projectMessageFactory as _
from iwlearn.project import harvest
from iwlearn.project.interfaces.projectdatabase import IProjectDatabase

logger = logging.getLogger('iwlearn.project')

class IGefOnlineHarvestView(Interface):
    """
    GefOnlineHarvest view interface
    """




class GefOnlineHarvestView(BrowserView):
    """
    GefOnlineHarvest browser view
    """
    implements(IGefOnlineHarvestView)

    view_usage = 'Added Projects'

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

        Id = 'reports'
        title='Technical Reports'
        description='TDAs, SAPs ...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'evaluations'
        title='Evaluations Reports'
        description='mid-term, final, appraisals...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id ='maps_graphics'
        title='Maps/Graphics'
        description='Maps and Graphics'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'data_sets'
        title='Datasets'
        description='measurement, statistical data'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'workshops'
        title='Workshops'
        description='presentations, participants list, meeting reports...'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'photos'
        title='Photos'
        description='Photos and other media'
        object.invokeFactory( 'Folder', id=Id, title=title, description=description)


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
        global_project = (pinfo.get('Region', '').find('Global') > -1)
        countries= harvest.get_countries(pinfo.get('Country',''))
        project_status = pinfo.get('Project Status', None)
        try:
            start_date = DateTime(pinfo.get('Approval Date',None))
        except:
            start_date = None
        if pinfo.has_key('Project Completion Date'):
            end_date = DateTime(pinfo.get('Project Completion Date'))
        else:
            end_date = None
        focal_area = pinfo.get('Focal Area', None)
        operational_program = harvest.split_semicolon(
                    pinfo.get('Operational Program', ''))
        strategic_program = harvest.split_semicolon(
                    pinfo.get('Strategic Program', '')))
        project_allocation = harvest.convert_currency_to_millions(
                            pinfo.get('GEF Grant','0'))
        total_cost = harvest.convert_currency_to_millions(
                            pinfo.get('Project Cost', '0'))
        wb_project_id = pinfo.get('IBRD PO ID', None)
        description = ""
        if pinfo.has_key('GEF Agency'):
            description += u"<h3>GEF Agency</h3> <p> %s </p>" % pinfo.get('GEF Agency')
        if pinfo.has_key('Executing Agency'):
            description += u"<h3>Executing Agency</h3> <p> %s </p>" % pinfo.get('Executing Agency')
        if pinfo.has_key('Description'):
            html = portal_transforms.convert(
                'web_intelligent_plain_text_to_html',
                pinfo.get('Description')).getData()
            description += u"<hr/><br/> %s" % html.decode('utf-8', 'ignore')
        if pinfo.has_key('Implementation Status'):
            description += u"<h3>Implementation Status</h3> <p> %s </p>" % pinfo.get('Implementation Status')

        portal_types.constructContent('Project', self.context, project_id)

        new_project = getattr(self.context,project_id)


        new_project.update(
                        title=name,
                        gef_project_id=project_id,
                        wb_project_id = wb_project_id,
                        globalproject=global_project,
                        country=countries,
                        project_status=project_status,
                        start_date=start_date,
                        focal_area=focal_area,
                        operational_programme=operational_program,
                        gef_project_allocation=str(project_allocation),
                        total_cost=str(total_cost),
                        project_summary=sanitize(description)
                       )

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
        # IW Projects
        gef_project_ids = harvest.extract_gefids_from_page(
                harvest.get_gef_iw_project_page('I'))
        logger.info('%i IW Projects found' % len(gef_project_ids) )
        for projectid in gef_project_ids:
            if projectid in project_ids:
                logger.info('Project %i already in iwlearn.net' % projectid )
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                if pinfo:
                    logger.info('Adding project %i' % projectid )
                    new_projects.append(self.create_project(pinfo, projectid))
                else:
                    logger.info('download failed for project %i' % projectid )
        # Multifocal Projects with Strategic Program IW-*
        gef_project_ids = harvest.extract_gefids_from_page(
                harvest.get_gef_iw_project_page('M'))
        logger.info('%i Multifocal Projects found' % len(gef_project_ids) )
        excluded_ids = list(self.context.getExclude_ids())
        for projectid in gef_project_ids:
            if projectid in project_ids:
                logger.info('Project %i already in iwlearn.net' % projectid )
                continue
            elif str(projectid) in excluded_ids:
                logger.info('Project %i excluded because it is not an IW project' % projectid )
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                if pinfo:
                    logger.info('Is Project %i an IW Project?' % projectid )
                    if pinfo.get('Strategic Program', 'nnn').find('IW-') >= 0:
                        logger.info('Adding project %i' % projectid )
                        new_projects.append(self.create_project(pinfo, projectid))
                    else:
                        logger.info('Project %i is not an IW project' % projectid )
                        excluded_ids.append(str(projectid))
                else:
                    logger.info('download failed for project %i' % projectid )
        if self.context.getInclude_ids():
            included_ids = [int(id) for id in self.context.getInclude_ids()]
        else:
            included_ids = []
        for projectid in included_ids:
            if projectid in excluded_ids:
                excluded_ids.remove(projectid)
            if projectid in project_ids:
                logger.info('Project %i already in iwlearn.net' % projectid )
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                if pinfo:
                    if 'GEF Project ID' in pinfo:
                        logger.info('Adding project %i' % projectid )
                        new_projects.append(self.create_project(pinfo, projectid))
                    else:
                        logger.info('download incomplete for project %i' % projectid )
                else:
                    logger.info('download failed for project %i' % projectid )
        self.context.setExclude_ids(excluded_ids)
        logger.info('harvest complete')
        return new_projects


class GefOnlineUpdateView(GefOnlineHarvestView):

    view_usage = 'Updated Projects'


    def harvest_projects(self):
        projects = self.portal_catalog(portal_type ='Project')
        new_projects =[]
        ratings = harvest.get_projects_ratings()
        for brain in projects:
            ob = brain.getObject()
            projectid = int(ob.getGef_project_id().strip())
            if projectid in ratings:
                iprating = ratings[projectid][0]
                dorating = ratings[projectid][1]
                if iprating != None and dorating != None:
                    if iprating != getattr(ob, 'iprating', None) or dorating != getattr(ob, 'dorating', None):
                        ob.update(iprating = iprating,
                            dorating = dorating)
                        logger.info('Updating project %i rating' % projectid )
                elif iprating !=None and iprating != getattr(ob, 'iprating', None):
                    ob.update(iprating = iprating)
                    logger.info('Updating project %i rating' % projectid )
                elif dorating !=None and dorating != getattr(ob, 'dorating', None):
                    ob.update(dorating = dorating)
                    logger.info('Updating project %i rating' % projectid )
            pinfo = None
            #XXX comment out to skip updateing from gef online
            pinfo = harvest.extract_project_info(projectid)
            if pinfo:
                project_status = pinfo.get('Project Status', None)
                if pinfo.get('Approval Date', None):
                    try:
                        start_date = DateTime(pinfo.get('Approval Date'))
                    except:
                        start_date = None
                else:
                    start_date = None
                project_allocation = harvest.convert_currency_to_millions(
                            pinfo.get('GEF Grant','0'))
                total_cost = harvest.convert_currency_to_millions(
                            pinfo.get('Project Cost', '0'))
                wb_project_id = pinfo.get('IBRD PO ID', None)
                operational_program = harvest.split_semicolon(
                            pinfo.get('Operational Program', ''))
                strategic_program = harvest.split_semicolon(
                            pinfo.get('Strategic Program', '')))
                if wb_project_id:
                    ob.update(wb_project_id=wb_project_id)
                if operational_program:
                    ob.update(operational_program=operational_program)
                if wb_project_id:
                    ob.update(strategic_program=strategic_program)
                #if ob.getProject_status() != project_status:
                #    ob.update(
                #        project_status=project_status,
                #        #start_date=start_date,
                #        gef_project_allocation=str(project_allocation),
                #        total_cost=str(total_cost),
                #        )
                    logger.info('Updating project %i' % projectid )
                    new_projects.append({'name': brain.Title,
                        'url': brain.getURL(),
                        'description': brain.Description})
                else:
                    logger.info('project %i unchanged' % projectid )
            else:
                logger.info('download failed for project %i' % projectid )
        logger.info('harvest complete')
        return new_projects
