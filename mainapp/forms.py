from django import forms
from .models import UserPasswords, UserCards, UserNotes, UsersEncryptionKey

class UserPasswordsForm(forms.ModelForm):
    widgets = {'user':forms.TextInput(attrs={'readonly':'readonly'})}
    class Meta:
        model = UserPasswords
        
        fields = [
            'URL',
            'name',
            'username_or_email',
            'site_password',
            'notes',
        ]

class UserCardsForm(forms.ModelForm):
    widgets = {'user':forms.TextInput(attrs={'readonly':'readonly'})}
    class Meta:
        model = UserCards
        fields = [
            'name_on_card',
            'card_type',
            'card_number',
            'security_CVV_code',
            'start_date',
            'expiration_date',
            'notes'
        ]

class UserNotesForm(forms.ModelForm):
    widgets = {'user':forms.TextInput(attrs={'readonly':'readonly'})}
    class Meta:
        model = UserNotes
        fields = ['note_title','note_content',]

class UsersEncryptionKeyForm(forms.ModelForm):
    widgets = {'user':forms.TextInput(attrs={'readonly':'readonly'})}
    class Meta:
        model = UsersEncryptionKey
        fields = ['enc_key',]

class changeUsersEncryptionForm(forms.ModelForm):
    widgets = {'user':forms.TextInput(attrs={'readonly':'readonly'})}
    class Meta:
        model = UsersEncryptionKey
        fields = ['enc_key',]