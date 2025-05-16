from datetime import datetime  # Добавить эту строку в начало файла
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
import app.forms
import app.views

urlpatterns = [
    path('', app.views.home, name='home'),
    path('anketa/', app.views.anketa, name='anketa'),
    path('contact/', app.views.contact, name='contact'),
    path('about/', app.views.about, name='about'),
    path('blog/', app.views.blog, name='blog'),
    path('blog/<int:pk>/', app.views.blogpost, name='blogpost'),
    path('links/', app.views.links, name='links'),
    path('newpost/', app.views.newpost, name='newpost'),
    path('videopost/', app.views.videopost, name='videopost'),
    path('registration/', app.views.register, name='registration'),
    path('login/',
        LoginView.as_view(
            template_name='app/login.html',
            authentication_form=app.forms.BootstrapAuthenticationForm,
            extra_context={
                'title': 'Log in',
                'year': datetime.now().year,  # Теперь datetime доступен
            }
        ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)