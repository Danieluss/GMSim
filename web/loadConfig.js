var btn = document.getElementById("load");


function load() {
    var json;
    $.getJSON("res/input.json", function(result){
        //settings = JSON.parse(json);
        //console.log("kek");
        //console.log(result);

        //console.log(document);

        document.getElementById("time-step").value = result.simulation.time_step;
        document.getElementById("steer-step").value = result.simulation.steer_step;
        document.getElementById("save-step").value = result.simulation.save_step;
        document.getElementById("humidity").value = result.simulation.humidity;
        document.getElementById("temperature").value = result.simulation.temperature;
        document.getElementById("pressure").value = result.simulation.pressure;
        document.getElementById("ground_level").value = result.simulation.ground_level;

        document.getElementById("windx").value = result.simulation.wind[0];
        document.getElementById("windy").value = result.simulation.wind[1];
        document.getElementById("windz").value = result.simulation.wind[2];
        document.getElementById("counter_velocity").value = result.simulation.counter_velocity;

        document.getElementById("altitude").value = result.rocket.flight_control.altitude;
        document.getElementById("proportional_regulation").value = result.rocket.flight_control.proportional_regulation;
        document.getElementById("differential_regulation").value = result.rocket.flight_control.differential_regulation;
        document.getElementById("max_thrust_angle").value = result.rocket.flight_control.max_thrust_angle;
        document.getElementById("react_angle").value = result.rocket.flight_control.react_angle;
        document.getElementById("start_steer").value = result.rocket.flight_control.start_steer;
        document.getElementById("start_dive").value = result.rocket.flight_control.start_dive;

        document.getElementById("total").value = result.rocket.mass.total;
        document.getElementById("change").value = result.rocket.mass.change;
        document.getElementById("fuel").value = result.rocket.mass.fuel;

        document.getElementById("angle").value = result.rocket.direction.angle;
        document.getElementById("x").value = result.rocket.direction.xyz[0];
        document.getElementById("y").value = result.rocket.direction.xyz[1];
        document.getElementById("z").value = result.rocket.direction.xyz[2];

        document.getElementById("front").value = result.rocket.drag_coefficient.front;
        document.getElementById("side").value = result.rocket.drag_coefficient.side;

        document.getElementById("lengths").value = result.rocket.surface.length;
        document.getElementById("widths").value = result.rocket.surface.width;

        document.getElementById("f0").value = result.rocket.thrust.f0;
        document.getElementById("thrustchange").value = result.rocket.thrust.change;
    });
}


document.onload = load();
btn.onclick = load();