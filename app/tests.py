from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages, SUCCESS, ERROR
from app import models


class TestHome(TestCase):
    def setUp(self):
        self.products = [
            models.DogProduct.objects.create(
                name="big rawhide",
                product_type="treat",
                dog_size="big",
                price=1.55,
                quantity=18,
            ),
            models.DogProduct.objects.create(
                name="peanut butter cookie",
                product_type="treat",
                dog_size="all",
                price=0.88,
                quantity=33,
            ),
            models.DogProduct.objects.create(
                name="squeaker mouse",
                product_type="toy",
                dog_size="small",
                price=5.44,
                quantity=10,
            ),
        ]

        self.response = self.client.get(reverse("home"))

    def test_user_can_see_all_dog_products(self):
        for product in self.products:
            self.assertContains(self.response, product.name)

    def test_user_can_see_a_link_to_each_detail_page(self):
        for product in self.products:
            self.assertContains(self.response, f"View {product.name}")


class TestDogProductDetail(TestCase):
    def setUp(self):
        self.products = [
            models.DogProduct.objects.create(
                name="big rawhide",
                product_type="treat",
                dog_size="big",
                price=1.55,
                quantity=18,
            ),
            models.DogProduct.objects.create(
                name="peanut butter cookie",
                product_type="treat",
                dog_size="all",
                price=0.88,
                quantity=33,
            ),
            models.DogProduct.objects.create(
                name="squeaker mouse",
                product_type="toy",
                dog_size="small",
                price=5.44,
                quantity=10,
            ),
        ]

    def test_detail_page_shows_important_user_information(self):
        for product in self.products:
            product_url = reverse("dog_product_detail", args=[product.id])
            response = self.client.get(product_url)
            self.assertContains(response, product.name)
            self.assertContains(response, product.product_type)
            self.assertContains(response, product.dog_size)
            self.assertContains(response, product.price)
            self.assertContains(response, product.quantity)

    def test_detail_page_shows_button_to_buy_product(self):
        for product in self.products:
            product_url = reverse("dog_product_detail", args=[product.id])
            response = self.client.get(product_url)
            self.assertContains(response, f"Buy {product.name}")


class TestDogProductPurchase(TestCase):
    def setUp(self):
        self.in_stock_products = [
            models.DogProduct.objects.create(
                name="big rawhide",
                product_type="treat",
                dog_size="big",
                price=1.55,
                quantity=18,
            ),
            models.DogProduct.objects.create(
                name="squeaker mouse",
                product_type="toy",
                dog_size="small",
                price=5.44,
                quantity=10,
            ),
        ]

        self.out_of_stock_product = models.DogProduct.objects.create(
            name="peanut butter cookie",
            product_type="treat",
            dog_size="all",
            price=0.88,
            quantity=0,
        )

    def test_purchasing_a_dog_product(self):
        for in_stock_product in self.in_stock_products:
            original_stock = in_stock_product.quantity
            purchase_url = reverse("purchase_dog_product", args=[in_stock_product.id])
            response = self.client.post(purchase_url)
            in_stock_product.refresh_from_db()

            with self.subTest("should reduce quantity"):
                self.assertEqual(in_stock_product.quantity, original_stock - 1)

            with self.subTest("should flash a success message"):
                messages = [
                    (m.level, m.message) for m in get_messages(response.wsgi_request)
                ]
                self.assertIn((SUCCESS, f"Purchased {in_stock_product.name}"), messages)

            with self.subTest("should create a purchase"):
                self.assertEqual(in_stock_product.purchase_set.count(), 1)

            with self.subTest("should redirect to the newly created purchase"):
                purchase = in_stock_product.purchase_set.first()
                purchase_url = reverse("purchase_detail", args=[purchase.id])
                self.assertRedirects(response, purchase_url)

    def test_attempting_to_purchasing_an_out_of_stock_product(self,):
        original_stock = self.out_of_stock_product.quantity
        purchase_url = reverse(
            "purchase_dog_product", args=[self.out_of_stock_product.id]
        )
        response = self.client.post(purchase_url)
        self.out_of_stock_product.refresh_from_db()

        with self.subTest("should not reduce quantity"):
            self.assertEqual(self.out_of_stock_product.quantity, original_stock)

        with self.subTest("should flash an error message"):
            messages = [
                (m.level, m.message) for m in get_messages(response.wsgi_request)
            ]
            self.assertIn(
                (ERROR, f"{self.out_of_stock_product.name} is out of stock"), messages
            )

        with self.subTest("should not create a purchase"):
            self.assertEqual(self.out_of_stock_product.purchase_set.count(), 0)

        with self.subTest("should redirect to the dog product's detail page"):
            dog_product_url = reverse(
                "dog_product_detail", args=[self.out_of_stock_product.id]
            )
            self.assertRedirects(response, dog_product_url)
