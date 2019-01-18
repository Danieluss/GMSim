var btn = document.getElementById("save");

var time_step = document.getElementById("time-step");
var steer_step = document.getElementById("steer-step");
var save_step = document.getElementById("save-step");
var humidity = document.getElementById("humidity");
var temperature = document.getElementById("temperature");
var pressure = document.getElementById("pressure");
var ground_level = document.getElementById("ground_level");

var windx = document.getElementById("windx");
var windy = document.getElementById("windy");
var windz = document.getElementById("windz");
var counter_velocity = document.getElementById("counter_velocity");

var altitude = document.getElementById("altitude");
var propotional_regulation = document.getElementById("proportional_regulation");
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

var length = document.getElementById("lengths");
var width = document.getElementById("widths");

var f0 = document.getElementById("f0");
var thrustchange = document.getElementById("thrustchange");

btn.onclick = function()
{
    eel.save_config(
        {
            simulation: {
                time_step: parseFloat(time_step.value),
                steer_step: parseFloat(steer_step.value),
                save_step: parseFloat(save_step.value),
                humidity: parseFloat(humidity.value),
                temperature: parseFloat(temperature.value),
                pressure: parseFloat(pressure.value),
                ground_level: parseFloat(ground_level.value),
                wind: [parseFloat(windx.value), parseFloat(windy.value), parseFloat(windz.value)],
                counter_velocity: counter_velocity.checked
            },
            rocket: {
                flight_control: {
                    altitude: parseFloat(altitude.value),
                    proportional_regulation: parseFloat(propotional_regulation.value),
                    differential_regulation: parseFloat(differential_regulation.value),
                    max_thrust_angle: parseFloat(max_thrust_angle.value),
                    react_angle: parseFloat(react_angle.value),
                    start_steer: parseFloat(start_steer.value),
                    start_dive: parseFloat(start_dive.value)
                },
                mass: {
                    total: parseFloat(total.value),
                    change: parseFloat(change.value),
                    fuel: parseFloat(fuel.value)
                },
                direction: {
                    angle: parseFloat(angle.value),
                    xyz: [parseFloat(x.value), parseFloat(y.value), parseFloat(z.value)]
                },
                drag_coefficient: {
                    front: parseFloat(front.value),
                    side: parseFloat(side.value)
                },
                surface: {
                    length: parseFloat(length.value),
                    width: parseFloat(width.value)
                },
                thrust: {
                    f0: parseFloat(f0.value),
                    change: parseFloat(thrustchange.value)
                }
            }
        }
    )
}