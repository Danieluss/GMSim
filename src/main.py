import numpy as np
import json
from collections import namedtuple
import scipy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint

G = 6.67408e-11
R_e = 6.371e6
M_e = 5.972e24
g = 9.80665
M_d = 0.028964
M_v = 0.018016
R_g = 8.314
L = 0.0065


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
    for i in range(len(line_point1)):
        if line_point1[i] == line_point2[i]:
            return []
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
    ord = line_point1[0], line_point2[0] if line_point1[0] < line_point2[0] else line_point2[0], line_point1[0]
    return line_point[0] >= ord[0] and line_point[0] <= ord[1]


def either_between(segment_point0, segment_point1, points):
    for point in points:
        if line_point_between(point, segment_point0, segment_point1):
            return True
    return False


def segment_sphere_intersection(segment_point0, segment_point1, sphere_centre, radius):
    intersections = sphere_line_intersection(segment_point0, segment_point1, sphere_centre, radius)
    return either_between(segment_point0, segment_point1, intersections)


class SimplePhysicsObject:
    def __init__(self):
        self.acceleration = np.asarray([0, 0, 0])
        self.velocity = np.asarray([0, 0, 0])
        self.max_velocity = None
        self.position = np.asarray([0, 0, 0])

    def update(self, time):
        if self.max_velocity != None:
            if self.max_velocity <= self.velocity + self.acceleration * time:
                self.acceleration = (self.max_velocity - self.velocity) / time
        self.position = self.position + self.velocity * time + self.acceleration * square(time) * 0.5
        self.velocity = self.velocity + self.acceleration * time


def opposite_vector(vector):
    return vector * (-1)


def pressure_falloff(pressure, height, temperature, moll_mass):
    return pressure * (1 - (L * height) / temperature) ** ((g * moll_mass) / (R_g * L))


def saturation_water_pressure(temperature):
    T_C = temperature - 273.15
    return 0.61078 * np.power(10, (7.5 * T_C) / (T_C + 237.3)) * 100.0


def get_air_density(humidity, temperature, height, air_pressure):
    T = temperature - L * height
    p_air = pressure_falloff(air_pressure, height, temperature, M_d)
    T_C = temperature - 273.15
    p_water0 = saturation_water_pressure(temperature) * humidity
    p_water = pressure_falloff(p_water0, height, temperature, M_v)
    ro = (p_air * M_d + p_water * M_v) / (T * R_g)
    return ro


class Rocket(SimplePhysicsObject):
    def __init__(self):
        super().__init__()
        self.thrust = None
        self.thrust_current = None
        self.thrust_change = 0
        self.thrust_direction = None
        self.humidity = None
        self.temperature = None
        self.pressure = None
        self.mass = 0
        self.fuel_mass = 0
        self.direction = np.asarray([0, 1, 0])
        self.current_mass = 0
        self.mass_change = 0
        self.drag_coefficient = 0.10
        self.side_surface = 1
        self.front_surface = 0.1
        self.force = None
        self.target = None
        self.inertia = None
        self.torque = None
        self.proportional_regulation = 1
        self.differential_regulation = 0
        self.wind_force = np.array([0, 0, 0])
        self.length = 2
        self.start_steer_time = 0
        self.react_angle = np.pi * 2 / 180
        self.flight_altitude = 0
        self.start_fly_down_distance = np.inf
        self.rotational_velocity = 0
        self.rotational_acceleration = 0
        self.previous_target_angle = 0

    def init(self):
        self.inertia = square(self.length) / 12 * self.current_mass

    def torque_drag(self):
        if vector_length(self.torque) == 0:
            return 0
        return opposite_vector(self.torque) / vector_length(self.torque) * \
               0.5 * (vector_length(self.rotational_velocity) ** 2) * \
               ((self.length / 2) ** 2) * \
               self.drag_coefficient * \
               get_air_density(self.humidity, self.temperature, self.position[1], self.pressure)

    def rotational_update(self, time):
        alpha = angle(self.thrust_direction, self.direction)
        if alpha > np.pi / 2:
            self.thrust_direction = rotate_towards(self.thrust_direction, self.direction, alpha - (np.pi / 2))
        self.torque = (-1) * np.cross(self.direction * self.length / 2, self.thrust_current * self.thrust_direction)
        self.torque = self.torque + self.torque_drag()
        self.rotational_acceleration = self.torque / self.inertia
        self.rotational_velocity = time * self.rotational_acceleration
        theta = vector_length(self.rotational_acceleration) * square(time) / 2 + vector_length(
            self.rotational_velocity) * time
        if vector_length(self.torque != 0):
            self.direction = rotate_by_axis(self.direction, self.torque, theta)
            p.direction = p.direction / vector_length(p.direction)

    def translational_update(self, time):
        self.force = self.force_function(time)
        self.acceleration = (self.force - (self.mass_change * time) * self.velocity) / self.current_mass
        self.current_mass += self.mass_change * time
        if self.current_mass < self.mass - self.fuel_mass:
            self.current_mass = self.mass - self.fuel_mass
        super().update(time)

    def update(self, time):
        self.rotational_update(time)
        self.translational_update(time)
        # self.thrust_direction = self.direction.copy()

    def get_surface(self):
        alpha = angle(self.direction, self.velocity)
        return self.front_surface * abs(np.cos(alpha)) + abs(np.sin(alpha)) * self.side_surface

    def gravity_force(self):
        return np.asarray([0, -G * M_e * self.current_mass / square(R_e + self.position[1]), 0])

    def translational_thrust_force(self):
        return np.cos(angle(self.thrust_direction, self.direction)) * self.thrust_current * self.direction

    def drag_force(self):
        vel_length = vector_length(self.velocity);
        if vel_length != 0:
            return opposite_vector(self.velocity) / vel_length * \
                   (0.5 *
                    vel_length ** 2 *
                    self.drag_coefficient *
                    self.get_surface() *
                    get_air_density(
                        self.humidity,
                        self.temperature,
                        self.position[1],
                        self.pressure))
        else:
            return np.asarray([0, 0, 0])

    def force_function(self, time):
        acc = np.asarray([0, 0, 0])
        acc = acc + self.drag_force() + \
              self.translational_thrust_force() + \
              self.gravity_force() + \
              self.wind_force
        self.thrust_current = self.thrust * (
                1 - ((self.mass - self.current_mass) / self.fuel_mass) * self.thrust_change)
        return acc

    def steer(self, global_time):
        if self.target != None and self.start_steer_time < global_time:
            distance_vector = self.target.position - self.position
            if vector_length(distance_vector) > self.start_fly_down_distance and self.flight_altitude is not None:
                distance_vector = np.asarray([self.target.position[0], self.flight_altitude, self.target.position[2]]) - self.position
            alpha = angle(distance_vector, self.direction)
            if alpha > self.react_angle:
                self.thrust_direction = rotate_towards(self.direction, distance_vector,
                                                       - ( alpha * self.proportional_regulation +
                                                           (alpha - self.previous_target_angle) * self.differential_regulation ) )
                self.thrust_direction = self.thrust_direction / vector_length(self.thrust_direction)
            else:
                self.thrust_direction = self.direction
            self.previous_target_angle = alpha

    def toJSON(self): #goes crazy with numpy
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

if __name__ == "__main__":
    json_data = open("input.json").read()
    data = json.loads(json_data)
    with open("output.txt") as output:
        p = Rocket()
        rd = data['rocket']
        rdm = rd['mass']
        p.mass = rdm['total']
        p.current_mass = p.mass
        p.mass_change = rdm['change']
        p.fuel_mass = rdm['fuel']
        p.drag_coefficient = rd['drag_coefficient']
        if rd['direction']['angle'] == None:
            p.direction = np.asarray(rd['direction']['xyz'])
        else:
            vec = np.asarray([1.0, 0.0, 0.0])
            p.direction = rotate_towards(vec, [0.0, 1.0, 0.0], rd['direction']['angle'])
        p.start_position = np.asarray([0, 0, 0])
        rds = rd['surface']
        p.side_surface = rds['side']
        p.front_surface = rds['front']
        p.thrust_direction = p.direction.copy()
        rdt = rd['thrust']
        p.thrust = rdt['f0']
        p.thrust_current = p.thrust
        p.thrust_change = rdt['change']
        sdt = data['simulation']
        delta_time = sdt['time-step']
        steer_step = sdt['steer-step']
        save_step = sdt['save-step']
        p.humidity = sdt['humidity']
        p.temperature = sdt['temperature']
        p.pressure = sdt['pressure']
        rdf = rd['flight']
        p.start_steer_time = 5
        p.flight_altitude = rd['altitude']
        p.start_fly_down_distance = 500
        p.wind_force = np.asarray([0, 0, 1])
        p.init()
        p.target = SimplePhysicsObject()
        p.target.position = np.asarray([1000, 100, 100])
        p.target.velocity[0] = 10
        p.differential_regulation = 1
        p.proportional_regulation = 1
        p.start_fly_down_distance = np.inf

        global_time = 0



        pos = p.position.copy()
        while not segment_sphere_intersection(pos, p.position, p.target.position, 10) and distance(p.start_position, p.position) < distance(p.start_position, p.target.position):
            p.update(delta_time)
            p.target.update(delta_time)
            global_time += delta_time
            p.steer(global_time)
            pos = p.position.copy()
            print("p", p.position)
        print("ep", p.target.position)


