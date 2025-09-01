from django.shortcuts import render
from rest_framework import viewsets
from .models import Movie, Review, Actor
from .serializers import MovieSerializer, ReviewSerializer, ActorSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        movie_id = response.data.get('id')
        actors = request.data.get('actors', [])
        if movie_id and actors:
            actor_pks = [actor['id'] if isinstance(actor, dict) and 'id' in actor else actor for actor in actors]
            movie = Movie.objects.get(pk=movie_id)
            movie.actors.set(actor_pks)
            movie.save()
            serializer = self.get_serializer(movie)
            response.data.update(serializer.data)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        movie_id = response.data.get('id')
        actors = request.data.get('actors', [])
        if movie_id is not None and actors is not None:
            actor_pks = [actor['id'] if isinstance(actor, dict) and 'id' in actor else actor for actor in actors]
            movie = Movie.objects.get(pk=movie_id)
            movie.actors.set(actor_pks)
            movie.save()
            serializer = self.get_serializer(movie)
            response.data.update(serializer.data)
        return response


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        review_id = response.data.get('id')
        movie_pk = request.data.get('movie')
        if review_id and movie_pk:
            review = Review.objects.get(pk=review_id)
            movie = Movie.objects.get(pk=movie_pk)
            review.movie = movie
            review.save()
            serializer = self.get_serializer(review)
            response.data.update(serializer.data)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        review_id = response.data.get('id')
        movie_pk = request.data.get('movie')
        if review_id and movie_pk:
            review = Review.objects.get(pk=review_id)
            movie = Movie.objects.get(pk=movie_pk)
            review.movie = movie
            review.save()
            serializer = self.get_serializer(review)
            response.data.update(serializer.data)
        return response

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        actor_id = response.data.get('id')
        movie_pk = request.data.get('movie')
        if actor_id and movie_pk:
            actor = Actor.objects.get(pk=actor_id)
            movie = Movie.objects.get(pk=movie_pk)
            movie.actors.add(actor)
            movie.save()
            serializer = self.get_serializer(actor)
            response.data.update(serializer.data)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        actor_id = response.data.get('id')
        movie_pk = request.data.get('movie')
        if actor_id and movie_pk:
            actor = Actor.objects.get(pk=actor_id)
            movie = Movie.objects.get(pk=movie_pk)
            movie.actors.add(actor)
            movie.save()
            serializer = self.get_serializer(actor)
            response.data.update(serializer.data)
        return response
