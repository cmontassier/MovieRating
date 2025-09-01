import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './HomePage.vue';
import FilmDetail from './MovieDetailled.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/film/:id', component: FilmDetail, name: 'FilmDetail' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
