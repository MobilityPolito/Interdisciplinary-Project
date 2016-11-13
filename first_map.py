import pandas as pd
import geopandas
import geopandas.tools
from shapely.geometry import Point

cleandata_path = "./CleanData/"

shapes_df = pd.read_csv(cleandata_path + "torino_it/" + "shapes.txt", \
                  index_col = 0)

shapes_df["geometry"] = \
shapes_df.apply(lambda row: Point(row["shape_pt_lon"], row["shape_pt_lat"]), axis=1)
shapes = geopandas.GeoDataFrame(shapes_df, geometry="geometry")
shapes.crs = {"init": "epsg:4326"}

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
shapes.plot(ax=ax, color="#cc0000")
plt.show()
