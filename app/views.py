from django.shortcuts import render, redirect
from app.models import DogProduct, Purchase, DogTag, Review
from app.forms import NewDogTagForm, NewReviewForm
from django.contrib import messages
from django.views import View
from django.utils import timezone


def home(request):
    dog_products = DogProduct.objects.all()
    return render(request, "home.html", {"dog_products": dog_products})


def dog_product_detail(request, dog_product_id):
    dog_product = DogProduct.objects.get(id=dog_product_id)
    reviews = dog_product.review_set.all().order_by("-rating")
    return render(
        request,
        "dog_product_detail.html",
        {"dog_product": dog_product, "reviews": reviews},
    )


def purchase_dog_product(request, dog_product_id):
    product = DogProduct.objects.get(id=dog_product_id)
    if product.quantity > 0:
        product.quantity -= 1
        purchase = product.purchase_set.create(purchased_at=timezone.now())
        messages.success(request, f"Purchased {product.name}")
        product.save()
        return redirect("purchase_detail", purchase.id)
    else:
        messages.error(request, f"{product.name} is out of stock")
        return redirect("dog_product_detail", product.id)


def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    return render(request, "purchase_detail.html", {"purchase": purchase})


class NewDogTag(View):
    def get(self, request):
        return render(request, "new_dog_tag.html")

    def post(self, request):
        form = NewDogTagForm(request.POST)
        if form.is_valid():
            owner = request.POST["owner_name"]
            dog = request.POST["dog_name"]
            birthday = request.POST["dog_birthday"]
            tag = DogTag.objects.create(
                owner_name=owner, dog_name=dog, dog_birthday=birthday
            )
            tag.save()
            return redirect("dog_tag_list")
        else:
            return render(request, "new_dog_tag.html", {"form": form})


def dog_tag_list(request):
    dog_tags = DogTag.objects.all()
    return render(request, "dog_tag_list.html", {"dog_tags": dog_tags})


def new_review(request, product_id):
    product = DogProduct.objects.get(id=product_id)
    review = product.review_set.create(
        author=request.POST["author"],
        content=request.POST["content"],
        rating=request.POST["rating"],
    )
    review.save()
    return redirect("dog_product_detail", product_id)


def ocd_helper(request):
    products = DogProduct.objects.all()
    for product in products:
        words = product.name.split(" ")
        new_name = ""
        for word in words:
            word = word.capitalize()
            new_name += f"{word} "
        product.name = new_name
        product.save()
    return redirect("home")
