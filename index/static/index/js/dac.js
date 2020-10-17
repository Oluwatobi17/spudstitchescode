$(function(){
	function mathround(number){
        number = parseFloat(number)
        li = number.toString()
        li = li.split('.')
        if(li.length==1) return li[0]
        // console.log(li)
        
        if(li[1].length==1) return number
        rn = li[1][2]
        if(rn>4){
            final = li[0]+'.'
            s = parseInt(li[1][0]+li[1][1])+1
            // console.log(s)
            if(s.toString().length>2){
                final = parseFloat(final)+1
            }else{
                final += s.toString()
            }
        }else{
            final = li[0]+'.'+li[1][0]+li[1][1] 
        }
        return final
    }

    // Add or remove item from favourite "General"
	$('.product-favourite .fav').on('click', function(){
		var self = $(this)
		self.removeClass('fav')
		$.ajax({
			url: '/api/favourite/'+self.closest('.single-product-wrapper').data('id')+'/'+self.data('action'),
			success: function(data){
				if(data){
					if(self.data('action')=='add'){
						self.data('action', 'remove')
					}else{
						self.data('action', 'add')

						// if in wishlist page
						self.closest('.wishlist').toggle()
						$proNum = $('.col-lg-9 .total-products .wish')
						$proNum.text(parseInt($proNum.text())-1)
					}
					self.addClass('fav')
				}
			},
			error: function(){
				self.addClass('fav')
			}
		})
	})

	// Add or remove item from favourite list "product.html"
	$('.cart-fav-box .fav').on('click', function(){
		var self = $(this)
		self.removeClass('fav')
		var id = self.data('id')
		$.ajax({
			url: '/api/favourite/'+id+'/'+self.data('action'),
			success: function(data){
				if(data){
					if(self.data('action')=='add'){
						self.data('action', 'remove')
					}else{
						self.data('action', 'add')
					}
					self.addClass('fav')
				}
			},
			error: function(){
				self.addClass('fav')
			}
		})
	})

	// Add or remove product from cart
	$('.single-product-wrapper .add-to-cart-btn a').on('click', function(){
		var self = $(this)
		self.removeClass('.add-to-cart-btn')
		var id = self.closest('.single-product-wrapper').data('id')
		$.ajax({
			url: '/api/addcart/'+id+'/'+self.data('action'),
			success: function(data){
				if(data){
					var carttemplate = $('#cartitemtemplate').html()
					var $cartnum = $('.right-side-cart-area .cart-button .cartlength')
					if(self.data('action')=='add'){
						self.data('action', 'remove') // changing the but data-action
						self.text('Remove Cart') // Changing the but text
						
						// Altering the cart list
						newval = parseInt($cartnum.text())+1
						$cartnum.text(newval)
						$('header .cart-area .cartlength').text(newval)
						data.content['id'] = id
						$('.cart-content .cart-list').append(Mustache.render(carttemplate, data.content))
						
							// Altering the cart numbers
						var $cartnumbers = $('.right-side-cart-area .cart-amount-summary')
						var subtotal = parseFloat($cartnumbers.find('.subtotal').text().replace('#', ''))
						
						subtotal += parseFloat(data.content.price)
						subtotal = mathround(subtotal)
						$cartnumbers.find('.subtotal').text('#'+subtotal)
						$cartnumbers.find('.total').text('#'+subtotal)
					}else{
						self.data('action', 'add')
						self.text('Add to Cart')
						$('#cart'+id).remove()
						self.closest('.forcart').remove()
						var cartl = $('.container .total-products span')
						cartl.text(parseInt(cartl.text())-1)
						newval = parseInt($cartnum.text())-1
						$cartnum.text(newval)
						$('header .cart-area .cartlength').text(newval)
						
							// Altering the cart numbers
						var $cartnumbers = $('.right-side-cart-area .cart-amount-summary')
						var subtotal = parseFloat($cartnumbers.find('.subtotal').text().replace('#', ''))

						subtotal -= (parseFloat(data.content.price)*parseInt(data.content.qty))
						subtotal = mathround(subtotal)
						$cartnumbers.find('.subtotal').text('#'+subtotal)
						$cartnumbers.find('.total').text('#'+subtotal)
					}
					self.addClass('.add-to-cart-btn')
				}
			},
			error: function(){
				self.addClass('.add-to-cart-btn')
			}
		})
	})

	// post request for adding item to cart
	$('.single_product_desc .cart-form').on('submit', function(e){
		e.preventDefault()
		var self = $(this)
		var id = self.attr('id')
		var input = {
			'commodity': id,
			'color': self.find('#productSize').val(),
			'size': self.find('#productColor').val(), 
			'quantity': self.find('#quantity').val(),
			'csrfmiddlewaretoken': self.find("input[name='csrfmiddlewaretoken']").val()
		}
		$.ajax({
			type: 'POST',
			url: '/api/addcart/'+id+'/add/',
			data: input,
			success: function(data){
				// Altering the cart numbers
				// var $cartnumbers = $('.right-side-cart-area .cart-amount-summary')
				// var subtotal = parseFloat($cartnumbers.find('.subtotal').text().replace('#', ''))
				
				// subtotal += parseFloat(data.content.price)
				// subtotal = mathround(subtotal)
				// $cartnumbers.find('.subtotal').text('#'+subtotal)
				// $cartnumbers.find('.total').text('#'+subtotal)
				
				if(data.status){
					// Altering the cart list
					var carttemplate = $('#cartitemtemplate').html()
					// data.content['id'] = id
					var $container = $('.cart-content .cart-list')
					
					$('.right-side-cart-area .cart-list').html('') //Empty the cart
					var cartlen=0
					var totalprice = 0
					for(x in data.content){
						$container.append(Mustache.render(carttemplate, data.content[x]))
						cartlen++;
						totalprice+=(parseFloat(data.content[x]['price'])*parseInt(data.content[x]['quantity']))
					}
					var $cartnum = $('.right-side-cart-area .cart-button .cartlength')
					// newval = parseInt($cartnum.text())+1
					$cartnum.text(cartlen)
					$('header .cart-area .cartlength').text(cartlen)	

						// Altering the cart numbers
					var $cartnumbers = $('.right-side-cart-area .cart-amount-summary')
					// var subtotal = parseFloat($cartnumbers.find('.subtotal').text().replace('#', ''))
					
					// subtotal += (parseFloat(data.content.price)*parseInt(data.content.quantity))
					subtotal = mathround(totalprice)
					$cartnumbers.find('.subtotal').text('#'+subtotal)
					$cartnumbers.find('.total').text('#'+subtotal)
				}else{
					alert('Error processing request')
				}
			},
			error: function(){
				self.addClass('.add-to-cart-btn')
			}
		})
	})
})
// DEAL WITH ERROR MESSAGE POPING