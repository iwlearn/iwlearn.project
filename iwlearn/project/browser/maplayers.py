#
from Products.CMFCore.utils import getToolByName

from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.file.browser.maplayer import KMLFileMapLayer


class MapLayerBase(MapLayer):

    def __init__(self, context, visible=True):
        self.context = context
        self.visible = str(visible).lower()



class ProjectDbKMLMapLayer(MapLayerBase):
    """
    a layer with the PCU locations of projects.
    """


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectdbpmo_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: false,
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
                            }
                        }),
                    /*eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent();
                                 this.map.zoomToExtent(extent);
                                }
                            },*/
                    visibility: %s,
                    displayInLayerSwitcher: false,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (
            #self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", "&apos;"),
            'Project management offices',
            context_url, self.visible)



class ProjectDbKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(ProjectDbKMLMapLayers, self).layers()
        layers.append(ProjectDbKMLMapLayer(self.context))
        return layers


class ProjectDbKMLBasinMapLayer(MapLayerBase):
    """
    Basins with (and/or without) projects.
    the detail layer comprises all projects and is rendered as polygons,
    the clusterlayer is renders points of the smaller basins in clusters
    """


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
                    visibility: %s,
                    displayInLayerSwitcher: false,
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
                                        fillColor: "#5566ff",
                                        fillOpacity: 0.8,
                                        strokeColor: "#1122ff",
                                        strokeWidth: 2,
                                        strokeOpacity: 0.8,
                                        label:"${count}"
                                    }, {
                                        rules: [
                                            new OpenLayers.Rule({
                                                    context: function(feature) {
                                                        return feature;
                                                    },
                                                    filter: new OpenLayers.Filter({
                                                        evaluate: function(feature) {
                                                            var isvisible = ((
                                                                (feature.cluster[0].geometry.getBounds().getSize().w *feature.cluster[0].geometry.getBounds().getSize().h)
                                                                /
                                                                (feature.layer.getExtent().getSize().w * feature.layer.getExtent().getSize().h)
                                                                ) *10240);

                                                            return (isvisible < 2)
                                                        }
                                                    })
                                                })
                                        ],
                                        context: {
                                            radius: function(feature) {
                                                return Math.min(feature.attributes.count, 7) + 3;
                                            }
                                        }
                                    }),
                        "select": {
                            fillColor: "#8aeeef",
                            strokeColor: "#32a8a9"
                            }
                        }),
                    visibility: %s,
                    displayInLayerSwitcher: false,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (context_url, self.visible ,context_url, self.visible)



class ProjectDbKMLCountryMapLayer(MapLayerBase):
    """
    countries with projects
    """


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectdbcountry_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    displayInLayerSwitcher: false,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Countries', context_url, self.visible)


class ProjectDbKMLNationalResultsMapLayer(MapLayerBase):


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectdbnationalresults_view.kml?getSubRegions:list=National",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    displayInLayerSwitcher: false,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'National Results', context_url, self.visible)



class ProjectDbKMLCountryMapLayers(MapLayers):
    def layers(self):
        layers = super(ProjectDbKMLCountryMapLayers, self).layers()
        layers.append(ProjectDbKMLCountryMapLayer(self.context))
        return layers




class ProjectDbKMLBasinMapLayers(MapLayers):
    def layers(self):
        layers = super(ProjectDbKMLBasinMapLayers, self).layers()
        layers.append(ProjectDbKMLBasinMapLayer(self.context))
        layers.append(ProjectDbKMLCountryMapLayer(self.context))
        return layers


class ProjectDbMapLayers(MapLayers):

    def layers(self):
        layers = super(ProjectDbMapLayers, self).layers()
        layers.append(ProjectDbKMLCountryMapLayer(self.context, False))
        layers.append(ProjectDbKMLBasinMapLayer(self.context, True))
        layers.append(ProjectDbKMLMapLayer(self.context, False))
        return layers


class ProjectDbKMLResultMapLayers(MapLayers):

    def layers(self):
        layers = super(ProjectDbKMLResultMapLayers, self).layers()
        layers.append(ProjectDbKMLNationalResultsMapLayer(self.context, True))
        return layers

########################################################################
# Project profile
########################################################################

class ProjectKMLMapLayer(MapLayerBase):
    """
    PCU Location
    """
    #XXX now appended in ProjectInnerKMLMapLayer


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return """
            function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@kml-document",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true}),
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    eventListeners: { 'loadend': function(event) {
                                 var c_lonlat = this.getDataExtent().getCenterLonLat();
                                 this.map.setCenter(new OpenLayers.LonLat(
                                 c_lonlat.lon, c_lonlat.lat), 5, false, false);
                                }
                            },
                    visibility: %s,
                    displayInLayerSwitcher: false,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (
            self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", ""),
            context_url, self.visible)


class ProjectInnerKMLMapLayer(MapLayerBase):
    """
    Geo annotated content of a project and the project location itself
    """
    #

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectkml_view",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    eventListeners: { 'loadend': function(event) {
                                 var c_lonlat = this.getDataExtent().getCenterLonLat();
                                 this.map.setCenter(new OpenLayers.LonLat(
                                 c_lonlat.lon, c_lonlat.lat), 5, false, false);
                                }
                            },
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" %  (u'Project Locations', context_url, self.visible)


                #(u"Maps of: " +
            #self.context.Title().decode('utf-8', 'ignore').encode('ascii', 'xmlcharrefreplace').replace("'", ""),
            #context_url, self.visible)



class ProjectKMLCountryMapLayer(MapLayerBase):
    """ Projects partnering countries """

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectcountry_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Partnering countries', context_url, self.visible)



class ProjectBasinMapLayer(MapLayerBase):
    """ Basins of a project """

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@projectbasin_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Basin', context_url, self.visible)




class ProjectKMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        #add basemaps
        layers = super(ProjectKMLMapLayers, self).layers()
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

        #check if the project has maplayers before adding this layer
        has_maplayers = False
        for brain in portal_catalog(path=path, review_state="published"):
            try:
                if brain.zgeo_geometry['coordinates']:
                    has_maplayers = True
                    break
                else:
                    continue
            except:
                continue
        if has_maplayers:
            layers.append(ProjectInnerKMLMapLayer(self.context))
        # PCU Location [is a part of ProjectInnerKMLMapLayer]
        # layers.append(ProjectKMLMapLayer(self.context))
        return layers


################################################################
#### Legal Frameworks
################################################################


class LegalFWCountryMapLayer(MapLayerBase):
    """ countries in this treaty"""

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@country_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    eventListeners: { 'loadend': function(event) {
                                    this.map.zoomToExtent(this.getDataExtent());
                                }
                            },
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Countries', context_url, self.visible)



class LegalFWBasinMapLayer(MapLayerBase):
    """ Basins of a project """

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@basin_view.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Basins', context_url, self.visible)

class LegalFWMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        #add basemaps
        layers = super(LegalFWMapLayers, self).layers()
        if self.context.getCountry():
            layers.append(LegalFWCountryMapLayer(self.context))
        if self.context.getBasin():
            layers.append(LegalFWBasinMapLayer(self.context))
        return layers

################################################################
### Legal framework overview maps
################################################################

class LegalFWFolderCountryMapLayer(MapLayerBase):
    """ countries in this treaty"""

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'


        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@country_overview.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    eventListeners: { 'loadend': function(event) {
                                    this.map.zoomToExtent(this.getDataExtent());
                                }
                            },
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Countries', context_url, self.visible)



class LegalFWFolderBasinMapLayer(MapLayerBase):
    """ Basins of a project """

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        return u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@basin_overview.kml",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: %s,
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (u'Basins', context_url, self.visible)

class LegalFWFolderMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        #add basemaps
        layers = super(LegalFWFolderMapLayers, self).layers()
        layers.append(LegalFWFolderCountryMapLayer(self.context))
        layers.append(LegalFWFolderBasinMapLayer(self.context))
        return layers
