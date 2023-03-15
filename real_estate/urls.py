from django.conf.urls.static import static
from django.urls import path

from Rose_House import settings
from real_estate.views import *

urlpatterns = [
                  path('', MainPage.as_view(), name='main-page'),
                  path('filter/<str:filter_attr>/', MainPage.as_view(), name='main-page-filter'),
                  path('show/<int:pk>/', ShowPage.as_view(), name='show-page'),
                  path('show-dev/', ShowDevPage.as_view(), name='show-dev-page'),
                  path('add/', PostEstatePage.as_view(), name='post-page'),
                  path('add-dev/', PostDevPage.as_view(), name='post-dev-page'),
                  path('logout/', LogoutPage.as_view(), name='logout-page'),
                  path('account/', AccountPage.as_view(), name='account-page'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
