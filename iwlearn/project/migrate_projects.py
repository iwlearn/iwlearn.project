#migrate IWProject to iwlearn.project


#Implementing agencies:
#     FAO
#     IADB
#     IBRD
#     IFOP(Chile)
#     IMARPE(Peru)
#     International Bank for Reconstruction and Development (WB)
#     International Fund for Agriculture and Development(IFAD)
#     Ministries of Environment
#     UNDP
#     UNEP
#     UNEP, IBRD
#     UNOPS
#     United Nations Development Programme
#     United Nations Development Programme (UNDP)
#     United Nations Environment Programme (UNEP)
#     United Nations Industrial Development Organization (UNIDO)

# unique names in contact db:
#   United Nations Development Programme (UNDP)
#   United Nations Industrial Development Organization (UNIDO)
#   United Nations Environment Programme (UNEP)
#   United Nations Office for Project Services (UNOPS)
#   International Bank for Reconstruction and Development (IBRD) <<< to be added
#   International Fund for Agriculture and Development(IFAD) <<< to be added
#   Instituto del Mar del Peru (IMARPE) <<< to be added
#   Instituto de Fomento Pesquero (IFOP) <<< to be added
#   Inter-American Development Bank (IADB) <<< to be added
#   Food and Agricultural Organization (FAO)



def get_implementing_agency_uid(agency):
    ia = self.portal_catalog(portal_type='ContactOrganization', Title=agency):
    assert(len(ia)==1)
    return ia[0].getObject().UID()

def get_agency_uid_map():
    agencies = {
        'UNDP' : {'name': 'United Nations Development Programme (UNDP)'},
        'UNIDO' : {'name': 'United Nations Industrial Development Organization (UNIDO)'},
        'UNEP': {'name': 'United Nations Environment Programme (UNEP)'},
        'UNOPS': {'name': 'United Nations Office for Project Services (UNOPS)'},
        'IBRD': {'name': 'International Bank for Reconstruction and Development (IBRD)'},
        'IFAD': {'name': 'International Fund for Agriculture and Development (IFAD)'},
        'IMARPE': {'name': 'Instituto del Mar del Peru (IMARPE)'},
        'IFOP': {'name': 'Instituto de Fomento Pesquero (IFOP)'},
        'IADB': {'name': 'Inter-American Development Bank (IADB)'},
        'FAO': {'name': 'Food and Agricultural Organization (FAO)'},
    }
    for agency in agencies.keys():
        uid = get_implementing_agency_uid(agency)
        agencies[agency]['uid'] = uid
    print agencies



def migrate(self):
    def migrate_project(old, old_parent, new_parent, f):
        new = None
        if callable(old.id):
            obj_id = old.id()
        else:
            obj_id = old.id
        portal_types = old_parent.portal_types
        #portal_types.constructContent('Project', new_parent, obj_id)
        #new = new_parent[obj_id]
        # set fields

        #copy or migrate child objects
        for child in old.objectValues():
            if child.portal_type == 'IWSubProject':
                migrate_project(child, old, new, f)
            elif child.portal_type == 'Folder':
                pass
                #new.manage_pasteObjects(old.manage_cutObjects(child.id))
            else:
                print 'ignored: ', child.portal_type, child.id
    ###########################################################
    print 'starting migration'
    for brain in self.portal_catalog(portal_type = 'IWProjectDatabase'):
        obj=brain.getObject()
        parent = obj.getParentNode()
        new = None
        if callable(obj.id):
            obj_id = obj.id()
        else:
            obj_id = obj.id
        #parent.manage_renameObject(obj_id, obj_id + '_old')
        portal_types = parent.portal_types
        #portal_types.constructContent('ProjectDatabase', parent, obj_id)
        print 'created project db: ', obj_id
        #new = parent[obj_id]
        #new.update(title=obj.title, description=obj.description )
        #migrate_metadata(obj, new, parent, parent)
        for child in obj.objectValues():
            if child.portal_type == 'IWProject':
                migrate_project(child, obj, new, f)
            else:
                print 'ignored: ', child.portal_type, child.id
        #parent.manage_delObjects(ids=[obj_id + '_old'])
    print 'migration finished'
