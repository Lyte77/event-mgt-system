from django.db import models
from django.conf import settings
import uuid
from django.utils.text import slugify
from .managers import TicketManager

class Event(models.Model):
    STATUS_CHOICES = [
        ("draft","Draft"),
        ("upcoming","Upcoming"),
        ("ongoing","Ongoing"),
        ("completed","Completed"),
        ("cancled","Cancled",)
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='organized_events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_image = models.ImageField(upload_to='event_pics/',null=True,blank=True)
    venue = models.CharField(max_length=255,blank=True,null=True)
    online_link = models.URLField(blank=True,null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True,null=True)
    capacity = models.PositiveIntegerField(null=True,blank=True)
    ticket_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    slug = models.SlugField(unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args,**kwargs)


    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.title


class TicketType(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='ticket_type')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name } - {self.event.title }" 

    def has_availability(self,quantity):
        return self.quantity_available >= quantity 

class Ticket(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending","Pending"),
        ("paid","Paid"),
        ("refunded","Refunded"),
    ]

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="tickets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='tickets')
    ticket_type = models.ForeignKey(TicketType,on_delete=models.CASCADE,
                                    related_name='tickets')
    quantity = models.PositiveBigIntegerField(default=1)
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS_CHOICES,default="pending")
    unique_code = models.CharField(max_length=100,unique=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TicketManager()

    def save(self,*args,**kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace("-","").upper()[:12]
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.email } - {self.event.title} ({self.ticket_type})"
    


    
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=120,unique=True)
    events = models.ManyToManyField(Event,related_name='categories',blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

