.. _part2_chap8:

***********************************************************************
Chapitre 8 : Link analysis (PageRank)
***********************************************************************

**PageRank** classe les pages du web par **importance**, en exploitant la
structure des **liens**. C'est l'algorithme fondateur de Google.

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Définir le PageRank comme la distribution stationnaire d'une marche aléatoire
- Le calculer par **itération de la puissance** (avec téléportation)
- Comprendre le rôle du calcul **MapReduce** pour le passage à l'échelle


1. Idée et formulation
======================

Modèle du **surfeur aléatoire** : il suit un lien au hasard depuis la page
courante. Le **PageRank** d'une page = la probabilité (stationnaire) de s'y
trouver. Une page est importante si elle est pointée par des pages importantes :

.. math::

   r_j = \sum_{i \rightarrow j} \frac{r_i}{d_i}

où :math:`d_i` = nombre de liens sortants de *i*. Sous forme matricielle
:math:`r = M r` (où *M* est la matrice de transition colonne-stochastique) :
*r* est le **vecteur propre** de *M* pour la valeur propre 1.


2. Téléportation (dead ends & spider traps)
===========================================

Deux problèmes cassent la marche : les **culs-de-sac** (*dead ends*, pages sans
lien sortant, qui « fuient » la probabilité) et les **pièges** (*spider traps*,
groupes de pages qui se renvoient entre elles et absorbent tout le rang).

**Solution** : à chaque étape, avec probabilité :math:`1-\beta`, le surfeur
**téléporte** vers une page au hasard (:math:`\beta \approx 0,85`) :

.. math::

   r = \beta\, M r + (1-\beta)\,\frac{1}{N}\,\mathbf{1}

(les *dead ends* sont traités en redistribuant leur masse uniformément, ou en les
supprimant récursivement).


3. Calcul par itération de la puissance
=======================================

1. Initialiser :math:`r^{(0)} = \frac{1}{N}\mathbf{1}`.
2. **Itérer** :math:`r^{(t+1)} = \beta M r^{(t)} + \frac{1-\beta}{N}\mathbf{1}`.
3. S'arrêter quand :math:`\lVert r^{(t+1)} - r^{(t)}\rVert_1 < \varepsilon`.

À l'échelle du web, chaque itération est un **produit matrice-vecteur**
:math:`M r` — exactement le patron MapReduce du :doc:`chapitre 2 <../part1/chap2>`
(*map* : ``(j, r_i/d_i)`` pour chaque lien ``i→j`` ; *reduce* : somme par *j*).
C'est l'esprit du **TP4** (PageRank + MapReduce, sujet « moteur de recherche »).


4. Variantes (brève description)
================================

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Méthode
     - Idée
   * - **Topic-Sensitive PageRank**
     - Téléportation vers un **ensemble thématique** → rangs spécialisés par sujet.
   * - **TrustRank / lutte anti-spam**
     - Téléporter vers des pages **de confiance** pour réduire le *link spam*.
   * - **HITS** (*Hubs & Authorities*)
     - Deux scores couplés : *hubs* (pages qui pointent) et *authorities* (pages pointées).


Exercices
=========

.. admonition:: Exercice 1 — Un pas de PageRank
   :class: tip

   Graphe : A→B, A→C, B→C, C→A. Sans téléportation, en partant de
   :math:`r=(1/3,1/3,1/3)` pour (A,B,C), calculez le vecteur après **une**
   itération :math:`r = Mr`.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

Degrés sortants : A=2 (→B,→C), B=1 (→C), C=1 (→A).
Nouveau rang :
:math:`r_A = r_C = 1/3` ;
:math:`r_B = r_A/2 = 1/6` ;
:math:`r_C = r_A/2 + r_B = 1/6 + 1/3 = 1/2`.
Donc :math:`r = (1/3,\ 1/6,\ 1/2)` (somme = 1). En itérant, on converge vers la
distribution stationnaire.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — Pourquoi la téléportation ?
   :class: tip

   Qu'arrive-t-il au PageRank en présence d'un *spider trap* sans téléportation ?
   Comment :math:`\beta` corrige-t-il cela ?

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

Sans téléportation, un *spider trap* (ex. une page qui pointe seulement vers
elle-même) **accumule toute la probabilité** : son rang tend vers 1 et tous les
autres vers 0. La téléportation (avec proba :math:`1-\beta`, sauter vers une page
au hasard) permet à la marche de **sortir** du piège, redistribuant le rang de
façon réaliste. :math:`\beta\approx0{,}85` équilibre suivi des liens et saut
aléatoire.

.. raw:: html

   </details>
