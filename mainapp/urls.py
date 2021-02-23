from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.home_view, name='homepage'),
    path('notes', views.notes_view, name='notes'),
    path('set-encryption-key', views.set_encryption_key, name='set-encryption'),
    path('passwords', views.passwords_view, name='passwords'),
    path('settings', views.settings_view, name='settings'),
    path('settings/<int:enc_id>', views.change_encryption_key, name='change-key'),

    path('passwords/<int:id>', views.password_view, name='password'),
    path('passwords/<int:id>/decrypt',views.decrypt_password, name='decrypt-password'),

    path('notes/<int:id>', views.note_view, name='note'),
    path('notes/<int:id>/decrypt', views.decrypt_note, name='decrypt-note'),
]