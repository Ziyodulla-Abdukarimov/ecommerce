from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from shared.models import MyBaseModel


# Create your models here.
class CustomUser(AbstractUser):
    HOD = '1'
    STAFF = '2'
    CLIENT = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'staff': STAFF,
        'client': CLIENT
    }

    user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (CLIENT, "Client"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class AdminHod(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin')
    id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff')
    address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Client(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHod.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Client.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.client.save()


class ProductCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Comment(MyBaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    commentary = models.CharField(max_length=1000)

    def __str__(self):
        return f'author: {self.author} Comment: {self.commentary}'


class Product(MyBaseModel):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=600)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='category', null=True)
    price = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    location = models.FloatField()
    status = models.BooleanField(default=True)
    comment = models.ManyToManyField(Comment)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    image = models.ImageField(upload_to='image/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
