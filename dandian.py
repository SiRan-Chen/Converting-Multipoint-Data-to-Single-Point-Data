import geopandas as gpd

# 输入文件路径（替换为你的文件路径）
input_file = "Air Conditioned and Cool Spaces - 4326.shp"
output_file = "singlepoint2.shp"

# 1. 读取数据
gdf = gpd.read_file(input_file)

# 2. 检查 CRS 是否存在
if gdf.crs is None:
    # 如果 CRS 未定义，则设置为 GCS_WGS_1984 (EPSG:4326)
    print("CRS not defined. Setting CRS to GCS_WGS_1984 (EPSG:4326)...")
    gdf.set_crs("EPSG:4326", inplace=True)
else:
    # 如果 CRS 已定义，打印其信息
    print(f"Existing CRS: {gdf.crs}")

# 3. 确认当前 CRS 是否为 EPSG:4326，否则转换
if gdf.crs.to_string() != "EPSG:4326":
    print("Transforming CRS to GCS_WGS_1984 (EPSG:4326)...")
    gdf = gdf.to_crs("EPSG:4326")

# 4. 将多点转换为单点
single_points = []

for idx, row in gdf.iterrows():
    geom = row.geometry
    # 检查是否为多点
    if geom.geom_type == "MultiPoint":
        # 将每个点单独提取
        for point in geom.geoms:
            new_row = row.copy()
            new_row.geometry = point
            single_points.append(new_row)
    else:
        # 如果是单点，直接添加
        single_points.append(row)

# 将提取的点转换为新的 GeoDataFrame
single_gdf = gpd.GeoDataFrame(single_points, columns=gdf.columns, crs=gdf.crs)

# 5. 保存数据到输出文件
print("Saving the file with CRS GCS_WGS_1984 (EPSG:4326)...")
single_gdf.to_file(output_file, driver="ESRI Shapefile")
print("File saved successfully!")
