# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
    VERSIONING = True
except ImportError:
    VERSIONING = False
# The profile id of your package:
PROFILE_ID = 'profile-iwlearn.project:default'

# put your custom types in this list
TYPES_TO_VERSION = ('Project',)


def reindex_projects(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type = 'Project')
    for brain in brains:
            obj = brain.getObject()
            logger.info( 'reindex: ' + '/'.join(obj.getPhysicalPath()))
            obj.reindexObject()

def update_project_types(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type = 'Project')
    logger.info( 'Update project types')
    for brain in brains:
        obj = brain.getObject()
        if obj.getProject_type() == 'Enabling Activity':
            obj.setProject_type('EA')
        elif obj.getProject_type() == 'Medium Sized Project':
            obj.setProject_type('MSP')
        elif obj.getProject_type() == 'Full Size Project':
            obj.setProject_type('FSP')
        else:
            continue
        logger.info( 'reindex: ' + '/'.join(obj.getPhysicalPath()))
        obj.reindexObject()
    logger.info( 'Project types updated')


def setVersionedTypes(context, logger=None):
    if VERSIONING:
        if logger is None:
            # Called as upgrade step: define our own logger.
            logger = logging.getLogger('iwlearn.project')
        portal_repository = getToolByName(context, 'portal_repository')
        versionable_types = list(portal_repository.getVersionableContentTypes())
        for type_id in TYPES_TO_VERSION:
            if type_id not in versionable_types:
                # use append() to make sure we don't overwrite any
                # content-types which may already be under version control
                logger.info('Adding %s to versionable types' % type_id)
                versionable_types.append(type_id)
                # Add default versioning policies to the versioned type
                for policy_id in DEFAULT_POLICIES:
                    portal_repository.addPolicyForContentType(type_id, policy_id)
        portal_repository.setVersionableContentTypes(versionable_types)


def add_harvest_menue(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')

def reindex_regions(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    logger.info("Reindexing getSubRegions")
    catalog = getToolByName(context, 'portal_catalog')
    catalog.manage_reindexIndex(ids=['getSubRegions',])


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('getSubRegions', 'KeywordIndex'),
              ('getAgencies', 'KeywordIndex'),
              ('getBasin', 'KeywordIndex'),
              ('getCountry', 'KeywordIndex'),
              ('getProject_status', 'FieldIndex'),
              ('getProject_type', 'FieldIndex'),
              ('getRawProjects', 'FieldIndex'),
              ('getBasin_type', 'FieldIndex'),
              ('getProject_category', 'KeywordIndex'),
              ('getEcosystem', 'KeywordIndex'),
              ('getCountryCode', 'KeywordIndex'),
              #XXX maybe better to index them seperately
              #('getGefRatings', 'FieldIndex'),
              )
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

def add_topic_criteria(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'atcttool')

def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('iwlearn.project_various.txt') is None:
        return
    logger = context.getLogger('iwlearn.project')
    site = context.getSite()
    add_catalog_indexes(site, logger)
    setVersionedTypes(site, logger)
    # Add additional setup code here

