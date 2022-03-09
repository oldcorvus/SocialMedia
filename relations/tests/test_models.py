from django.test import TestCase
from django.contrib.auth import get_user_model
from relations.models import Contact
User = get_user_model()

class RelationModelTest(TestCase):
    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(username='testuser1',email='example1@gmail.com',phone_number='111', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(username='testuser2',email='example2@gmail.com',phone_number='222', password='2HJ1vRV0Z&3iD')

        self.test_user1.save()
        self.test_user2.save()

        # Create a Contact
        self.test_contact = Contact.objects.create(user_from= self.test_user1, user_to= self.test_user2)


    def test_user_contact(self):
        
        self.assertTrue(self.test_user1.rel_from_set.exists())
        self.assertFalse(self.test_user2.rel_from_set.exists())

        self.assertTrue(self.test_user2.rel_to_set.exists())
        self.assertFalse(self.test_user1.rel_to_set.exists())
