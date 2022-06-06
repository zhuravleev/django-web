from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name,password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
