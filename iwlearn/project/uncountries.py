#
import csv
from plone.i18n.locales.countries import _countrylist

REGION_SUBREGION_COUNTRIES ={
    u'Europe': {
         'SIDS (Europe)':[],
         'Southern Europe':['cs',]
    },
    u'Oceania': {
        'SIDS (Oceania)':[]
    },
    u'Africa': {
        'SIDS (Africa)':[]
    },
    u'Asia': {
         'SIDS (Asia)':[]
    },
    u'Americas': {
         'SIDS (Americas)':['an',],
          'Caribbean': ['an',]
    },
    u'Antarctica': {
        u'Antarctica': [u'aq']
    },
    u'SIDS' : {
        'Small island developing States': ['an',]
    },
    u'Global' : {
     }
}

def get_countrycode(data, isonum):
    print data
    for d in data:
        print d
        print d['Numeric Code'], d['Alpha-2 Code']
        if int(d['Numeric Code']) == int(isonum):
            return d['Alpha-2 Code']

def get_subregions():
    data = csv.DictReader(open('un-regions-subregions.csv', 'r'))
    isodata = csv.DictReader(open('country_iso_codes.csv', 'r'))
    isod = {}
    for di in isodata:
        isod[di['Numeric code ']] = di['Alpha-2 code ']
    print isod
    for d in data:
        if d['region'] and d['subregion']:
           # print  REGION_SUBREGION_COUNTRIES[d['region']].get(d['subregion'], d['subregion'])
            REGION_SUBREGION_COUNTRIES[d['region']][d['subregion']] = REGION_SUBREGION_COUNTRIES[d['region']].get(d['subregion'], [])
            try:
                REGION_SUBREGION_COUNTRIES[d['region']][d['subregion']].append(
                        isod[d['iso']].lower())
                REGION_SUBREGION_COUNTRIES[d['region']][d['subregion']].sort()
            except:
                print 'error: ', d['iso'], d['name']
    for sid in REGION_SUBREGION_COUNTRIES['SIDS']['Small island developing States']:
        rc = []
        for subregion in REGION_SUBREGION_COUNTRIES['Europe'].items():
            if sid in subregion[1]:
                REGION_SUBREGION_COUNTRIES['Europe']['SIDS (Europe)'].append(sid)
                REGION_SUBREGION_COUNTRIES['Europe']['SIDS (Europe)'] = list(
                    set(REGION_SUBREGION_COUNTRIES['Europe']['SIDS (Europe)']))
                REGION_SUBREGION_COUNTRIES['Europe']['SIDS (Europe)'].sort()

        for subregion in REGION_SUBREGION_COUNTRIES['Oceania'].items():
            if sid in subregion[1]:
                REGION_SUBREGION_COUNTRIES['Oceania']['SIDS (Oceania)'].append(sid)
                REGION_SUBREGION_COUNTRIES['Oceania']['SIDS (Oceania)'] = list(
                    set(REGION_SUBREGION_COUNTRIES['Oceania']['SIDS (Oceania)']))
                REGION_SUBREGION_COUNTRIES['Oceania']['SIDS (Oceania)'].sort()

        for subregion in REGION_SUBREGION_COUNTRIES['Africa'].items():
            if sid in subregion[1]:
                REGION_SUBREGION_COUNTRIES['Africa']['SIDS (Africa)'].append(sid)
                REGION_SUBREGION_COUNTRIES['Africa']['SIDS (Africa)'] = list(
                    set(REGION_SUBREGION_COUNTRIES['Africa']['SIDS (Africa)']))
                REGION_SUBREGION_COUNTRIES['Africa']['SIDS (Africa)'].sort()

        for subregion in REGION_SUBREGION_COUNTRIES['Asia'].items():
            if sid in subregion[1]:
                REGION_SUBREGION_COUNTRIES['Asia']['SIDS (Asia)'].append(sid)
                REGION_SUBREGION_COUNTRIES['Asia']['SIDS (Asia)'] = list(
                    set(REGION_SUBREGION_COUNTRIES['Asia']['SIDS (Asia)']))
                REGION_SUBREGION_COUNTRIES['Asia']['SIDS (Asia)'].sort()

        for subregion in REGION_SUBREGION_COUNTRIES['Americas'].items():
            if sid in subregion[1]:
                REGION_SUBREGION_COUNTRIES['Americas']['SIDS (Americas)'].append(sid)
                REGION_SUBREGION_COUNTRIES['Americas']['SIDS (Americas)'] = list(
                    set(REGION_SUBREGION_COUNTRIES['Americas']['SIDS (Americas)']))
                REGION_SUBREGION_COUNTRIES['Americas']['SIDS (Americas)'].sort()

    print REGION_SUBREGION_COUNTRIES
    COUNTRYS_SUB_REGION = {}
    gef_countries =[]
    for _r in REGION_SUBREGION_COUNTRIES:
        for _sr in REGION_SUBREGION_COUNTRIES[_r]:
            for _c in REGION_SUBREGION_COUNTRIES[_r][_sr]:
                gef_countries.append(_c)
                if _c not in _countrylist:
                    print _c
    for pc in _countrylist:
        if pc not in gef_countries:
            print 'Not found in GEF:', pc, _countrylist[pc]['name']
    #import ipdb; ipdb.set_trace()

get_subregions()
