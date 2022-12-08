from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    
   def create_user(self, username, first_name, last_name, email,  password=None):
       if not email:
           raise ValueError('Email must be provided')

       if not username:
           raise ValueError('User must have a username')

       if not first_name:
           raise ValueError('User must have a first name')

       if not last_name:
           raise ValueError('User must have a last name')
 
       user = self.model(
              email=self.normalize_email(email),
              username=username,
              first_name=first_name,
              last_name=last_name,
            )
       user.set_password(password)
       user.save(using=self._db)
       return user

   def create_superuser(self, username, first_name, last_name, email,  password):
       user = self.create_user(
              email=self.normalize_email(email),
              password=password,
              username=username,
              first_name=first_name,
              last_name=last_name,
            )
       user.is_admin = True
       user.is_staff= True
       user.is_superuser = True
       user.save(using=self._db)
       return user


# create a user and superuser if all details are provided