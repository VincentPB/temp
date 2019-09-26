# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from .views import GeneratePDF
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/dashboard', permanent=False), name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^management$', views.management, name='management'),
    url(r'^management/change$', views.set_permission, name='set_permission'),
    url(r'^perimetre/add$', views.create_perimetre, name='create_perimetre'),
    url(r'^perimetre/([0-9]+)$', views.view_perimetre, name='view_perimetre'),
    url(r'^perimetre/edit/([0-9]+)$', views.edit_perimetre, name='edit_perimetre'),
    url(r'^vulnerability/add/([0-9]+)$', views.create_vulnerability,
name='create_vulnerability'),
    url(r'^vulnerability/([0-9]+)/([0-9]+)$', views.view_vulnerability,
name='view_vulnerability'),
    url(r'^vulnerability/edit/([0-9]+)/([0-9]+)$', views.edit_vulnerability,
name='edit_vulnerability'),
url(r'^generate/pdf/([0-9]+)$', views.html_to_pdf_view, name='generate_pdf'),
url(r'^pdf/([0-9]+)$', GeneratePDF.as_view()),
]
