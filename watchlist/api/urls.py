from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (WatchListAV, WatchListDetails, StreamPlatformList, StreamPlatformDetails,
                    StreamViewset, ReviewList, ReviewDetail, ReviewCreate,UserReview)

router = DefaultRouter()
router.register('stream', StreamViewset, basename='stream')
urlpatterns = [
    path('list/', WatchListAV.as_view(), name="watch_list"),
    path('', include(router.urls)),
    path('list/<int:pk>/', WatchListDetails.as_view(), name="watch_details"),
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')
    path('list/<int:pk>/review-create/', ReviewCreate.as_view(), name="review-create"),
    path('list/<int:pk>/review/', ReviewList.as_view(), name="review-list"),
    path('list/review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
    path("review/", UserReview.as_view(), name="user-reviews"),
    
]
# urlpatterns+=router.urls
