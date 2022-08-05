"""richpanel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from assignment import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('monthly_plans/<int:user_id>', views.monthly_plans, name='monthly_plans'),
    path('annual_plans/<int:user_id>', views.annual_plans, name='annual_plans'),
    path('choosen_plan/<int:user_id>/<int:plan_id>', views.choosen_plan, name='choosen_plan'),
    # path('checkout', views.checkout, name='checkout'),
    path('success/<int:user_id>/<int:plan_id>', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('logout/<int:user_id>', views.logout, name='logout'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,  document_root = settings.STATICFILES_DIRS[0])
