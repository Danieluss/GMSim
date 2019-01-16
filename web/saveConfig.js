var btn = document.getElementById("save");

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

/*
var data = {
    simulation : {
        time-step : 0.010,
        steer-step : 1,
        save-step : 15,
        humidity : 0.6,
        temperature : 293,
        pressure : 101325,
        wind : [0, 0, 1],
        counter_velocity : true
    },

    rocket : {
        flight_control : {
            altitude : null,
            proportional_regulation : 1,
            differential_regulation : 1,
            max_thrust_angle : 0.10,
            react_angle : 0.01,
            start_steer : 1,
            start_dive : 0
        },
        mass : {
            total : 1,
            change : -0.001,
            fuel : 0.5
        },
        direction : {
            angle: null,
            xyz : [ 0.0, 1.0, 0.0 ]
        },
        drag_coefficient : {
            front : 0.05,
            side : 0.15},
        surface : {
            side : 1.0,
            front : 0.1
        },
        thrust : {
            f0 : 100,
            change : 1
        }
    }
};

btn.onclick = function()
{
    console.log("Reeeee");
    download(JSON.stringify(data), 'res/input.json', 'text/plain');
    console.log("Raaaaaa");
};*/