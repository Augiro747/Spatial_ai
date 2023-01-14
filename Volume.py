import math
from functools import reduce

import numpy as np
from matplotlib.path import Path
from scipy.spatial import Delaunay
from scipy.spatial.qhull import QhullError
from scipy.stats import gaussian_kde
from scipy.signal import argrelextrema
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union, transform
from shapely.wkt import loads
import open3d as o3d

INPUT_FILE = "/datasets/project/odm_filterpoints/point_cloud.ply"
SAVE_PATH = "/datasets/project/"


def get_triangles_vertices(triangles, vertices):
    triangles_vertices = []
    for triangle in triangles:
        new_triangles_vertices = [vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]]
        triangles_vertices.append(new_triangles_vertices)
    return np.array(triangles_vertices)

def volume_under_triangle(triangle):
    p1, p2, p3 = triangle
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    return abs((z1+z2+z3)*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3)/6)



if __name__ == "__main__":
    pcd = o3d.io.read_point_cloud(INPUT_FILE)
    axes = o3d.geometry.TriangleMesh.create_coordinate_frame()

    plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=10000)
    [a, b, c, d] = plane_model
    plane_pcd = pcd.select_by_index(inliers)
    plane_pcd.paint_uniform_color([1.0, 0, 0])
    stockpile_pcd = pcd.select_by_index(inliers, invert=True)
    stockpile_pcd.paint_uniform_color([0, 0, 1.0])

    plane_pcd = plane_pcd.translate((0, 0, d / c))
    stockpile_pcd = stockpile_pcd.translate((0, 0, d / c))
    cos_theta = c / math.sqrt(a ** 2 + b ** 2 + c ** 2)
    sin_theta = math.sqrt((a ** 2 + b ** 2) / (a ** 2 + b ** 2 + c ** 2))
    u_1 = b / math.sqrt(a ** 2 + b ** 2)
    u_2 = -a / math.sqrt(a ** 2 + b ** 2)
    rotation_matrix = np.array([[cos_theta + u_1 ** 2 * (1 - cos_theta), u_1 * u_2 * (1 - cos_theta), u_2 * sin_theta],
                                [u_1 * u_2 * (1 - cos_theta), cos_theta + u_2 ** 2 * (1 - cos_theta), -u_1 * sin_theta],
                                [-u_2 * sin_theta, u_1 * sin_theta, cos_theta]])
    plane_pcd.rotate(rotation_matrix)
    stockpile_pcd.rotate(rotation_matrix)

    cl, ind = stockpile_pcd.remove_statistical_outlier(nb_neighbors=500, std_ratio=0.1)
    stockpile_pcd = stockpile_pcd.select_by_index(ind)

    downpdc = stockpile_pcd.voxel_down_sample(voxel_size=0.05)
    xyz = np.asarray(downpdc.points)
    xy_catalog = []
    for point in xyz:
        xy_catalog.append([point[0], point[1]])
    tri = Delaunay(np.array(xy_catalog))

    surface = o3d.geometry.TriangleMesh()
    surface.vertices = o3d.utility.Vector3dVector(xyz)
    surface.triangles = o3d.utility.Vector3iVector(tri.simplices)

    volume = reduce(lambda a, b: a + volume_under_triangle(b),
                    get_triangles_vertices(surface.triangles,
                                           surface.vertices), 0)
    print(f"The volume of the stockpile is: {round(volume, 4)} m3")
    o3d.io.write_point_cloud(SAVE_PATH + "cut_banana.ply", stockpile_pcd)
