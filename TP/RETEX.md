# RETEX - Triangulator (TP)

## Contexte
Ce projet implémente un micro-service de triangulation (`Triangulator`) qui récupère des ensembles de points depuis un `PointSetManager` et renvoie une représentation binaire des triangles calculés. L'objectif du TP est d'appliquer la méthodologie *Test First*, d'écrire des tests unitaires, d'intégration et des tests de performance, puis de fournir une implémentation correcte et documentée.

## Ce qui a été fait
- Implémentation complète du Triangulator :
  - `TP/triangulator/server.py` : API HTTP exposée (`/triangulate/<id>`).
  - `TP/triangulator/client_psm.py` : client simple pour récupérer le PointSet auprès du PSM.
  - `TP/triangulator/binary.py` : encode/decode PointSet et Triangles au format binaire.
  - `TP/triangulator/triangulation.py` : algorithme de triangulation (ear-clipping + fallback pour points alignés).
- Implémentation du PointSetManager en mémoire (`TP/point_set_manager`) avec endpoints pour créer et récupérer PointSet.
- Tests :
  - Tests unitaires (`TP/tests/unit/*`) : `PointSet`, encodage binaire, triangulation, décodage.
  - Tests d'intégration (`TP/tests/integration/test_api.py`) : simulation du PSM via monkeypatch.
  - Tests de performance (`TP/tests/performance/test_perf.py`) : triangulation sur grands ensembles.
- Makefile, pytest.ini, requirements.txt et dev_requirements.txt fournis.
- Documentation (pdoc3) générée depuis le code.

## Points positifs
- Approche **test-driven** respectée : tous les tests écrits et exécutables via `pytest`.
- Couverture des cas limites : PointSet vide, points alignés, points dupliqués.
- Interface HTTP simple et documentée (OpenAPI yaml fournie).
- Encodage binaire conforme à la spécification du sujet (point count + float32 pour chaque coordonnée).
- Triangulation robuste : ear-clipping pour polygones simples et fallback pour cas dégénérés.

## Difficultés rencontrées
- Gestion des valeurs flottantes : encodage en float32 provoque de petites différences numériques — tests adaptés avec tolérance.
- Cas dégénérés (points alignés ou non-simple) : l'algorithme ear-clipping peut échouer ; ajout d'un fallback simple pour couvrir ces cas pour le TP.
- Communication inter-service lors des tests : nécessité d'utiliser monkeypatch pour simuler le PointSetManager dans les tests d'intégration afin d'éviter dépendance réseau.

## Ce que j'aurais fait différemment
- Ajouter une persistance (SQLite) pour le PointSetManager pour tests plus réalistes.
- Tests de concurrence plus poussés (utiliser locust ou pytest-xdist).
- Implémenter un algorithme de triangulation plus complet (Delaunay) si le temps le permettait.
- Mesures mémoire plus précises pour très grands ensembles.

## Instructions pour exécuter le projet
1. Créer/activer un venv :
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r dev_requirements.txt
