.. _part2_chap4:

***********************************************************************
Chapitre 4 : Systèmes de recommandation
***********************************************************************

Un **système de recommandation** prédit l'intérêt d'un utilisateur pour des items
(films, produits…) à partir d'une matrice **utilisateurs × items** de notes,
**creuse** (la plupart des notes manquent). But : prédire les notes manquantes et
**recommander** les meilleures.

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Distinguer recommandation **basée contenu** et **filtrage collaboratif**
- Dérouler le **filtrage collaboratif item-item (top-N)**
- Comprendre l'approche par **facteurs latents (SVD)**


1. Généralités
==============

- **Basé contenu** : recommander des items **similaires à ceux aimés** par
  l'utilisateur, à partir de leurs **attributs** (profil d'item). Pas besoin des
  autres utilisateurs, mais nécessite de bons descripteurs.
- **Filtrage collaboratif** (*collaborative filtering*, CF) : exploiter les **notes
  des autres** utilisateurs. Deux variantes : **user-user** (utilisateurs
  similaires) et **item-item** (items co-notés similairement) — cette dernière est
  plus stable et plus utilisée.
- **Facteurs latents** : factoriser la matrice de notes pour découvrir des
  **dimensions cachées** (genre, ton…).


2. Filtrage collaboratif item-item (top-N)
==========================================

**Idée** : pour prédire la note de l'utilisateur *u* sur l'item *i*, on regarde les
items que *u* a déjà notés et qui **ressemblent** à *i*.

**Étape 1 — similarité entre items.** On mesure la similarité entre colonnes (items)
de la matrice de notes, typiquement par la **similarité cosinus** (de préférence
**centrée**, en retranchant la moyenne de chaque ligne → *Pearson* ajusté, pour
neutraliser les biais de notation) :

.. math::

   \text{sim}(i, j) = \frac{\sum_{u} r_{ui}\, r_{uj}}{\sqrt{\sum_u r_{ui}^2}\,\sqrt{\sum_u r_{uj}^2}}

**Étape 2 — top-N voisins.** Pour l'item *i*, garder les **N items les plus
similaires** que *u* a notés (voisinage :math:`N(i;u)`).

**Étape 3 — prédiction** (moyenne pondérée par la similarité) :

.. math::

   \hat r_{ui} = \frac{\sum_{j \in N(i;u)} \text{sim}(i,j)\, r_{uj}}{\sum_{j \in N(i;u)} |\text{sim}(i,j)|}

**Étape 4 — recommander** les items de plus forte note prédite, non encore vus.

.. tip::
   Les similarités item-item sont **stables** dans le temps : on peut les
   **pré-calculer** hors-ligne (et en MapReduce), ce qui rend la recommandation
   très rapide en ligne. C'est l'objet du **TP1**.


3. Facteurs latents & SVD
=========================

**Idée** : approcher la matrice de notes :math:`R` (utilisateurs × items) par le
**produit de deux matrices** de faible rang :math:`k` :

.. math::

   R \approx P\, Q^\top, \qquad
   \hat r_{ui} = p_u \cdot q_i = \sum_{f=1}^{k} p_{uf}\, q_{if}

où :math:`p_u` (resp. :math:`q_i`) est le vecteur de l'utilisateur *u* (resp. de
l'item *i*) dans un espace de **k facteurs latents**.

**Étapes :**

1. Choisir le nombre de facteurs *k*.
2. **Apprendre** *P* et *Q* en minimisant l'erreur **sur les notes connues**, avec
   régularisation :

   .. math::

      \min_{P,Q} \sum_{(u,i)\,\text{connus}} \big(r_{ui} - p_u\cdot q_i\big)^2
      + \lambda\big(\lVert p_u\rVert^2 + \lVert q_i\rVert^2\big)

   par **descente de gradient** (SGD) ou **ALS** (*Alternating Least Squares*, qui
   se parallélise très bien) — la **SVD** donne la meilleure approximation de rang
   *k* au sens des moindres carrés.
3. **Prédire** :math:`\hat r_{ui} = p_u \cdot q_i` ; recommander les meilleures.

C'est l'objet du **TP1\*** (facteurs latents).


4. Autres approches (brève description)
=======================================

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Approche
     - Idée
   * - **CF user-user**
     - Prédire à partir des **utilisateurs** les plus similaires à *u*.
   * - **Basé contenu**
     - Profil d'item (attributs/TF-IDF) + profil d'utilisateur ; recommander par similarité de profils.
   * - **Hybride**
     - Combiner contenu + collaboratif (atténue le *cold start*).


Exercices
=========

.. admonition:: Exercice 1 — Prédiction item-item
   :class: tip

   *u* a noté A=5 et B=3. On veut prédire sa note sur *i*, avec
   ``sim(i,A)=0,8`` et ``sim(i,B)=0,2``. Calculez :math:`\hat r_{ui}`.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

:math:`\hat r_{ui} = \dfrac{0{,}8\times 5 + 0{,}2\times 3}{0{,}8 + 0{,}2}
= \dfrac{4{,}6}{1{,}0} = 4{,}6`.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — Pourquoi item-item plutôt que user-user ?
   :class: tip

   Donnez deux raisons pour lesquelles le CF **item-item** est souvent préféré au
   **user-user** à grande échelle.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

(1) Les **similarités entre items** sont plus **stables** que celles entre
utilisateurs (les goûts d'un user évoluent ; un film reste le même), donc
**pré-calculables hors-ligne**. (2) Il y a souvent **moins d'items que
d'utilisateurs**, et chaque item a plus de notes → estimations de similarité plus
fiables et matrice de similarité plus petite.

.. raw:: html

   </details>
