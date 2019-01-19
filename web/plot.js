eel.expose(redraw)
function redraw() {
     var groundlvl;
     $.getJSON("res/input.json", function(result) {
         groundlvl = result.simulation.ground_level;
         });

    Plotly.d3.csv('out/output.csv', function (err, rows) {
        function unpack(rows, key) {
            return rows.map(function (row) {
                return row[key];
            });
        }

        var x = unpack(rows, 'x');
        var z = unpack(rows, 'y');
        var y = unpack(rows, 'z');

        var c = unpack(rows, 'color');

        var xt = unpack(rows, 'xt');
        var zt = unpack(rows, 'yt');
        var yt = unpack(rows, 'zt');

        var ct = unpack(rows, 'color');

        var size = unpack(rows, 'colort');

        var maxt = 0;

        for(var temp in x)
        {
            if(x[temp] !== 'MISS' || x[temp] !== 'HIT')
            {
                buff = parseFloat(x[temp]);
                //console.log("dupa");
                if (Math.abs(buff) > maxt) {
                    //console.log(Math.abs(buff));
                    maxt = Math.abs(buff);
                }
            }
        }

        for(var temp in y)
        {
            if(y[temp] !== 'MISS' || y[temp] !== 'HIT')
            {
                buff = parseFloat(y[temp]);
                //console.log("dupa");
                if (Math.abs(buff) > maxt) {
                    //console.log(Math.abs(buff));
                    maxt = Math.abs(buff);
                }
            }
        }

        for(var temp in z)
        {
            if(z[temp] !== 'MISS' || z[temp] !== 'HIT')
            {
                buff = parseFloat(z[temp]);
                //console.log("dupa");
                if (Math.abs(buff) > maxt) {
                    //console.log(Math.abs(buff));
                    maxt = Math.abs(buff);
                }
            }
        }


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
            },
            name: "rocket"
        };

        var trace1 = {
            type: 'scatter3d',
            mode: 'lines',
            x: xt,
            y: yt,
            z: zt,
            opacity: 1,
            line: {
                width: 15,
                color: 200,
                colorscale: "Greens",
                reversescale: false
            },
            name: "targets"
        };


        var frames = [];
        for (i = 0; i < x.length; i++) {
            frames.push(
                {
                    name: i,
                    data: [trace0, trace1[i]]
                }
            );
        }

        var sliderSteps = [];
        for (i = 1; i < x.length; i++) {
            sliderSteps.push({
                method: 'animate',
                label: i,
                args: [i, {
                    mode: 'immediate',
                    transition: {duration: 100},
                    frame: {duration: 100, redraw: false},
                }]
            });
        }

        var layout = {
            height: 640,
            scene: {
                xaxis: {
                    title: "OX",
                    autorange: false,
                    range: [maxt*-1.0, maxt]
                },
                yaxis: {
                    autorange: false,
                    title: "OZ",
                    range: [maxt*-1.0, maxt]
                },
                zaxis: {
                    title: "OY",
                    autorange: false,
                    range: [maxt*-1.0, maxt]
                }
            }

            /*updatemenus: [{
                x: 0,
                y: 0,
                yanchor: 'top',
                xanchor: 'left',
                showactive: true,
                direction: 'left',
                type: 'buttons',
                pad: {t: 87, r: 10},
                buttons: [{
                    method: 'animate',
                    args: [null, {
                        mode: 'immediate',
                        fromcurrent: true,
                        transition: {duration: 300},
                        frame: {duration: 500, redraw: false}
                    }],
                    label: 'Play'
                }, {
                    method: 'animate',
                    args: [[null], {
                        mode: 'immediate',
                        transition: {duration: 0},
                        frame: {duration: 0, redraw: false}
                    }],
                    label: 'Pause'
                }]
            }],
            // Finally, add the slider and use `pad` to position it
            // nicely next to the buttons.
            sliders: [{
                pad: {l: 130, t: 55},
                currentvalue: {
                    visible: true,
                    prefix: 'Step:',
                    xanchor: 'right',
                    font: {size: 20, color: '#666'}
                },
                steps: sliderSteps
            }]*/
        };
        const min = (x, y) => x < y ? x : y ;
        const max = (x, y) => x > y ? x : y ;
        alert(x.reduce(max));

        Plotly.react('graph', {
            data: [trace0, trace1/*,trace1*/],
            layout: layout
        })
    })
}
