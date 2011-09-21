#
import csv
import geojson
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from plone.i18n.locales.countries import _countrylist
import logging
logger = logging.getLogger('iwlearn.project')

def annotate_110(self):
    data = csv.DictReader(open('src/iwlearn.project/iwlearn/project/dataimport/110m_admin_0_countries.csv', 'r'))
    for brain in self.portal_catalog(portal_type = 'Folder', path='iwlearn/images/countries/'):
        obj=brain.getObject()
    for d in data:
        #print d['json_4326']
        #print d['admin']
        print d['iso_a2']
        child_id = d['iso_a2'].lower() + '.png'
        q = geojson.loads(d['json_4326'])
        print q
        if d['iso_a2'] != '-99':
            child = obj[child_id]
            geo = IGeoManager(child)
            #geo.setCoordinates(**q)
            geo.setCoordinates(q['type'], q['coordinates'])
            child.setDescription('Population: %s' % d['pop_est'])

def name_countries(self):
    for brain in self.portal_catalog(portal_type = 'Image', path='iwlearn/images/countries/'):
        cc = brain.getId
        if cc[:2] in _countrylist:
            obj = brain.getObject()
            obj.setTitle(_countrylist[cc[:2]]['name'])
            print _countrylist[cc[:2]]['name']

MISSING_IN_110 = ['ad', 'ag', 'ai', 'an', 'as', 'aw', 'ax', 'bb', 'bh', 'bl',
'bm', 'bv', 'cc', 'ck', 'cs', 'cv', 'cx', 'dm', 'eh', 'fm', 'fo', 'fx',
'gd', 'gf', 'gg', 'gi', 'gp', 'gs', 'gu', 'hk', 'hm', 'io', 'je', 'ki',
'km', 'kn', 'ky', 'lc', 'li', 'mc', 'mf', 'mh', 'mo', 'mp', 'mq', 'ms',
'mt', 'mu', 'mv', 'nf', 'nr', 'nu', 'pf', 'pm', 'pn', 'pw', 're', 'sc',
'sg', 'sh', 'sj', 'sm', 'st', 'tc', 'tk', 'to', 'tp', 'tv', 'um', 'va',
'vc', 'vg', 'vi', 'wf', 'ws', 'xt', 'yt', 'yu']

def annotate_50m(self):
    data = csv.DictReader(open('src/iwlearn.project/iwlearn/project/dataimport/50m_admin_0_countries.csv', 'r'))
    for brain in self.portal_catalog(portal_type = 'Folder', path='iwlearn/images/countries/'):
        obj=brain.getObject()
    for d in data:
        #print d['json_4326']
        print d['iso_a2']

        child_id = d['iso_a2'].lower() + '.png'
        #print q
        if d['iso_a2'].lower() in MISSING_IN_110:
            logger.info('added: ' + d['admin'])
            print d['iso_a2']
            q = geojson.loads(d['json_4326'])
            child = obj[child_id]
            geo = IGeoManager(child)
            #geo.setCoordinates(**q)
            geo.setCoordinates(q['type'], q['coordinates'])
            child.setDescription('Population: %s' % d['pop_est'])

MISSING_IN_50 = ['an', 'ax', 'bv', 'cc', 'cs', 'cx', 'eh', 'fx', 'gf',
'gi', 'gp', 'mq', 're', 'sj', 'tk', 'tp', 'tv', 'um', 'xt', 'yt', 'yu']

def annotate_10m(self):
    data = csv.DictReader(open('src/iwlearn.project/iwlearn/project/dataimport/10m_admin_0_countries.csv', 'r'))
    for brain in self.portal_catalog(portal_type = 'Folder', path='iwlearn/images/countries/'):
        obj=brain.getObject()
    for d in data:
        #print d['json_4326']
        print d['iso_a2']

        child_id = d['iso_a2'].lower() + '.png'
        #print q
        if d['iso_a2'].lower() in MISSING_IN_50:
            logger.info('added: ' + d['admin'])
            print d['iso_a2']
            q = geojson.loads(d['json_4326'])
            child = obj[child_id]
            geo = IGeoManager(child)
            #geo.setCoordinates(**q)
            geo.setCoordinates(q['type'], q['coordinates'])
            child.setDescription('Population: %s' % d['pop_est'])

def annotate_all(self):
        annotate_50m(self)
        annotate_10m(self)
        annotate_110(self)
        name_countries(self)
        return 'countries annotated and named'

