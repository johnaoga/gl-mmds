.. _part2_chap5:

***********************************************************************
Chapitre 5 : Frequent Itemset Mining à grande échelle
***********************************************************************

Le **Frequent Itemset Mining** (FIM) cherche les combinaisons d'items fréquentes
dans une base de transactions (analyse du panier). Ici, la base est **massive**.

Objectifs
=========

À la fin de ce chapitre, vous devez pouvoir :

- Rappeler **Apriori** et la propriété d'antimonotonicité
- Citer les optimisations big data (PCY) et les approches distribuées (SON, Toivonen)


1. Rappel : Apriori
===================

.. note::
   Le FIM, le support, l'algorithme **Apriori** (antimonotonicité) et les règles
   d'association sont détaillés dans le cours de Data Mining :
   `DM — Frequent Itemset Mining
   <https://johnaoga.github.io/gl-dm/part2/chap6.html>`_ (**→ DM**).

En bref : un itemset est **fréquent** si son **support** (nombre de transactions
qui le contiennent) atteint un seuil :math:`\theta`. **Antimonotonicité** : tout
sous-ensemble d'un itemset fréquent est fréquent → on **élague** les candidats
dont un sous-ensemble n'est pas fréquent (génération par niveaux).


2. Le défi big data
===================

Sur des données massives, le coût d'Apriori vient surtout du **comptage des
paires** (et du nombre de **passages** sur la base, coûteux si elle est sur disque
distribué). D'où des optimisations et des approches **distribuées**.


3. Optimisations & approches distribuées (brève description)
============================================================

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Méthode
     - Idée
   * - **PCY** (*Park-Chen-Yu*)
     - Utilise la mémoire libre du 1ᵉʳ passage pour **hacher les paires** dans des compteurs (*buckets*) ; un *bucket* non fréquent élimine d'emblée ses paires → moins de paires candidates au 2ᵉ passage.
   * - **Multistage / Multihash**
     - Variantes de PCY avec plusieurs tables de hachage pour filtrer encore plus de paires.
   * - **Échantillonnage (simple)**
     - Faire tourner Apriori sur un **échantillon** tenant en mémoire (seuil abaissé) → candidats, puis vérifier sur toute la base.
   * - **Toivonen**
     - Échantillon + *negative border* : garantit (sans faux négatifs) le résultat exact, quitte à refaire un passage.
   * - **SON** (*Savasere-Omiecinski-Navathe*)
     - Adapté à **MapReduce** (voir ci-dessous) : exact, deux passages.


4. SON en MapReduce
===================

**SON** repose sur le principe : *un itemset globalement fréquent est fréquent dans
au moins un fragment*. On l'implémente en **deux jobs MapReduce** :

- **Job 1 — candidats.** *Map* : sur chaque fragment (chunk) de la base, trouver les
  itemsets fréquents **localement** (seuil proportionnel :math:`p\cdot\theta`) et
  les émettre comme **candidats**. *Reduce* : dédupliquer la liste des candidats.
- **Job 2 — comptage global.** *Map* : pour chaque transaction, émettre
  ``(candidat, 1)`` pour les candidats qu'elle contient. *Reduce* : sommer ;
  garder ceux dont le support **global** ≥ :math:`\theta`.

Résultat **exact**, en deux passages, parfaitement parallélisable. (C'est l'esprit
du **TP3** + du **TP4 projet** « FIM distribué ».)


Exercices
=========

.. admonition:: Exercice 1 — Principe de SON
   :class: tip

   Pourquoi un itemset globalement fréquent est-il nécessairement fréquent dans
   **au moins un** fragment ? (raisonnez par l'absurde)

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

Si la base est découpée en fragments de fraction *p* et qu'un itemset a un support
local **< p·θ dans chaque** fragment, alors en sommant sur tous les fragments son
support global serait **< θ** : il ne serait pas fréquent globalement.
Par contraposée, s'il est fréquent globalement (≥ θ), il dépasse le seuil local
dans **au moins un** fragment. SON ne produit donc **aucun faux négatif**.

.. raw:: html

   </details>

.. admonition:: Exercice 2 — PCY
   :class: tip

   En quoi PCY réduit-il le nombre de **paires candidates** par rapport à Apriori,
   et qu'exploite-t-il pendant le **premier** passage ?

.. raw:: html

   <details class="mmds-sol"><summary>▶ Voir la correction</summary>

Pendant le 1ᵉʳ passage (comptage des items), PCY exploite la **mémoire libre**
pour hacher **chaque paire** vue dans des *buckets* et compter les *buckets*. Au
2ᵉ passage, une paire n'est candidate que si ses deux items sont fréquents **et**
si son *bucket* est fréquent. Les paires tombant dans un *bucket* non fréquent
sont éliminées d'emblée → beaucoup moins de candidats à compter.

.. raw:: html

   </details>
