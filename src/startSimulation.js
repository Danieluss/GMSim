var btn = document.getElementById("start");

btn.onclick = function startSim(input) {
    $.ajax({
        type: "POST",
        url: "src/simulation.py",
        data: { param: input },
    });
}
