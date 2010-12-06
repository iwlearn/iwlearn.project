from collective.geo.contentlocations.interfaces import IGeoManager

def migrate(self):
    projects = self.portal_catalog(portal_type = 'Project')
    for brain in projects:
        project = brain.getObject()
        geo = IGeoManager(project)
        print project.Title()
        print geo.isGeoreferenceable()
        lat =  project.getLatitude()
        lon = project.getLongitude()
        if lat and lon and geo.isGeoreferenceable():
            print lat, lon
            geo.setCoordinates('Point', (lon, lat))
    return 'finished setting coordinates'
