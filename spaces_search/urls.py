from django.conf.urls import url
from spaces.urls import space_patterns
from .views import SearchView

app_name = 'spaces_search'
urlpatterns = space_patterns(

    url(r'^search/$', SearchView.as_view(), name='search'),
)