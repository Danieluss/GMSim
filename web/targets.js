// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "closet";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("closet");
var i;
for (i = 0; i < close.length; i++)
{
    var div = this.parentElement;
    div.style.display = "none";
}



// Add a "checked" symbol when clicking on a list item
var list = document.querySelector('span');
list.addEventListener('click', function(ev) {
  if (ev.target.className === 'closet') {
    eel.remove_target("dupa");
    ev.target.classList.display ="none";
  }
}, false);


// Create a new list item when clicking on the "Add" button
function newElement() {
  var li = document.createElement("li");
  var inputValue = document.getElementById("tnumber").value;
  var radius = document.getElementById("radius");
  var sx = document.getElementById("tsx");
  var sy = document.getElementById("tsy");
  var sz = document.getElementById("tsz");
  var vx = document.getElementById("tvx");
  var vy = document.getElementById("tvy");
  var vz = document.getElementById("tvz");
  var vmax = document.getElementById("tvmax");
  var ax = document.getElementById("tax");
  var ay = document.getElementById("tay");
  var az = document.getElementById("taz");
  var new_target = { new_target: {
          radius: parseFloat(radius.value),
          s: [parseFloat(sx.value), parseFloat(sy.value), parseFloat(sz.value)],
          v: [parseFloat(vx.value), parseFloat(vy.value), parseFloat(vz.value)],
          vmax: parseFloat(vmax.value),
          a: [parseFloat(ax.value), parseFloat(ay.value), parseFloat(az.value)]
      } };
  var tstring = JSON.stringify(new_target);
  console.log(tstring);
  tstring = tstring.replace('new_target',inputValue);
  console.log(tstring);
  new_target = JSON.parse(tstring);
  eel.add_target(inputValue,new_target);

  var t = document.createTextNode(String(inputValue)+" s: ["+String(sx.value)+", "+String(sy.value)+", "+String(sz.value)+"]");
  li.appendChild(t);
  if (inputValue === '') {
    alert("You must write something!");
  } else {
    document.getElementById("myUL").appendChild(li);
  }
  document.getElementById("tnumber").value = "";

  document.getElementById("radius").value = 0;
  document.getElementById("tsx").value = 0;
  document.getElementById("tsy").value = 0;
  document.getElementById("tsz").value = 0;
  document.getElementById("tvx").value = 0;
  document.getElementById("tvy").value = 0;
  document.getElementById("tvz").value = 0;
  document.getElementById("tax").value = 0;
  document.getElementById("tay").value = 0;
  document.getElementById("taz").value = 0;

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "closet";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      div.style.display = "none";
    }
  }
}

window.onload = function ()
{
  //console.log("dupa");
  $.getJSON("res/targets.json", function(result) {
    //console.log(result);
    //console.log(Object.keys(result.targets));
    for(var it in result.targets)
    {
      var li = document.createElement("li");
      if(result.targets.hasOwnProperty(it)) {
        var t = document.createTextNode(it + " s: [" + result.targets[it].s+"]");
        li.appendChild(t);
        document.getElementById("myUL").appendChild(li);
      }
    }
  });
};