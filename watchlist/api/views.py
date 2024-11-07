from django.shortcuts import render
from watchlist.models import WatchList, StreamPlatform, Review
from django.http import JsonResponse
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist.api.permissions import UserWriteAndAllRead, AdminOrReadOnly
# Create your views here.


class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class WatchListDetails(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"message": "resource deleted"})
    
class StreamPlatformList(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        streamPlatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamPlatform, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
class StreamPlatformDetails(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        try:
            streamPlatform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error": "Stream platform not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(streamPlatform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        streamPlatform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streamPlatform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        streamPlatform = StreamPlatform.objects.get(pk=pk)
        streamPlatform.delete()
        return Response({"message": "resource deleted"})
        

class StreamViewset(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # def list(self, request):
    #     streamPlatform = StreamPlatform.objects.all()
    #     serializer = StreamPlatformSerializer(streamPlatform, many = True)
    #     return Response(serializer.data)
    
    # def retrive(self, request, pk=None):
    #     try:
    #         streamPlatform = StreamPlatform.objects.get(pk=pk)
    #     except StreamPlatform.DoesNotExist:
    #         return Response({"error": "Stream platform not found"}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = StreamPlatformSerializer(streamPlatform)
    #     return Response(serializer.data)
        

        
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Review.objects.filter(watchlist = pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserWriteAndAllRead]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    # def get_queryset(self):
    #     return Review.objects.get(pk=self.kwargs['pk'])

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        watchlist = WatchList.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        if Review.objects.filter(watchlist=watchlist, reviewer = user).exists():
            raise ValidationError("You have already reviewed this movie")
            
        serializer.save(watchlist=watchlist, reviewer = user)
        

        
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        # username = self.kwargs["username"]
        reviews = Review.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            reviews = reviews.filter(reviewer__username=username)
        return reviews
        
    
        


# @api_view(['GET', 'POST'])
# def movies_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many = True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         movie.delete()
#         return Response({"message": "resource deleted"})