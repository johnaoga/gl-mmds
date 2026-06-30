.. _part1_chap2:

***********************************************************************
Chapitre 2 : MapReduce
***********************************************************************

**MapReduce** est un modèle de programmation pour traiter de **grands jeux de
données en parallèle** sur un *cluster* de machines, en cachant au programmeur la
complexité de la distribution (partitionnement, communication, tolérance aux
pannes). C'est le socle du big data (Hadoop, Spark).

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Décrire les trois temps de MapReduce : **Map → regroupement par clé → Reduce**
- Modéliser un problème en *mappers* et *reducers*
- Connaître des patrons classiques (word count, matrice-vecteur, opérations relationnelles)


1. Le modèle
============

Les données sont vues comme des **paires (clé, valeur)**. Le calcul se fait en
trois temps :

1. **Map** : chaque *mapper* traite un fragment des données en entrée et émet des
   paires intermédiaires ``(clé, valeur)``.
2. **Regroupement par clé** (*shuffle & sort*) : le système regroupe toutes les
   valeurs partageant la **même clé** : ``(clé, [valeurs])``. *(Pris en charge
   automatiquement.)*
3. **Reduce** : chaque *reducer* reçoit une clé et la liste de ses valeurs, et émet
   le résultat agrégé.

.. math::

   \text{map}: (k_1, v_1) \rightarrow \text{list}(k_2, v_2)
   \qquad
   \text{reduce}: (k_2, \text{list}(v_2)) \rightarrow \text{list}(v_3)


2. Exemple canonique : *word count*
===================================

Compter les occurrences de chaque mot dans une énorme collection de documents.

.. code-block:: python

   def map(doc_id, texte):
       for mot in texte.split():
           emit(mot, 1)                 # (mot, 1)

   def reduce(mot, comptes):            # comptes = [1, 1, 1, ...]
       emit(mot, sum(comptes))          # (mot, total)

**Déroulé** sur deux documents ``d1="le chat le"`` et ``d2="le chien"`` :

- Map(d1) → ``(le,1) (chat,1) (le,1)`` ; Map(d2) → ``(le,1) (chien,1)``
- Regroupement → ``(le,[1,1,1]) (chat,[1]) (chien,[1])``
- Reduce → ``(le,3) (chat,1) (chien,1)``

.. tip::
   Un **combiner** (mini-reduce local côté mapper) réduit le volume transféré :
   Map(d1) émettrait directement ``(le,2)(chat,1)``. Possible quand l'agrégation
   est **associative et commutative** (somme, max…).


3. Produit matrice-vecteur
==========================

Calculer :math:`x_i = \sum_j m_{ij} v_j` (utile pour **PageRank**,
:doc:`chap8 <../part2/chap8>`).

- **Map** : pour chaque élément non nul :math:`m_{ij}`, émettre ``(i, m_ij * v_j)``
  (le vecteur ``v`` est diffusé à tous les mappers).
- **Reduce** : pour chaque ligne ``i``, sommer les valeurs reçues → ``(i, x_i)``.

Si ``v`` ne tient pas en mémoire, on découpe ``M`` et ``v`` en **bandes**.


4. Opérations relationnelles
============================

MapReduce exprime aussi les opérations de l'algèbre relationnelle :

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Opération
     - Idée MapReduce
   * - **Sélection** σ
     - Map émet les tuples satisfaisant la condition ; pas de reduce
   * - **Projection** π
     - Map émet les attributs gardés ; reduce déduplique
   * - **Jointure** R ⋈ S sur ``a``
     - Map émet ``(a, (R, reste))`` et ``(a, (S, reste))`` ; reduce combine les tuples R×S de même clé ``a``
   * - **Group-by / agrégation**
     - Map émet ``(clé_de_groupe, valeur)`` ; reduce agrège (somme, count…)


5. Exécution et tolérance aux pannes
====================================

Le *framework* gère : le découpage des entrées, l'ordonnancement des tâches sur
les nœuds, le *shuffle & sort*, et la **reprise sur panne** (une tâche échouée est
**ré-exécutée** ailleurs, car map/reduce sont des fonctions **sans état**).

**Écosystème** : **Hadoop** (HDFS + MapReduce) puis **Spark** (calcul en mémoire,
*RDD/DataFrame*, bien plus rapide pour les algorithmes itératifs comme K-means ou
PageRank).


Exercices
=========

.. admonition:: Exercice 1 — Map/Reduce d'une moyenne
   :class: tip

   On a des relevés ``(ville, température)``. Écrivez les fonctions *map* et
   *reduce* qui calculent la **température moyenne par ville**. Attention au piège
   du combiner.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

``map(_, (ville, temp)) → emit(ville, (temp, 1))`` puis
``reduce(ville, liste) → emit(ville, somme(temps)/somme(comptes))``.

**Piège** : la moyenne n'est **pas** associative ; un combiner naïf qui ferait la
moyenne des moyennes serait faux. Il faut transporter des **paires (somme,
compte)** et n'effectuer la division qu'au reduce final.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — Jointure
   :class: tip

   Soit ``Ventes(produit, montant)`` et ``Produits(produit, catégorie)`` réparties
   sur plusieurs serveurs. Décrivez la jointure en MapReduce pour obtenir le
   montant total **par catégorie**.

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

**Job 1 (jointure)** : map émet ``(produit, ("V", montant))`` et
``(produit, ("P", catégorie))`` ; le reduce, pour chaque produit, associe la
catégorie à chaque montant → ``(catégorie, montant)``. **Job 2 (agrégation)** :
map relaye ``(catégorie, montant)`` ; reduce somme par catégorie. (On peut aussi
fusionner en chaînant les deux étapes.)

.. raw:: html

   </details>
