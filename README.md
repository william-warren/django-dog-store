# Benchmark - Django Dog Store

For this assignment you will build out the backend for a web app based on the
dog store python benchmark.

The application has two sections:

- Dog Store
- Dog Tags

The dog store side of the application is responsible for selling dog products to users.
Users can:

- view the list of available dog products
- view details for a single dog product
- purchase a single dog product

On the dog tags side of the application, the user can:

- view the list of existing dog tags
- create a new dog tag

I've included screenshots of each page in the `screenshots` directory and a test suite
to help you check your work.

The front end for this application has been provided for you, and you are responsible
for building the URLs, views, models, and forms required to complete the features.

## Models

This application has three models: `DogProduct`, `Purchase`, `DogTag`.

### `DogProduct`

This model represents an individual product to be sold.
It has the following fields:

- `name` - The name of the product (e.g. `"Dog Bone"`)
- `product_type` - The type of product (e.g. `"treat"`)
- `dog_size` - The size of dog appropriate for this product (e.g. `"big dogs"`)
- `price` - The price of the product in dollars (e.g. `3.4`)
- `quantity` - The number of this product left in stock (e.g. `14`)

Once this model is complete, you can use `python3 manage.py seed_dog_products`
to populate your database with initial data.

### `Purchase`

This model represents a `DogProduct` being purchased.
It has the following fields:

- `dog_product` - The `DogProduct` being purchased
- `purchased_at` - The date and time when the product was purchased

### `DogTag`

This model represents a user created dog tag.
It has the following fields:

- `owner_name` - The name of the dog's owner (e.g. `"Nate"`)
- `dog_name` - The name of the dog (e.g. `"Amos"`)
- `dog_birthday` - The date when the dog was born

## URLs

The application has 6 paths:

- `""` should route to a `home` view
- `"dog-product/<dog_product_id>"` should route to a `purchase_dog_product` view
- `"dog-product/<dog_product_id>/purchase"` should route to a `purchase_dog_product` view
- `"purchase/<purchase_id>"` should route to a `purchase_detail` view
- `"dogtag/new"` should route to a `new_dog_tag` view
- `"dogtag"` should route to a `dog_tag_list` view

## Forms

This application should use one form in the `new_dog_tag` view.
The form should be named `NewDogTagForm`.
The form should match the shape of the `DogTag` model, so it should
have the following fields:

- `owner_name` - The name of the dog's owner (e.g. `"Nate"`)
- `dog_name` - The name of the dog (e.g. `"Amos"`)
- `dog_birthday` - The date when the dog was born

## Views

### `home`

This view should render all of the `DogProduct`s using the `home.html`
template and the context key `dog_products`.

### `dog_product_detail`

This view should render the `DogProduct` identified by the path param using
the `dog_product_detail.html` template and the context key `dog_product`.

### `purchase_dog_product`

This view should attempt to purchase the `DogProduct` identified by path param.

If it is in stock the following should happen:
- `quantity` should be reduced
- a `Purchase` should be created to mark that the product was purchased at this time
- a success message (`"Purchased <product name>"`) should be shown to the user
- the user should be redirected to the newly created purchase's detail page

If it is not in stock, an error message (`"<product name> is out of stock"`) should
be shown to the user and they should be redirected to this dog product's detail page.

### `purchase_detail`

This view should render the `Purchase` identified by the path param using
the `purchase_detail.html` template and the context key `purchase`.

### `new_dog_tag`

On `GET`, this view should render the `new_dog_template.html` template.

On `POST`, this view should validate the POSTed form data using the
`NewDogTagForm` form. If the submission is valid, a new `DogTag` should
be created with the POSTed data and the user should be redirected to
the `dog_tag_list` view. If the submission is not valid,
`new_dog_template.html` should be rendered and the invalid form should
be provided to the context using the key `form`.