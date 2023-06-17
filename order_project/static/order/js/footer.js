document.addEventListener("DOMContentLoaded",()=>{
  stop_loading();
})

function start_loading(){
  document.getElementById("loading_div").style.display = "";
}

function stop_loading(){
  document.getElementById("loading_div").style.display = "none";
}