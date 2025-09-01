# Movie Rating App

## Démarrage rapide avec Docker Compose

**Lancer uniquement les services backend, frontend et db**
```sh
docker-compose up --build backend frontend db
```
Cela démarre :
- Le backend Django (API, admin)
- Le frontend Vue.js
- La base de données PostgreSQL

**Accéder à l'application**
- Frontend : [http://localhost:8080](http://localhost:8080)
- API backend : [http://localhost:8000/api/](http://localhost:8000/api/)
- Admin Django : [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Gestion et administration
- Ajoutez/modifiez des films, acteurs et avis via l'interface web ou l'admin Django.
- Les fichiers statiques et la base de données sont gérés automatiquement par Docker.

## Lancer les tests backend avec Docker Compose
```sh
docker-compose run --rm backend python manage.py test
```

## Problèmes courants
- Si vous avez des soucis de volumes ou de fichiers statiques, essayez :
  ```sh
  docker-compose down -v
  docker-compose up --build backend frontend db
  ```

## Configuration
- Les variables d'environnement sont définies dans les fichiers `.env` du backend et du frontend.

## Licence
MIT