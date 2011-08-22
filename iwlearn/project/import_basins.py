# import from geojson
import geojson
from shapely.geometry import asShape
from plone.i18n.normalizer import IDNormalizer
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
import random
idn = IDNormalizer()

def import_aquifers(self):
    aquifers = geojson.load(open(
        '/home/ledermac/Documents/aquifers/aquifers.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['aquifers']
    for aquifer in aquifers['features']:
        rnd = str(-random.randrange(1000,10000))
        new_obj_id = idn.normalize(aquifer['properties']['NAME']) + rnd
        self.portal_types.constructContent('Document', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        print new_obj_id
        new_obj.setTitle(aquifer['properties']['NAME'])
        color='c1742c'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)

        q = asShape(aquifer['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])


def import_rivers(self):
    rivers = geojson.load(open(
        '/home/ledermac/Documents/basins/basins.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['rivers']
    for river in rivers['features']:
        rnd = str(-random.randrange(100,1000))
        new_obj_id = idn.normalize(river['properties']['BCODE']) #+ rnd
        print new_obj_id
        self.portal_types.constructContent('Document', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        new_obj.setTitle(river['properties']['CATEGORY'])
        new_obj.setDescription("Area: %s; Length: %s" % (
                        river['properties']['Shape_Area'],
                        river['properties']['Shape_Leng']))
        color='56ffff'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)
        q = asShape(river['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])


def import_lmes(self):
    lmes = geojson.load(open(
        '/home/ledermac/Documents/lmes/lmes.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['lmes']
    for lme in lmes['features']:
        rnd = str(-random.randrange(1000,10000))
        new_obj_id = idn.normalize(lme['properties']['LME_NAME']) #+ rnd
        if new_obj_id in parent:
            new_obj_id = new_obj_id + rnd
        self.portal_types.constructContent('Document', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        print new_obj_id
        new_obj.setTitle(lme['properties']['LME_NAME'] + ' (LME)')
        new_obj.setDescription("Area: %s; Length: %s" % (
                        lme['properties']['Shape_Area'],
                        lme['properties']['Shape_Leng']))
        color='0000bf'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)
        q = asShape(lme['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])
