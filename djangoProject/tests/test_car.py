from django.test import TestCase
from market.models import Car, Purchase, Order


class PurchaseTest(TestCase):
    # подготовка базы данных к тесту
    def setUp(self):
        Car.objects.create(name="Audi A6")
        Car.objects.create(name="Audi A7")
        Car.objects.create(name="Audi A8")

    def test_car_count(self):
        self.assertEqual(Car.objects.all().count(), 3)
        car = Car.objects.get(name="Audi A7")
        assert car.name == "Audi A7"

    def cars_left_function(self):
        car = Car.objects.get(name="Audi A6")
        # buy 3 cars
        Purchase.objects.create(car=car)
        Purchase.objects.create(car=car)
        Purchase.objects.create(car=car)
        # sell 1 car
        Order.objects.create(car=car)
        # we should have 1 car left
        self.assertEqual(car.cars_left(), 2)
        car = Car.objects.get(name="Audi A7")
        self.assertEqual(car.cars_left(), 0)

    def test_cars_orders_by_client(self):
        # buy_car/<int:id_>
        car = Car.objects.get(name="Audi A6")
        # buy 3 cars
        Purchase.objects.create(car=car)
        Purchase.objects.create(car=car)
        Purchase.objects.create(car=car)
        # sell 1 car
        Order.objects.create(car=car)
        url = f"/buy_car/{car.id}"
        response = self.client.post(url, {
            "name": "Zhassurbek",
            "email": "zhassurbekk@gmail.com",
            "phone": "87477002335"
        })
        self.assertEqual(response.status_code, 302)
        assert car.cars_left() == 2

