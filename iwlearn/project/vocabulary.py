# -*- coding: utf-8 -*-
import logging
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
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

# this is the UN definition of Regions/Subregions/countries
# from http://unstats.un.org/unsd/methods/m49/m49regin.htm
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
            'mw', 'mz', 're', 'rw', 'sc', 'so', 'ss', 'tz', 'ug', 'yt', 'zm', 'zw'],
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
            'mo', 'tj', 'tm', 'tw', 'uz']},
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
    ('EA', 'Enabling Activity'),
    ('MSP', 'Medium Sized Project'),
    ('FSP', 'Full Size Project'),
    ('PFD', 'PFD'),
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
    'CEO PIF Rejection',
    'PIF Approved',
    'PPG Approved',
    'Council Approved',
    'Council Endorsed',
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


BASIN_TYPE = ['LME',
    'River',
    'Lake',
    'Aquifer',
    'Ocean']

PROJECT_SCALE = [
    'Global',
    'Regional',
    'National',
]

ECOSYSTEM = [
    'River',
    'Lake',
    'Sea',
    'LME',
    'SIDS',
    'Groundwater',
]


PROJECT_CATEGORY = [
    'ABNJ',
    'Coastal Management',
    'Fisheries',
    'Foundational',
    'LBS',
    'Nutrient Reduction Investment',
    'Oil Spill',
    'Persistent Toxic Substances',
    'Policy',
    'Portfolio Learning',
    'SAP Implementation',
    'Ship Safety',
    'Ship Waste',
    'Wastewater',
    ]


RATINGS ={ 'N/A' : None,
        '': None,
        'Highly Unsatisfactory' : '0',
        'Unsatisfactory': '1',
        'Moderately Unsatisfactory': '2',
        'Moderately Satisfactory': '3',
        'Satisfactory': '4',
        'Highly Satisfactory': '5'}


OUTCOME_RATING ={ 'UA' : None,
        '': None,
        'Highly Unsatisfactory' : '6',
        'Unsatisfactory': '5',
        'Moderately Unsatisfactory': '4',
        'Moderately Satisfactory': '3',
        'Satisfactory': '2',
        'Highly Satisfactory': '1'}

GEF_PHASE = [
    ('0', 'Pilot'),
    ('1', 'GEF - 1'),
    ('2', 'GEF - 2'),
    ('3', 'GEF - 3'),
    ('4', 'GEF - 4'),
    ('5', 'GEF - 5'),
#   ('6', 'GEF - 6'),
    ]

def gef_phase_vocabulary_factory(context):
    terms = []
    for value in GEF_PHASE:
        terms.append(SimpleTerm(*value))
    return SimpleVocabulary(terms)





def basin_vocabulary_factory(context):
    catalog = getToolByName(context, 'portal_catalog')
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

