import logging
import transaction
from zope.interface import implements, Interface
from DateTime import DateTime
from htmllaundry import sanitize

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.geo.contentlocations.interfaces import IGeoManager

from iwlearn.project.vocabulary import my_countrylist as _countrylist
from iwlearn.project import projectMessageFactory as _
from iwlearn.project import harvest
from iwlearn.project.interfaces.projectdatabase import IProjectDatabase

logger = logging.getLogger('iwlearn.project')

UNEP_GEF_PHASE = {'Pilot': '0',
                'I': '1',
                'II': '2',
                'III': '3',
                'IV': '4',
                'V': '5',
                'VI': '6',}

PLONE_COUNTRIES = [c['name'] for c in _countrylist.values()]


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

    def _create_project_folders(self, obj):
        Id = "project_doc"
        title = 'Project Documents'
        description = 'project document, fact sheets, annexes...'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = "links"
        title = 'Links'
        description = 'Links to further information about the project or project objives'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'newsletters'
        title='Outreach materials'
        description="newsletters, brochures."
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'reports'
        title='Technical Reports'
        description='TDAs, SAPs ...'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'evaluations'
        title='Evaluations Reports'
        description='mid-term, final, appraisals...'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id ='maps_graphics'
        title='Maps/Graphics'
        description='Maps and Graphics'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'data_sets'
        title='Datasets'
        description='measurement, statistical data'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'workshops'
        title='Workshops'
        description='presentations, participants list, meeting reports...'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)

        Id = 'photos'
        title='Photos'
        description='Photos and other media'
        if not hasattr(obj, Id):
            obj.invokeFactory( 'Folder', id=Id, title=title, description=description)


    def _create_project_location(self, project, location, project_name, description):
        wftool = getToolByName(self, 'portal_workflow')
        if not hasattr(project, 'maps_graphics'):
            Id ='maps_graphics'
            title='Maps/Graphics'
            description='Maps and Graphics'
            project.invokeFactory( 'Folder', id=Id, title=title, description=description)
            wftool.doActionFor( project['maps_graphics'], 'submit')
        mgfolder = project['maps_graphics']
        if not hasattr(mgfolder, 'project_locations'):
            Id ='project_locations'
            title='Project locations'
            description='Project Locations, Hotspots and Demonstration Sites'
            mgfolder.invokeFactory( 'Folder', id=Id, title=title, description=description)
            locfolder = mgfolder['project_locations']
            locfolder.setLayout('kml-openlayers')
            wftool.doActionFor(locfolder,'submit')
        else:
            locfolder = mgfolder['project_locations']
        if location['geoLocId'] not in locfolder.objectIds():
            Id = location['geoLocId']
            title = location['geoLocName']
            locfolder.invokeFactory('Document', id=Id, title=title, description=project_name)
            obj = locfolder[Id]
            obj.update(text=description)
            lat = float(location['latitude'])
            lon = float(location['longitude'])
            geo = IGeoManager(obj)
            geo.setCoordinates('Point', (lon, lat))
            wftool.doActionFor( obj,  'submit')
        #else:
        #    locob = locfolder[location['geoLocId']]
        #    if not locob.Description():
        #        if project_name:
        #            locob.update(description=project_name)
        #        elif description:
        #            locob.update(description=description)
        #            description = None
        #        if description:
        #            locob.update(text=description)

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
    'Strategic Program', 'Project Cost (CEO Appr.)',
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
        if 'Regional' in pinfo.get('Region', ''):
            project_scale = 'Regional'
        elif 'Global' in pinfo.get('Region', '') or 'Global' in pinfo.get('Country', ''):
             project_scale = 'Global'
        else:
            project_scale = 'National'
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
                    pinfo.get('Strategic Program', ''))
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
                        #globalproject=global_project,
                        country=countries,
                        project_status=project_status,
                        start_date=start_date,
                        end_date=end_date,
                        focal_area=focal_area,
                        operational_programme=operational_program,
                        strategic_priority = strategic_program,
                        gef_project_allocation=str(project_allocation),
                        total_cost=str(total_cost),
                        project_summary=sanitize(description),
                        project_scale=project_scale,
                       )

        self._create_project_folders(new_project)
        wftool.doActionFor(new_project, 'submit')
        return {'name': name, 'url': url, 'description': description}

    def harvest_projects(self):
        logger.info('starting harvest')
        projects = self.portal_catalog(portal_type ='Project')
        project_ids=[]
        new_projects=[]
        done = 0
        for brain in projects:
            obj = brain.getObject()
            if obj.getGef_project_id():
                project_ids.append(int(obj.getGef_project_id().strip()))
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
                    done += 1
                    logger.info('Adding project %i' % projectid )
                    new_projects.append(self.create_project(pinfo, projectid))
                    project_ids.append(projectid)
                    if done % 10 == 0:
                        # Commit subtransaction for every 10th processed item
                        transaction.get().commit()
                else:
                    logger.info('download failed for project %i' % projectid )
        transaction.get().commit()
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
                        done += 1
                        logger.info('Adding project %i' % projectid )
                        new_projects.append(self.create_project(pinfo, projectid))
                        project_ids.append(projectid)
                        if done % 10 == 0:
                            # Commit subtransaction for every 10th processed item
                            transaction.get().commit()
                    else:
                        logger.info('Project %i is not an IW project' % projectid )
                        excluded_ids.append(str(projectid))
                else:
                    logger.info('download failed for project %i' % projectid )
        transaction.get().commit()
        if self.context.getInclude_ids():
            included_ids = [int(id) for id in set(self.context.getInclude_ids())]
        else:
            included_ids = []
        unep_iw_projects = harvest.get_unep_iw_projects()
        for p in unep_iw_projects:
            try:
                if int(p['GEFid']) not in included_ids:
                    included_ids.append(int(p['GEFid']))
                    logger.info('apppended UNEP Project with GefId %s' % p['GEFid'])
            except:
                pass
        for projectid in included_ids:
            if str(projectid) in excluded_ids:
                excluded_ids.remove(str(projectid))
            if projectid in project_ids:
                logger.info('Project %i already in iwlearn.net' % projectid )
                continue
            else:
                pinfo = harvest.extract_project_info(projectid)
                if pinfo:
                    if 'GEF Project ID' in pinfo:
                        done += 1
                        logger.info('Adding project %i' % projectid )
                        new_projects.append(self.create_project(pinfo, projectid))
                        if done % 10 == 0:
                            # Commit subtransaction for every 10th processed item
                            transaction.get().commit()
                    else:
                        logger.info('download incomplete for project %i' % projectid )
                else:
                    logger.info('download failed for project %i' % projectid )
        excluded_ids.sort()
        self.context.setExclude_ids(excluded_ids)
        included_ids.sort()
        self.context.setInclude_ids([str(i) for i in included_ids])
        transaction.get().commit()
        logger.info('harvest complete')
        return new_projects



IPDORATINGS = { 'N/A' : None,
        '': None,
        'HU' : '0',
        'U': '1',
        'MU': '2',
        'MS': '3',
        'S': '4',
        'HS': '5'}

OUTCOMERATINGS = { 'UA' : None,
        '': None,
        '6' : '0',
        '5': '1',
        '4': '2',
        '3': '3',
        '2': '4',
        '1': '5'}


class GefOnlineUpdateView(GefOnlineHarvestView):

    view_usage = 'Updated Projects'


    def harvest_projects(self):
        logger.info('starting update harvest')
        projects = self.portal_catalog(portal_type ='Project')
        new_projects =[]
        ratings = harvest.get_projects_ratings()
        done = 0
        for brain in projects:
            done += 1
            updated = False
            obj = brain.getObject()
            self._create_project_folders(obj)
            projectid = int(obj.getGef_project_id().strip())
            if projectid in ratings:
                iprating = IPDORATINGS[ratings[projectid]['iprating']]
                dorating = IPDORATINGS[ratings[projectid]['dorating']]
                if 'outcomerating' in [ratings[projectid]]:
                    outcomerating = OUTCOMERATINGS[ratings[projectid]['outcomerating']]
                else:
                    outcomerating = None
                project_status = ratings[projectid]['status']
                if project_status == 'Completed':
                    project_status = 'Project Completion'
                if project_status:
                    if obj.getProject_status() != project_status:
                        logger.info('updating status for project %i to %s' %(projectid, project_status))
                        obj.update(project_status=project_status)
                        updated = True
                if iprating != None and dorating != None:
                    if iprating != getattr(obj, 'iprating', None) or dorating != getattr(ob, 'dorating', None):
                        obj.update(iprating = iprating,
                            dorating = dorating)
                        logger.info('Updating project %i rating' % projectid )
                        updated = True
                elif iprating !=None and iprating != getattr(obj, 'iprating', None):
                    obj.update(iprating = iprating)
                    updated = True
                    logger.info('Updating project %i rating' % projectid )
                elif dorating !=None and dorating != getattr(obj, 'dorating', None):
                    obj.update(dorating = dorating)
                    updated = True
                    logger.info('Updating project %i rating' % projectid )
                if outcomerating:
                    if outcomerating != getattr(obj, 'outcomerating', None):
                        obj.update(outcomerating = outcomerating)
                        updated = True
                        logger.info('Updating project %i outcomerating' % projectid )
            pinfo = None
            #XXX comment out to skip updateing from gef online
            pinfo = harvest.extract_project_info(projectid)
            if pinfo:
                if pinfo.get('Approval Date', None):
                    try:
                        start_date = DateTime(pinfo.get('Approval Date'))
                    except:
                        start_date = None
                else:
                    start_date = None
                #XXX only needed once
                #if 'Regional' in pinfo.get('Country', ''):
                #    project_scale = 'Regional'
                #elif 'Global' in pinfo.get('Region', '') or 'Global' in pinfo.get('Country', ''):
                #     project_scale = 'Global'
                #else:
                #    project_scale = 'National'
                #obj.update(project_scale = project_scale)
                project_allocation = harvest.convert_currency_to_millions(
                            pinfo.get('GEF Grant','0'))
                total_cost = harvest.convert_currency_to_millions(
                            pinfo.get('Project Cost', '0'))
                wb_project_id = pinfo.get('IBRD PO ID', None)
                operational_program = harvest.split_semicolon(
                            pinfo.get('Operational Program', ''))
                strategic_program = harvest.split_semicolon(
                            pinfo.get('Strategic Program', ''))
                if pinfo.has_key('Project Completion Date'):
                    end_date = DateTime(pinfo.get('Project Completion Date'))
                else:
                    end_date = None
                if end_date and obj.end() is None:
                    obj.update(end_date=end_date)
                if wb_project_id:
                    obj.update(wb_project_id=wb_project_id)
                    updated = True
                if operational_program:
                    obj.update(operational_programme=operational_program)
                    updated = True
                if strategic_program:
                    obj.update(strategic_priority=strategic_program)
                    updated = True
                #project_status = pinfo.get('Project Status', None)
                #if obj.getProject_status() != project_status:
                #    obj.update(
                #        project_status=project_status,
                #        #start_date=start_date,
                #        gef_project_allocation=str(project_allocation),
                #        total_cost=str(total_cost),
                #        )
                    new_projects.append({'name': brain.Title,
                        'url': brain.getURL(),
                        'description': brain.Description})
            else:
                logger.info('download failed for project %i' % projectid )
            ibrd_id = obj.getWb_project_id()
            if ibrd_id:
                try:
                    pinfo = harvest.get_ibrd_info(ibrd_id)
                except KeyError:
                    pinfo = False
                if pinfo:
                    logger.info('Update project %i from WB Data' % projectid )
                    if 'closingdate' in pinfo:
                        end_date = DateTime(pinfo['closingdate'])
                        if end_date and obj.end() is None:
                            obj.update(end_date=end_date)
                            updated = True
                    if not obj.Description():
                        if 'project_abstract' in pinfo:
                            obj.update(Description=pinfo['project_abstract']['cdata'])
                            updated = True
                    if 'locations' in pinfo:
                        logger.info('Update project %i Locations from WB Data' % projectid )
                        if 'project_abstract' in pinfo:
                            desc = pinfo['project_abstract']['cdata']
                        else:
                            desc=None
                        if 'project_name' in pinfo:
                            project_name = pinfo['project_name']
                        else:
                            project_name = None
                        for location in pinfo['locations']:
                            if ('geoLocName' in location and
                                'longitude' in location and
                                'latitude' in location and
                                'geoLocId' in location):
                                self._create_project_location(obj, location, project_name, desc)
                                updated = True
            #get unep projects from addis
            unep_project = harvest.get_unep_iw_projects(projectid)
            if unep_project:
                if int(unep_project[0]['GEFid'])== projectid:
                    logger.info('updating from unep')
                    obj.update(unep_addis_project_id= int(unep_project[0]['DatabaseID']))
                    obj.update(unep_addis_url=unep_project[0]['url'])
                    if unep_project[0]['FocalAreas']:
                        fa = list(obj.getFocal_area())
                        fb = set(fa + unep_project[0]['FocalAreas'])
                        if set(fa) != fb:
                            logger.info('ADDIS Updating Focal Area from %s to %s' %(fa, fb))
                            obj.update(focal_area=fb)
                            updated = True
                    if unep_project[0]['GEFPhase']:
                        gp = UNEP_GEF_PHASE[unep_project[0]['GEFPhase']]
                        obj.update(gef_phase = gp)
                        updated = True
                    if unep_project[0]['Countries']:
                        countries = list(obj.getField('country').get(obj))
                        cdb = []
                        for c in unep_project[0]['Countries']:
                            if c not in PLONE_COUNTRIES:
                                logger.error('GEFID %i ADDIS Country %s not found' %(projectid, c) )
                            else:
                                cdb.append(c)
                        c2 = set(countries + cdb)
                        if len(countries) != len(c2):
                            logger.info('ADDIS Updating Country from %s to %s' %(countries, c2))
                            obj.update(country=c2)
                            updated = True
                else:
                    logger.error('GEFIds do not match %s != %i' %(unep_project['GEFId'], projectid))
            if updated:
                logger.info('Updated project %i' % projectid )
            if done % 10 == 0:
                # Commit subtransaction for every 10th processed item
                transaction.get().commit()
        transaction.get().commit()
        logger.info('update harvest complete')
        return new_projects
