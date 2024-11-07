from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ("watchlist",)

class WatchListSerializer(serializers.ModelSerializer):
    # length_name = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many = True, read_only = True)
    platform = serializers.CharField(source = 'platform.name')
    avg_rating = serializers.SerializerMethodField()
    number_rating = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = "__all__"
    def get_number_rating(self, object):
        return object.reviews.count()
    def get_avg_rating(self, object):
        average = object.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return average if average is not None else 0
    

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many = True, read_only = True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
    
    # def get_length_name(self, object):
    #     return len(object.name)
   
    # def validate_name(self, value):
    #     if len(value)<3:
    #         raise serializers.ValidationError("Name is too short")
    #     return value
    
    # def validate(self, object):
    #     if object["name"]==object["description"]:
    #         raise serializers.ValidationError("Description and name should be different")
    #     return object 
    

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.active = validated_data.get("active", instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):
#         if len(value)<3:
#             raise serializers.ValidationError("Name is too short")
#         return value
    
#     def validate(self, object):
#         if object["name"]==object["description"]:
#             raise serializers.ValidationError("Description and name should be different")
#         return object