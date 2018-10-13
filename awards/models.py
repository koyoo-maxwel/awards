from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    profilePic = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile

    @classmethod
    def find_profile(cls, search_term):
        profile = cls.objects.filter(user__username__icontains=search_term)
        return profile

    @classmethod
    def update_profile(cls, id, bio):
        updated = Image.objects.filter(id=id).update(bio=bio)
        return updated


# my images for the projects uploads here
class Project(models.Model):
    image = models.ImageField(upload_to='project-uploads/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null='True')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

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
        project = Project.objects.filter(id=Project.id)
        return project


# comments on the projects
class Comment(models.Model):
    comments = models.CharField(max_length=500, blank=True, null=True)
    commented_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.comments

    class Meta:
        ordering = ['-commented_on']

    def save_comment(self):
        return self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comment(cls):
        comment = Comment.objects.all()
        return comment
