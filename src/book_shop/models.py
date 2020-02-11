from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(null=True, blank=True)


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    info = models.TextField(max_length=1000)


class Book(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(blank=True)
    authors = models.ManyToManyField(Author)
    publishers = models.ManyToManyField(Publisher)
    pages_count = models.IntegerField()
    publish_year = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, through='OrderItem')
    phone_number = models.CharField(max_length=20)

    class Status(models.IntegerChoices):
        PENDING = 0
        DONE = 1
    status = models.SmallIntegerField(default=0, choices=Status.choices)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_cost(self):
        return self.book.cost * self.quantity
