.. _part2_chap7:

***********************************************************************
Chapitre 7 : Mining de graphes
***********************************************************************

Les **graphes** (réseaux sociaux, web, interactions) sont au cœur du big data. On
s'intéresse ici à deux tâches : **détecter les communautés** (Girvan-Newman) et
**mesurer la similarité de nœuds** (SimRank).

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Dérouler **Girvan-Newman** (détection de communautés par *betweenness*)
- Dérouler **SimRank** (similarité de nœuds par marche aléatoire)


1. Girvan-Newman (détection de communautés)
===========================================

**Idée** : les arêtes **entre** communautés sont traversées par beaucoup de plus
courts chemins. On retire itérativement les arêtes de plus forte
**intermédiarité** (*edge betweenness*) pour faire apparaître les communautés.

La **betweenness** d'une arête = nombre de paires de nœuds dont un plus court chemin
emprunte cette arête (créditée fractionnellement quand il y a plusieurs plus courts
chemins).

**Algorithme :**

1. Calculer la **betweenness** de **toutes** les arêtes (BFS depuis chaque nœud :
   comptage des plus courts chemins descendant, puis crédit remontant).
2. **Retirer** l'arête de betweenness maximale.
3. **Recalculer** les betweenness des arêtes restantes.
4. Répéter : le graphe se **scinde** progressivement en composantes = communautés.

On obtient une **hiérarchie** de communautés (comme un dendrogramme) ; on choisit le
niveau de coupe (souvent via la **modularité**).


2. SimRank (similarité de nœuds)
================================

**Idée** : « deux nœuds sont similaires s'ils sont **référencés par des nœuds
similaires** ». C'est une définition **récursive**, évaluée par **marche aléatoire**.

.. math::

   s(a, b) = \frac{C}{|I(a)|\,|I(b)|} \sum_{u \in I(a)} \sum_{v \in I(b)} s(u, v)

où :math:`I(x)` = voisins entrants de *x*, et :math:`C \in (0,1)` un facteur
d'atténuation ; avec :math:`s(a,a) = 1`.

**Algorithme** (itératif) : initialiser :math:`s(a,b)=1` si :math:`a=b`, sinon 0 ;
puis **itérer** la formule jusqu'à convergence. (Interprétation : *expected meeting
distance* de deux marcheurs aléatoires remontant les arêtes.) Utilisé pour la
recommandation, la désambiguïsation, la recherche de pages liées.


3. Autres (brève description)
=============================

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Méthode
     - Idée
   * - **Modularité (Louvain)**
     - Optimiser la **modularité** par fusions locales — très **scalable** (≫ Girvan-Newman).
   * - **Clustering spectral**
     - Utiliser les **valeurs/vecteurs propres** du laplacien du graphe pour partitionner.
   * - **Comptage de triangles / clustering coefficient**
     - Mesurer la cohésion locale (souvent en MapReduce).
   * - **Plus courts chemins en MapReduce**
     - BFS distribué (cf. *friend recommendation*, **TP4**).


Exercices
=========

.. admonition:: Exercice 1 — Betweenness
   :class: tip

   Dans un graphe « haltère » (deux triangles A-B-C et D-E-F reliés par l'unique
   arête **C–D**), quelle arête a la plus forte betweenness, et pourquoi
   Girvan-Newman la retire-t-il en premier ?

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

L'arête **C–D** : c'est le **seul pont** entre les deux groupes, donc **tous** les
plus courts chemins reliant un nœud de {A,B,C} à un nœud de {D,E,F} passent par
elle → betweenness maximale. La retirer **sépare** le graphe en ses deux
communautés naturelles.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — SimRank
   :class: tip

   Pourquoi SimRank est-il défini de façon **récursive**, et que représente le
   facteur :math:`C` ?

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

Parce que la similarité de deux nœuds dépend de celle de leurs voisins, qui
dépend à son tour de la leur, etc. — d'où une définition récursive résolue par
itérations jusqu'au point fixe. Le facteur :math:`C \in (0,1)` **atténue** la
contribution des voisins éloignés (sinon la similarité « se propagerait » sans
décroître) ; il garantit la convergence et reflète que la similarité **décroît**
avec la distance.

.. raw:: html

   </details>
