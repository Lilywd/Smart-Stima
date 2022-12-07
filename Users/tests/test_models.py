from django.test import TestCase
from Users.models import User

class ModelsTestCase(TestCase):
    
    def test_creates_user(self):
        user=User.objects.create_user('lily','lilian','wn','lily@gmail.com','password1234!@')
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email,'lily@gmail.com')
        

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='', first_name='lilian', last_name='wn', email='lily@gmail.com',password='password1234!@')
        self.assertRaisesMessage(ValueError, 'User must have a username')
    
    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='', first_name='lilian', last_name='wn', email='lily@gmail.com',password='password1234!@')
        self.assertRaisesMessage(ValueError, 'User must have a username')
    
    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='lily', first_name='lilian', last_name='wn', email='',password='password1234!@')
        self.assertRaisesMessage(ValueError, 'User must have an email')

    def test_raises_error_when_no_first_name_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='lily', first_name='', last_name='wn', email='lily@gmail.com',password='password1234!@')
        self.assertRaisesMessage(ValueError, 'User must have a firstname')

    def test_raises_error_when_no_last_name_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='lily', first_name='lilian', last_name='', email='lily@gmail.com',password='password1234!@')
        self.assertRaisesMessage(ValueError, 'User must have a lastname')

    def test_creates_super_user(self):
        user=User.objects.create_superuser('lily','lilian','wn','lily@gmail.com','password1234!@')
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email,'lily@gmail.com')


    def test_returns_self_username(self):
        user=User.objects.create_user('lily','lilian','wn','lily@gmail.com','password1234!@')
        self.assertIsInstance(user,User)
        self.assertEqual(str(user),'lily')
     

   
       
    

        
    