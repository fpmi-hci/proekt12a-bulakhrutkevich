from django.urls import path

from test_app.views import main_view

urlpatterns = [
   path('', main_view),
]
