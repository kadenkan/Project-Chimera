from django.test import TestCase
from .models import User, Chimera
from .forms import UserRegForm

# Create your tests here.

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.sampleUser = User.objects.create_user(userName="testuser", email="abc@123.com", password="t1e2s3t4")

class RegistrationModelTestCase(RegistrationTestCase):
    def test_user_is_admin(self):
        self.assertEquals(self.sampleUser.is_admin, False)

    def test_user_is_superuser(self):
        self.assertEquals(self.sampleUser.is_superuser, False)
    
    def test_user_is_staff(self):
        self.assertEquals(self.sampleUser.is_staff, False)

    def test_user_string(self):
        self.assertEquals(str(self.sampleUser), self.sampleUser.userName)

class RegistrationFormTestCase(RegistrationTestCase):
    # Valid Form Data
    def test_UserRegForm_valid(self):
        form = UserRegForm(data={'userName': "ValidUser1", 'email': "ValidUser123@test.com", 'password': "t1e2s3t4",})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserRegForm_invalid(self):
        form = UserRegForm(data={'userName': "InvalidUser1", 'email': "InvalidUser123@test.com", 'password': "",})
        self.assertFalse(form.is_valid())

class ViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(userName="ViewUser1", email="viewuser@test.com", password="user123view")

class Test_views(ViewTestCase):

    def test_login_view(self):
        user_login = self.client.login(userName="testUser1", email="user@test.com", password="user123valid")
        self.assertTrue(user_login)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_registration_view(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration")

    # Invalid Data
    def test_registration_view_invalid(self):
        response = self.client.post("/user_login/", {'userName': "userInvalid2", 'email': "asd123@test.com", 'password': "",})
        print('"error": true' in response.content)
        self.assertTrue('"error": true' in response.content)
