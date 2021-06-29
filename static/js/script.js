// SELECT AND UNSELECT  radio boxes
function checkButton() {
  var getSelectedValue = document.querySelector('input[name=""]:checked');
  var zipVal = document.getElementById("customer_zip_code").value;
  var zipVal2 = document.querySelector('input[name="customer_zip_code"]').value;

  console.log(1)

  if ((getSelectedValue != null)){
    document.getElementById("disp").innerHTML
      = getSelectedValue.value
      + "selected";
  }
  else {
    document.getElementById("error").innerHTML
      = "Please select all fields "
    $("#button").on("click", function () {
      $("body").scrollTop(0);
    });
  }
}


// SELECT AND UNSELECT  radio boxes
var radios = Array.from(document.getElementsByClassName('radio'))

for (let i of radios) {
  i.state = false

  i.onclick = () => {
    i.checked = i.state = !i.state

    for (let j of radios)
      if (j !== i) j.state = false
  }
}
// Verify the radio boxes

var createAllErrors = function () {
  var form = $(this),
    errorList = $("ul.errorMessages", form);

  var showAllErrorMessages = function () {
    errorList.empty();

    // Find all invalid fields within the form.
    var invalidFields = form.find(":invalid").each(function (index, node) {

      // Find the field's corresponding label
      var label = $("label[for=" + node.id + "] "),
        // Opera incorrectly does not fill the validationMessage property.
        message = node.validationMessage || 'Invalid value.';

      errorList
        .show()
        .append("<li><span>" + label.html() + "</span> " + message + "</li>");
    });
  };

  // Support Safari
  form.on("submit", function (event) {
    if (this.checkValidity && !this.checkValidity()) {
      $(this).find(":invalid").first().focus();
      event.preventDefault();
    }
  });

  $("input[type=submit], button:not([type=button])", form)
    .on("click", showAllErrorMessages);

  $("input", form).on("keypress", function (event) {
    var type = $(this).attr("type");
    if (/date|email|month|number|search|tel|text|time|url|week/.test(type)
      && event.keyCode == 13) {
      showAllErrorMessages();
    }
  });
};

$("form").each(createAllErrors);

//  cart variables
const cartBtn = document.querySelector('.cart-btn')
const closeCartBtn = document.querySelector('.close-cart')
const clearCartBtn = document.querySelector('.clear-cart')
const cartDOM = document.querySelector('.cart')
const cartOverlay = document.querySelector('.cart-overlay')
const cartItems = document.querySelector('.cart-items')
const cartTotal = document.querySelector('.cart-total')
const cartContent = document.querySelector('.cart-content')
const productsDOM = document.querySelector('.products-center')
// cart
let cart = [];

//getting products
class  Products {
  async getProducts(){
    try{
      let result = await fetch("products.json")
      let data = await result.json();
      return data;
    }
    catch(error){
      console.log(error);
    }
  }
}
//display products
class UI{

}
//local storage
class Storage{

}

document.addEventListener("DOMContentLoaded",()=>{
  const ui = new UI();
  const products = new Products();

  //get all products
  products.getProducts().then(data => console.log(data));
  console.log(1)
})

