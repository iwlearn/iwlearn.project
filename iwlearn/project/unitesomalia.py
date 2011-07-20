from shapely.geometry import Point, LineString, Polygon
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon

from shapely.wkt import loads


somalia = loads('POLYGON((49.729 11.579,50.259 11.68,50.732 12.022,51.111 12.025,51.134 11.748,51.042 11.167,51.045 10.641,50.834 10.28,50.552 9.199,50.071 8.082,49.453 6.805,48.595 5.339,47.741 4.219,46.565 2.855,45.564 2.046,44.068 1.053,43.136 0.292,42.042 -0.919,41.811 -1.446,41.585 -1.683,40.993 -0.858,40.981 2.785,41.855 3.919,42.129 4.234,42.77 4.253,43.661 4.958,44.964 5.002,47.789 8.003,48.487 8.838,48.938 9.452,48.938 9.974,48.938 10.982,48.942 11.394,48.948 11.411,49.268 11.43,49.729 11.579))')
somaliland = loads('POLYGON((48.939 11.258,48.938 10.982,48.938 10.714,48.938 10.433,48.938 9.974,48.938 9.808,48.938 9.564,48.938 9.452,48.794 9.233,48.617 8.965,48.429 8.68,48.273 8.443,48.127 8.222,47.978 7.997,47.638 7.997,47.306 7.997,46.978 7.997,46.92 8.026,46.645 8.118,46.296 8.235,45.863 8.38,45.555 8.483,45.227 8.591,44.894 8.7,44.632 8.786,44.306 8.893,44.023 8.986,43.984 9.009,43.827 9.151,43.621 9.337,43.581 9.341,43.483 9.379,43.394 9.48,43.303 9.609,43.218 9.77,43.182 9.88,43.069 9.926,43.015 10.013,42.912 10.141,42.842 10.203,42.816 10.257,42.784 10.37,42.725 10.492,42.669 10.568,42.656 10.6,42.66 10.621,42.763 10.787,42.81 10.846,42.863 10.903,42.906 10.96,42.923 10.999,43.049 11.194,43.159 11.366,43.246 11.5,43.441 11.346,43.631 11.035,43.853 10.784,44.158 10.551,44.279 10.472,44.386 10.43,44.943 10.437,45.338 10.65,45.696 10.804,45.817 10.836,46.025 10.794,46.254 10.781,46.46 10.734,46.565 10.746,46.973 10.925,47.23 11.1,47.405 11.174,47.474 11.175,47.712 11.112,48.019 11.139,48.439 11.29,48.573 11.32,48.674 11.323,48.903 11.255,48.939 11.258))')

so = MultiPolygon([somalia, somaliland]).simplify(0.01)
print so.wkt