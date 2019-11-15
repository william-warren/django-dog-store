from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path(
        "dog-product/<dog_product_id>",
        views.dog_product_detail,
        name="dog_product_detail",
    ),
    path(
        "dog-product/<dog_product_id>/purchase",
        views.purchase_dog_product,
        name="purchase_dog_product",
    ),
    path("puchase/<purchase_id>", views.purchase_detail, name="purchase_detail"),
    path("dogtag/new", views.NewDogTag.as_view(), name="new_dog_tag"),
    path("dogtag", views.dog_tag_list, name="dog_tag_list"),
    path("review/new/<product_id>", views.new_review, name="new_review"),
    path("help", views.ocd_helper, name="help"),
]
