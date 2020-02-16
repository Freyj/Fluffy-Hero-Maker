function displayStats(stats) {
  var x = document.getElementById(stats);
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

function exportCharacter(character, name) {
  var element = document.createElement("a");
  element.setAttribute("href", "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(character, null, 2)));
  element.setAttribute("download", name);

  element.style.display = " none";
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function download(character) {
    exportCharacter(character, "save.json");
}