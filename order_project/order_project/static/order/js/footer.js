document.addEventListener("DOMContentLoaded",()=>{
  stop_loading();
})

function start_loading(){
  document.getElementById("loading_div").style.display = "";
}

function stop_loading(){
  document.getElementById("loading_div").style.display = "none";
}

function add_to_cart(eve,id,qtn){
  let url = "/api/cart/"
  let data = {
    "product_added": [
          {
              "product": {
                  "id": parseInt(id)
              },
              "quantity": parseInt(qtn)
          }
      ]
  }
  start_loading();
  $.ajax({
    url:url,
    method:"POST",
    data:JSON.stringify(data),
    headers:{"X-CSRFToken":document.querySelector("[name='csrfmiddlewaretoken']").value,"Content-Type":"application/json"},
    success:(res)=>{
      cart_count();
      stop_loading();
    },
    error:(erres)=>{
      cart_count();
      if(erres.status == 403){
        errors = JSON.parse(erres.responseText);
        window.location.href = "/login";
      }
      else{
      alert(erres.responseText);
    }
      stop_loading();
    }
  })

}

function cart_count(){
  start_loading();
  url = "/cart/count"
  $.ajax({
    url:url,
    method:"GET",
    success:(res)=>{
      stop_loading();
      $("#cart_number").html(res["cart_count"])
    },
    error:(err)=>{
      stop_loading();
    }
  })
}

document.addEventListener("DOMContentLoaded",()=>{cart_count();});

