from django.db.models import Count, F, Q
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.views import APIView

from .models import Candidate
from .serializers import CandidateSerializer
from .utils import api_response


class CandidateView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                candidate = Candidate.objects.get(pk=pk)
                serializer = CandidateSerializer(candidate)
                return api_response(
                    code=status.HTTP_200_OK, message="Candidate retrieved successfully", data=serializer.data
                )
            except Candidate.DoesNotExist:
                return api_response(code=status.HTTP_404_NOT_FOUND, message="Candidate not found", data=None)

        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return api_response(code=status.HTTP_200_OK, message="Candidates retrieved successfully", data=serializer.data)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                code=status.HTTP_201_CREATED, message="Candidate created successfully", data=serializer.data
            )
        return api_response(code=status.HTTP_400_BAD_REQUEST, message="Invalid data provided", data=serializer.errors)

    def put(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return api_response(
                    code=status.HTTP_200_OK, message="Candidate updated successfully", data=serializer.data
                )
            return api_response(
                code=status.HTTP_400_BAD_REQUEST, message="Invalid data provided", data=serializer.errors
            )
        except Candidate.DoesNotExist:
            return api_response(code=status.HTTP_404_NOT_FOUND, message="Candidate not found", data=None)

    def delete(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            candidate.delete()
            return api_response(code=status.HTTP_204_NO_CONTENT, message="Candidate deleted successfully", data=None)
        except Candidate.DoesNotExist:
            return api_response(code=status.HTTP_404_NOT_FOUND, message="Candidate not found", data=None)


class CandidateSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("query", None)
        if not query:
            return api_response(code=status.HTTP_200_OK, message="No search query provided", data=[])

        # Split the search query into words
        search_words = query.lower().split()

        # Create a Q object for each word to search in name field
        q_objects = Q()
        for word in search_words:
            q_objects |= Q(name__icontains=word)

        # Get candidates that match any of the words
        candidates = Candidate.objects.filter(q_objects)

        # Annotate with match counts for each word in name
        annotations = {f"match_{word}": Count("id", filter=Q(name__icontains=word)) for word in search_words}

        # Apply all match annotations in a single call
        candidates = candidates.annotate(**annotations)

        # Build total_matches using Coalesce to avoid None
        total_match_expr = sum(Coalesce(F(f"match_{word}"), 0) for word in search_words)

        candidates = candidates.annotate(total_matches=total_match_expr)

        # Order by relevance, ID, and name
        candidates = candidates.order_by("-total_matches", "id", "name")

        serializer = CandidateSerializer(candidates, many=True)
        return api_response(
            code=status.HTTP_200_OK, message="Search results retrieved successfully", data=serializer.data
        )
