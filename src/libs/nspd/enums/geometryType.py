from enum import Enum

class GeometryType(Enum):
    FeatureCollection = 'FeatureCollection'
    Feature = 'Feature'
    Point = 'Point'
    LineString = 'LineString'
    Polygon = 'Polygon'
    MultiPoint = 'MultiPoint'
    MultiLineString = 'MultiLineString'
    MultiPolygon = 'MultiPolygon'
    GeometryCollection = 'GeometryCollection'
