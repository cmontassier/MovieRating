from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from movie.models import Movie, Actor, Review

class ActorModelTest(TestCase):
    def test_str(self):
        actor = Actor.objects.create(first_name='xxxxx', last_name='yyyyy')
        self.assertEqual(str(actor), 'xxxxx yyyyy')

class MovieModelTest(TestCase):
    def test_str(self):
        movie = Movie.objects.create(title='xxxxx', description='yyyyy')
        self.assertEqual(str(movie), 'xxxxx')

class ReviewModelTest(TestCase):
    def test_create_review(self):
        movie = Movie.objects.create(title='xxxxx', description='yyyyy')
        review = Review.objects.create(grade=5, movie=movie)
        self.assertEqual(review.grade, 5)
        self.assertEqual(review.movie, movie)

class MovieAPITest(APITestCase):
    def setUp(self):
        self.actor1 = Actor.objects.create(first_name='xxxxx', last_name='yyyyy')
        self.actor2 = Actor.objects.create(first_name='zzzzz', last_name='wwwww')
        self.movie = Movie.objects.create(title='xxxxx', description='yyyyy')
        self.movie.actors.add(self.actor1)
        self.movie.actors.add(self.actor2)
        self.review = Review.objects.create(grade=4, movie=self.movie)

    def test_list_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'xxxxx')
        self.assertEqual(len(response.data[0]['actors']), 2)
        self.assertEqual(response.data[0]['actors'][0]['first_name'], 'xxxxx')

    def test_create_movie(self):
        url = reverse('movie-list')
        data = {
            'title': 'aaaaa',
            'description': 'qwerty',
            'actors': [self.actor2.pk]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'aaaaa')
        self.assertTrue(any(actor['id'] == self.actor2.pk for actor in response.data['actors']))

    def test_list_actors(self):
        url = reverse('actor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'xxxxx')
        self.assertEqual(response.data[1]['first_name'], 'zzzzz')

    def test_add_actor_to_movie(self):
        url = reverse('movie-detail', args=[self.movie.pk])
        data = {
            'actors': [self.actor1.pk, self.actor2.pk]
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['actors']), 2)

    def test_remove_actor_from_movie(self):
        url = reverse('movie-detail', args=[self.movie.pk])
        data = {
            'actors': []
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['actors']), 2)

    def test_list_reviews(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['grade'], 4)

    def test_add_review(self):
        url = reverse('review-list')
        data = {'grade': 5, 'movie': self.movie.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['grade'], 5)
