# -*- coding: utf-8 -*-
import geojson
from shapely.geometry import asShape
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely import wkt
from plone.i18n.normalizer import IDNormalizer
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
import random
idn = IDNormalizer()

def import_aquifers(self):
    aquifers = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/aquifers.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['aquifers']
    for aquifer in aquifers['features']:
        ext = idn.normalize(aquifer['properties']['FIRST_ISAR'])
        new_obj_id = idn.normalize(aquifer['properties']['NAME']) + ext
        if new_obj_id in parent:
            mpoly = []
            new_obj=parent[new_obj_id]
            geo = IGeoManager(new_obj)
            add_geom = asShape(aquifer['geometry']).simplify(0.2)
            my_geom = wkt.loads(geo.wkt)
            if my_geom.geom_type == 'MultiPolygon':
                for poly in my_geom.geoms:
                    if poly.contains(add_geom):
                        continue
            elif my_geom.contains(add_geom):
                continue
            elif add_geom.contains(my_geom):
                q = add_geom.__geo_interface__
            else:
                if add_geom.geom_type == 'Polygon':
                    mpoly.append(add_geom)
                elif add_geom.geom_type == 'MultiPolygon':
                    mpoly += list(add_geom.geoms)
                if my_geom.geom_type == 'Polygon':
                    mpoly.append(my_geom)
                elif my_geom.geom_type == 'MultiPolygon':
                    mpoly += list(my_geom.geoms)
                q = MultiPolygon(mpoly).__geo_interface__
            geo.setCoordinates(q['type'], q['coordinates'])
            print new_obj_id, '*'
        else:
            self.portal_types.constructContent('Basin', parent, new_obj_id)
            new_obj=parent[new_obj_id]
            print new_obj_id
            new_obj.setTitle(aquifer['properties']['NAME'])
            new_obj.setDescription("Area: %s; Length: %s" % (
                            aquifer['properties']['Shape_Area'],
                            aquifer['properties']['Shape_Leng']))
            new_obj.setBasin_type('Aquifer')
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
        'src/iwlearn.project/iwlearn/project/dataimport/basins.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['rivers']
    for river in rivers['features']:
        rnd = str(-random.randrange(100,1000))
        new_obj_id = idn.normalize(river['properties']['BCODE'])
        print new_obj_id
        self.portal_types.constructContent('Basin', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        new_obj.setTitle(river['properties']['CATEGORY'])
        new_obj.setDescription("Area: %s; Length: %s" % (
                        river['properties']['Shape_Area'],
                        river['properties']['Shape_Leng']))
        new_obj.setBasin_type('River')
        color='56ffff'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)
        q = asShape(river['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])

def import_giwarivers(self):
    rivers = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/missing_rivers.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['rivers']
    for river in rivers['features']:
        #rnd = str(-random.randrange(100,1000))
        new_obj_id = 'giwalme-id-' + idn.normalize(river['properties']['GIWALME_ID'])
        print new_obj_id
        self.portal_types.constructContent('Basin', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        new_obj.setTitle(river['properties']['NAME'])
        #new_obj.setDescription("Area: %s; Length: %s" % (
        #                river['properties']['Shape_Area'],
        #                river['properties']['Shape_Leng']))
        new_obj.setBasin_type('River')
        color='56ffff'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)
        q = asShape(river['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])

def import_lakes(self):
    lakes = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/lakes.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['lakes']
    for lake in lakes['features']:
        if ((lake['properties']['TYPE']=='Lake') and ( lake['properties']['SEC_CNTRY'])):
            new_obj_id = idn.normalize(lake['properties']['GLWD_ID'])
            print new_obj_id
            self.portal_types.constructContent('Basin', parent, new_obj_id)
            new_obj=parent[new_obj_id]
            if lake['properties']['LAKE_NAME']:
                new_obj.setTitle(lake['properties']['LAKE_NAME'])
            new_obj.setDescription("Area: %s; Perimeter: %s; Countries: %s, %s" % (
                            lake['properties']['AREA_SKM'],
                            lake['properties']['PERIM_KM'],
                            lake['properties']['COUNTRY'],
                            lake['properties']['SEC_CNTRY'],
                            ))
            new_obj.setBasin_type('Lake')
            color='2c80d3'
            style = IGeoCustomFeatureStyle(new_obj)
            style.geostyles.data['use_custom_styles']=True
            style.geostyles.data['polygoncolor']=color
            style.geostyles.update(style.geostyles)
            geo = IGeoManager(new_obj)
            q = asShape(lake['geometry']).simplify(0.1).__geo_interface__
            geo.setCoordinates(q['type'], q['coordinates'])

def import_lakes2(self):
    lakes = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/missing_lakes.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['lakes']
    for lake in lakes['features']:
        if lake['properties']['TYPE']=='Lake':
            new_obj_id = idn.normalize(lake['properties']['GLWD_ID'])
            print new_obj_id
            self.portal_types.constructContent('Basin', parent, new_obj_id)
            new_obj=parent[new_obj_id]
            if lake['properties']['LAKE_NAME']:
                new_obj.setTitle(lake['properties']['LAKE_NAME'])
            new_obj.setDescription("Area: %s; Perimeter: %s; Countries: %s" % (
                            lake['properties']['AREA_SKM'],
                            lake['properties']['PERIM_KM'],
                            lake['properties']['COUNTRY'],
                            ))
            new_obj.setBasin_type('Lake')
            color='2c80d3'
            style = IGeoCustomFeatureStyle(new_obj)
            style.geostyles.data['use_custom_styles']=True
            style.geostyles.data['polygoncolor']=color
            style.geostyles.update(style.geostyles)
            geo = IGeoManager(new_obj)
            q = asShape(lake['geometry']).simplify(0.1).__geo_interface__
            geo.setCoordinates(q['type'], q['coordinates'])

def import_lmes(self):
    lmes = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/lmes.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['lmes']
    for lme in lmes['features']:
        new_obj_id = idn.normalize(lme['properties']['LME_NAME']) #+ rnd
        if new_obj_id in parent:
            mpoly = []
            new_obj=parent[new_obj_id]
            geo = IGeoManager(new_obj)
            add_geom = asShape(lme['geometry']).simplify(0.2)
            my_geom = wkt.loads(geo.wkt)
            if add_geom.geom_type == 'Polygon':
                mpoly.append(add_geom)
            elif add_geom.geom_type == 'MultiPolygon':
                mpoly += list(add_geom.geoms)
            if my_geom.geom_type == 'Polygon':
                mpoly.append(my_geom)
            elif my_geom.geom_type == 'MultiPolygon':
                mpoly += list(my_geom.geoms)
            q = MultiPolygon(mpoly).__geo_interface__
            geo.setCoordinates(q['type'], q['coordinates'])
            #import ipdb; ipdb.set_trace()
            print new_obj_id, '*'
        else:
            self.portal_types.constructContent('Basin', parent, new_obj_id)
            new_obj=parent[new_obj_id]
            print new_obj_id
            new_obj.setTitle(lme['properties']['LME_NAME'] + ' (LME)')
            new_obj.setDescription("Area: %s; Length: %s" % (
                            lme['properties']['Shape_Area'],
                            lme['properties']['Shape_Leng']))
            new_obj.setBasin_type('LME')
            color='0000bf'
            style = IGeoCustomFeatureStyle(new_obj)
            style.geostyles.data['use_custom_styles']=True
            style.geostyles.data['polygoncolor']=color
            style.geostyles.update(style.geostyles)
            geo = IGeoManager(new_obj)
            q = asShape(lme['geometry']).simplify(0.2).__geo_interface__
            geo.setCoordinates(q['type'], q['coordinates'])

def import_giwalmes(self):
    lmes = geojson.load(open(
        'src/iwlearn.project/iwlearn/project/dataimport/add_lmes.json',
        'r'))
    parent = self.portal_url.getPortalObject()['iw-projects']['basins']['lmes']
    for lme in lmes['features']:
        new_obj_id = 'giwalme-id-' + idn.normalize(lme['properties']['GIWALME_ID'])
        self.portal_types.constructContent('Basin', parent, new_obj_id)
        new_obj=parent[new_obj_id]
        print new_obj_id
        new_obj.setTitle(lme['properties']['NAME'] + ' (LME)')
        #new_obj.setDescription("Area: %s; Length: %s" % (
        #                lme['properties']['Shape_Area'],
        #                lme['properties']['Shape_Leng']))
        new_obj.setBasin_type('LME')
        color='0000bf'
        style = IGeoCustomFeatureStyle(new_obj)
        style.geostyles.data['use_custom_styles']=True
        style.geostyles.data['polygoncolor']=color
        style.geostyles.update(style.geostyles)
        geo = IGeoManager(new_obj)
        q = asShape(lme['geometry']).simplify(0.2).__geo_interface__
        geo.setCoordinates(q['type'], q['coordinates'])

BASIN_TRANSLATE = {
'Agusan': 'Mindanao Island coastal drainage (S) Celebes Sea, (N) Pacifi',
'Arctic Basin': 'Arctic (LME)',
'Baikal Basin': 'Baikal',
'Bermejo': 'La Plata',
'Bravo': 'Rio Grande (North America)',
'Carribean Islands': 'Caribbean Sea (LME)',
'Carribean Sea (LME)': 'Caribbean Sea (LME)',
'Coral Sea Basin': 'Coral Sea Basin (LME)',
'Dinaric karst Aquifer': 'Dinaric Littoral (West Coast aquifer)',
'Dnipro': 'Dnieper',
#'East Africa - Western Indian Ocean': '',
#'East Africa Rift Valley Lakes': '',
'East-China Sea (LME)': 'East China Sea (LME)',
'Guarani Aquifer': 'Guaraní',
'Gulf of Aden': 'Arabian Sea (LME)',
'Gulf of Fonseca': 'Pacific Central-American Coastal (LME)',
'Gulf of Guinea (LME)': 'Guinea Current (LME)',
'Gulf of Honduras': 'Caribbean Sea (LME)',
'Hai': 'Hai He River Basin',
'Huai': 'Da Yunhe R.B. & Grand Canal district between (Yellow & Yangt',
'Iullemeden Aquifer': 'Irhazer-Iullemeden Basin',
'Kura': 'Kura-Araks',
'La Plata/Parana': 'La Plata',
#'Lake Nicaragua': '',
'Lake Skadar': 'Scutari',
'Niger/Benue': 'Niger',
'North West Sahara Aquifer': 'Northwest Sahara Aquifer System (NWSAS)',
'Nubian Aquifer': 'Nubian Sandstone Aquifer System (NSAS)',
'Oranje': 'Orange',
'Orontes': 'Asi/Orontes',
'Paraguay': 'La Plata',
'Pearl River': 'Bei Jiang/Hsi',
'Peipsi/Chudskoe': 'Peipus',
'San Juan River': 'San Juan',
'Sao Francisco': 'Rio Sao Francisco River Basin',
'Sistan': 'Helmand',
#'Southeast Asia': '',
#'Southeast Pacific': '',
#'Southern Ocean': '',
'Tisza': 'Danube',
'Western Mediterranean': 'Mediterranean Sea (LME)',
'Wider Carribean': 'Caribbean Sea (LME)',
'Yangtse': 'Chang Jiang (Yangtze) River Basin (Yellow Sea)',
'Yellow Sea': 'Yellow Sea (LME)'
}

def relate_basins(self):
    path='iwlearn/iw-projects/basins/'
    basin_query = {'portal_type': 'Basin', 'path': path}
    basins = {}
    for brain in self.portal_catalog(**basin_query):
        uids = basins.get(brain.Title, [])
        uids.append(brain.UID)
        basins[brain.Title] = uids
    for brain in self.portal_catalog(portal_type = 'Project'):
        old_basins = list(brain.getBasin)
        change = False
        new_basins =[]
        for old_basin in old_basins:
            if old_basin in basins:
                change = True
                new_basins = new_basins + basins[old_basin]
        if change:
            ob = brain.getObject()
            ob.setBasins(new_basins)
            print old_basins


def rename_basins(self):
    for brain in self.portal_catalog(portal_type = 'Project'):
        basins = list(brain.getBasin)
        b_in = False
        for basin in basins:

            if basin in BASIN_TRANSLATE:
                b_in = True
                basins.remove(basin)
                basins.append(BASIN_TRANSLATE[basin])
                print basin, BASIN_TRANSLATE[basin]
        if b_in:
            ob = brain.getObject()
            ob.setBasin(basins)

def import_basins(self):
    import_lmes(self)
    import_giwalmes(self)
    import_rivers(self)
    import_giwarivers(self)
    import_aquifers(self)
    import_lakes(self)
    import_lakes2(self)
    rename_basins(self)
    return 'basins imported and renamed, reindex getBasin'

