// console.log("Hello Ankit Ji");
// console.log("Hello Ankit!");
// console.log("Hello Ankit!");


//document.getElementsByClassName('dis-hide').hidden = true;
var updateBtns = document.getElementsByClassName('update-cart');
// console.log(updateBtns);
// function updateQuantity(){
//      const quantity = document.querySelector('td .count');
//      // quantity.textContent = '';
// }

// updateQuantity();

for (let i = 0; i < updateBtns.length; i++){
     updateBtns[i].addEventListener('click', function(){
          var productId = this.dataset.product;
          var action = this.dataset.action;
          console.log('productID :', productId, 'Action :', action)

          console.log('User :', user);
          if(user == 'AnonymousUser'){
               // console.log("User is not authenticated");
               window.location = "/register"
          }else{
               updateUserOrder(productId, action)
          }
     })
}


function updateUserOrder(productId, action){
     console.log("User is authenticated, sending data ...");

     var url = '/update_cart/'

     fetch(url, {
     method: 'POST',
     headers:{
          'Content-Type': 'application/json',
          
     },
     body:JSON.stringify({
          'productId': productId,
          'action': action
     })
})
     .then((response) => {
          console.log(response);
          return response.json()
     })
     .then((data) => {
          console.log('data :', data)
          location.reload()
          // $(`.cart_container`).load(` #cart-table`)
          // $(`#countOf_${productId}`).load(` .count_${productId}`)
          // $(`.order-bill`).load(window.location.href + ` .order-bill-container`)
          
          // productView Page
          // $(`#item_count`).load(window.location.href + ` #item_count`)

     })
}


