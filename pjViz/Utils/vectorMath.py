__author__ = 'twoods0129'
import math, pjViz.Visual.node
import operator as op

#Normalizes a 2D vector
def normalize(direction):
    magnitude = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))
    if magnitude == 0:
        return direction
    else:
        return map(lambda x: x / magnitude, direction)


def magnitude(vec):
    return math.fabs(math.sqrt(math.pow(vec[0], 2) + math.pow(vec[1], 2)))

#Returns the angle between 2 vectors
def angle(vector1, vector2):
    return math.acos(sum(map(op.mul, vector1, vector2)))

def add_vectors(vector1, vector2):
    return map(op.add, vector1, vector2)

def scale(vector, scale_factor):
    return map(lambda x: x * scale_factor, vector)

def mult(vector, scalar):
    return map(lambda x: x * scalar, vector)

#Returns a vector pointing from v1 -> v2
def get_direction(v1, v2):
        return map(op.sub, v1, v2)

def dist(v1, v2):
    return magnitude(get_direction(v1, v2))

def perpendicular(v1, v2, weight=1.0):
    dir = get_direction(v1, v2)
    return (-dir[1] * weight, dir[0] * weight)

def midpoint(v1, v2):
    dir = get_direction(v1, v2)
    half_dist = magnitude(dir) / 2
    dir = normalize(dir)
    return (v1[0] - (half_dist * dir[0]), v1[1] - (half_dist * dir[1]))



