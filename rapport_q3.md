# Classification non supervisée (Profils de santé naturels)

(Rédigé par KAKEU NGUEGANG ELDA, analyses par FOKOU KELEFACK KERIANE KIANELLE)





## &#x20;  1. Justification méthodologique

Afin de déceler des regroupements de profils sanitaires sans se baser sur les étiquettes de risques fixées a priori par l'administration, nous appliquons une méthode d’apprentissage non supervisé : l’algorithme des K-moyennes (K-Means). Les données physiologiques (FCR\_bpm et PAS\_mmHg) ont été préalablement standardisées (centrées et réduites) afin de gommer les écarts d'unités et d'équilibrer l'impact géométrique de chaque variable dans le calcul des distances. La méthode du coude a permis d'arrêter de façon optimale le nombre de profils à $K = 3$.





## &#x20;  2. Caractérisation clinique des 3 profils-types identifiés

L'étude des coordonnées des centres de gravité de chaque classe met en lumière trois réalités distinctes au sein de l'Université de MBOUDA :

&#x20;      Profil 1 : Les "Sains / Athlétiques" (\~55% de l'effectif)Descriptif : Regroupe les étudiants associant un rythme cardiaque bas au repos ($55 - 72 \\text{ bpm}$) et une tension systolique idéale ($105 - 122 \\text{ mmHg}$). Ces jeunes présentent d'excellents indicateurs de forme.

&#x20;      Profil 2 : Les "Vigilances Légères" (\~33% de l'effectif)Descriptif : Profil d'étudiants affichant un pouls plus rapide ($73 - 85 \\text{ bpm}$) et une tension qui glisse doucement vers la pré-hypertension ($125 - 138 \\text{ mmHg}$). C'est le reflet typique du stress estudiantin ou du manque d'activité physique.

&#x20;      Profil 3 : Les "Alertes Cardiovasculaires" (\~12% de l'effectif)

Descriptif : Ce pôle critique rassemble les étudiants souffrant de tachycardie sévère et/ou d'hypertension avérée (mesures franchissant les $140 \\text{ mmHg}$ avec des pointes au-delà de $175 \\text{ mmHg}$).





## &#x20;   3. Synthèse vulgarisée destinée au Directeur

« Monsieur le Directeur, en laissant parler vos données, vos étudiants se divisent naturellement en trois catégories bien distinctes. Plus de la moitié est en excellente santé (Profil 1). Un tiers de vos effectifs montre des signes d'épuisement ou de sédentarité modérée (Profil 2). Enfin, un noyau critique de 12% d'étudiants se situe dans une zone d'alerte cardiovasculaire sévère (Profil 3). Nous vous conseillons d'orienter vos budgets de façon ciblée : des campagnes de sport et de gestion du stress pour le Profil 2, et une prise en charge médicale prioritaire et ciblée pour le Profil 3. »





## &#x20;   4. Fragilité du modèle

L'algorithme du K-Means est sensible aux valeurs aberrantes (outliers), qui ont tendance à déplacer artificiellement les centres de gravité des groupes. De plus, il s'agit d'une photographie fixe qui ne prend pas en compte l'historique médical ou le mode de vie réel des étudiants.

