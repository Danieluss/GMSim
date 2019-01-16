import numpy as np


def square(f):
    return f * f


def rotation_matrix(axis, theta):
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def rotate_by_axis(vector, axis, theta):
    return np.dot(rotation_matrix(axis, theta), vector)


def rotate_towards(src_vector, dst_vector, theta):
    axis = np.cross(src_vector, dst_vector)
    return np.dot(rotation_matrix(axis, theta), src_vector)


def vector_length(vector):
    return np.linalg.norm(vector)


def angle(vector0, vector1):
    dot = np.dot(vector0, vector1) / (vector_length(vector0) * vector_length(vector1))
    if dot < -1:
        dot = -1
    elif dot > 1:
        dot = 1
    return np.arccos(dot)


def distance(point0, point1):
    acc = 0
    for i in range(len(point0)):
        acc += square(point0[i] - point1[i])
    return np.sqrt(acc)


def normalize(vector):
    return vector / vector_length(vector)


def sphere_line_intersection(line_point1, line_point2, sphere_centre, radius):
    # for i in range(len(line_point1)):
    #     if line_point1[i] == line_point2[i]:
    #         return []
    p1 = p2 = None

    a = square(line_point2[0] - line_point1[0]) + square(line_point2[1] - line_point1[1]) + square(
        line_point2[2] - line_point1[2])
    b = 2.0 * ((line_point2[0] - line_point1[0]) * (line_point1[0] - sphere_centre[0]) +
               (line_point2[1] - line_point1[1]) * (line_point1[1] - sphere_centre[1]) +
               (line_point2[2] - line_point1[2]) * (line_point1[2] - sphere_centre[2]))
    c = (square(sphere_centre[0]) + square(sphere_centre[1]) + square(sphere_centre[2]) + square(line_point1[0]) +
         square(line_point1[1]) + square(line_point1[2]) -
         2.0 * (sphere_centre[0] * line_point1[0] + sphere_centre[1] * line_point1[1] + sphere_centre[2] * line_point1[
                2]) - square(radius))

    i = b * b - 4.0 * a * c
    if i < 0.0:
        pass
    elif i == 0.0:
        mu = -b / (2.0 * a)
        p1 = (line_point1[0] + mu * (line_point2[0] - line_point1[0]),
              line_point1[1] + mu * (line_point2[1] - line_point1[1]),
              line_point1[2] + mu * (line_point2[2] - line_point1[2]))
    elif i > 0.0:
        mu = (-b + np.sqrt(i)) / (2.0 * a)
        p1 = (line_point1[0] + mu * (line_point2[0] - line_point1[0]),
              line_point1[1] + mu * (line_point2[1] - line_point1[1]),
              line_point1[2] + mu * (line_point2[2] - line_point1[2]))
        mu = (-b - np.sqrt(i)) / (2.0 * a)
        p2 = (line_point1[0] + mu * (line_point2[0] - line_point1[0]),
              line_point1[1] + mu * (line_point2[1] - line_point1[1]),
              line_point1[2] + mu * (line_point2[2] - line_point1[2]))
    return p1, p2


def line_point_between(line_point, line_point1, line_point2):
    if line_point is None:
        return False
    if line_point1[0] != line_point2[0]:
        ord = line_point1[0], line_point2[0] if line_point1[0] < line_point2[0] else line_point2[0], line_point1[0]
        return line_point[0] >= ord[0] and line_point[0] <= ord[1]
    elif line_point1[1] != line_point2[1]:
        ord = line_point1[1], line_point2[1] if line_point1[1] < line_point2[1] else line_point2[1], line_point1[1]
        return line_point[1] >= ord[0] and line_point[1] <= ord[1]
    elif line_point1[2] != line_point2[2]:
        ord = line_point1[2], line_point2[2] if line_point1[2] < line_point2[2] else line_point2[2], line_point1[2]
        return line_point[2] >= ord[0] and line_point[2] <= ord[1]


def either_between(segment_point0, segment_point1, points):
    for point in points:
        if line_point_between(point, segment_point0, segment_point1):
            return True
    return False


def segment_sphere_intersection(segment_point0, segment_point1, sphere_centre, radius):
    intersections = sphere_line_intersection(segment_point0, segment_point1, sphere_centre, radius)
    return either_between(segment_point0, segment_point1, intersections)


def opposite_vector(vector):
    return vector * (-1)
