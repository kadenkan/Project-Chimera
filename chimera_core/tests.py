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
    def test_registration_form(self):
        invalid_data_dicts = [
            # Already-existing username.
            {
            'data':
            { 'userName': 'testuser',
              'email': 'test@abc.com',
              'password': 'password'},
            'error':
            ('userName', [u"User with this User name already exists."])
            },
            ]

        for invalid_dict in invalid_data_dicts:
            form =UserRegForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])

        form = UserRegForm(data={ 'userName': 'foo',
                                             'email': 'foo@example.com',
                                             'password': 'password',
                                             }
                                            )
        self.assertEqual(form.is_valid(), True)

