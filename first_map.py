import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point
from shapely.geometry import Polygon
from geopandas.geoseries import GeoSeries
import matplotlib.pyplot as plt

path = "./StaticData/Clean/torino_it/"

shapes_df = pd.read_csv(path + "shapes.txt", \
                  index_col = 0)

#pl = []
#for shape_id, group in shapes_df.groupby("shape_id"):
#    print shape_id
#    group["geometry"] = \
#        group.apply(lambda row: (row["shape_pt_lon"], row["shape_pt_lat"]), axis=1)
#    pl += [Polygon(list(group["geometry"].values))]
#s = GeoSeries(pl).convex_hull
#s.plot()
#plt.show()

import gmplot

gmap = gmplot.GoogleMapPlotter(45.116177, 7.742615, 16)

gmap.scatter(shapes_df["shape_pt_lat"][shapes_df.shape_id == 1640],\
             shapes_df["shape_pt_lon"][shapes_df.shape_id == 1640],\
             '#3B0B39', marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")
