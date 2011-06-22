#
import csv
import geojson
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from plone.i18n.locales.countries import _countrylist

def annotate(self):
    data = csv.DictReader(open('110m_admin_0_countries.csv', 'r'))
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

def name_countries(self):
    for brain in self.portal_catalog(portal_type = 'Image', path='iwlearn/countries/'):
        cc = brain.getId
        if cc[:2] in _countrylist:
            obj = brain.getObject()
            obj.setTitle(_countrylist[cc[:2]]['name'])
            print _countrylist[cc[:2]]['name']
    import ipdb; ipdb.set_trace()
