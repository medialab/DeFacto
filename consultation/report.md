# Analyse linguistique des propositions de la consultation
## "Comment permettre à chacun de mieux s'informer"

### Contexte de la consultation
- 1 723 propositions validées de la consultation
- début : 27/06/2022
- fin : 31/10/2022

# Question de recheche 1 : Sujets invoqués dans les propositions

La première question de recherche était de savoir quels sujets ont été invoqués dans les propositions écrites par les participants de la consultation. Pour répondre à cette question, on a fait l'analyse linguistique qui s'appelle _topic modeling_, dans laquelle on extrait les sujets (topics) invoqués dans plusieurs documents de texte. La méthode qu'on a préféré est [`BERTopic`](https://maartengr.github.io/BERTopic/index.html).

## Propositions inférées par la consultation de Make.org
La consultation a regroupé les propositions et créé des représentations de ces _clusters_. 15 _clusters_ ou topics ont été inférés par l'équipe de Make.org. Ils ont représenté chaque topic par une nouvelle proposition qui vise à résumer tous les propositions concernées.

1. Encourager une approche critique de l'information
2. Renforcer l'éducation aux médias et à l'information à l'école
3. Former à la détection des fake news et à la vérification de l'information
4. Assurer l'indépendance éditoriale des médias
5. Proposer une information plus diversifiée
6. Réguler plus efficacement les réseaux sociaux
7. Renforcer les pratiques de vérification de l'information
8. Sanctionner la diffusion de fake news
9. Sourcer et référencer autant que possible les information publiées
10. ne pas céder à la culture de buzz et du sensationnel
11. Lutter contre la concentration des médias
12. Exiger davantage d'expertise dans le traitement de l'information
13. Accroître la transparence sur le financement et les intérêts des médias
14. Améliorer la protection des journalistes et des lanceurs d'alerte
15. Mieux encadrer les publicités

## Topics inférés par l'analyse du médialab

L'approche de l'équipe de Make.org cherche à proposer les propositions qui résument les positions prises par les participants sur de divers sujets. Notre approche cherche à inférer les sujets invoqués dans les propositions, sans regard pour la position de la proposition concernée.

En prenant les 1 723 propositions produites par la consultation, notre analyse a inféré 13 topics. Afin de créer les représentations vectorielles des propositions, spécifiquement les _embeddings_ de phrase (_sentence embeddings_), on a profité d'un [_sentence transformer_](https://huggingface.co/dangvantuan/sentence-camembert-large) fine-tuné par le laboratoire français [La Javaness](https://www.lajavaness.com/) et basé sur le modèle linguistique français [CamemBERT](https://huggingface.co/camembert/camembert-large). Après avoir reduit la complexité de la représentation en utilisant UMAP (_Uniform Manifold Approximation and Projection for Dimension Reduction_), les _embeddings_ des propositions ont été regroupés par l'algorithme HDBSCAN (_Hierarchical Density-Based Spatial Clustering of Applications with Noise_). Ensuite, on a construit les représentations de ces clusters inférés, c'est-à-dire les topics inférés. Pour créer ces représentations, on a utilisé un autre _transformer_, c-TF-IDF (_Class-based term frequency-inverse document frequency_), qui se base sur le _TfidfTransformer_ de scikit-learn. Pour terminer, on a mergé certains topics et leur tous donner un nom.

![barchart](topic_visualisations/barchart.png)


1. L'opinion et le journalisme
    - Invoqué dans 263 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - journalistes
        - politiques
        - sujets
        - débats
        - arrêtent
        - opinion
    - Des propositions représentatives:
        - Il faut que les journalistes des médias, télévisions, radios arrêtent de donner leur avis en permanence.
        - Il faut que les journalistes se drapent d'humilité et arrêtent de voir dans le journalisme un métier d'ambitions personnelles.
        - Il faut organiser la mise en débat publique des idées sur des temps assez longs pour permettre aux contradicteurs d'argumenter leur position

2. Financement et l'indépendance des médias
    - Invoqué dans 210 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - financement
        - concentration médias
        - milliardaires
        - interdire
        - grands groupes
        - médias indépendants
    - Des propositions représentatives:
        - Il faut que les médias soient financés en partie par les finances publiques et en partie par le secteur privé, mais en toute transparence.
        - Il faut que la loi empêche l'achat de médias par une ou plusieurs personnes. L'information n'est pas une marchandise.
        - Il faut que les médias français ne soit plus possédé par 8 milliardaires qui protègent leurs intérêts
3. Désinformation
    - Invoqué dans 178 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - fake news
        - vérifiée
        - qualité
        - plusieurs
        - sources information
        - citer
    - Des propositions représentatives:
        - Il faut que chaque publication cite obligatoirement ses sources.
        - Il faut former un organisme de débunk de fake news de qualité et forcer les algorithmes de recommandations à largement partager leur travail.
        - Il faut des experts en désamorçage de fake news, reconnus et crédibles.
4. Formation au secondaire
    - Invoqué dans 152 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - réseaux sociaux
        - éducation médias information
        - professeurs documentalistes
        - alogirthmes
        - responsables
        - fake
    - Des propositions représentatives:
        - Il faut faire de l'éducation aux médias et à l'information, une grande cause nationale.
        - Il faut que l'école explique le fonctionnement des réseaux sociaux à chaque enfant pour qu'ils comprennent la perversité des mécanismes.
        - Il faut créer une discipline d'information-documentation dispensée par les professeurs documentalistes pour tous les élèves du secondaire.
5. Formation au primaire
    - Invoqué dans 85 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - esprit
        - développer
        - développer esprit critique
        - analyser
        - âge
        - dès jeune âge
    - Des propositions représentatives:
        - Il faut généraliser depuis l'école primaire un apprentissage de l'esprit critique.
        - Il faut apprendre très tôt, à développer son esprit critique. Cours ludiques et dédiés.
        - Il faut développer et renforcer les compétences psycho-sociales dès l'école maternelle, et ce, jusqu'à l'âge adulte.
6. Accès à l'information
    - Invoqué dans 51 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - rendre accessible
        - papier
        - abonnements gratuits
        - beaucoup
        - établissements scolaires
        - démocratiser
    - Des propositions représentatives:
        - Il faut faciliter l'accès financier aux médias sous forme numérique. Ils sont trop chers.
        - Il faut voir comment fournir une offre d'informations de qualité à un prix accessible aux plus pauvres.
        - Il faut permettre un abonnement en ligne à un panel de titres de presse d'information avec une ristourne pour les étudiants, chômeurs etc.
7. Chaînes d'information en continu
    - Invoqué dans 47 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - europe
        - chaînes information continu
        - france télévision
        - créer chaîne
        - affranchir
        - quota
    - Des propositions représentatives:
        - Il faut limiter les chaines d'info en boucle sources de conditionnement et favoriser, par un financement public, celles qui font réfléchir.
        - Il faut des chaînes d’informations indépendantes à la télévision, et libres de paroles.
        - Il faut que les chaînes d’information en continu soient supprimées pour arrêter la pratique du vide.
8. Législation
    - Invoqué dans 46 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - news
        - propos
        - diffusant
        - élus
        - sanctionner médias
        - pénalement
    - Des propositions représentatives:
        - Il faut sanctionner les médias qui diffusent trop de fake news : retrait licence journalisme, suspension d’audience, déconnexion du site web.
        - Il faut que les auteurs de fake News soient sanctionnés pénalement et financièrement.
        - Il faut punir financièrement et fortement les auteurs de fausses info ainsi que les médias, supports, plateformes etc.... qui les diffusent.
9. Éthique du journalisme
    - Invoqué dans 45 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - éthique
        - charte munique
        - déontologie journalistique
        - respect
        - professionnelle
        - conseil
    - Des propositions représentatives:
        - Il faut inclure dans toutes les formations dédiées, un code de déontologie, voire un serment, à l'image des médecins (Hippocrate).
        - Il faut créer un organisme indépendant pour contrôler le travail des médias et le respect de l’éthique journalistique.
        - Il faut transformer le « Conseil de déontologie des médias » créé en 2019 en véritable contre-pouvoir citoyen.
10. Désanonymisation en ligne
    - Invoqué dans 24 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - anonymat réseaux sociaux
        - réseaux sociaux interdir
        - sociaux interdire
        - supprimer
        - vrai nom
        - internet
    - Des propositions représentatives:
        - Il faut protéger les utilisateurs d’Internet et des réseaux sociaux contre toute atteinte résultant de l’utilisation de leurs données.
        - Il faut supprimer l'anonymat sur les réseaux sociaux.
        - Il faut interdire les réseaux sociaux ou obliger de donner sa véritable identité pour poster.
11. Arnaques et influenceurs
    - Invoqué dans 20 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - sanctionner youtube lorqu
        - pubs arnaques
        - médias informations
        - influenceurs
        - pub institutinonelles dénoncer
        - moins respect victimes
    - Des propositions représentatives:
        - Il faut responsabiliser les médias d'informations qui alertent sur les arnaques alors qu'ils laissent eux-mêmes ce type de pub sur leur site.
        - Il faut imposer aux médias de signaler les espaces publicitaires/ partenariats avec un symbole uniformisé clairement visible.
        - Il faut ne plus autoriser de publicité après des informations dramatiques, au moins par respect pour les victimes et leurs familles.
12. Échelles des médias
    - Invoqué dans 17 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - médias locaux
        - web
        - niveau local retrouver
        - nationales internationales publier
        - notoriété légitimté moins
        - national européen laisser
    - Des propositions représentatives:
        - Il faut remettre en avant les médias (presse, site web, app...) pour s'informer sur les actualités locales.
        - Il faut remettre en avant l'actualité des territoires en diffusant plus facilement les actualités locales sur le web et dans les médias.
        - Il faut laisser aux chaines régionales et à la PQR le traitement de l'info du village et traiter plus souvent de l'international.
13. Enseignment et l'EMI (Éducation aux médias et à l'information)
    - Invoqué dans 16 propositions.
    - Les mots ou les phrases les plus représentatifs:
        - emploi temps élèves
        - emi professeurs
        - élèves
        - donner moyens professeurs
        - enseignement emi
        - documentalistes enseigner emi
    - Des propositions représentatives:
        - Il faut prévoir dans l'emploi du temps 1h par semaine pour que les professeurs documentalistes puissent former les élèves à l'EMI.
        - Il faut donner les moyens aux professeurs documentalistes d'exercer une véritable formation à l'EMI avec une progression du collège au lycée.
        - Il faut inscrire l'EMI dans l'emploi du temps des élèves de la 6e à la Terminale gérée par les profs docs dont c'est le domaine d'expertise.

569 propositions ne se tiennent pas suffisament à aucun topic inféré.

## Analyse de la proximité entre topics
Certains sujets invoqués dans les propositions sont liés à l'un et l'autre, tels que les deux qui discutent l'éducation des jeunes et celui qui discute l'enseignement. Un regroupement hiérarchique (_hierarchical clustering analysis_ ou HCA) montre la proximité entre les représentations des topics inférés. On a implementé la méthode Ward pour relever la proximité entre topics.

![hierarchy](topic_visualisations/hierarchy.png)

Comme attendu, le regroupement hiérarchique relève une proximité entre les trois sujets qui appartienent aux discussions de l'éducation : `Enseignement & L'EMI`, `Formation au secondaire`, `Formation au primaire`. Plus intéressante est la proximité que montre le regroupement hiérarchique entre la discussion de la désinformation (`Désinformation`) et la discussion de l'opinion dans le journalisme (`L'opinion & le journalisme`). En outre, la discussion sur la législation (`Legislation`) se lie à deux des sujets en particulier. Dans un premier temps, le regroupement hiérarchique trouve que la législation est liée aux soucis sur les arnaques et les influenceurs en ligne (`Arnaques & influenceurs`). Dans un deuxième temps, elle se lie aussi à la question de la désanoymisation en ligne (`Désanoymisation en ligne`).

## Analyse de la similarité entre topics
La similarité cosinus est une autre méthode mathématique pour examiner les relations entre les représentations des topics inférés. Cette méthode prend les représentations de deux topics et détermine le cosinus de leur angle. En mettant ces calculations dans une matrice, où la similarité cosinus de chaque pair de représentations occupe un carré, des nouvelles relations ressortent.

![heatmap](topic_visualisations/heatmap.png)

L'idée de législation (`Legislation`) se tient le plus aux propositions qui discutent l'éducation en secondaire (`Formation au secondaire`). D'un dégré moins important, la législation (`Legislation`) est aussi liée aux discussions sur l'accès à l'information (`Accès à l'information`). Contrairement au regroupement hierarchique, l'analyse par la similarité cosinus suggère que la similarité entre les trois topics sur l'éducation n'est pas si forte. Selon cette dernière analyse, trois topics en particulier, l'éducation en secondaire (`Formation au secondaire`), l'accès à l'information (`Accès à l'information`), et la législation (`Legislation`), ont les relations les plus importantes.

# Question de recherche 2 : Analyse de la vote sur les propositions

La deuxième question de recherche s'appuie sur les votes qu'ont reçu les propositions.

## Accord entre propositions par topic de la proposition
[<img src="topic_visualisations/agreement_clusters_with_topic_color.png" width="480"/>](topic_visualisations/agreement_clusters_with_topic_color.png)

## Accord entre propositions par l'âge de l'auteur de la proposition
[<img src="topic_visualisations/agreement_clusters_with_age_color.png" width="480"/>](topic_visualisations/agreement_clusters_with_age_color.png)
