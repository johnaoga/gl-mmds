.. _part2_chap6:

***********************************************************************
Chapitre 6 : Éléments similaires (shingling, min-hashing, LSH)
***********************************************************************

Trouver les **paires d'éléments similaires** (documents quasi-dupliqués, articles,
…) dans une **énorme** collection. Comparer toutes les paires est en
:math:`O(n^2)` — impossible à grande échelle. La chaîne **shingling →
min-hashing → LSH** résout ce problème.

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Représenter un document par ses **k-shingles** et la **similarité de Jaccard**
- Compresser les ensembles par des **signatures min-hash**
- Trouver les paires candidates par **LSH** sans comparer toutes les paires


1. Shingling
============

Un **k-shingle** est une sous-chaîne (ou suite de *k* mots) consécutive du document.
Un document devient l'**ensemble de ses k-shingles**. Deux documents proches
partagent beaucoup de shingles.

On mesure la similarité de deux ensembles par la **similarité de Jaccard** :

.. math::

   \text{sim}(A, B) = \frac{|A \cap B|}{|A \cup B|}

*(Choix de k : assez grand pour que la probabilité qu'un shingle apparaisse par
hasard soit faible — typiquement k = 5 à 10 pour des caractères.)* On **hache**
souvent les shingles en entiers pour gagner de la place.


2. Min-hashing
==============

Les ensembles de shingles sont énormes. On les **résume** par de courtes
**signatures** qui **préservent la similarité de Jaccard**.

**Principe.** On représente la collection par une **matrice caractéristique**
(lignes = shingles, colonnes = documents, 1 si présent). Une fonction de
**min-hash** :math:`h` correspond à une **permutation** des lignes ; la valeur
min-hash d'une colonne = **le numéro de la première ligne** (dans cette
permutation) où la colonne vaut 1.

**Propriété fondamentale** : pour deux colonnes,

.. math::

   \Pr[\,h(A) = h(B)\,] = \text{sim}_{\text{Jaccard}}(A, B)

En utilisant **n** fonctions de min-hash, la **signature** d'un document est le
vecteur de ses *n* valeurs min-hash ; la **fraction** de positions égales entre
deux signatures **estime** leur Jaccard. En pratique, on simule les permutations
par *n* fonctions de hachage.


3. Locality-Sensitive Hashing (LSH)
===================================

But : ne produire qu'un petit nombre de **paires candidates** (celles
probablement similaires), sans examiner les :math:`O(n^2)` paires.

**Technique des bandes** (*banding*). On découpe la signature (longueur *n*) en
**b bandes de r lignes** (:math:`n = b\cdot r`). Pour chaque bande, on **hache** la
tranche de signature de chaque document dans des *buckets*. Deux documents
deviennent **candidats** s'ils tombent dans le **même bucket pour au moins une
bande**.

**Analyse.** Si deux documents ont une similarité *s*, la probabilité qu'ils
soient candidats est :

.. math::

   1 - \left(1 - s^{\,r}\right)^{b}

Cette courbe a une forme en **S** : un **seuil** approximatif
:math:`t \approx (1/b)^{1/r}`. On choisit *b* et *r* pour que le seuil sépare bien
les paires similaires (rendues candidates) des dissemblables (écartées).

**Étape finale** : ne vérifier (calcul exact de la similarité) que les **paires
candidates** — bien moins nombreuses.


4. Mesures de distance & autres (brève description)
===================================================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Notion
     - Idée
   * - **Distances**
     - Jaccard, Euclidienne, **Cosinus**, Hamming, édition — chacune adaptée à un type de données.
   * - **LSH pour le cosinus**
     - **Hyperplans aléatoires** (*random projections* / sketches) : :math:`\Pr[\text{même signe}] = 1 - \theta/\pi`.
   * - **LSH pour l'euclidien**
     - Projection sur des droites aléatoires découpées en segments.
   * - **Applications**
     - Détection de **plagiat**, articles d'actualité similaires, résolution d'entités (*entity resolution*), empreintes.


Exercices
=========

.. admonition:: Exercice 1 — Jaccard
   :class: tip

   ``A = {1,2,3,4}``, ``B = {2,3,5}``. Calculez la similarité de Jaccard.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

:math:`A\cap B = \{2,3\}` (taille 2) ; :math:`A\cup B = \{1,2,3,4,5\}` (taille 5).
Donc :math:`\text{sim} = 2/5 = 0{,}4`.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — Banding LSH
   :class: tip

   Signatures de longueur ``n = 20``, découpées en ``b = 5`` bandes de ``r = 4``.
   Pour une paire de similarité ``s = 0,8``, probabilité d'être candidate ?

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

:math:`1-(1-s^{r})^{b} = 1-(1-0{,}8^{4})^{5} = 1-(1-0{,}4096)^{5}
= 1-0{,}5904^{5} \approx 1-0{,}0717 \approx \mathbf{0{,}93}`.
Une paire très similaire (0,8) a donc ~93 % de chances d'être candidate ; une paire
dissemblable (petit *s*) a une probabilité très faible — c'est l'effet de seuil en S.

.. raw:: html

   </details>
