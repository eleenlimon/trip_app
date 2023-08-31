from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
User = get_user_model()


# Create your models here.
# two tables- img and note (images)

class Trip(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=2)  # ex/ US
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)  # ok to input blank values
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='trips')

    # user owner of the img (one to one relationship)

    def __str__(self):
        return self.city


class Note(models.Model):
    EXCURSIONS = (
        ('event', 'Event'),
        ('dining', 'Dining'),
        ('experience', 'Experience'),
        ('general', 'General'),
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=EXCURSIONS)
    img = models.ImageField(upload_to='notes', blank=True, null=True)
    # pillow - install
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5)])
    # blank/null means img not needed, notes the directory where img will be uploaded

    def __str__(self):
        return f'{self.name} in {self.trip.city}'