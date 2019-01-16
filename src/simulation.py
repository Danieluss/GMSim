from sim_physics import *
import json


def write_record(rocket, output):
    output.write(str(rocket.position[0])+","+str(rocket.position[1])+","+str(rocket.position[2]) + "," + "0")
    output.write("\n")


if __name__ == "__main__":
    json_data = open("../web/res/input.json").read()
    data = json.loads(json_data)
    with open("../web/out/output.csv", "w+") as output:
        output.write("x,y,z,color\n")
        rocket = Rocket()
        rd = data['rocket']
        rdm = rd['mass']
        rocket.mass = rdm['total']
        rocket.current_mass = rocket.mass
        rocket.mass_change = rdm['change']
        rocket.fuel_mass = rdm['fuel']
        rocket.drag_coefficient_front = rd['drag_coefficient']['front']
        rocket.drag_coefficient_side = rd['drag_coefficient']['side']
        if rd['direction']['angle'] == None:
            rocket.direction = np.asarray(rd['direction']['xyz'])
            normalize(rocket.direction)
        else:
            vec = np.asarray([1.0, 0.0, 0.0])
            rocket.direction = rotate_towards(vec, [0.0, 1.0, 0.0], rd['direction']['angle'])
        rocket.start_position = np.asarray([0, 0, 0])
        rds = rd['surface']
        rocket.side_surface = rds['side']
        rocket.front_surface = rds['front']
        rocket.thrust_direction = rocket.direction.copy()
        rdt = rd['thrust']
        rocket.thrust = rdt['f0']
        rocket.thrust_current = rocket.thrust
        rocket.thrust_change = rdt['change']
        sdt = data['simulation']
        counter_velocity = sdt['counter_velocity']
        delta_time = sdt['time-step']
        steer_step = sdt['steer-step']
        save_step = sdt['save-step']
        ground_level = sdt['ground_level']
        ground_hit = False
        rocket.humidity = sdt['humidity']
        rocket.temperature = sdt['temperature']
        rocket.pressure = sdt['pressure']
        rocket.wind_velocity = np.asarray(sdt['wind'])
        rdf = rd['flight_control']
        rocket.react_angle = rdf['react_angle']
        rocket.start_steer_time = rdf['start_steer']
        rocket.flight_altitude = rdf['altitude']
        rocket.dive = rdf['start_dive']
        rocket.proportional_regulation = rdf['proportional_regulation']
        rocket.differential_regulation = rdf['differential_regulation']
        rocket.max_thrust_angle = rdf['max_thrust_angle'] * np.pi

        rocket.init()

        tdt = data['targets']
        targets = []

        for key in sorted(tdt, key=lambda x: int(x)):
            new_target = Target()
            new_target.radius = tdt[key]['radius']
            new_target.position = np.asarray(tdt[key]['s'])
            new_target.velocity = np.asarray(tdt[key]['s.'])
            new_target.acceleration = np.asarray(tdt[key]['s..'])
            new_target.max_velocity = np.asarray(tdt[key]['s.max'])
            targets.append(new_target)

        global_time = 0

        pos = rocket.position.copy()
        for target in targets:
            if ground_hit:
                break
            rocket.target = target
            ticks = 0
            rocket.start_position = rocket.position
            while True:
                if ticks % save_step == 0:
                    write_record(rocket, output)
                pos = rocket.position.copy()
                rocket.update(delta_time)
                for target_ in targets:
                    target_.update(delta_time)
                global_time += delta_time
                if ticks % steer_step == 0:
                    rocket.steer(global_time, counter_velocity)

                write_record(rocket, output)

                if rocket.position[1] < ground_level:
                    output.write("MISS\n")
                    ground_hit = True
                    break
                elif segment_sphere_intersection(pos, rocket.position, rocket.target.position, rocket.target.radius) or distance(rocket.target.position, rocket.position) <= rocket.target.radius:
                    output.write("HIT\n")
                    break
                elif distance(rocket.start_position, rocket.position) > distance(rocket.start_position,
                                                                                 rocket.target.position) + rocket.target.radius:
                    output.write("MISS\n")
                    break
                ticks += 1
