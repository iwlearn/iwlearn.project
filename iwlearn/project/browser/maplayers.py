#
from Products.CMFCore.utils import getToolByName

from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.file.browser.maplayer import KMLFileMapLayer

class ProjectDbKMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return """
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '@@projectdbkml_view',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (self.context.Title().replace("'", "\'"), context_url)


class ProjectDbKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(ProjectDbKMLMapLayers, self).layers()
        layers.append(ProjectDbKMLMapLayer(self.context))
        return layers


class ProjectKMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return """
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '@@kml-document',
            { format: OpenLayers.Format.KML,
              eventListeners: { 'loadend': function(event) {
                                 var c_lonlat = this.getDataExtent().getCenterLonLat();
                                 this.map.setCenter(new OpenLayers.LonLat(
                                 c_lonlat.lon, c_lonlat.lat), 5, false, false);
                                }
                            },
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (self.context.Title().replace("'", "\'"), context_url)


class ProjectInnerKMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return """
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '@@projectkml_view',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (u"Maps of: " + self.context.Title().replace("'", "\'"), context_url)


class ProjectKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(ProjectKMLMapLayers, self).layers()
        layers.append(ProjectKMLMapLayer(self.context))
        layers.append(ProjectInnerKMLMapLayer(self.context))
        path = '/'.join(self.context.getPhysicalPath())
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        for brain in portal_catalog(path=path, Subject='map-layer',
            portal_type='File', review_state="published"):
            object = brain.getObject()
            if object.content_type == 'application/vnd.google-earth.kml+xml':
                layers.append(KMLFileMapLayer(self.context,object))
        return layers

