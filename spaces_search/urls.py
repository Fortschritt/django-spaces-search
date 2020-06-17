from django.conf.urls import url
from django.urls import path

from spaces.urls import space_patterns
from .views import SearchView

app_name = 'spaces_search'
urlpatterns = (
    path(r'^search/$', SearchView.as_view(), name='search'),
)