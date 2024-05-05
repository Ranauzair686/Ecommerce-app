var updatebBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updatebBtns.length; i++) {
    updatebBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log(user)  // until this now we have product id and user which is logged in 
        if (user == 'AnonymousUser') {
            // console.log('Not logged in') intead of consoling out now will console that cokkie function
            addCookieItem(productId, action)

        } else {
            updateUserOrder(productId, action)
        }

    })

}

function addCookieItem(productId, action) {
    console.log('Not logged in ....')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }

        } else {
            cart[productId]['quantity'] += 1
        }

    }
    if(action == 'remove'){
        cart[productId]['quantity'] -=1

        if(cart[productId]['quantity'] <=0){
            console.log('remove item')
            delete cart[productId]
        }

    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()


}



function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data')

    var url = '/update_item/'

    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, //now we have throughn the token now we can send data to backend X-CSRFToken this has to be string that why we used comaas 
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })


}