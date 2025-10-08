var returnBtn = document.getElementsByClassName('return-order')
console.log("return JS")


for (var i = 0; i < returnBtn.length; i++) {
    returnBtn[i].addEventListener('click', function () {
        var orderId = this.dataset.product
        var productId = this.dataset.action
        

        console.log('orderId:', orderId)

        sendUserRequest(orderId, productId)
    })
}


function sendUserRequest(orderId, productId) {

    console.log('User is Requesting for Return Order..')

    var url = '/auth/return_order_request/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'orderId': orderId, 'productId': productId})
    })

    .then((response) => {
        return response.json()
    })
    
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })    
}