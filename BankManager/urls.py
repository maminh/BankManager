"""BankManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import authentication, permissions
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('transaction/', include('transactions.urls')),
    path('docs/', include_docs_urls(title='Bank API',
                                    description='User JSON authentication only (scheme value is JWT)',
                                    authentication_classes=(authentication.BasicAuthentication,),
                                    permission_classes=(permissions.IsAdminUser,),
                                    schema_url=f'{settings.HOST_NAME}:{settings.HOST_PORT}',
                                    )
         ),
]
