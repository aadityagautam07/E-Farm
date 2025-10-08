var updateBtns = document.getElementsByClassName('update-wishlist')
console.log('Inside Wishlist')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('productId:', productId, 'action:', action)

        addCookieItem(productId, action)
    })
}


function addCookieItem(productId, action) {
    console.log('Guest User Sending Data ....')

    if (action == 'add') {

        console.log('cart: ', cart)
        if (wishlist[productId] === undefined) {
            wishlist[productId] = { 'Added': 1 }
        } else {
            wishlist[productId]['Added'] = 1
        }
    }

    if (action == 'delete') {
        console.log('Remove Item')
        delete wishlist[productId]

    }
    console.log('wishlist:', wishlist)
    document.cookie = 'wishlist=' + JSON.stringify(wishlist) + ";domain=;path=/"
    location.reload()
}
