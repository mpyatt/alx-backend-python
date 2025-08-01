from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender', password='pass')
        self.receiver = User.objects.create_user(
            username='receiver', password='pass')

    def test_notification_created_on_message_send(self):
        msg = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, msg)

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello!")
        msg.content = "Hello, edited!"
        msg.save()

        self.assertTrue(msg.edited)
        self.assertEqual(msg.history.count(), 1)
        history = msg.history.first()
        self.assertEqual(history.old_content, "Hello!")

    def test_user_deletion_cleans_up_related_data(self):
        msg = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hi")
        Notification.objects.create(user=self.receiver, message=msg)

        self.sender.delete()

        self.assertFalse(Message.objects.filter(sender=self.sender).exists())
        self.assertFalse(Notification.objects.filter(
            user=self.receiver).exists())
