from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile


class AccountsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ComplexPassword123!',
            first_name='Ali',
            last_name='Reza',
        )
        self.profile = Profile.objects.create(
            user=self.user,
            phone_number='0412345678',
            address='789 Swanston St',
            suburb='Carlton',
            postcode='3053',
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "testuser's profile")

    def test_register_view(self):
        # GET
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

        # POST
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassword456!',
            'password2': 'StrongPassword456!',
        }
        response = self.client.post(reverse('accounts:register'), register_data)
        self.assertRedirects(response, reverse('core:home'))

        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))

    def test_login_logout_view(self):
        # Login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'ComplexPassword123!',
        })
        self.assertRedirects(response, reverse('core:home'))

        # Logout via GET
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('core:home'))

    def test_profile_view_requires_login(self):
        # Anonymous access redirects to login
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

        # Authenticated access
        self.client.login(username='testuser', password='ComplexPassword123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

        # Update profile
        update_data = {
            'phone_number': '0499887766',
            'address': '12 New Address',
            'suburb': 'Fitzroy',
            'postcode': '3065',
        }
        response = self.client.post(reverse('accounts:profile'), update_data)
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, '0499887766')
        self.assertEqual(self.profile.suburb, 'Fitzroy')
