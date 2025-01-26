import geopandas as gpd

input_file = "Air Conditioned and Cool Spaces - 4326.shp"
output_file = "singlepoint2.shp"

gdf = gpd.read_file(input_file)

if gdf.crs is None:
    print("CRS not defined. Setting CRS to GCS_WGS_1984 (EPSG:4326)...")
    gdf.set_crs("EPSG:4326", inplace=True)
else:
    print(f"Existing CRS: {gdf.crs}")

if gdf.crs.to_string() != "EPSG:4326":
    print("Transforming CRS to GCS_WGS_1984 (EPSG:4326)...")
    gdf = gdf.to_crs("EPSG:4326")

single_points = []

for idx, row in gdf.iterrows():
    geom = row.geometry
    if geom.geom_type == "MultiPoint":
        for point in geom.geoms:
            new_row = row.copy()
            new_row.geometry = point
            single_points.append(new_row)
    else:
        single_points.append(row)

single_gdf = gpd.GeoDataFrame(single_points, columns=gdf.columns, crs=gdf.crs)

print("Saving the file with CRS GCS_WGS_1984 (EPSG:4326)...")
single_gdf.to_file(output_file, driver="ESRI Shapefile")
print("File saved successfully!")
