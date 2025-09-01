from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from movie.models import Movie, Actor, Review

class ActorModelTest(TestCase):
    def test_str(self):
        actor = Actor.objects.create(first_name='John', last_name='Doe')
        self.assertEqual(str(actor), 'John Doe')

class MovieModelTest(TestCase):
    def test_str(self):
        movie = Movie.objects.create(title='Test Movie', description='A test movie.')
        self.assertEqual(str(movie), 'Test Movie')

class ReviewModelTest(TestCase):
    def test_create_review(self):
        movie = Movie.objects.create(title='Test Movie', description='A test movie.')
        review = Review.objects.create(grade=5, movie=movie)
        self.assertEqual(review.grade, 5)
        self.assertEqual(review.movie, movie)

class MovieAPITest(APITestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name='John', last_name='Doe')
        self.movie = Movie.objects.create(title='Test Movie', description='A test movie.')
        self.movie.actors.add(self.actor)
        self.review = Review.objects.create(grade=4, movie=self.movie)

    def test_list_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Movie')

    def test_create_movie(self):
        url = reverse('movie-list')
        data = {'title': 'New Movie', 'description': 'Desc'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_actors(self):
        url = reverse('actor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_list_reviews(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['grade'], 4)
