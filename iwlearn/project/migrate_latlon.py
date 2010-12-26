# call this script as an external procedure after aplying the interface to projects
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle, IGeoFeatureStyle

def migrate(self):
    projects = self.portal_catalog(portal_type = 'Project')
    for brain in projects:
        project = brain.getObject()
        geo = IGeoManager(project)
        style = IGeoCustomFeatureStyle(project)
        print project.Title()
        print geo.isGeoreferenceable()
        lat =  project.getLatitude()
        lon = project.getLongitude()
        leadagency = project.getLeadagency()
        la =''
        if leadagency:
            la = leadagency.Title().strip()
        if lat and lon and geo.isGeoreferenceable():
            print lat, lon
            #import pdb; pdb.set_trace()
            geo.setCoordinates('Point', (lon, lat))
            style.geostyles.data['use_custom_styles']=True
            if la == 'Food and Agricultural Organization (FAO)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-fao.png'
            elif la == 'United Nations Development Programme (UNDP)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-undp.png'
            elif la == 'International Bank for Reconstruction and Development (WB)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-wb.png'
            elif la == 'United Nations Environment Programme (UNEP)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-unep.png'
            elif la == 'United Nations Office for Project Services (UNOPS)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-unops.png'
            elif la == 'Inter-American Development Bank (IADB)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-iabd.png'
            elif la == 'International Fund for Agriculture and Development (IFAD)':
                style.geostyles.data['marker_image'] = 'string:${portal_url}/marker-icon-ifad.png'
            style.geostyles.update(style.geostyles)
    return 'finished setting coordinates'
