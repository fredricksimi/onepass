from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.views import SignupView, LoginView
from .forms import UserPasswordsForm, UserCardsForm, UserNotesForm, UsersEncryptionKeyForm, changeUsersEncryptionForm
from .models import UserPasswords, UserNotes, UserCards, CustomUser, UsersEncryptionKey
from django.contrib.auth.decorators import login_required
from . import crypting
from cryptography.fernet import fernet
import time

def home_view(request):
    user_key = UsersEncryptionKey.objects.get(user__id=request.user.id)
    context = {'user_key':user_key}
    return render(request, 'mainapp/index.html', context)

@login_required
def passwords_view(request):
    use_pass = UserPasswords.objects.filter(user=request.user)
    user_key = UsersEncryptionKey.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        form = UserPasswordsForm(request.POST or None)
        userskey = UsersEncryptionKey.objects.get(id = request.user.id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.user.id = request.user.id
            new_form.site_password = crypting.encryptMessage(userskey.enc_key, new_form.site_password)
            new_form.notes = crypting.encryptMessage(userskey.enc_key, new_form.notes)
            new_form.save()
        return redirect('mainapp:passwords')
    else:
        form = UserPasswordsForm()
    context = {'form':form, 'use_pass':use_pass, 'user_key':user_key}
    return render(request, 'mainapp/passwords.html', context)

def password_view(request, id):
    use_pass = UserPasswords.objects.get(id=id)
    context ={
        'use_pass':use_pass
    }
    return render(request,'mainapp/encrypted-password-view.html', context)

def decrypt_password(request, id):
    use_pass = UserPasswords.objects.get(id=id)
    user_key = UsersEncryptionKey.objects.get(user__id = request.user.id)
    site_pass = crypting.decryptMessage(user_key.enc_key, use_pass.site_password)
    the_notes = crypting.decryptMessage(user_key.enc_key, use_pass.notes)
    context = {
        'site_pass':site_pass,
        'the_notes':the_notes,
        'use_pass':use_pass
    }
    return render(request, 'mainapp/decrypted-password-view.html', context)


def notes_view(request):
    notes = UserNotes.objects.filter(user=request.user)
    user_key = UsersEncryptionKey.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        form = UserNotesForm(request.POST or None)
        userskey = UsersEncryptionKey.objects.get(id = request.user.id)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.user.id = request.user.id
            new_form.note_content = crypting.encryptMessage(userskey.enc_key, new_form.note_content)
            new_form.save()
        return redirect('mainapp:notes')
    else:
        form = UserNotesForm()
    context = {'form':form, 'notes':notes, 'user_key':user_key}    
    return render(request, 'mainapp/notes.html', context)

def note_view(request, id):
    use_note = UserNotes.objects.get(id=id)
    context ={
        'use_note':use_note
    }
    return render(request,'mainapp/encrypted-note-view.html', context)

def decrypt_note(request, id):
    use_note = UserNotes.objects.get(id=id)
    user_key = UsersEncryptionKey.objects.get(user__id = request.user.id)
    the_notes = crypting.decryptMessage(user_key.enc_key, use_note.note_content)
    context = {
        'the_notes':the_notes,
        'use_note':use_note
    }
    return render(request, 'mainapp/decrypted-note-view.html', context)





def set_encryption_key(request):
    if request.method == 'POST':
        form = UsersEncryptionKeyForm(request.POST or None)
        spacing = ' '
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.user.id = request.user.id
            new_form.save()
        return redirect('mainapp:homepage')
    else:
        form = UsersEncryptionKeyForm()
    context = {
        'form':form
    }
    return render(request, 'mainapp/set-encryption.html', context)
def settings_view(request):
    enkeys = UsersEncryptionKey.objects.filter(user = request.user.id)
    context = {
        'enkeys':enkeys
    }
    return render(request, 'mainapp/keys.html', context)

def change_encryption_key(request, enc_id):
    old_enc_key = get_object_or_404(UsersEncryptionKey, id=enc_id)
    print(old_enc_key.enc_key)
    userpass = UserPasswords.objects.filter(user__id = request.user.id)
    usernotes = UserNotes.objects.filter(user__id = request.user.id)
    # userkey = .objects.get(user__id=request.user.id)
    
    if request.method == 'POST':
        form = UsersEncryptionKeyForm(request.POST, instance=old_enc_key)
        # spacing = ' '
        if form.is_valid():
            new_form = form.save(commit=False)

            for usepass in userpass:
                dec_notes = crypting.decryptMessage(old_enc_key.enc_key, usepass.notes)
                enc_notes = crypting.encryptMessage(new_form.enc_key, dec_notes)
                usepass.notes = enc_notes
                dec_site_pass = crypting.decryptMessage(old_enc_key.enc_key, usepass.site_password)
                enc_site_pass = crypting.encryptMessage(new_form.enc_key, dec_site_pass)
                usepass.site_password = enc_site_pass
                usepass.save()

            for usenote in usernotes:
                dec_note =crypting.decryptMessage(old_enc_key.enc_key, usenote.note_content)
                enc_note = crypting.encryptMessage(new_form.enc_key, dec_note)
                usenote.note_content = enc_note
                usenote.save()
            
            new_form.user = request.user
            new_form.user.id = request.user.id
            time.sleep(5)
            new_form.save()
        return redirect('mainapp:homepage')
    else:
        form = UsersEncryptionKeyForm(instance=old_enc_key)
    context = {
        'form':form,
        'key':old_enc_key
    }
    return render(request, 'mainapp/change-encryption.html', context)

class MySignUpView(SignupView):
    template_name = 'mainapp/signup.html'


class MyLoginView(LoginView):
    template_name = 'mainapp/login.html'

