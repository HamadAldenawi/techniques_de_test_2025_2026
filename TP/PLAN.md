# TODO
# PLAN DE TESTS - Triangulator

## Objectif
L'objectif de ce plan de tests est de définir les différentes étapes pour valider le composant **Triangulator**, en s'assurant de :
- la **justesse des triangulations** calculées,
- la **récupération correcte des PointSets** depuis le PointSetManager,
- la **conformité aux API exposées**,
- les **performances** et la **stabilité** du service,
- la gestion correcte des **cas limites et erreurs**.

---

## Types de tests

### 1. Tests unitaires
Les tests unitaires permettront de vérifier les fonctionnalités fondamentales du Triangulator sans dépendre des autres composants.

#### 1.1 Conversion PointSet ↔ format binaire
- Vérifier que la fonction de **serialisation** transforme correctement un ensemble de points en bytes.
- Vérifier que la fonction de **désérialisation** reconstruit exactement le PointSet original.
- Cas à tester :
  - 0 points
  - 1 point
  - 10 points aléatoires
  - Points avec coordonnées négatives ou décimales

#### 1.2 Conversion Triangles ↔ format binaire
- Vérifier que les triangles peuvent être convertis en bytes et récupérés correctement.
- Cas à tester :
  - Un triangle simple
  - Plusieurs triangles avec des sommets partagés
  - Cas limite : triangles avec indices identiques ou invalides

#### 1.3 Algorithme de triangulation
- Vérifier que l'algorithme renvoie des triangles corrects pour :
  - un triangle simple (3 points)
  - 4 ou 5 points formant un polygone simple
  - points aléatoires (10 à 100 points)
  - points alignés horizontalement ou verticalement (cas limite)
  - points identiques (duplicated points)

- Vérifier que :
  - Tous les indices des triangles sont valides
  - Aucun triangle n'a des sommets en dehors du PointSet
  - Les triangles couvrent bien l'ensemble des points

---

### 2. Tests d'intégration API
Ces tests permettent de vérifier la communication entre le Triangulator et le PointSetManager via les API HTTP.

#### 2.1 Récupération de PointSet
- Tester GET `/point_set/{id}` pour :
  - ID existant → renvoie le PointSet correct
  - ID inexistant → renvoie une erreur 404
  - ID invalide (string au lieu de number) → renvoie une erreur 400

#### 2.2 Triangulation via POST
- Tester POST `/triangulator` avec un PointSetID valide → renvoie les triangles corrects
- Tester POST avec ID inexistant → renvoie une erreur 404
- Tester POST avec PointSet vide → vérifier comportement (erreur ou triangle vide)
- Tester POST avec données mal formées → renvoie erreur 400

#### 2.3 Cas limites API
- Vérifier que le service ne plante pas si plusieurs requêtes concurrentes sont envoyées
- Vérifier que les indices des triangles correspondent toujours au PointSet envoyé

---

### 3. Tests de performance
- Mesurer le temps de conversion PointSet ↔ bytes pour :
  - 10, 100, 1000, 10000 points
- Mesurer le temps de triangulation pour :
  - 10 points, 100 points, 1000 points
- Vérifier que le service ne plante pas et ne dépasse pas des temps raisonnables (ex. < 1s pour 1000 points)
- Vérifier la consommation mémoire sur de grands ensembles

---

### 4. Autres tests
- Cas limites et robustesse :
  - PointSet vide (0 point)
  - PointSet avec 1 point
  - Tous les points identiques
  - Points alignés (tous sur une ligne horizontale ou verticale)
- Vérifier que la sortie Triangles est cohérente :
  - Aucun triangle avec des indices hors PointSet
  - Aucune duplication inutile
  - Respect de la topologie (triangles connectés correctement)

---

## Notes de méthodologie
- **Test First** : écrire les tests avant l’implémentation
- **Automatisation** : tous les tests seront exécutables avec `pytest`
- **Différenciation** : tests unitaires, intégration et performance séparés pour exécution ciblée
- **Documentation** : chaque test doit être commenté et expliquer ce qu’il vérifie
- **Couverture** : s'assurer que toutes les fonctions importantes sont couvertes par au moins un test
