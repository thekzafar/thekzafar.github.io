from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    objects = models.Manager()


class Librarian(models.Model):
    admin_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    tel = models.CharField(max_length=15)
    c_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Librarian"
        ordering = ["-c_time"]
        verbose_name = "Librarian"
        verbose_name_plural = "Librarians"


class Book(models.Model):
    bno = models.CharField(max_length=20, primary_key=True)
    category = models.CharField(max_length=10)
    title = models.CharField(max_length=40)
    press = models.CharField(max_length=50)
    year = models.IntegerField()
    author = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.IntegerField()
    stock = models.IntegerField()
    objects = models.Manager()

    class Meta:
        db_table = "book"
        ordering = ["bno"]


class Card(models.Model):
    cno = models.CharField(max_length=7, primary_key=True)
    name = models.CharField(max_length=10)
    department = models.CharField(max_length=40)
    objects = models.Manager()
    TYPE_CHOICE = (
        (1, 'T'),
        (2, 'G'),
        (2, 'U'),
        (4, 'O')
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICE, default='U')

    class Meta:
        db_table = "card"


class Borrow(models.Model):
    cno = models.ForeignKey('Card', on_delete=models.CASCADE)
    bno = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "borrow"



