from django.urls import path

from score.views import add_website, get_pdf

urlpatterns = [
    path('add-website', add_website, name="add-website"),
    path('pdf-report/<url>', get_pdf, name="pdf-report"),
]
