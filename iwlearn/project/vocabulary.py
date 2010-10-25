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

from plone.i18n.locales.countries import _countrylist


REGION_SUBREGION_COUNTRIES ={
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
     u'Global' : [] #_countrylist.keys()
     }
}

COUNTRYS_SUB_REGION = {}
for _r in REGION_SUBREGION_COUNTRIES:
    for _sr in REGION_SUBREGION_COUNTRIES[_r]:
        for _c in REGION_SUBREGION_COUNTRIES[_r][_sr]:
            _country = _countrylist[_c][u'name']
            _regions = COUNTRYS_SUB_REGION.get(_country,
                {u'region':[], u'subregion':[]})
            _regions[u'region'].append(_r)
            _regions[u'subregion'].append(_sr)
            COUNTRYS_SUB_REGION[_country]=_regions
        
        
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
    'CEO Approved',
    'CEO Endorsed',
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
    'Okavango (internal)',
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

    
def get_regions(countries = None, subregions=None):
    ''' return the regions for a list of countries or all regions
    if no countries are given'''
    regions =[]
    if countries:
        pass 
    elif subregions:
        pass 
    else:
        regions = REGION_SUBREGION_COUNTRIES.keys()
    regions.sort()
    return regions

def get_subregions(regions=None, countries=None):
    ''' return subregions for a list of regions or countries or all
    if no regions or countries are given'''
    def get_region_subgegion(regions):
        subregions = []
        regions.sort()
        for region in regions:
            subregion = REGION_SUBREGION_COUNTRIES[region].keys()
            subregion.sort()
            subregions= subregions + subregion
        return subregions
    if regions:
        subregions = get_region_subgegion(regions)
    elif countries:
        subregions=[]
        pass 
    else:
        subregions = get_region_subgegion(
            REGION_SUBREGION_COUNTRIES.keys())
    return subregions    
    
def get_countries(subregions=None, regions=None):
    ''' return all countries belonging to a list of subregions 
    or regions or all if no regions or subregions are given'''
    countries = []
    if subregions:
        pass
    elif regions:
        pass
    else:
        countries=COUNTRYS_SUB_REGION.keys()
        countries.sort()
    return countries 
    
