var btn = document.getElementById("save");

var timestep = document.getElementById("time-step");
var steerstep = document.getElementById("steer-step");
var savestep = document.getElementById("save-step");
var humidity = document.getElementById("humidity");
var temperature = document.getElementById("temperature");
var pressure = document.getElementById("pressure");
var ground_level = document.getElementById("ground_level");

var windx = document.getElementById("windx");
var windy = document.getElementById("windy");
var windz = document.getElementById("windz");
var counter_velocity = document.getElementById("counter_velocity");

var altitude = document.getElementById("altitude");
var propotional_regulation = document.getElementById("propotional_regulation");
var differential_regulation = document.getElementById("differential_regulation");
var max_thrust_angle = document.getElementById("max_thrust_angle");
var react_angle = document.getElementById("react_angle");
var start_steer = document.getElementById("start_steer");
var start_dive = document.getElementById("start_dive");

var total = document.getElementById("total");
var change = document.getElementById("change");
var fuel = document.getElementById("fuel");

var angle = document.getElementById("angle");
var x = document.getElementById("x");
var y = document.getElementById("y");
var z = document.getElementById("z");

var front = document.getElementById("front");
var side = document.getElementById("side");

var fronts = document.getElementById("fronts");
var sides = document.getElementById("sides");

var f0 = document.getElementById("f0");
var thrustchange = document.getElementById("thrustchange");

btn.onclick = function()
{
    eel.save_config(
        {
            simulation: {
                timestep: timestep.value,
                steerstep: steerstep.value,
                savesteo: savestep.value,
                humidity: humidity.value,
                temperature: temperature.value,
                pressure: pressure.value,
                ground_level: ground_level.value,
                wind: [windx.value, windy.value, windz.value],
                counter_velocity: counter_velocity.value
            },
            rocket: {
                flight_control: {
                    altitude: altitude.value,
                    proportional_regulation: propotional_regulation.value,
                    differential_regulation: differential_regulation.value,
                    max_thrust_angle: max_thrust_angle.value,
                    react_angle: react_angle.value,
                    start_steer: start_steer.value,
                    start_dive: start_dive.value
                },
                mass: {
                    total: total.value,
                    change: change.value,
                    fuel: fuel.value
                },
                direction: {
                    angle: angle.value,
                    xyz: [x.value, y.value, z.value]
                },
                drag_coefficient: {
                    front: front.value,
                    side: side.value
                },
                surface: {
                    front: fronts.value,
                    side: sides.value
                },
                thrust: {
                    f0: f0.value,
                    change: thrustchange.value
                }
            }
        }
    )
}