# rename projects - set objectId = gef_project_id
import logging
logger = logging.getLogger('iwlearn.project')
from iwlearn.project.config import _is_renaming


def rename_contained_projects(parent):
    j = 0
    for child in parent.objectValues('Project'):
        j += rename_contained_projects(child)
        if j > 50:
            break
        child_id = child.id
        obj_id = str(int(child.getGef_project_id().strip()))
        if obj_id != child_id:
            try:
                parent.manage_renameObject(child_id, obj_id)
                logger.info('renamed Project %s' % obj_id )
                j += 1
            except:
                logger.info('Failed to rename Project from %s to %s' %(child_id, obj_id ))
        else:
            logger.info('No need to rename project %s' % obj_id )
    return j


def mv_projects(self):
    if _is_renaming:
        return 'another rename process is running'
    else:
        _is_renaming = True
    logger.info( 'search for projects')
    i=0
    parent = self.portal_url.getPortalObject()['iw-projects']
    i = rename_contained_projects(parent)
    logger.info('renaming complete')
    _is_renaming = False
    return '%i projects renamed' %i
