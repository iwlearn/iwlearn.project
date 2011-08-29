# rename projects - set objectId = gef_project_id
import logging
logger = logging.getLogger('iwlearn.project')

def rename_projects(self):
    logger.info( 'search for projects')
    i = 0
    for brain in self.portal_catalog(portal_type = 'Project'):
        obj=brain.getObject()
        parent = obj.getParentNode()
        child_id = brain.getId
        obj_id = str(int(obj.getGef_project_id().strip()))
        if obj_id != child_id:
            try:
                parent.manage_renameObject(child_id, obj_id)
                logger.info('renamed Project %s' % obj_id )
                i += 1
            except:
                logger.info('Failed to rename Project from %s to %s' %(child_id, obj_id ))
    logger.info('renaming complete')
    return '%i projects renamed' %i
