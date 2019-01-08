from sim_math import *

G = 6.67408e-11
R_e = 6.371e6
M_e = 5.972e24
g = 9.80665
M_d = 0.028964
M_v = 0.018016
R_g = 8.314
L = 0.0065


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


class SimplePhysicsObject:
    def __init__(self):
        self.acceleration = np.asarray([0, 0, 0])
        self.velocity = np.asarray([0, 0, 0])
        self.max_velocity = None
        self.position = np.asarray([0, 0, 0])

    def update(self, time):
        self.position = self.position + self.velocity * time + self.acceleration * square(time) * 0.5
        self.velocity = self.velocity + self.acceleration * time
        # if self.max_velocity is not None:
        #     if self.max_velocity <= vector_length(self.velocity):
        #         self.velocity = self.velocity * (self.max_velocity / vector_length(self.velocity))


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
        self.drag_coefficient_front = 0.10
        self.drag_coefficient_side = 0.10
        self.side_surface = 1
        self.front_surface = 0.1
        self.force = None
        self.target = None
        self.inertia = None
        self.torque = None
        self.proportional_regulation = 1
        self.differential_regulation = 0
        self.max_thrust_angle = 0.5
        self.wind_velocity = np.array([0, 0, 0])
        self.length = 2
        self.start_steer_time = 0
        self.react_angle = np.pi * 2 / 180
        self.flight_altitude = 0
        self.dive = np.inf
        self.rotational_velocity = 0
        self.rotational_acceleration = 0
        self.previous_dis_dir_angle = 0

    def init(self):
        self.inertia = square(self.length) / 12 * self.current_mass

    def torque_drag(self):
        if vector_length(self.torque) == 0:
            return 0
        return opposite_vector(self.torque) / vector_length(self.torque) * \
               0.5 * (vector_length(self.rotational_velocity) ** 2) * \
               ((self.length / 2) ** 2) * \
               self.drag_coefficient_side * \
               self.side_surface * \
               get_air_density(self.humidity, self.temperature, self.position[1], self.pressure) / 3

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
            self.direction = self.direction / vector_length(self.direction)

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

    def get_surface(self, alpha):
        return self.front_surface * abs(np.cos(alpha)) + abs(np.sin(alpha)) * self.side_surface

    def gravity_force(self):
        return np.asarray([0, -G * M_e * self.current_mass / square(R_e + self.position[1]), 0])

    def translational_thrust_force(self):
        return np.cos(angle(self.thrust_direction, self.direction)) * self.thrust_current * self.direction

    def wind_pressure(self):
        if vector_length(self.wind_velocity) == 0:
            return np.asarray([0, 0, 0])
        return 0.5 * normalize(self.wind_velocity) * get_air_density(self.humidity, self.temperature, self.position[1],
                                                                     self.pressure) * vector_length(
            self.wind_velocity) ** 2 * self.get_surface(angle(self.direction, self.wind_velocity))

    def get_drag_coefficient(self, alpha):
        return abs(np.sin(alpha)) * self.drag_coefficient_side + abs(np.cos(alpha)) * self.drag_coefficient_front

    def drag_force(self):
        vel_length = vector_length(self.velocity);
        if vel_length != 0:
            alpha = angle(self.direction, self.velocity)
            return opposite_vector(self.velocity) / vel_length * \
                   (0.5 *
                    vel_length ** 2 *
                    self.drag_coefficient_front *
                    # self.get_drag_coefficient(alpha) *
                    self.get_surface(alpha) *
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
              self.wind_pressure()
        self.thrust_current = self.thrust * (
                1 - ((self.mass - self.current_mass) / self.fuel_mass) * self.thrust_change)
        return acc

    def steer(self, global_time, counter_velocity):
        if self.target != None and self.start_steer_time < global_time:
            distance_vector = self.target.position - self.position
            if self.dive is not None and vector_length(
                    distance_vector) > self.dive and self.flight_altitude is not None:
                distance_vector = np.asarray(
                    [self.target.position[0], self.target.position[1] + self.flight_altitude,
                     self.target.position[2]]) - self.position

            if counter_velocity:
                alpha_dis_vel = angle(distance_vector, self.velocity) * (1)
                if alpha_dis_vel > self.max_thrust_angle:
                    alpha_dis_vel = self.max_thrust_angle
                dir_steer = rotate_towards(normalize(distance_vector), self.velocity, - alpha_dis_vel)
                alpha_steer = angle(dir_steer, self.direction)
            else:
                alpha_steer = angle(distance_vector, self.direction)
                dir_steer = distance_vector

            if alpha_steer > self.react_angle:
                rotate_angle = (alpha_steer * self.proportional_regulation + (
                        alpha_steer - self.previous_dis_dir_angle) * self.differential_regulation)
                if rotate_angle > self.max_thrust_angle:
                    rotate_angle = self.max_thrust_angle
                self.thrust_direction = rotate_towards(self.direction, dir_steer,
                                                       -rotate_angle)
                self.thrust_direction = self.thrust_direction / vector_length(self.thrust_direction)
            else:
                self.thrust_direction = self.direction
            self.previous_dis_dir_angle = alpha_steer

    # def toJSON(self):  # goes crazy with numpy
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


class Target(SimplePhysicsObject):
    def __init__(self):
        super().__init__()
        self.radius = 0