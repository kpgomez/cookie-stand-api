from django.urls import path
from .views import CookieStandList, CookieStandDetail

urlpatterns = [
    path("", CookieStandList.as_view(), name="cookie_stand_list"),
    path("<int:pk>/", CookieStandDetail.as_view(), name="cookie_stand_detail"),
    path("<int:pk>/update/", CookieStandDetail.as_view(), name="cookie_stand_update"), # new
    path("<int:pk>/delete/", CookieStandDetail.as_view(), name="cookie_stand_delete")# new
]
