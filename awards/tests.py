# from django.test import TestCase

# # Create your tests here.





# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from .models import  Project, Review, User, Profile
from django.core.files.uploadedfile import SimpleUploadedFile

class Review(TestCase):

    def setUp(self):

        self.koyoo = User.objects.create(username="koyoo")
        self.picture = Image.objects.create(image='image',
                                            user=self.koyoo)
        self.comment = Review.objects.create(comment = 'cool-photo')

        self.test_review = Review.objects.create(user=self.koyoo,
                                                 image=self.picture,
                                                 comment='cool-photo')
        self.test_review.save()

    def test_instance(self):

        self.assertTrue(isinstance(self.test_reviews, Review))

    #Testing Save method

    def test_save_method(self):
        reviews = Review.objects.all()
        self.assertTrue(len(reviews)>0)

    def test_save_review(self):
        self.assertEqual(len(Review.objects.all()), 1)

    # Tear down method
    def tearDown(self):
        Review.objects.all().delete()

        # Testing delete method

    def test_delete_review(self):
        self.test_review.delete()
        self.assertEqual(len(Review.objects.all()), 0)


class ProfileTestClass(TestCase):
    #setup method
    def setUp(self):
        #set up user class
        self.new_user = User(username="koyoo",email="koyoomaxwel@gmail.com")
        self.new_user.save()
        #set up profile class
        self.profile=Profile(bio="yes am Dev koyoo maxwel",user=self.new_user)
        self.profile.save_profile()

        # self.user.add(self.koyoo)

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()

    #testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_profile(self):
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)

    def test_delete_profile(self):
        self.profile.save_profile()
        self.profile.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)<1)

    def test_find_profile(self):
        self.profile.save_profile()
        me = Profile.objects.all()
        profiles = Profile.find_profile('koyoo')
        self.assertEqual(profiles,profiles)

    def test_get_profile(self):
        self.profile.save_profile()
        prof = Profile.get_profile()
        self.assertEqual(len(prof),1)
