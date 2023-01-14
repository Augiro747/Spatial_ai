import numpy as np
import open3d as o3d

INPUT_FILE = "/datasets/project/odm_meshing/odm_mesh.ply"
MAX_RADIUS = 30.0
OUTPUT_FILE = "/datasets/project/"

if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud(INPUT_FILE)
    print("Before coarsening",pcd)
    x=5
    x=int(input("Input coarsening level:"))
    pcd2=o3d.geometry.PointCloud.voxel_down_sample(pcd,float(x/1000))
    print("After coarsening",pcd2)
    o3d.io.write_point_cloud(OUTPUT_FILE+"Coarsed_version.ply",pcd2)

