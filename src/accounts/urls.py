from django.contrib.auth.decorators import login_required
from django.urls import path, include

from src.accounts.views import login_view, register, logout_view, profile_edit, profile, settings_account, \
    settings_password, upload_cover, upload_profile
from django.conf import settings
from django.conf.urls.static import static

app_name = "accounts"

urlpatterns = [
    path('login', login_view, name='login'),
    path('register', register, name='register'),
    path('logout', logout_view, name='logout'),
    path('profile/edit', profile_edit, name='profile_update'),
    path('profile/<slug:username>', profile, name='profile'),
    path('settings/account', settings_account, name='settings_account'),
    path('settings/password', settings_password, name='settings_password'),
    path('profile/upload/cover', upload_cover, name='upload_cover'),
    path('profile/upload/profile', upload_profile, name='upload_profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
