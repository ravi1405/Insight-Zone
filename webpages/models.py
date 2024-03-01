from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField



class College(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=500)
    College_picture = models.ImageField(upload_to='thumbpath', blank=True, )


class Semester(models.Model):
    sem_id = models.IntegerField()

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE,related_name="profile")
    College = models.ForeignKey(College, on_delete=models.NullBooleanField, null=True)
    Semester = models.ForeignKey(Semester, on_delete=models.NullBooleanField, null=True)    
    gender = MultiSelectField(choices=[
        ('male', 'Male'),
        ('female', 'Female')
    ], max_choices=1, max_length=9, null=False, default='male')
    profile_picture = models.ImageField(upload_to='media', blank=True, )
    usertype = MultiSelectField(choices=[
        ('student', 'Student'),
        ('professor', 'Professor')
    ], max_choices=1, max_length=9, null=False, default='student')
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __unicode__(self):
        return u'Profile of user: %s' % str(self.user)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    desc = models.CharField(max_length=500)
    pdf = models.FileField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"Rating by: {self.rated_by.username} for {self.rated_user.username}"

