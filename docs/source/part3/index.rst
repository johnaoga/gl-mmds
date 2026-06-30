.. _part3:

*************************************************************************************************
Partie 3 | TPs & Projet
*************************************************************************************************

Cette partie regroupe les **travaux pratiques** (implémentation) et le **projet
MapReduce** en équipe. Les TP individuels visent à *implémenter* les algorithmes
vus en cours ; le projet à *modéliser et distribuer* un problème avec MapReduce.


TP0 — Word count avec MapReduce (échauffement)
==============================================

Appliquer MapReduce sur une situation simple (**comptage de mots**) sur un grand
corpus (ex. Project Gutenberg, > 1 Go). Objectif : prendre en main le modèle
*map → regroupement → reduce*.


TP1 — Système de recommandation : filtrage collaboratif (item-item top-N)
=========================================================================

**Individuel.** Implémenter le filtrage collaboratif **item-item top-N** (voir
:doc:`chap4 <../part2/chap4>`) avec **Python + Streamlit** (ou **R + Shiny**) :

1. Charger les données (saisie manuelle **obligatoire** ; import CSV en bonus) ;
2. Demander le *n* du top-N et afficher la matrice (notes connues / manquantes) ;
3. Permettre, pour un utilisateur et un film donnés, d'afficher la note (réelle ou
   **prédite**) et la recommandation.

*Livrables : code + déploiement sur le dépôt commun.*


TP1\* — Système de recommandation : facteurs latents
=====================================================

**Individuel.** Implémenter l'approche par **facteurs latents** (factorisation de
la matrice de notes, :doc:`chap4 <../part2/chap4>`) et la comparer au CF item-item.


TP2 — Clustering K-means / Hclust
=================================

**Individuel.** Implémenter **K-means** (et/ou le clustering hiérarchique) sur un
jeu assigné ; déterminer le **K optimal** (méthode du coude) et interpréter les
clusters (voir :doc:`chap3 <../part2/chap3>` et **→ DM**).


TP3 — Apriori (Frequent Itemset Mining)
=======================================

**Individuel.** Implémenter **Apriori** (voir :doc:`chap5 <../part2/chap5>` et
**→ DM**) : à partir d'une base de transactions et d'un seuil, renvoyer les
itemsets fréquents.


Exposés (algorithme avancé)
===========================

**En groupe.** Présenter un **algorithme avancé** (souvent une section du manuel
MMDS non traitée en cours) : (1) **description** de l'algorithme ; (2) un **exemple
concret d'exécution pas-à-pas** (*le plus important*) ; (3) les **cas d'usage**.
~2 h. *(Sujets attribués par l'enseignant ; s'il y a plusieurs algorithmes,
détailler le principal et donner les différences.)*


TP4 — Projet MapReduce (groupe)
===============================

**En groupe.** Modéliser un problème pour l'**exécution parallèle** et
l'implémenter en MapReduce.

**Livrables :** code (**30 %**, sur GitHub) · rapport ≤ 10 pages (**50 %**) ·
vidéo ≤ 5 min (**20 %**). Le rapport doit décrire la **modélisation**
(mappers/reducers), expliquer le code et un **exemple d'exécution** commenté.

**Sujets (un par groupe) :**

.. list-table::
   :header-rows: 1
   :widths: 8 92

   * - #
     - Sujet
   * - 1
     - **Filtrage collaboratif** avec MapReduce (recommandation à grande échelle : *map* des interactions user-item, *reduce* des scores).
   * - 2
     - **Jointures** sur de très grands jeux de données (ex. ventes ⋈ produits) ne tenant pas en mémoire.
   * - 3
     - **FIM distribué** avec MapReduce (plusieurs datasets → retrouver les patterns fréquents globaux — cf. SON, :doc:`chap5 <../part2/chap5>`).
   * - 4
     - **Éléments similaires** distribués (détection de **plagiat** : documents répartis sur un ou plusieurs serveurs).
   * - 5
     - **Plus courts chemins** dans un graphe social (*friend recommendation*).
   * - 6
     - **Plus courts chemins** dans un graphe social (*information spread analysis*).
   * - 7
     - Analyse de structures d'entreprises pour des **stratégies de publicité** sur le web.
   * - 8
     - **PageRank** du graphe du web avec MapReduce (moteur de recherche, :doc:`chap8 <../part2/chap8>`).

.. note::
   Les **dates** de rendu, l'**attribution** des sujets et les **poids** globaux
   d'évaluation sont communiqués par l'enseignant.
