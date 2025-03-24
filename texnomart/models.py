from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/products/', null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"


class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment_product')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='comments/', null=True, blank=True)
    bad_comment = models.TextField(null=True, blank=True)
    good_comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE)

    def __str__(self):
        return f"Comment for {self.product.name}"
