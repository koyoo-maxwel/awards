from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


# class Profile(models.Model):
#     profilepic = models.ImageField(upload_to='profile/', null=True, blank=True)
#     bio = models.CharField(max_length=100, blank=True)
#     user = models.OneToOneField(User)


class Project(models.Model):
    title = models.TextField(max_length=100, null=True,
                             blank=True, default="title")
    project_image = models.ImageField(
        upload_to='project_upload/', null=True, blank=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    commented_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    project_url = models.URLField(max_length=250)

    class Meta:
        ordering = ['-upload_date']

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def get_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def get_project_by_id(cls, id):
        project = Project.objects.filter(id=project.id)
        return project()

    # @classmethod
    # def get_project_by_id(cls,id):
    #     project = cls.objects.get(pk=id)
    #     return project
    #     return project()

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),

    )
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
   
    comment = models.TextField()
    design_rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    usability_rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    content_rating = models.IntegerField(choices=RATING_CHOICES, default=0)

    def save_comment(self):
        self.save()

    def get_comment(self, id):
        comments = Review.objects.filter(image_id=id)
        return comments

    def __str__(self):
        return self.comment


class Profile(models.Model):
    class Meta:
        db_table = 'profile'

    bio = models.TextField(max_length=200, null=True,
                           blank=True, default="bio")
    profile_pic = models.ImageField(
        upload_to='picture/', null=True, blank=True, default=0)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', null=True)
    contact = models.IntegerField(default=0)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls, user):
        profile = Profile.objects.get(user=user)
        return profile

    @classmethod
    def find_profile(cls, search_term):
        profile = cls.objects.filter(user__username__icontains=search_term)
        return profile

    @classmethod
    def update_profile(cls, id, bio):
        updated = Image.objects.filter(id=id).update(bio=bio)
        return updated

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username
