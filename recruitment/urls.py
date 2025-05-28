from django.urls import path

from .views import CandidateSearchView, CandidateView

urlpatterns = [
    path("candidates", CandidateView.as_view(), name="candidate-list-create"),
    path("candidates/<int:pk>", CandidateView.as_view(), name="candidate-detail"),
    path("candidates/search", CandidateSearchView.as_view(), name="candidate-search"),
]
