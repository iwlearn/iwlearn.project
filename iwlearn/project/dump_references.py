# -*- coding: utf-8 -*-
# save references and backreferences as a python script to restore them
# after the content migration link restore_references.py into
# parts/clientX/Extensions and execute the script as an external method
# dump_references.py


def get_implementing_agency_uid(agency, context, tags):
    sa = '"' + agency +'"'
    ia = context.portal_catalog(
            portal_type='mxmContactsOrganization',
            Title=sa)
    assert(len(ia)==1), agency
    ia[0].getObject().setSubject(tags)
    ia[0].getObject().reindexObject(idxs=['Subject'])
    return ia[0].getObject().UID()

#   International Fund for Agriculture and Development (IFAD) <<< to be added
#   Instituto del Mar del Peru (IMARPE) <<< rename Peru; Institute of the Sea (IMARPE)
#   Instituto de Fomento Pesquero (IFOP) <<< rename Institute of Fishing Promotion (IFOP)
#   Inter-American Development Bank (IADB) <<< to be added

def get_agency_uid_map(context):
    agencies = {
        'UNDP' : {'name': 'United Nations Development Programme (UNDP)',
            'alias':['UNDP', 'United Nations Development Programme', ],
            'tags':['Lead Implementing Agency', 'Implementing Agency']},
        'UNIDO' : {'name': 'United Nations Industrial Development Organization (UNIDO)',
            'alias':[],
            'tags':['Implementing Agency']},
        'UNEP': {'name': 'United Nations Environment Programme (UNEP)',
            'alias':['UNEP', 'UNEP, IBRD', 'United Nations Environment Programme'],
            'tags':['Lead Implementing Agency', 'Implementing Agency']},
        'UNOPS': {'name': 'United Nations Office for Project Services (UNOPS)',
            'alias': ['UNOPS'],
            'tags':['Implementing Agency']},
        'IBRD': {'name': 'International Bank for Reconstruction and Development (WB)',
            'alias': ['UNEP, IBRD', 'IBRD', 'World Bank'],
            'tags':['Lead Implementing Agency', 'Implementing Agency']},
        'IFAD': {'name': 'International Fund for Agriculture and Development (IFAD)',
            'alias': ['International Fund for Agriculture and Development(IFAD)'] ,
            'tags':['Implementing Agency']},
        'IMARPE': {'name': 'Peru; Institute of the Sea (IMARPE)',
            'alias': ['IMARPE(Peru)','Instituto del Mar del Peru (IMARPE)'],
            'tags':['Implementing Agency']},
        'IFOP': {'name': 'Institute of Fishing Promotion (IFOP)',
            'alias': ['IFOP(Chile)', 'Instituto de Fomento Pesquero (IFOP)'],
            'tags':['Implementing Agency']},
        'IADB': {'name': 'Inter-American Development Bank (IADB)',
            'alias': ['IADB','Inter-American Development Bank'],
            'tags':['Lead Implementing Agency', 'Implementing Agency']},
        'FAO': {'name': 'Food and Agricultural Organization (FAO)',
            'alias': ['FAO', 'Food and Agriculture Organization'],
            'tags':['Lead Implementing Agency', 'Implementing Agency']},
        'AfDB': {'name': 'African Development Bank (AfDB)',
            'alias': ['African Development Bank',],
            'tags':['Lead Implementing Agency', 'Implementing Agency']}
    }
    for agency in agencies.keys():
        uid = get_implementing_agency_uid(agencies[agency]['name'],
            context, agencies[agency]['tags'])
        agencies[agency]['uid'] = uid
    #print agencies
    return agencies


def migrate_project(old, f, agency_map, context):
    uid_tool = context.reference_catalog
    # lead implementing agency
    la = old.getLeadagency()
    hit = False
    lauid = None
    for agency in agency_map.keys():
        if ((la in agency_map[agency]['alias']) or
                (la==agency_map[agency]['name'])):
            # set lead agency reference
            hit = True
            lauid = agency_map[agency]['uid']
            pass
    if hit:
        #new.setLeadagency(lauid)
        f.write('    #project leadagency \n')
        f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
        f.write('    obj.setLeadagency("' + lauid + '")\n')
        #set backreferences from organization
        f.write('    #organization set leadagency backrefs\n')
        f.write('    obj=uid_tool.lookupObject("' + lauid + '")\n')
        f.write('    project_uids = list(obj.getRawProjectlead())\n')
        f.write('    project_uids.append("' + old.UID() + '")\n')
        f.write('    obj.setProjectlead(project_uids)\n')
    else:
        print 'leadagency not found: ', la
    # Implementing agencies
    ias = old.getOther_implementing_agency()
    hit = False
    auids =[]
    for ia in ias:
        for agency in agency_map.keys():
            if ((ia in agency_map[agency]['alias']) or
                    (ia==agency_map[agency]['name'])):
                hit = True
                auids.append(agency_map[agency]['uid'])
    if hit:
        #set other implementing agencies
        f.write('    #project implementing agencies \n')
        f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
        f.write('    obj.setOther_implementing_agency([')
        for auid in auids:
            f.write('"' + auid + '", ')
        f.write('])\n')
        #set the backreferences from organization
        f.write('    #backrefs for  implementing agencies from org to project\n')
        for auid in auids:
            f.write('    oia_obj=uid_tool.lookupObject("' + auid +'")\n')
            f.write('    project_uids = list(oia_obj.getRawProjectimplementing())\n')
            f.write('    project_uids.append("' + old.UID() +'")\n')
            f.write('    oia_obj.setProjectimplementing(project_uids)\n')
    else:
        print 'could not find other implementing agency: ', ias


def migrate_person(old, f):
    f.write('    #person \n')
    f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
    if old.getRawOrganization():
        f.write('    try:\n')
        f.write('        obj.setOrganization("' + old.getRawOrganization() + '")\n')
        f.write('    except:\n')
        f.write('        print "set organization failed"\n')
    if old.getBRefs('Rel1'):
        f.write('    obj.setProjects([')
        for project in old.getBRefs('Rel1'):
            f.write(' "' + project.UID() + '",')
        f.write('])\n')

def migrate_organization(old, f):
    if old.getBRefs():
        f.write('    #organization \n')
        f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
        f.write('    if obj:\n')
        f.write('        obj.setContactpersons([')
        for person in old.getBRefs():
            f.write(' "' + person.UID() + '",')
        f.write('])\n')


def migrate(self):
    print 'saving references'
    agency_map = get_agency_uid_map(self)
    f = open('restore_references.py', 'w')
    f.write('def migrate(self):\n')
    f.write('    print "start setting uids"\n')
    f.write('    uid_tool = self.reference_catalog\n')
    for brain in self.portal_catalog(portal_type = [
            'mxmContactsOrganization', 'mxmContactsPerson', 'IWProject',
            'IWSubProject']):
        obj=brain.getObject()
        if brain.portal_type == 'mxmContactsOrganization':
            migrate_organization(obj, f)
        elif brain.portal_type == 'mxmContactsPerson':
            migrate_person(obj, f)
        elif brain.portal_type in ['IWSubProject', 'IWProject']:
            migrate_project(obj, f, agency_map, self)
    f.write('    print "finished setting uids"\n')
    f.write('    return "uids restored"\n')
    f.close()
    print 'references saved'
    return 'success'
