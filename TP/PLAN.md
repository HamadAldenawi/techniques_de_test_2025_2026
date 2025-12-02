# PLAN DE TESTS — Projet Triangulator  


# 1. 🎯 Objectif général

L’objectif de ce plan de tests est de définir toutes les stratégies de validation nécessaires pour garantir la qualité et la robustesse du composant **Triangulator**.  
Ce plan vise à :

- Vérifier la **validité des triangulations** générées.
- S’assurer de la **conversion correcte** entre les formats binaires et les PointSets.
- Tester les **endpoints HTTP** du Triangulator.
- Mesurer les **performances**.
- Gérer les **cas limites** et les erreurs réseau/données.

---

# 2. 🧱 Structure des tests

Le projet est organisé en trois niveaux :
TP/tests/
│
├── unit/ → Tests unitaires
├── integration/ → Tests d’intégration API
└── performance/ → Tests de performance

Les tests sont exécutés automatiquement via **pytest**.

---

# 3. 🧪 Tests unitaires

Les tests unitaires valident chaque composant individuellement.

---

## 3.1 Tests du module PointSet

Objectifs :

- Vérifier la structure (listes de points).
- Valider les méthodes : `__len__`, `__getitem__`, `to_list()`, `as_dict()`, `from_dict()`.
- Test du comportement avec données vides.

Cas testés :

- Création d’un PointSet.
- Accès par indice.
- Conversion en dictionnaire.
- Reconstruction depuis dictionnaire.
- PointSet vide.

---

## 3.2 Tests du module binary (encode/decode)

Objectifs :

- Vérifier l’encodage binaire conformément au format imposé.
- Valider la précision des floats (tolérance `1e-5`).
- Tester les erreurs en cas de buffer trop court ou données corrompues.

Cas testés :

- PointSet vide.
- Un seul point.
- PointSet large (100 points).
- Données corrompues → `ValueError`.
- Type de retour : toujours `bytes`.
- Cohérence du nombre de points.

---

## 3.3 Tests du module triangulation

Objectifs :

- Valider l’algorithme Ear Clipping.
- Tester plusieurs scénarios géométriques.

Cas testés :

- Triangle simple.
- Carré (2 triangles attendus).
- Polygone régulier à 10 points (8 triangles).
- Ordre inversé (CW ↔ CCW).
- Points dupliqués.
- Points alignés.
- Ensemble vide.
- Points aléatoires.

---

# 4. 🌐 Tests d’intégration API

Ces tests vérifient la communication entre :

- le serveur Triangulator (Flask),
- le client PointSetManager (mocké via `monkeypatch`).

Cas testés :

### ✔ 4.1 Endpoint `/`
- Retourne un JSON `"Triangulator running"`.

### ✔ 4.2 Endpoint `/triangulate/<id>`
- Type de retour : `application/octet-stream`.
- Contenu binaire non vide.

### ✔ 4.3 Gestion des erreurs
- ID inexistant → 502.
- Client renvoie `None` → 502.
- JSON mal formé → 502.
- Simulation client cassé → 502.

---

# 5. 🚀 Tests de performance

But : vérifier que la triangulation fonctionne sur des ensembles massifs.

Cas testés :

- Polygone de 1000 points.
- Réalisation rapide et sans crash.
- Marqués avec `@pytest.mark.performance`.

---

# 6. 📊 Outils utilisés

| Outil | Utilité |
|-------|---------|
| **pytest** | Exécution des tests |
| **coverage** | Mesure de couverture |
| **ruff** | Qualité du code |
| **pdoc3** | Génération de documentation HTML |
| **makefile** | Automatisation (Linux/Mac) — sous Windows : commandes directes |

---

# 7. 📌 Critères de validation

- Tous les tests doivent passer (`28 passed`).
- Couverture ≥ **85%** (obtenu : **89%**).
- Algorithme correct pour tous les cas.
- Module binaire robuste aux erreurs.
- API fonctionnelle et stable.
- Documentation générée (`pdoc`).
- Qualité de code conforme (`ruff`).

---

# 8. 🏁 Conclusion

Ce plan définit un ensemble complet de tests couvrant :

- les fonctionnalités internes,
- l’encodage binaire,
- la triangulation,
- les APIs,
- la performance,
- la robustesse aux erreurs.

Le projet a été développé suivant une approche **Test First**, et l’implémentation finale passe tous les tests avec succès.

---


