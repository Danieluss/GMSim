from sim_physics import *
import json


def write_record(rocket, output, param, delim):
    output.write(str(rocket.position[0]) + "," + str(rocket.position[1]) + "," + str(rocket.position[2]) + "," + str(param))
    output.write(delim)


def run():
    json_data = open("web/res/input.json").read()
    data = json.loads(json_data)
    json_targets = open("web/res/targets.json").read()
    targetin = json.loads(json_targets)
    with open("web/out/output.csv", "w+") as output:
        output.write("x,y,z,color,xt,yt,zt,colort,xm,ym,zm,hit\n")
        #traces.write("x,y,z,color\n")
        #markers.write("x,y,z,size\n")
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
            rocket.direction = rotate_towards(vec, [0.0, 1.0, 0.0], rd['direction']['angle'] * np.pi)
        rocket.start_position = np.asarray([0, 0, 0])
        rds = rd['surface']
        rocket.length = rds['length']
        rocket.width = rds['width']
        rocket.side_surface = rocket.length * rocket.width
        rocket.front_surface = np.pi * (rocket.width / 2) ** 2
        rocket.thrust_direction = rocket.direction.copy()
        rdt = rd['thrust']
        rocket.thrust = rdt['f0']
        rocket.thrust_current = rocket.thrust
        rocket.thrust_change = rdt['change']
        sdt = data['simulation']
        counter_velocity = sdt['counter_velocity']
        delta_time = sdt['time_step']
        steer_step = sdt['steer_step']
        save_step = sdt['save_step']
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

        tdt = targetin['targets']
        targets = []

        for key in sorted(tdt, key=lambda x: int(x)):
            new_target = Target()
            new_target.radius = tdt[key]['radius']
            new_target.position = np.asarray(tdt[key]['s'])
            new_target.velocity = np.asarray(tdt[key]['v'])
            new_target.acceleration = np.asarray(tdt[key]['a'])
            new_target.max_velocity = np.asarray(tdt[key]['vmax'])
            targets.append(new_target)

        global_time = 0

        pos = rocket.position.copy()
        it = 0
        for target in targets:
            if ground_hit:
                break
            rocket.target = target
            ticks = 0
            rocket.start_position = rocket.position
            while True:
                it+=1
                if ticks % save_step == 0:
                    write_record(rocket, output, it*5, ",")
                    write_record(rocket.target, output, it*5, ",")
                    output.write("None,None,None,None\n")
                pos = rocket.position.copy()
                rocket.update(delta_time)
                for target_ in targets:
                    target_.update(delta_time)
                global_time += delta_time
                if ticks % steer_step == 0:
                    rocket.steer(delta_time, global_time, counter_velocity)
                write_record(rocket, output, it*5, ",")
                write_record(rocket.target, output, it*5, ",")
                output.write("None,None,None,None\n")
                if rocket.position[1] < ground_level:
                    output.write("MISS,MISS,MISS,1,None,None,None,None,")
                    write_record(rocket.target, output, "#F01", "\n")
                    ground_hit = True
                    break
                elif segment_sphere_intersection(pos, rocket.position, rocket.target.position,
                                                 rocket.target.radius) or distance(rocket.target.position,
                                                                                   rocket.position) <= rocket.target.radius:
                    output.write("HIT,HIT,HIT,1,None,None,None,None,")
                    write_record(rocket.target, output, "#0F1", "\n")
                    break
                elif distance(rocket.start_position, rocket.position) > distance(rocket.start_position,
                                                                                 rocket.target.position) + rocket.target.radius:
                    output.write("MISS,MISS,MISS,1,None,None,None,None,")
                    write_record(rocket.target, output, "#F01", "\n")
                    break
                ticks += 1

if __name__ == "__main__":
    run()