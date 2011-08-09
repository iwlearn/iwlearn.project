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


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectdbkml_view",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [
                        new OpenLayers.Strategy.Fixed(),
                         new OpenLayers.Strategy.Cluster()
                        ],
                     styleMap: new OpenLayers.StyleMap({
                        "default": new OpenLayers.Style({
                                        pointRadius: "${radius}",
                                        fillColor: "#ffcc66",
                                        fillOpacity: 0.8,
                                        strokeColor: "#cc6633",
                                        strokeWidth: 2,
                                        strokeOpacity: 0.8,
                                        label:"${count}"
                                    }, {
                                        context: {
                                            radius: function(feature) {
                                                return Math.min(feature.attributes.count, 7) + 3;
                                            }
                                        }
                                    }),
                        "select": {
                            fillColor: "#8aeeef",
                            strokeColor: "#32a8a9"
                            },
                        }),
                    eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent();
                                 this.map.zoomToExtent(extent);
                                }
                            },
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (
            self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", "&apos;"),
            context_url)



class ProjectDbKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(ProjectDbKMLMapLayers, self).layers()
        layers.append(ProjectDbKMLMapLayer(self.context))
        return layers


class ProjectDbKMLBasinMapLayer(MapLayer):
    """
    layer for project basins
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return u"""
            function() {
                return new OpenLayers.Layer.Vector("Basin Detail", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectbasindetail_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true}),
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                },
            function() {
                return new OpenLayers.Layer.Vector("Basin Cluster", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectbasincluster_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [
                        new OpenLayers.Strategy.Fixed(),
                         new OpenLayers.Strategy.Cluster()
                        ],
                     styleMap: new OpenLayers.StyleMap({
                        "default": new OpenLayers.Style({
                                        pointRadius: "${radius}",
                                        fillColor: "#ffcc66",
                                        fillOpacity: 0.8,
                                        strokeColor: "#cc6633",
                                        strokeWidth: 2,
                                        strokeOpacity: 0.8,
                                        label:"${count}"
                                    }, {
                                        context: {
                                            radius: function(feature) {
                                                return Math.min(feature.attributes.count, 7) + 3;
                                            }
                                        }
                                    }),
                        "select": {
                            fillColor: "#8aeeef",
                            strokeColor: "#32a8a9"
                            },
                        }),
                    /*eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent();
                                 this.map.zoomToExtent(extent);
                                }
                            },*/
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (context_url ,context_url)





        XXX= """
        function() { return new OpenLayers.Layer.GML('%s', '%s@@projectbasin_view.kml',
            { format: OpenLayers.Format.KML,
              /*eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent();
                                 this.map.zoomToExtent(extent);
                                }
                            },*/
              projection: cgmap.createDefaultOptions().displayProjection,
              visibility: false,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % ( "Basins",
            context_url)

class ProjectDbKMLCountryMapLayer(MapLayer):
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


        #return """
        #function() { return new OpenLayers.Layer.GML('%s', '%s@@projectdbcountry_view.kml',
            #{ format: OpenLayers.Format.KML,
              #/*eventListeners: { 'loadend': function(event) {
                                    #if (this.getVisibility()){
                                         #var extent = this.getDataExtent();
                                         #this.map.zoomToExtent(extent);
                                    #};
                                #}
                            #},*/
              #projection: cgmap.createDefaultOptions().displayProjection,
              #formatOptions: {
                  #extractStyles: true,
                  #extractAttributes: true }
            #});}""" % (u"Countries",
            #context_url)


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectdbcountry_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    /*eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent();
                                 this.map.zoomToExtent(extent);
                                }
                            },*/
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Countries', context_url)

class ProjectDbKMLCountryMapLayers(MapLayers):
    def layers(self):
        layers = super(ProjectDbKMLCountryMapLayers, self).layers()
        layers.append(ProjectDbKMLCountryMapLayer(self.context))
        layers.append(ProjectDbKMLBasinMapLayer(self.context))
        return layers




#class ProjectDbKMLBasinMapLayers(MapLayers):
#    def layers(self):
#        layers = super(ProjectDbKMLBasinMapLayers, self).layers()
#        layers.append(ProjectDbKMLBasinMapLayer(self.context))
#        return layers


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
            });}""" % (
            self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", ""),
            context_url)


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
            });}""" % (u"Maps of: " +
            self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", ""),
            context_url)


class ProjectKMLCountryMapLayer(MapLayer):

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return """
        function() { return new OpenLayers.Layer.GML('%s', '%s@@projectcountry_view.kml',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              visibility: false,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (u'Partnering countries', context_url)

class ProjectBasinMapLayer(MapLayer):

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return """
        function() { return new OpenLayers.Layer.GML('%s', '%s@@projectbasin_view.kml',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              visibility: true,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % (u'Basin', context_url)



class ProjectKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(ProjectKMLMapLayers, self).layers()
        layers.append(ProjectKMLMapLayer(self.context))
        layers.append(ProjectInnerKMLMapLayer(self.context))
        if self.context.getCountry():
            layers.append(ProjectKMLCountryMapLayer(self.context))
        if self.context.getBasin():
            layers.append(ProjectBasinMapLayer(self.context))
        path = '/'.join(self.context.getPhysicalPath())
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        for brain in portal_catalog(path=path, Subject='map-layer',
            portal_type='File', review_state="published"):
            object = brain.getObject()
            if object.content_type == 'application/vnd.google-earth.kml+xml':
                layers.append(KMLFileMapLayer(self.context,object))
        return layers

