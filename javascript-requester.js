function Get()
{
  let dat = "x";
  fetch("http://localhost:8080/", {
    mode: 'no-cors'
  }).then(Response =>Response.text()).then(data => {console.log(data)});
}
function Get2()
{
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "http://localhost:8080", true);
  xhr.onload = function () {
    console.log(xhr.responseText);
  };
  xhr.send();
}