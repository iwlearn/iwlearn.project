# -*- coding: utf-8 -*-
# migrate IWProject to iwlearn.project
# migrate_projects

from iwlearn.project import vocabulary
from plone.i18n.locales.countries import _countrylist

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
#>     United Nations Development Programme (UNDP)
#>     United Nations Environment Programme (UNEP)
#>    United Nations Industrial Development Organization (UNIDO)

# unique names in contact db:
#   United Nations Development Programme (UNDP)
#   United Nations Industrial Development Organization (UNIDO)
#   United Nations Environment Programme (UNEP)
#   United Nations Office for Project Services (UNOPS)
#   International Bank for Reconstruction and Development (IBRD) <<< to be added
#   International Fund for Agriculture and Development (IFAD) <<< to be added
#   Instituto del Mar del Peru (IMARPE) <<< rename Peru; Institute of the Sea (IMARPE)
#   Instituto de Fomento Pesquero (IFOP) <<< rename Institute of Fishing Promotion (IFOP)
#   Inter-American Development Bank (IADB) <<< to be added
#   Food and Agricultural Organization (FAO)



def get_implementing_agency_uid(agency, context):
    sa = '"' + agency +'"'
    ia = context.portal_catalog(
            portal_type='ContactOrganization',
            Title=sa)
    assert(len(ia)==1)
    return ia[0].getObject().UID()

def get_agency_uid_map(context):
    agencies = {
        'UNDP' : {'name': 'United Nations Development Programme (UNDP)',
            'alias':['UNDP', 'United Nations Development Programme', ]},
        'UNIDO' : {'name': 'United Nations Industrial Development Organization (UNIDO)',
            'alias':[]},
        'UNEP': {'name': 'United Nations Environment Programme (UNEP)',
            'alias':['UNEP', 'UNEP, IBRD']},
        'UNOPS': {'name': 'United Nations Office for Project Services (UNOPS)',
            'alias': ['UNOPS']},
        'IBRD': {'name': 'International Bank for Reconstruction and Development (IBRD)',
            'alias': ['UNEP, IBRD', 'IBRD',
            'International Bank for Reconstruction and Development (WB)']},
        'IFAD': {'name': 'International Fund for Agriculture and Development (IFAD)',
            'alias': ['International Fund for Agriculture and Development(IFAD)'] },
        'IMARPE': {'name': 'Instituto del Mar del Peru (IMARPE)',
            'alias': ['IMARPE(Peru)']},
        'IFOP': {'name': 'Instituto de Fomento Pesquero (IFOP)',
            'alias': ['IFOP(Chile)']},
        'IADB': {'name': 'Inter-American Development Bank (IADB)',
            'alias': ['IADB']},
        'FAO': {'name': 'Food and Agricultural Organization (FAO)',
            'alias': ['FAO']},
    }
    for agency in agencies.keys():
        uid = get_implementing_agency_uid(agencies[agency]['name'], context)
        agencies[agency]['uid'] = uid
    #print agencies
    return agencies

# Regions and subregions

SUB_REGIONS_MAP = {
# africa
    'Eastern Africa': ['Eastern Africa'],
    'Central Africa': ['Central Africa'],
    'Northern Africa': ['Northern Africa'],
    'Southern Africa': ['Southern Africa'],
    'Western Africa': ['Western Africa', 'Indian Ocean'],
#americas
    'Caribbean': ['Caribbean'],
    'Central America': ['Central America'],
    'Northern America': ['North America'],
    'Southern America': ['South America'],
#europe
    'Eastern Europe': ['Eastern Europe','South East Europe'],
    'Northern Europe': ['Northern Europe'],
    'Southern Europe': ['Southern Europe','South East Europe','South West Europe'],
    'Western Europe': ['Western Europe','South West Europe'],
#asia
    'Eastern Asia': ['East Asia'],
    'South-Central Asia': ['Central Asia', 'South Asia'],
    'South-Eastern Asia': ['South East Asia'],
    'Western Asia': ['South West Asia'],
#oceania
    'Australia & New Zealand': ['Australasia'],
    'Melanesia': ['Melanesia'],
    'Micronesia': ['Micronesia'],
    'Polynesia': ['Polynesia'],
    }

def getRegions(region, subregions,countries):
    ''' Try to guess the regions from countries,
    regions and subregions '''
    # dict to make regions unique
    rd = {}
    if region:
        rd[region] = region
    srl = []
    for subregion in subregions:
        srl = srl + SUB_REGIONS_MAP[subregion]
        rl = vocabulary.get_regions(subregions=srl)
        for r in rl:
            rd[r]=''
    if countries:
        rl = vocabulary.get_regions(countries=countries)
        for r in rl:
            rd[r]=''
    regions = rd.keys()
    regions.sort()
    print regions
    return regions

COUNTRY_MAP = {
 u"africa": None,
 u"america": None,
 u"antigua barbuda": u"Antigua and Barbuda",
 u"barbados, w.i": u"Barbados",
 u"bosnia & herzegovina": u"Bosnia and Herzegovina",
 u"bosnia herzegovina": u"Bosnia and Herzegovina",
 u"brasil": u"Brazil",
 u"central african repulic": u"Central African Republic",
 u"central america": None,
 u"china,": u"China",
 u"congo, democratic republic": u"Congo The Democratic Republic of",
 u"congo, democratic republic of the": u"Congo The Democratic Republic of",
 u"country": None,
 u"fiji islands": u"Fiji",
 u"fyr macedonia": u"Macedonia the former Yugoslavian Republic of",
 u"fyr of macedonia": u"Macedonia the former Yugoslavian Republic of",
 u"geneva": u"Switzerland",
 u"guinea bissau": u"Guinea-Bissau",
 u"i.r. iran": u"Iran Islamic Republic of",
 u"iran": u"Iran Islamic Republic of",
 u"iran,": u"Iran Islamic Republic of",
 u"iran, islamic republic": u"Iran Islamic Republic of",
 u"iran, islamic republic of": u"Iran Islamic Republic of",
 u"kingdom of saudi arabia": u"Saudi Arabia",
 u"korea": u"Korea Republic of",
 u"korea, democratic people's republic": u"Korea Democratic People's Republic of",
 u"korea, democratic people's republic of": u"Korea Democratic People's Republic of",
 u"korea, republic": u"Korea Republic of",
 u"korea, republic of": u"Korea Republic of",
 u"lao pdr": u"Lao People's Democratic Republic",
 u"libya": u"Libyan Arab Jamahiriya",
 u"luxemburg": u"Luxembourg",
 u"macedonia, former yugoslav republic": u"Macedonia the former Yugoslavian Republic of",
 u"macedonia, former yugoslav republic of": u"Macedonia the former Yugoslavian Republic of",
 u"micronesia": u"Micronesia Federated States of",
 u"micronesia, federated states": u"Micronesia Federated States of",
 u"moldova": u"Moldova Republic of",
 u"moldova, republic": u"Moldova Republic of",
 u"moldova, republic of": u"Moldova Republic of",
 u"méxico": u"Mexico",
 u"northern africa": None,
 u"null": None,
 u"palestinian territory, occupied": u"Palestinian Territory occupied",
 u"pr china": u"China",
 u"republic of chad": u"Chad",
 u"republic of kazakhstan": u"Kazakhstan",
 u"republic of korea": u"Korea Republic of",
 u"russia": u"Russian Federation",
 u"saint kitts nevis": u"Saint Kitts and Nevis",
 u"saint vincent grenadines": u"Saint Vincent and the Grenadines",
 u"sao tome principe": u"Sao Tome and Principe",
 u"serbia": u"Serbia and Montenegro",
 u"serbia and montegnegro": u"Serbia and Montenegro",
 u"serbia montenegro": u"Serbia and Montenegro",
 u"slovak republic": u"Slovakia",
 u"tanzania": u"Tanzania United Republic of",
 u"tanzania, united republic": u"Tanzania United Republic of",
 u"tanzania, united republic of": u"Tanzania United Republic of",
 u"the netherlands": u"Netherlands",
 u"trinidad tobago": u"Trinidad and Tobago",
 u"tunisie": u"Tunisia",
 u"usa": u"United States",
 u"vietnam": u"Viet Nam",
 u"western africa": None,
 u"western asia": None,
 u"western europe": None,
}
for k, v in _countrylist.iteritems():
    COUNTRY_MAP[v['name'].lower()] = v['name']

def update_countries(countries):
    cl = []
    if countries:
        for country in countries:
            c = COUNTRY_MAP[country.lower()]
            if c:
                cl.append(c)
    return cl

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
        # Implementing agencies
        ias = old.getOther_implementing_agency()
        hit = False
        auids =[]
        for ia in ias:
            for agency in agency_map.keys():
                if ((ia in agency_map[agency]['alias']) or
                        (ia == agency_map[agency]['name'])):
                    hit = True
                    auids.append(agency_map[agency]['uid'])
        if hit:
            pass
        else:
            pass
        region = old.getRegion()
        subregions = old.getSubregion()
        countries = update_countries(old.getCountry())
        getRegions(region, subregions,countries)

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
    f = None
    agency_map = get_agency_uid_map(self)
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
    return 'success'
