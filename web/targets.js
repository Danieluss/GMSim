// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
    div.style.display = "none";
    eel.remove_target(i);
  }
}

/*
// Add a "checked" symbol when clicking on a list item
var list = document.querySelector('ul');
list.addEventListener('click', function(ev) {
  if (ev.target.tagName === 'LI') {
    ev.target.classList.toggle('checked');
  }
}, false);
*/

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

  eel.add_target({
      target: {
          radius: radius.value,
          sx: sx.value,
          sy: sy.value,
          sz: sz.value,
          vx: vx.value,
          vy: vy.value,
          vz: vz.value,
          vmax: vmax.value,
          ax: ax.value,
          ay: ay.value,
          az: az.value
      }
  });

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
  document.getElementById("tvmax").value = 0;
  document.getElementById("tax").value = 0;
  document.getElementById("tay").value = 0;
  document.getElementById("taz").value = 0;

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      div.style.display = "none";
    }
  }
}