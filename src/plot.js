
Plotly.d3.csv('out/output.csv', function(err, rows){
    function unpack(rows, key) {
        return rows.map(function(row)
        { return row[key]; }); }

    var x = unpack(rows , 'x');
    var y = unpack(rows , 'y');
    var z = unpack(rows , 'z');

    var c = unpack(rows , 'color');

    var trace0 = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: x,
        y: y,
        z: z,
        opacity: 1,
        line: {
            width: 6,
            color: c,
            colorscale: "Viridis",
            reversescale: false
        },
        marker: {
            size: 1,
            color: c,
            colorscale: "Reds",
            cmin: -20,
            cmax: 50
        }
    };

    var layout = {
        height: 640,
        xaxis: {
            range: [Math.min(Math.min(x),Math.min(y),Math.min(z)),Math.max(Math.max(x),Math.max(y),Math.max(z))]
        },
        yaxis: {
            range: [Math.min(Math.min(x),Math.min(y),Math.min(z)),Math.max(Math.max(x),Math.max(y),Math.max(z))]
        },
        zaxis:{
            range: [Math.min(Math.min(x),Math.min(y),Math.min(z)),Math.max(Math.max(x),Math.max(y),Math.max(z))]
        }
    };

    Plotly.plot('graph', [trace0], layout);
});

