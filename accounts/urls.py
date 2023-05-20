# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from accounts import viewsets as account_views


router = DefaultRouter()


router.register('accounts', account_views.UserProfileViewset, basename='user')

urlpatterns = []

urlpatterns = router.urls
