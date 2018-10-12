from django.shortcuts import render

# Create your views here.
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