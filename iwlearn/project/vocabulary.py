# -*- coding: utf-8 -*-


# http://en.wikipedia.org/wiki/List_of_countries_spanning_more_than_one_continent
# Africa and Asia
# Two of 29 governorates of Egypt lie entirely on the Asian Sinai
# Peninsula and two are transcontinental

# Asia and Europe
#    * Azerbaijan - situated in Eastern Europe and Western Asia.
#    * Georgia - situated in Eastern Europe and Western Asia.
#    * Kazakhstan - situated in Central Asia and Eastern Europe.
#    * Russia - situated in Northern Asia and Eastern Europe.
#    * Turkey - situated in Western Asia and Eastern Europe.
import logging
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from copy import copy

from plone.i18n.locales.countries import _countrylist
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('iwlearn.project')

my_countrylist = copy(_countrylist)
my_countrylist['cs'] = {u'flag': u'/++resource++country-flags/cs.gif',
        u'name': u'Serbia and Montenegro'}

my_countrylist['me'] = {u'name': u'Montenegro'}
my_countrylist['rs'] = {u'name': u'Serbia'}
my_countrylist['bl'] = {u'name': u'Saint Barthélemy'}
my_countrylist['bq'] = {u'name': u'Bonaire, Sint Eustatius and Saba'}
my_countrylist['cw'] = {u'name': u'Curaçao'}
my_countrylist['mf'] = {u'name': u'Saint Martin (French part)'}
my_countrylist['sx'] = {u'name': u'Sint Maarten (Dutch part)'}

REGION_SUBREGION_COUNTRIES_XXX ={
u'Europe': {
    u'Northern Europe':
        [u'dk', u'fo', u'fi', u'is', u'no', u'sj', u'se', u'ax'],
    u'Eastern Europe':
        [u'by', u'ee', u'lv', u'lt', u'md', u'pl', u'ua', u'az', u'kz',
        u'ru'],
    u'South East Europe':
        [u'al', u'ba', u'bg', u'hr', u'gr', u'mk', u'ro',
        u'cs', u'si', u'ge', u'tr'],
    u'Southern Europe':
        [u'va', u'it', u'mt', u'sm'],
    u'Central Europe':
        [u'at', u'cz', u'hu', u'li', u'sk', u'ch'],
    u'Western Europe':
        [u'be', u'fr', u'de', u'ie', u'lu', u'im', u'mc', u'nl',
        u'gb', u'gg', u'je'],
    u'South West Europe':
        [u'ad', u'gi', u'pt', u'es']
    },
u'Atlantic Ocean': {
    u'South Atlantic Ocean':
        ['bv', u'sh', u'gs']
    },
u'Oceania': {
# http://en.wikipedia.org/wiki/Oceania#Geopolitical_Oceania
    u'Australasia': [u'au', u'nz', u'cx', u'cc', u'nf'],
    u'Melanesia': [u'fj', u'id', u'nc', u'pg', u'sb', u'vu'],
    u'Micronesia': [u'fm', u'gu', u'ki', u'mh', u'nr', u'mp', u'pw', u'um'],
    u'Polynesia': [u'as', u'ck', u'cl', u'pf', u'us', u'nu', u'pn', u'ws',
       u'tk', u'to', u'tv', u'wf'],
#    u'North Pacific Ocean':
#        [u'um'],
#    u'South Pacific Ocean': [],
#    u'Pacific':
#        [u'as', u'au', u'ck', u'fj', u'pf', u'gu', u'ki', u'mh', u'fm',
#        u'nr', u'nc', u'nz', u'nu', u'nf', u'mp', u'pw', u'pg', u'pn', u'sb',
#        u'tk', u'to', u'tv', u'vu', u'wf', u'ws']
    },
u'Africa': {
    u'Eastern Africa':
        [u'dj', u'er', u'et', u'ke', u'so', u'tz', u'ug'],
    u'Northern Africa':
        [u'dz', u'eg', u'ly', u'ma', u'sd', u'tn', u'eh'],
    u'Indian Ocean':
        [u'km', u'mg', u'mu', u'yt', u're', u'sc'],
    u'Southern Africa':
        [u'ao', u'bw', u'ls', u'mw', u'mz', u'na', u'za', u'sz',
        u'zm', u'zw'],
    u'Western Africa':
        [u'bj', u'bf', u'cm', u'cv', u'ci', u'gq', u'ga', u'gm',
        u'gh', u'gn', u'gw', u'lr', u'ml', u'mr', u'ne', u'ng', u'st', u'sn',
        u'sl', u'tg'],
    u'Central Africa':
        [u'bi', u'cf', u'td', u'cg', u'rw', u'cd']
    },
u'Asia': {
    u'Northern Asia':
        [u'mn', u'ru'],
    u'East Asia':
        ['cn', u'jp', u'kp', u'kr', u'tw', u'hk', u'mo'],
    u'South West Asia':
        [u'am', u'az', u'bh', u'cy', u'ge', u'ir', u'iq', u'il',
        u'jo', u'kw', u'lb', u'om', u'ps', u'qa', u'sa', u'sy', u'tr', u'ae',
        u'ye', u'eg'],
    u'South East Asia':
        [u'bn', u'kh', u'cx', u'cc', u'id', u'la', u'my', u'mm',
        u'ph', u'sg', u'th', u'vn', u'tl'],
    u'Central Asia':
        [u'kz', u'kg', u'tj', u'tm', u'uz'],
    u'South Asia':
        ['af', u'bd', u'bt', u'in', u'mv', u'np', u'pk', u'lk',
        u'io']
    },
u'Americas': {
    u'Central America':
        [u'bz', u'cr', u'sv', u'gt', u'hn', u'mx', u'ni', u'pa'],
    u'North America':
        [u'ca', u'gl', u'pm', u'us'],
    u'South America':
        [u'ar', u'bo', u'br', u'cl', u'co', u'ec', u'fk', u'gf',
        u'gy', u'py', u'pe', u'sr', u'uy', u've'],
    u'Caribbean':
        [u'ai', u'ag', u'aw', u'bs', u'bb', u'bm', u'vg', u'ky', u'cu',
        u'dm', u'do', u'gd', u'gp', u'ht', u'jm', u'mq', u'ms', u'an', u'pr',
        u'kn', u'lc', u'vc', u'tt', u'tc', u'vi'],
    #'North Pacific Ocean': []
    },
u'Antarctica': {
    u'Antarctica': [u'aq']
    },
u'Indian Ocean': {
    u'Southern Indian Ocean': [u'tf', u'hm']
    },
u'Global' : {
     #u'Global' : [] #_countrylist.keys()
     }
}

REGION_SUBREGION_COUNTRIES = {
u'Europe':
    {'Eastern Europe': ['bg', 'by', 'cz', 'hu', 'md', 'pl', 'ro', 'ru', 'sk', 'ua'],
    'Western Europe': ['at', 'be', 'ch', 'de', 'fr', 'li', 'lu', 'mc', 'nl'],
#    'SIDS (Europe)': [],
    'Southern Europe': ['ad', 'al', 'ba', 'cs', 'es', 'gi', 'gr', 'hr', 'it',
    'me', 'mk', 'mt', 'pt', 'rs', 'si', 'sm', 'va'],
    'Northern Europe': ['ax', 'dk', 'ee', 'fi', 'fo', 'gb', 'gg', 'ie',
    'im', 'is', 'je', 'lt', 'lv', 'no', 'se', 'sj']},
u'Antarctica': {u'Antarctica': [u'aq']},
u'Oceania': {'Melanesia': ['fj', 'nc', 'pg', 'sb', 'vu'],
    'SIDS (Oceania)': ['as', 'ck', 'fj', 'fm', 'gu', 'ki', 'mh', 'mp', 'nc',
            'nr', 'nu', 'pf', 'pg', 'pw', 'sb', 'to', 'tv', 'vu', 'ws'],
    'Australia and New Zealand': ['au', 'nf', 'nz'],
    'Micronesia': ['fm', 'gu', 'ki', 'mh', 'mp', 'nr', 'pw'],
    'Polynesia': ['as', 'ck', 'nu', 'pf', 'pn', 'tk', 'to', 'tv', 'wf', 'ws']},
u'Global': {},
u'SIDS': {
    'Small island developing States': ['ag', 'ai', 'an' 'as', 'aw', 'bb',
        'bs', 'bz', 'ck', 'cu', 'cv', 'dm', 'do', 'fj', 'fm', 'gd',
        'gu', 'gw', 'gy', 'ht', 'jm', 'ki', 'km', 'kn', 'lc', 'mh',
        'mp', 'ms', 'mu', 'mv', 'nc', 'nr', 'nu', 'pf', 'pg', 'pr',
        'pw', 'sb', 'sc', 'sg', 'sr', 'st', 'tl', 'to', 'tt', 'tv',
        'vc', 'vg', 'vi', 'vu', 'ws']},
u'Africa': {
    'Eastern Africa': ['bi', 'dj', 'er', 'et', 'ke', 'km', 'mg', 'mu',
        'mw', 'mz', 're', 'rw', 'sc', 'so', 'tz', 'ug', 'yt', 'zm', 'zw'],
    'Northern Africa': ['dz', 'eg', 'eh', 'ly', 'ma', 'sd', 'tn'],
    'Middle Africa': ['ao', 'cd', 'cf', 'cg', 'cm', 'ga', 'gq', 'st', 'td'],
    'Southern Africa': ['bw', 'ls', 'na', 'sz', 'za'],
    'Western Africa': ['bf', 'bj', 'ci', 'cv', 'gh', 'gm', 'gn', 'gw',
    'lr', 'ml', 'mr', 'ne', 'ng', 'sh', 'sl', 'sn', 'tg'],
    'SIDS (Africa)': ['cv', 'gw', 'km', 'mu', 'sc', 'st']},
u'Asia': {
    'Western Asia': ['ae', 'am', 'az', 'bh', 'cy', 'ge', 'il', 'iq',
        'jo', 'kw', 'lb', 'om', 'ps', 'qa', 'sa', 'sy', 'tr', 'ye'],
    'Southern Asia': ['af', 'bd', 'bt', 'in', 'ir', 'lk', 'mv', 'np', 'pk'],
    'South-Eastern Asia': ['bn', 'id', 'kh', 'la', 'mm', 'my', 'ph', 'sg',
        'th', 'tl', 'vn'],
    'SIDS (Asia)': ['mv', 'sg', 'tl'],
    'Central Asia': ['cn', 'hk', 'jp', 'kg', 'kp', 'kr', 'kz', 'mn',
        'mo', 'tj', 'tm', 'uz']},
u'Americas': {
    'Central America': ['bz', 'cr', 'gt', 'hn', 'mx', 'ni', 'pa', 'sv'],
    'South America': ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'fk', 'gf', 'gy',
        'pe', 'py', 'sr', 'uy', 've'],
    'Caribbean': ['ag', 'ai', 'an', 'aw', 'bb', 'bl', 'bq', 'bs', 'cu', 'cw',
        'dm', 'do', 'gd', 'gp', 'ht', 'jm', 'kn', 'ky', 'lc', 'mf', 'mq',
        'ms', 'pr', 'sx', 'tc', 'tt', 'vc', 'vg', 'vi'],
    'Northern America': ['bm', 'ca', 'gl', 'pm', 'us'],
    'SIDS (Americas)': ['ag', 'ai', 'an', 'aw', 'bb', 'bs', 'bz', 'cu', 'dm',
    'do', 'gd', 'gy', 'ht', 'jm', 'kn', 'lc', 'ms', 'pr', 'sr', 'tt', 'vc', 'vg', 'vi']}
}



COUNTRYS_SUB_REGION = {}
for _r in REGION_SUBREGION_COUNTRIES:
    for _sr in REGION_SUBREGION_COUNTRIES[_r]:
        for _c in REGION_SUBREGION_COUNTRIES[_r][_sr]:
            try:
                _country = my_countrylist[_c][u'name']
                _regions = COUNTRYS_SUB_REGION.get(_country,
                    {u'region':[], u'subregion':[]})
                _regions[u'region'].append(_r)
                _regions[u'subregion'].append(_sr)
                COUNTRYS_SUB_REGION[_country]=_regions
            except KeyError:
                logger.info("Key Error %s" %_c)


FOCAL_AREAS = [
    'Biodiversity',
    'Climate Change',
    'International Waters',
    'Land Degradation',
    'Persistent Organic Pollutants',
    'Ozone Depletion',
    'Multiple Focal Areas',
    ]

OPERATIONAL_PROGRAMMES = [
    'OP1 - Arid and Semi-Arid Ecosystems',
    'OP2 - Costal Marine and Freshwater Ecosystems',
    'OP3 - Forest Ecosystems',
    'OP4 - Mountain Ecosystems',
    'EA - Biodiversity Enabling Activities',
    'STRM - Biodiversity Short Term Measures',
    'OP5 - Removal of Barriers to Energy Efficiency and Energy Conservation',
    'OP6 - Promoting the Adoption of Renewable Energy by Removing Barriers and Reducing Implementation Costs',
    'OP7 - Reducing long term costs of low greenhouse gas-emitting energy technologies',
    'OP11 - Promoting Environmentally Sustainable Transport',
    'EA - Climate Change Enabling Activities',
    'STRM - Climate Change Short Term Measures',
    'OP8 - Water based Program',
    'OP9 - Integrated Ecosystem and Resource Management',
    'OP10 - Contaminant-Based Program',
    'STRM - Projects and Country Programs to identify/prepare eligible projects.',
    'OP12 - Integrated Ecosystem Management',
    'EA - Multiple Focal Areas Enabling Activities',
    'STRM - Multiple Focal Areas Short Term Measures',
    'STRM - International Waters Short Term Measures',
    'EA - International Waters Enabling Activities',
    'EA - Land Degradation Enabling Activities',
    'EA - Ozone Depletion Enabling Activities',
    'EA - Persistent Organic Pollutants Enabling Activities',
    'STRM - Persistent Organic Pollutants Enabling Activities',
    'STRM - Ozone Depletion Short Term Measures',
    'OP13 - Conservation and Sustainable Use of Biological Diversity Important to Agriculture',
    'OP14 - Draft Operational Program on Persistent Organic Pollutants',
    'OP15 - Operational Program on Sustainable Land Management',
    ]


STRATEGIC_PRIORITIES = [
    'BD1 - Catalyzing Sustainability of Protected Areas',
    'BD2 - Mainstreaming Biodiversity in Production Landscapes and Sectors',
    'BD3 - Capacity Building for the Implementation of the Cartagena Protocol on Biosafety',
    'BD4 - Generation and Dissemination of Best Practices for Addressing Current and Emerging Biodiversity Issues',
    'CC1 - Transformation of Markets for High Volume Products and Processes',
    'CC2 - Increased Access to Local Sources of Financing for Renewable Energy and Energy Efficiency',
    'CC3 - Power Sector Policy Frameworks Supportive of Renewable Energy and Energy Efficiency',
    'CC4 - Productive Uses of Renewable Energy',
    'CC5 - Global Market Aggregation and National Innovation for Emerging Technologies',
    'CC6 - Modal Shifts in Urban Transport and Clean Vehicle/Fuel Technologies',
    'CC7 - Short Term Measures',
    'IW1 - Catalyzing Financial Resources for Implementation of Agreed Actions',
    'IW2 - Expand Global Coverage with Capacity Building Foundational Work',
    'IW3 - Undertake Innovative Demonstrations for Reducing Contaminants and Addressing Water Scarcity',
    'OZ1 - Methyl Bromide Reduction',
    'POP1 - Targeted Capacity Building',
    'POP2 - Implementation of Policy/Regulatory Reforms and Investments',
    'POP3 - Demonstration of Innovative and Cost Effective Technologies',
    'SLM1 - Targeted Capacity Building',
    'SLM2 - Implementation of Innovative and Indigenous Sustainable Land Management Practices',
    'CB1 - Enabling Activities',
    'CB2 - Crosscutting Capacity Building',
    'EM1 - Integrated Approach to Ecosystem Management',
    'SGP1 - Small Grants Progam',
    ]



PROJECT_TYPES = [
    'Enabling Activity',
    'Medium Sized Project',
    'Full Size Project',
    ]

PROJECT_STATUS = [
    'Agency Concept',
    'Completed',
    'Closed',
    'GEF Approved Project',
    'GEF Approved Concept',
    'PDFA',
    'PDFB',
    'Under Implementation',
    '---',
    'CEO PIF Clearance',
    'PIF Approved',
    'PPG Approved',
    'Council Approved',
    'Council Endorsed'
    'CEO Approved',
    'CEO Endorsed',
    'IA Approved',
    'Under Implementation',
    'Project Completion',
    'Project Closure',
    'Cancelled',
    ]


LEAD_AGENCY= [
    'African Development Bank',
    'Asian Development Bank',
    'European Bank for Reconstruction and Development',
    'Food and Agriculture Organization',
    'Inter-American Development Bank',
    'International Fund for Agriculture and Development',
    'United Nations Development Programme',
    'United Nations Environment Programme',
    'World Bank',
    ]

BASINS = [
    '',
    'Agulhas Current (LME)',
    'Albemarle Sound',
    'Amazon',
    'Amu Dariya',
    'Amur',
    'Anadyr',
    'Androscoggin',
    'Antarctic',
    'Arabian Sea',
    'Arabian Sea (LME)',
    'Araguia',
    'Aral Sea',
    'Arctic Basin',
    'Avon',
    'Azov Sea',
    'Baffin Bay, Labrador Sea, Canadian Archipelago',
    'Baltic Sea (LME)',
    'Barents Sea (LME)',
    'Bay of Bengal (LME)',
    'Bay of Fundy',
    'Baykal Lake',
    'Benguela Current (LME)',
    'Bering Sea',
    'Bermejo',
    'Black River',
    'Black Sea (LME)',
    'Bohai Sea',
    'Brahmaputra',
    'Bravo',
    'Brazil Current (LME)',
    'Brazos',
    'Bug',
    'California Current (LME)',
    'Canary Current (LME)',
    'Carribean Islands',
    'Carribean Sea (LME)',
    'Caspian Sea',
    'Celtic-Biscay Shelf (LME)',
    'Central Pacific',
    'Chaophria',
    'Chesapeake Bay',
    'Chilean Southern Lakes',
    'Chorokh',
    'Colorado',
    'Columbia',
    'Congo',
    'Connecticut',
    'Copper',
    'Coral Sea Basin',
    'Cunene',
    'Dalelven',
    'Danube',
    'Delaware',
    'Delaware Bay',
    'Dniestr',
    'Dnipro',
    'Don',
    'Douro, Tejo',
    'East Africa - Western Indian Ocean',
    'East Africa Rift Valley Lakes',
    'East Bering Sea (LME)',
    'East Greenland (LME)',
    'East-China Sea (LME)',
    'Eastern Equatorial Pacific',
    'Eastern Mediterranean',
    'Eastern North Atlantic',
    'Ebro',
    'Elbe',
    'Enisey',
    'Faroe Plateau (LME)',
    'Fraser',
    'Fuerte',
    'Gambia',
    'Ganges',
    'Great Australian Bight',
    'Great Barrier Reef (LME)',
    'Great Lakes',
    'Great Ruaha',
    'Grijalva/Colorado',
    'Guanabara Bay',
    'Gulf of Aden',
    'Gulf of Alaska',
    'Gulf of Aqaba',
    'Gulf of California (LME)',
    'Gulf of Guinea (LME)',
    'Gulf of Honduras',
    'Gulf of Maine',
    'Gulf of Mexico (LME)',
    'Gulf of Thailand',
    'Gulf St. Lawrence',
    'Hai',
    'Hawaiian Archipelago (LME)',
    'Huai',
    'Hudson',
    'Humber',
    'Humboldt Current (LME)',
    'Iberian Coastal (LME)',
    'Iceland Shelf (LME)',
    'Indonesian Seas (LME)',
    'Indus',
    'Irriwaddy',
    'James',
    'Jordan',
    'Juba',
    'Kolyma',
    'Kura',
    'Kuroshio Current (LME)',
    'La Plata/Parana',
    'Ladoga Lake',
    'Lake Chad',
    'Lake Titicaca',
    'Lena',
    'Liao',
    'Limpopo',
    'Loire',
    'Long Island Sound',
    'MacKenzie',
    'Magdalena',
    'Mangoky',
    'Maputo River',
    'Matanuska',
    'Mediterranean Sea (LME)',
    'Mekong',
    'Mississippi',
    'Murray-Darling',
    'N. Dvina',
    'Namsen',
    'Narmada',
    'Neuse',
    'Neva',
    'New Zealand Shelf (LME)',
    'Newfoundland Shelf (LME)',
    'Niger/Benue',
    'Nile',
    'North Caspian',
    'North Pacific',
    'North Sea',
    'Northeast Brazil Shelf (LME)',
    'Northeast Shelf (LME)',
    'Northern Australian Shelf (LME)',
    'Norwegian Sea (LME)',
    'Ob',
    'Oder',
    'Okavango',
    'Oranje',
    'Oyashio Current (LME)',
    'Pamlico',
    'Pamlico Sound',
    'Paraguay',
    'Paraibe do Sul',
    'Parana',
    'Patagonian Shelf (LME)',
    'Patos Lagoon',
    'Pearl River',
    'Pechora',
    'Penobscot',
    'Persian Gulf',
    'Po',
    'Potomac',
    'Red River',
    'Red Sea (LME)',
    'Rhine',
    'Rhone',
    'Rio Grande',
    'Ruyuma',
    'Sacramento',
    'Sao Francisco',
    'Scotian Shelf (LME)',
    'Sea of Japan (LME)',
    'Sea of Okhotsk (LME)',
    'Senegal',
    'Senegal/Cape Verde Island',
    'Shannon',
    'Shelde',
    'Skeena',
    'Small Islands',
    'Somali Coastal Current (LME)',
    'South Asia Seas',
    'South Caspian',
    'South China Sea (LME)',
    'South Pacific',
    'Southeast Asia',
    'Southeast Atlantic',
    'Southeast Pacific',
    'Southeast Shelf (LME)',
    'Southern Ocean',
    'St. John',
    'St. Lawrence',
    'Sulu-Celebes Sea (LME)',
    'Susitna',
    'Susquehanna',
    'Tambre',
    'Tana',
    'Tasman Sea',
    'Thames',
    'Tigris-Euphrates',
    'Tocantins',
    'Tuloma',
    'Tumen',
    'Tyne',
    'Ural',
    'Uruguay',
    'Vistula',
    'Volga',
    'Volta',
    'Weddell Sea',
    'Weser',
    'West & Central Africa',
    'West Bering Sea (LME)',
    'West Greenland (LME)',
    'Western Mediterranean',
    'Western North Atlantic',
    'Wider Carribean',
    'Xingu',
    'Yangtse',
    'Yellow',
    'Yellow Sea',
    'Yukon',
    'Zambezi']

def basin_vocabulary_factory(context):
    """ combine BASINS with additional values from the index """
    catalog = getToolByName(context, 'portal_catalog')
    #basins = list(catalog.Indexes['getBasin'].uniqueValues()) + BASINS
    path='iwlearn/iw-projects/basins/'
    query = {'portal_type': 'Document', 'path': path, 'sort_on': 'sortable_title'}
    brains = catalog(**query)
    basins=[brain.Title for brain in brains]
    basins = list(set(basins))
    basins.sort()
    items = [(basin,basin) for basin in basins]
    return SimpleVocabulary.fromItems(items)

def rating_vocabulary_factory(context):
    ratings =( (u'N/A', ''),
            (u'Highly Unsatisfactory', '0'),
            (u'Unsatisfactory', '1'),
            (u'Moderately Unsatisfactory', '2'),
            (u'Moderately Satisfactory', '3'),
            (u'Satisfactory', '4'),
            (u'Highly Satisfactory', '5'))
    return SimpleVocabulary.fromItems(ratings)


def get_regions(countries = None, subregions=None, regions=None):
    ''' return the regions for a list of countries or all regions
    if no countries are given'''
    rd ={} #dict to make entries in list regions unique
    if countries:
        for country in countries:
            for region in COUNTRYS_SUB_REGION[country]['region']:
                rd[region]=''
    if subregions:
        for subregion in subregions:
            rsc = REGION_SUBREGION_COUNTRIES
            for subregions_region in [[s.keys(),r] for r,s in rsc.iteritems()]:
                if subregion in subregions_region[0]:
                    rd[subregions_region[1]]=''
    if regions:
        for region in regions:
            if region in REGION_SUBREGION_COUNTRIES.keys():
                rd[region]=''
    _regions = rd.keys()
    if ((countries == None) and (subregions==None) and (regions==None)):
        _regions = REGION_SUBREGION_COUNTRIES.keys()
    _regions.sort()
    return _regions

def get_subregions(regions=None, countries=None, subregions=None):
    ''' return subregions for a list of regions or countries or all
    if no regions or countries are given'''
    def sort_subregions(subregions):
        sorted_subregions =[]
        regions = REGION_SUBREGION_COUNTRIES.keys()
        regions.sort()
        for region in regions:
            region_subregion = []
            for subregion in subregions:
                if subregion in REGION_SUBREGION_COUNTRIES[region].keys():
                    region_subregion.append(subregion)
            region_subregion.sort()
            sorted_subregions = sorted_subregions + region_subregion
        return sorted_subregions

    srd ={}
    if regions:
        for region in regions:
            if region in REGION_SUBREGION_COUNTRIES.keys():
                for subregion in REGION_SUBREGION_COUNTRIES[region].keys():
                    srd[subregion] = ''
    if countries:
        for country in countries:
            for subregion in COUNTRYS_SUB_REGION[country]['subregion']:
                srd[subregion] = ''

    if subregions:
        for subregion in subregions:
            srd[subregion] = ''
    if (regions==None and countries==None and subregions==None):
        rsc = REGION_SUBREGION_COUNTRIES
        for region in [s.keys() for r,s in rsc.iteritems()]:
            for subregion in region:
                srd[subregion] = ''
    return sort_subregions(srd.keys())


def get_countries(subregions=None, regions=None, countries=None):
    ''' return all countries belonging to a list of subregions
    or regions or all if no regions or subregions are given'''
    _countries = []
    if subregions:
        pass
    if regions:
        pass
    if countries:
        pass
    if (regions==None and countries==None and subregions==None):
        _countries=COUNTRYS_SUB_REGION.keys()

    _countries.sort()
    return _countries

