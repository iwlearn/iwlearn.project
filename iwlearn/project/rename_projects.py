# rename projects - set objectId = gef_project_id
import logging
logger = logging.getLogger('iwlearn.project')
import transaction


def rename_contained_projects(parent):
    j = 0
    for child in parent.objectValues('Project'):
        j += rename_contained_projects(child)
        child_id = child.id
        obj_id = str(int(child.getGef_project_id().strip()))
        if obj_id != child_id:
            try:
                logger.info('Try to rename Project from %s to %s' %(child_id, obj_id ))
                parent.manage_renameObject(child_id, obj_id)
                transaction.commit()
                logger.info('renamed Project to %s' % obj_id )
                j += 1
            except:
                logger.info('Failed to rename Project %s' % child_id)
        else:
            logger.info('No need to rename project %s' % obj_id )
    return j


def mv_projects(self):
    logger.info( 'search for projects')
    i=0
    parent = self.portal_url.getPortalObject()['iw-projects']
    i = rename_contained_projects(parent)
    logger.info('renaming complete')

    return '%i projects renamed' %i

