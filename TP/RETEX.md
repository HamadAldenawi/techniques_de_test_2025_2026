
# 1. Contexte du projet

Le projet consiste à développer un micro-service appelé **Triangulator**, chargé de :

- récupérer un **PointSet** depuis un PointSetManager,
- effectuer une **triangulation** (Ear-Clipping),
- renvoyer un **fichier binaire** contenant les points et les triangles,
- fournir une API HTTP accessible via `/triangulate/<id>`.

L’objectif principal du TP est d’appliquer une démarche **Test First** et d’implémenter progressivement toutes les fonctionnalités autour d’un environnement de tests complet.

---

# 2. Ce qui a été réalisé

## 2.1 Implémentation Logicielle
Le projet complet inclut :

### 🔹 Triangulator
- `server.py` : expose l’API HTTP.
- `client_psm.py` : récupère un PointSet auprès du PSM.
- `binary.py` : encode/décode les PointSets et Triangulations au format binaire.
- `triangulation.py` : algorithme Ear-Clipping + gestion des cas spéciaux.

### 🔹 PointSetManager (simulé)
- Création / récupération de PointSets.
- Stockage mémoire simple.

### 🔹 Documentation générée automatiquement
- via `pdoc3` → HTML placé dans `/docs`.

### 🔹 Qualité du code
- Linting automatisé : `ruff`
- Tests automatisés : `pytest`
- Couverture : `coverage`

---

# 3.  Mise en place des tests

## 3.1 Tests unitaires
Situés dans `TP/tests/unit/` :

- **PointSet**
  - accès indexé, conversion dict → objet.
- **binary**
  - encode/decode sur petits et grands PointSets.
  - tolérance float32 vs float64.
  - tests d’erreurs sur buffer corrompu.
- **triangulation**
  - triangle simple, carré, polygone régulier, points dupliqués, points alignés.
  - stabilité avec points aléatoires.

## 3.2 Tests d’intégration
Situés dans `TP/tests/integration/test_api.py` :

- Test de l’endpoint `/`
- Test de `/triangulate/<id>`
- Simulation du PSM via `monkeypatch`
- Gestion des erreurs :
  - ID inexistant → 502
  - client cassé → 502
  - JSON invalide → 502

## 3.3 Tests de performance
Situés dans `TP/tests/performance/test_perf.py` :

- Triangulation sur polygone de 1000 points.
- Exécution rapide sans crash.

---

# 4.  Points positifs

- **Méthodologie Test First** respectée du début à la fin.
- **28 tests automatiques**, tous passés avec succès.
- **Couverture 89%**, largement au-dessus de ce qui est attendu.
- **API claire et robuste**, gestion correcte des erreurs.
- **Encodage binaire fiable**, conforme aux spécifications.
- **Triangulation stable**, même dans cas limites.
- **Structure propre**, lisible, bien organisée.
- Documentation générée automatiquement (pdoc) → professionnalisme.

---

# 5. Difficultés rencontrées

### 5.1 Précision des flottants
L’encodage utilise **float32**, alors que Python utilise float64.  
Cela crée de très légères différences → nécessité d’utiliser une **tolérance 1e-5** dans les tests.

### 5.2 Cas dégénérés
- Points alignés
- Points dupliqués  
Le Ear-Clipping classique échoue dans ces cas → ajout d’un **fallback** de triangulation simple.

### 5.3 Tests d’intégration
Le PSM n’étant pas réellement lancé, j’ai dû utiliser `monkeypatch` pour simuler son comportement dans les tests → évite les dépendances réseau.

### 5.4 Gestion du binaire
L'encodage/décodage binaire demande rigueur (struct pack/unpack) → erreurs difficiles à débugger au début.

---

# 6.  Ce que j’aurais fait différemment

- Ajouter une **vraie base de données** pour le PSM (ex. SQLite).
- Implémenter une triangulation plus avancée (ex : **Delaunay**).
- Ajouter des **tests de charge concurrentiels** (ex : Locust).
- Ajouter un mode CI (Github Actions) pour exécuter automatiquement :
  - tests
  - linting
  - couverture
- Ajouter un outil de calcul de performance mémoire.

---

# 7.  Instructions pour exécuter le projet

```bash
# 1. Créer un venv
python -m venv .venv

# 2. Activer venv
.\.venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
pip install -r dev_requirements.txt

# 4. Lancer les tests
pytest -q

# 5. Générer la documentation
pdoc --html TP -o docs --force

# 6. Lancer Triangulator
python -m TP.triangulator.server
