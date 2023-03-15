from django.contrib.auth.models import User
from django.db import models


class BuildCompany(models.Model):
    name = models.CharField(max_length=100)
    developer_src = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='developer_logo')

    def __str__(self):
        return self.name


class RealEstate(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    floor = models.IntegerField()
    rooms = models.IntegerField()
    bathrooms = models.IntegerField(default=1)
    squares = models.IntegerField()
    buy_price = models.IntegerField(default=0)
    rent_price = models.IntegerField(default=0)
    main_photo = models.ImageField(upload_to='estate_photos')
    developer = models.ForeignKey(BuildCompany, on_delete=models.CASCADE)
    build_at = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}-{self.name}'


class RealEstatePhoto(models.Model):
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='estate_photos')

    def __str__(self):
        return f'{self.id}-{self.real_estate.name}'


class EstateComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.id}-{self.user.username}'


class FavouriteEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}-{self.user.username}-{self.estate.name}'
