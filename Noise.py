import copy
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

INPUT_FILE = "/datasets/project/filled.ply"
SAVE_PATH = "/datasets/project/"

def apply_noise(pcd, mu, sigma):
    noisy_pcd = copy.deepcopy(pcd)
    points = np.asarray(noisy_pcd.points)
    points += np.random.normal(mu, sigma, size=points.shape)
    noisy_pcd.points = o3d.utility.Vector3dVector(points)
    return noisy_pcd

if __name__ == "__main__":
    pcd= o3d.io.read_point_cloud(INPUT_FILE)
    height=0.05
    mu, sigma = 0, 0.1  # mean and standard deviation
    source_noisy = apply_noise(pcd, mu, sigma)
    o3d.io.write_point_cloud(SAVE_PATH + "noised.ply", source_noisy)
