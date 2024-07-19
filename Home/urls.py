# Home/urls.py

from django.urls import path
from .views import get_rss_urls, get_rss_data, add_rss_url, skills_view

urlpatterns = [
    path('rss-urls/', get_rss_urls, name='get_rss_urls'),
    path('rss-data/', get_rss_data, name='get_rss_data'),
    path('add-rss-url/', add_rss_url, name='add_rss_url'),
    path('skills/', skills_view, name='skills_view'),

]
