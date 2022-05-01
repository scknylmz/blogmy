from itertools import chain
from turtle import mode
from unicodedata import category
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Personnel(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    title2 = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Pesonnel"


class Education(models.Model):
    name = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    school = models.CharField(max_length=50)
    section = models.CharField(max_length=50 , null=True, blank=True )
    degree = models.IntegerField(choices=((0, "DOCTORATE"),(1,"MASTER DEGREE"), (2,"BACHELOR DEGREE"),(3,"DIPLOMA IN"),(4,"ASSOCIATE DEGREE"),(5,"HIGH SCHOOL"), ))
    graduation = models.IntegerField(choices=((1,"Graduated"),(2,"Student")),default=1)
    start_date_month = models.SmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(12)])
    start_date_year = models.SmallIntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2100)])
    end_date_month = models.SmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=True)
    end_date_year = models.SmallIntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2100)], null=True, blank=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table="Education"
    
class Contact(models.Model):
    name = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    mail = models.EmailField(max_length=254)
    adress = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table="Contact"

class Blog(models.Model):
    title = models.CharField(max_length=40)
    entry = models.CharField(max_length=130)
    body = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=False)
    category = models.IntegerField(choices=((1,"Django"),),default=1)
    img = models.ImageField(upload_to="blog/", height_field=None, width_field=None, max_length=None, null=True, blank=True)

    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        db_table="Blog"

class WorksCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"

class Works(models.Model):
    title = models.CharField(max_length=40)
    entry = models.CharField(max_length=130)
    body = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=False)
    category = models.ForeignKey(WorksCategory, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="works/", height_field=None, width_field=None, max_length=None, null=True, blank=True)

    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('works_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        db_table="Work"