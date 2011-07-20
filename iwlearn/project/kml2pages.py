#
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle
from elementtree.ElementTree import XML
from htmllaundry import sanitize

from shapely.geometry import Point, LineString, Polygon
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon

def extractfeatures_from_file(data):
    kmldom = XML(data)
    ns = kmldom.tag.strip('kml')
    points = kmldom.findall('.//%sPoint' % ns)
    lines = kmldom.findall('.//%sLineString' % ns)
    polygons = kmldom.findall('.//%sPolygon' % ns)
    mpoint = []
    mline =[]
    mpoly = []
    for point in points:
        coordinates = point.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlon = coordinate.text.strip().split(',')
            coords = [float(c) for c in latlon]
            try:
                p = Point(coords)
                mpoint.append(p)
            except:
                logger.info('invalid point geometry: %s' % coordinates[:10] )

    for line in lines:
        coordinates = line.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlons = coordinate.text.split()
            coords = []
            for latlon in latlons:
                coords.append([float(c) for c in latlon.split(',')])
            try:
                l = LineString(coords)
                mline.append(l)
            except:
                logger.info('invalid linestring geometry: %s' % coordinates[:10] )

    for polygon in polygons:
        coordinates = polygon.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlons = coordinate.text.split()
            coords = []
            for latlon in latlons:
                coords.append([float(c) for c in latlon.split(',')])
            try:
                l = Polygon(coords)
                mpoly.append(l)

            except:
                logger.info('invalid polygon geometry: %s' % coordinates[:10] )

    result = {'MultiPoint':None, 'MultiLineString':None, 'MultiPolygon':None}
    if mpoint:
        result['MultiPoint'] =  MultiPoint(mpoint)
    if mline:
        result['MultiLineString'] = MultiLineString(mline)
    if mpoly:
        result['MultiPolygon'] = MultiPolygon(mpoly)


    return result

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

        new_obj.setText(sanitize(text))
        new_obj.setTitle(title)
        if features:
            geo = IGeoManager(new_obj)
            if features['MultiPolygon']:
                shp = features['MultiPolygon']
                q = shp.simplify(0.2).__geo_interface__
                geo.setCoordinates(q['type'], q['coordinates'])


