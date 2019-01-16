var btn = document.getElementById("start");

function startSim(input) {
    $.ajax({
        type: "POST",
        url: "src/simulation.py",
        data: { param: input },
    }).done(function (o) {
        console.log("done");
        document.getElementById("graph").innerHTML;
    })
};

btn.onclick = function() {
    console.log("started");
    startSim();
};
