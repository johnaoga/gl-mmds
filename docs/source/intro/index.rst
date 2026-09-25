.. _intro:

*********************
Organisation du cours
*********************

.. important::
   Si vous suivez ce cours actuellement, vous devez signer la charte d'utilisation de l'IA ici :
   `https://forms.gle/TtNLyc4pNSYaANTX9 <https://forms.gle/TtNLyc4pNSYaANTX9>`_

Le **Big Data** désigne des données si **massives** que les algorithmes et
machines classiques ne suffisent plus. Ce cours montre comment **fouiller ces
données massives** (*Mining of Massive Datasets*) : via le **calcul distribué**
(MapReduce) et des algorithmes pensés pour le passage à l'échelle (recommandation,
similarité, graphes, PageRank).

.. note::
   Cours **extrait de Stanford `CS246` <https://web.stanford.edu/class/cs246/>`_**,
   d'après le manuel **MMDS** (`mmds.org <http://www.mmds.org/>`_). Vidéos en
   anglais : `chaîne Mining Massive Datasets
   <https://www.youtube.com/@miningmassivedatasets6799>`_.

À la fin de ce cours, l'étudiant.e doit être capable de :

* Définir le big data (les **5V**) et les défis du calcul sur données massives
* Modéliser un problème sous forme **MapReduce** et l'implémenter
* Construire un **système de recommandation** (filtrage collaboratif, facteurs latents/SVD)
* Adapter le **clustering** et le **frequent itemset mining** au contexte distribué
* Trouver des **éléments similaires** à grande échelle (shingling, min-hashing, **LSH**)
* Analyser des **graphes** massifs (détection de communautés, **PageRank**)
* Lire un article/chapitre technique et présenter un algorithme avancé

.. note::
   Ce cours **prolonge le cours de Data Mining**. Les fondations (qu'est-ce que le
   data mining, le clustering K-means, l'algorithme Apriori) y sont introduites :
   on s'y réfèrera (voir les renvois ``→ DM`` dans les chapitres).


Pédagogie
=======================================

Pédagogie mixte, par projet : cours magistraux, **vidéos** à visionner avant les
séances, travaux pratiques d'implémentation, **exposés** de groupe sur des
algorithmes avancés, et un **projet MapReduce** en équipe.


Répartition du cours
=======================================

* :doc:`Partie 1 <../part1/index>` — **Préliminaires** : introduction au big data (5V), MapReduce.
* :doc:`Partie 2 <../part2/index>` — **Algorithmes pour données massives** : clustering, recommandation, frequent itemset mining, éléments similaires (LSH), mining de graphes, link analysis (PageRank).
* :doc:`Partie 3 <../part3/index>` — **TPs & Projet**.

Une partie :doc:`QCM <../part6/index>` interactive complète le cours.


Déroulé des séances (indicatif)
=======================================

.. list-table::
   :header-rows: 1
   :widths: 12 52 36
   :class: longtable

   * - Séance
     - Contenu
     - TP / Vidéos
   * - Séance 1
     - Mise en situation + introduction au big data (5V)
     - —
   * - Séance 2
     - Systèmes de recommandation (CF item-item, facteurs latents)
     - Vidéos · TP1 lancé
   * - Séance 3
     - Clustering (K-means) + Frequent Itemset Mining (Apriori)
     - Vidéos · TP2 lancé
   * - Séance 4
     - MapReduce + Hadoop/Spark
     - Vidéos · TP3 / TP0 lancés
   * - Séances 5 à 8
     - **Exposés** de groupe (algorithmes avancés) + restructuration
     - Préparation + lab
   * - Séances 9–10
     - Éléments similaires (LSH), graphes & PageRank ; visualisation
     - TP4 (projet MapReduce) lancé


Évaluation
=======================================

L'évaluation combine (les poids exacts sont communiqués par l'enseignant) :

* **TP0** — *word count* avec MapReduce (échauffement) ;
* **TP1** — système de recommandation (filtrage collaboratif item-item top-N), **individuel** ;
* **TP1*** — système de recommandation (facteurs latents), **individuel** ;
* **TP2** — clustering K-means / Hclust, **individuel** ;
* **TP3** — Apriori (frequent itemset mining), **individuel** ;
* **Exposé** de groupe — un algorithme avancé (description + exécution pas-à-pas + cas d'usage) ;
* **TP4 / Projet MapReduce** (groupe) — code (30 %) + rapport ≤10 p (50 %) + vidéo ≤5 min (20 %) ;
* **Examen**.

Voir la :doc:`Partie 3 <../part3/index>` pour le détail des TPs et du projet.


Contact et communication
=======================================

Les communications se feront par mail.

:Email: `John Aoga <johnaoga@gmail.com>`_


Cours Open-Source
=======================================

Les sources de ce site web sont open-source et disponibles sur `GitHub <https://github.com/johnaoga/gl-mmds>`_.
N'hésitez pas à faire des pull requests si vous voyez des erreurs ou des éléments à corriger.

La licence utilisée est Creative Commons Attribution-ShareAlike 4.0 International License :

.. image:: https://i.creativecommons.org/l/by-sa/4.0/88x31.png
    :alt: CC-BY-SA
