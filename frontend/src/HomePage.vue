<template>
  <v-container>
    <h1>Liste des films</h1>
    <v-data-table
      :headers="headers"
      :items="movies"
      :items-per-page="pageSize"
      class="elevation-1"
    >
      <template #item="{ item }">
        <tr @click="goToDetail(item)" style="cursor:pointer;">
          <td>{{ item.title }}</td>
          <td>{{ item.average_grade ? item.average_grade.toFixed(2) : 'Aucune note' }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import axios from 'axios';
import { VDataTable, VContainer, VRow, VBtn } from 'vuetify/components';

export default {
  name: 'HomePage',
  components: {
    VDataTable,
    VContainer,
    VRow,
    VBtn
  },
  data() {
    return {
      movies: [],
      pageSize: 5,
      headers: [
        { text: 'Titre', value: 'title' },
        { text: 'Note moyenne', value: 'average_grade' }
      ]
    };
  },
  methods: {
    goToDetail(item) {
      if (item && item.id) {
        this.$router.push({ name: 'FilmDetail', params: { id: item.id } });
      }
    }
  },
  mounted() {
    axios.get('http://localhost:8000/api/movies/')
      .then(response => {
        // Always set movies as an array
        this.movies = Array.isArray(response.data) ? response.data : [response.data];
        console.log('Movies set to:', this.movies);
      })
      .catch(error => {
        console.error(error);
      });
  }
};
</script>
