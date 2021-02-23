from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from . import crypting
from django.conf import settings


class CustomUser(AbstractUser):
	pass

class CustomUserManager(UserManager):
	pass

class UserPasswords(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	URL = models.URLField()
	name = models.CharField(max_length=150)
	username_or_email = models.CharField(max_length=150)
	site_password = models.CharField(max_length=150)
	notes = models.TextField()


	class Meta:
		verbose_name_plural = 'User Passwords'
	# def save(self, *args, **kwargs):
	# 	self.site_password = crypting.encryptMessage(UsersEncryptionKey., self.site_password)
	# 	self.notes = crypting.encryptMessage('ASIMOV', self.notes)
	# 	super(UserPasswords, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.name} - {self.username_or_email}'

class UserCards(models.Model):
	CARDS = (
		('Visa', 'Visa'),
		('Mastercard', 'Mastercard'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name_on_card = models.CharField(max_length=150)
	card_type = models.CharField(choices=CARDS, max_length=100)
	card_number = models.IntegerField()
	security_CVV_code = models.IntegerField()
	start_date = models.DateField()
	expiration_date = models.DateField()
	notes = models.TextField()

	class Meta:
		verbose_name_plural = 'User Cards'

	def __str__(self):
		return f'{self.name_on_card} - {self.card_number}'

class UserNotes(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	note_title = models.CharField(max_length=150)
	note_content = models.TextField()

	class Meta:
		verbose_name_plural = 'User Notes'

	def __str__(self):
		return self.note_title


class UsersEncryptionKey(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	enc_key = models.CharField(max_length=50, blank=False, null=False)

	class Meta:
		verbose_name_plural = 'User Encryption Keys'

	def __str__(self):
		return f'{self.user}'