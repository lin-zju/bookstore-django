* Models
* Model specific views, corresponding templates

# Views to design

* Book
  * Add book: GET/POST, with form
  * Edit book: GET/POST, with form
  
* CartItem
  * Add to cart: POST, book_id
  * Modify quantity: POST, quantity
  * Remove: POST book_id
  
* OrderItem
  * Add Order: POST cart_id
  * Complete Order: POST
  
* WishListItem
  * Add to wishlist: POST book_id
  * Remove: POST book_id 
