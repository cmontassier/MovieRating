<template>
  <v-container>
    <v-card v-if="movie" class="mx-auto my-8" max-width="700">
      <v-card-title>
        <h1>{{ movie.title }}</h1>
      </v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" class="d-flex align-center justify-space-between">
            <strong>Description :</strong>
            <v-btn size="small" color="primary" @click="editDescriptionPopup = true" class="ml-2">Éditer</v-btn>
          </v-col>
          <v-col>
            <v-card class="pa-2" outlined>
              <v-card-text>{{ movie.description }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="12" class="d-flex align-center justify-space-between">
            <strong>Note moyenne :</strong>
            <v-btn color="success" @click="showPopup = true">Ajouter un avis</v-btn>
          </v-col>
          <v-col>
            <v-card class="pa-2" outlined>
              <v-card-text>
                {{ movie.average_grade ? movie.average_grade.toFixed(1) + ' / 5' : 'Aucune note' }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="12" class="d-flex align-center justify-space-between">
            <strong>Acteurs</strong>
            <v-btn size="small" color="primary" @click="editActorPopup = true">Éditer</v-btn>
          </v-col>
          <v-col>
            <v-card class="pa-2" outlined>
              <v-list>
                <v-list-item v-for="actor in movie.actors" :key="actor.id">
                  <v-list-item-title>{{ actor.first_name }} {{ actor.last_name }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn color="secondary" @click="$router.back()" class="ml-2">Retour</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog v-model="editDescriptionPopup" max-width="500">
      <v-card>
        <v-card-title>Modifier la description</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="editDescription">
            <v-textarea v-model="editDescriptionText" label="Nouvelle description" required></v-textarea>
            <v-row justify="end">
              <v-btn color="primary" type="submit">Enregistrer</v-btn>
              <v-btn color="secondary" @click="editDescriptionPopup = false">Annuler</v-btn>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="editActorPopup" max-width="400">
      <v-card>
        <v-card-title>Modifier les acteurs</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item v-for="(actor, idx) in movie.actors" :key="actor.id">
              <v-row align="center">
                <v-col>
                  <v-text-field v-model="movie.actors[idx].first_name" label="Prénom" dense></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field v-model="movie.actors[idx].last_name" label="Nom" dense></v-text-field>
                </v-col>
                <v-col cols="auto">
                  <v-btn icon color="error" @click="removeActor(actor.id)"><v-icon>mdi-delete</v-icon></v-btn>
                </v-col>
              </v-row>
            </v-list-item>
          </v-list>
          <v-row>
            <v-col>
              <v-btn color="primary" @click="addActor">Ajouter un acteur</v-btn>
            </v-col>
          </v-row>
          <v-row justify="end">
            <v-btn color="primary" @click="saveActors">Enregistrer</v-btn>
            <v-btn color="secondary" @click="editActorPopup = false">Annuler</v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showPopup" max-width="400">
      <v-card>
        <v-card-title>Ajouter un avis</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="addReview">
            <v-select
              v-model="newGrade"
              :items="[1, 2, 3, 4, 5]"
              label="Note"
              required
            ></v-select>
            <v-row justify="end">
              <v-btn color="primary" type="submit">Envoyer</v-btn>
              <v-btn color="secondary" @click="showPopup = false">Annuler</v-btn>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { VContainer, VCard, VCardTitle, VCardText, VBtn, VRow, VCol, VList, VListItem, VListItemTitle, VDialog, VForm, VTextField, VTextarea, VSelect, VIcon } from 'vuetify/components';
import axios from 'axios';

export default {
  name: 'FilmDetail',
  components: {
    VContainer,
    VCard,
    VCardTitle,
    VCardText,
    VBtn,
    VRow,
    VCol,
    VList,
    VListItem,
    VListItemTitle,
    VDialog,
    VForm,
    VTextField,
    VTextarea,
    VSelect,
    VIcon
  },
  data() {
    return {
      movie: null,
      newGrade: '',
      showPopup: false,
      editActorPopup: false,
      editActorId: null,
      editActorFirstName: '',
      editActorLastName: '',
      editDescriptionPopup: false,
      editDescriptionText: ''
    };
  },
  mounted() {
    this.fetchMovie();
  },
  methods: {
    fetchMovie() {
      const id = this.$route.params.id;
      axios.get(`http://localhost:8000/api/movies/${id}/`)
        .then(response => {
          this.movie = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addReview() {
      const id = this.$route.params.id;
      axios.post('http://localhost:8000/api/reviews/', {
        grade: this.newGrade,
        movie: id
      })
      .then(() => {
        this.newGrade = '';
        this.showPopup = false;
        this.fetchMovie();
      })
      .catch(error => {
        alert('Erreur lors de l\'ajout de l\'avis');
        console.error(error);
      });
    },
    openEditActor(actor) {
      this.editActorId = actor.id;
      this.editActorFirstName = actor.first_name;
      this.editActorLastName = actor.last_name;
      this.editActorPopup = true;
    },
    addActor() {
      this.movie.actors.push({ first_name: '', last_name: '' });
    },
    removeActor(id) {
      this.movie.actors = this.movie.actors.filter(actor => actor.id !== id);
    },
    saveActors() {
      const id = this.$route.params.id;
      // Update existing actors
      const updatePromises = this.movie.actors.filter(a => a.id).map(actor =>
        axios.patch(`http://localhost:8000/api/actors/${actor.id}/`, {
          first_name: actor.first_name,
          last_name: actor.last_name
        })
      );
      // Add new actors
      const addPromises = this.movie.actors.filter(a => !a.id && a.first_name && a.last_name).map(actor =>
        axios.post('http://localhost:8000/api/actors/', {
          first_name: actor.first_name,
          last_name: actor.last_name,
          movie: id
        })
      );
      Promise.all([...updatePromises, ...addPromises])
        .then(() => {
          this.editActorPopup = false;
          setTimeout(() => this.fetchMovie(), 300);
        })
        .catch(error => {
          alert('Erreur lors de la modification des acteurs');
          console.error(error);
        });
    },
    editActor() {
      axios.patch(`http://localhost:8000/api/actors/${this.editActorId}/`, {
        first_name: this.editActorFirstName,
        last_name: this.editActorLastName
      })
      .then(() => {
        this.editActorPopup = false;
        this.fetchMovie();
      })
      .catch(error => {
        alert('Erreur lors de la modification de l\'acteur');
        console.error(error);
      });
    },
    editDescription() {
      const id = this.$route.params.id;
      axios.patch(`http://localhost:8000/api/movies/${id}/`, {
        description: this.editDescriptionText
      })
      .then(() => {
        this.editDescriptionPopup = false;
        this.fetchMovie();
      })
      .catch(error => {
        alert('Erreur lors de la modification de la description');
        console.error(error);
      });
    }
  },
  watch: {
    editDescriptionPopup(val) {
      if (val) {
        this.editDescriptionText = this.movie ? this.movie.description : '';
      }
    }
  }
};
</script>

<style scoped>
</style>
