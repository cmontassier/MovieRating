from rest_framework import serializers
from .models import Movie, Review, Actor

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'grade', 'movie']

class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_grade = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'actors', 'reviews', 'average_grade']

    def get_average_grade(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum([r.grade for r in reviews]) / reviews.count()
        return None
