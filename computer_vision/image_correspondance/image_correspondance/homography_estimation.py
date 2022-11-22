
"""References: Learning OpenCV 4 Computer vision with Python 3"""

import numpy as np
import cv2 as cv


def compute_homography(pairs):
    A = []
    for x1, y1, x2, y2 in pairs:
        A.append([x1, y1, 1, 0, 0, 0, -x2 * x1, -x2 * y1, -x2])
        A.append([0, 0, 0, x1, y1, 1, -y2 * x1, -y2 * y1, -y2])
    A = np.array(A)

    U, S, V = np.linalg.svd(A)

    H = np.reshape(V[-1], (3, 3))

    H = (1 / H.item(8)) * H
    return H


def calculate_geometric_distance(pair, h):
    p1 = np.array([pair[0], pair[1], 1])
    p2 = np.array([pair[2], pair[3], 1])

    p2_estimate = np.dot(h, np.transpose(p1))
    p2_estimate = (1 / p2_estimate[2]) * p2_estimate

    return np.linalg.norm(np.transpose(p2) - p2_estimate)


def random_sample_consensus(point_map, threshold, iters):
    """RANSAC"""
    best_inliers = set()
    homography = None

    for _ in range(iters):
        pairs = [
            point_map[i] for i in np.random.choice(len(point_map), 4)
        ]  # According to literature 10 is better

        H = compute_homography(pairs)

        inliers = {
            (c[0], c[1], c[2], c[3])
            for c in point_map
            if calculate_geometric_distance(c, H) < 500
        }

        if len(inliers) > len(bestInliers):
            bestInliers = inliers
            homography = H
            if len(bestInliers) > (len(point_map) * threshold):
                break
    return homography, best_inliers


def create_point_map(img_1, img_2):
    sift = cv.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img_1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img_2, None)

    bf_matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=True)  # cv.NORM_L2
    matches = bf_matcher.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)

    img_matches = cv.drawMatches(
        img_1, keypoints_1, img_2, keypoints_2, matches[:25], img_2
    )

    img_matches = cv.resize(img_matches, (1200, 1080))

    cv.imwrite("data/matches.png", img_matches)

    _point_map = []
    for match in matches:
        point = [
            keypoints_1[match.queryIdx].pt[0],
            keypoints_1[match.queryIdx].pt[1],
            keypoints_2[match.trainIdx].pt[0],
            keypoints_2[match.trainIdx].pt[1],
        ]
        _point_map.append(point)
    point_map = np.array(_point_map)
    return point_map


def compute_image_correspondance(img_1, img_2):
    point_map = create_point_map(img_1, img_2)
    homography, inliers = random_sample_consensus(point_map, 0.7, 1000)

