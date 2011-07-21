#
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from collective.geo.file.browser.extractgeometry import extractfeatures_from_file
from elementtree.ElementTree import XML
from htmllaundry import sanitize

from shapely.geometry import Point, LineString, Polygon
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon


def extract_title(data):
    kmldom = XML(data)
    ns = kmldom.tag.strip('kml')
    titles = kmldom.findall('.//%sname' % ns)
    if titles:
        return titles[0].text.strip()
    else:
        return 'N/A'

def extract_description(data):
    kmldom = XML(data)
    ns = kmldom.tag.strip('kml')
    descriptions = kmldom.findall('.//%sdescription' % ns)
    desc = ''
    for description in descriptions:
        if 'Double click to zoom in' != description.text.strip():
            desc += description.text.strip()

    return desc


def convert_kml_to_page(self):
    for brain in self.portal_catalog(portal_type = 'File', path='iwlearn/iw-projects/basins'):
        obj = brain.getObject()
        data = obj.get_data()
        parent = obj.getParentNode()
        if callable(obj.id):
            obj_id = obj.id()
        else:
            obj_id = obj.id
        new_obj_id = obj_id.strip('kml') +'htm'
        try:
            self.portal_types.constructContent('Document', parent, new_obj_id)
        except:
            pass
        new_obj=parent[new_obj_id]
        if parent.id =='lmes':
            color='0000bf'
        elif parent.id =='rivers':
            color='56ffff'
        elif parent.id =='lakes':
            color='2c80d3'
        elif parent.id =='aquifers':
            color='c1742c'
        else:
            color ='00ff00'
        features = None
        try:
            features = extractfeatures_from_file(data)
            title = extract_title(data).strip('.kml')
            text = extract_description(data)
            #print features['MultiPolygon']
            print title
            #print text
        except:
            print 'exception in %s' % brain.getId
            pass
        if new_obj.getText():
            print 'skipping set text for %s' % brain.getId
        else:
            new_obj.setText(sanitize(text))
            new_obj.setTitle(title)
        if features:
            style = IGeoCustomFeatureStyle(new_obj)
            style.geostyles.data['use_custom_styles']=True
            style.geostyles.data['polygoncolor']=color
            style.geostyles.update(style.geostyles)
            geo = IGeoManager(new_obj)
            if features['MultiPolygon']:
                shp = features['MultiPolygon']
                q = shp.simplify(0.2).__geo_interface__
                geo.setCoordinates(q['type'], q['coordinates'])


