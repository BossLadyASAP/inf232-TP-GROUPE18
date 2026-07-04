# Question 4 — Prédiction automatique du risque à partir des mesures physiologiques

*Rédaction : BABINE BAMBE AIME (23V2213) — Groupe 18, Thème A : Service de santé universitaire*

## 1. Reformulation de la question posée

Le directeur du service de santé souhaite qu'un nouvel étudiant dépisté soit automatiquement classé « à risque » ou « non à risque », dès que ses deux mesures physiologiques (fréquence cardiaque au repos **FCR_bpm** et pression artérielle systolique **PAS_mmHg**) sont disponibles, sans attendre le reste des analyses. Il demande également quelle confiance accorder à une telle prédiction et quelles seraient les conséquences d'une erreur pour un vrai étudiant.

Cette question relève de la **classification supervisée** : on dispose déjà, pour chaque étudiant de l'échantillon, d'une étiquette connue (`Risque` = 0 ou 1), et l'on cherche à construire un modèle capable de prédire cette étiquette pour un nouvel individu à partir de `FCR_bpm` et `PAS_mmHg` seules.

## 2. Données mobilisées

- **Échantillon** : 250 étudiants dépistés.
- **Variables explicatives (features)** : `FCR_bpm` (fréquence cardiaque au repos) et `PAS_mmHg` (pression artérielle systolique).
- **Variable cible** : `Risque` (0 = non à risque, 1 = à risque).
- **Distribution de la cible** : 200 étudiants non à risque (80 %) contre 50 étudiants à risque (20 %).

Cette distribution est **déséquilibrée** (classes non équilibrées, ratio 4:1). C'est un point important à garder à l'esprit pour l'interprétation des résultats : un modèle « paresseux » qui prédirait systématiquement « non à risque » obtiendrait déjà 80 % de bonnes réponses sans avoir rien appris. L'accuracy seule n'est donc pas suffisante pour juger la qualité du modèle ; il faut regarder précision, rappel et matrice de confusion.

## 3. Démarche et méthode retenue

Deux modèles de classification ont été entraînés et comparés :

1. **Régression logistique** : modèle linéaire simple, souvent utilisé comme référence (baseline) en classification binaire.
2. **Random Forest** (forêt aléatoire) : modèle non linéaire, capable de capturer des frontières de décision plus complexes.

Les données ont été séparées en un jeu d'entraînement (70 %) et un jeu de test (30 %), avec stratification sur la cible pour conserver la même proportion d'étudiants à risque dans les deux sous-ensembles. Les modèles ont été entraînés sur le jeu d'entraînement puis évalués sur le jeu de test, qu'ils n'ont jamais vu pendant l'apprentissage — condition nécessaire pour juger honnêtement de leur capacité de généralisation à de nouveaux étudiants.

Le choix du Random Forest (en plus de la régression logistique) est justifié par le fait que la relation entre les deux mesures physiologiques et le risque n'est pas nécessairement linéaire ; un modèle par arbres permet de vérifier si une frontière plus flexible améliore la détection des cas à risque.

## 4. Résultats obtenus

### 4.1 Performances globales

| Métrique | Régression logistique | Random Forest |
|---|---|---|
| Accuracy | 0,9600 | 0,9600 |
| Précision | 1,0000 | 1,0000 |
| Rappel (Recall) | 0,8000 | 0,8000 |
| F1-Score | 0,8889 | 0,8889 |

Les deux modèles obtiennent des performances identiques sur ce jeu de test, avec une exactitude globale de 96 %.

### 4.2 Matrice de confusion (Random Forest)

|  | Prédit : non à risque | Prédit : à risque |
|---|---|---|
| **Réel : non à risque** | 60 | 0 |
| **Réel : à risque** | 3 | 12 |

*(voir `matrice_confusion_q4.png`)*

Sur les 75 étudiants du jeu de test :
- Les **60 étudiants réellement non à risque** ont tous été correctement identifiés (aucun faux positif).
- Sur les **15 étudiants réellement à risque**, **12 ont été détectés**, mais **3 sont passés inaperçus** (faux négatifs).

### 4.3 Frontières de décision

*(voir `frontieres_decision_q4.png`)*

La visualisation des frontières de décision montre que la séparation entre les deux classes se fait essentiellement à des valeurs élevées de `PAS_mmHg` et, dans une moindre mesure, de `FCR_bpm`. La régression logistique trace une frontière rectiligne unique, tandis que le Random Forest dessine une zone de décision plus découpée, en escalier, autour du même nuage de points à risque. Les deux modèles isolent globalement la même zone de la représentation graphique, ce qui explique leurs performances identiques sur ce jeu de test.

## 5. Réponse à la question du directeur

**Oui**, il est possible, à partir des seules mesures `FCR_bpm` et `PAS_mmHg`, de construire un système qui suggère automatiquement si un étudiant est probablement « à risque » ou non, dès son dépistage.

Concrètement :
- Le système se trompe rarement lorsqu'il annonce qu'un étudiant est à risque : **toutes les alertes « à risque » émises sont fiables** (précision de 100 % sur le jeu de test), il n'y a donc pas de fausse alerte inutile.
- En revanche, le système **ne détecte pas tous les cas réellement à risque** : environ **1 étudiant à risque sur 5 (20 %) n'est pas repéré** par le modèle (rappel de 80 %), et serait donc classé à tort comme « non à risque ».

**Confiance à accorder** : une confiance élevée peut être accordée lorsque le système signale un risque (peu de fausses alertes), mais une confiance seulement modérée lorsqu'il rassure un étudiant en le classant « non à risque » — car cette classe peut, dans une minorité de cas, cacher un véritable étudiant à risque non détecté.

**Conséquences d'une erreur** : dans ce contexte de santé, l'erreur la plus grave est le **faux négatif** (un étudiant réellement à risque classé « non à risque »), car cela retarderait une prise en charge médicale nécessaire. C'est précisément le type d'erreur observé ici (3 cas sur 75). À l'inverse, un faux positif (fausse alerte) n'a pas été observé dans ce test, mais aurait un coût plus faible : un examen complémentaire inutile.

## 6. Discussion des limites — ce qui pourrait rendre cette réponse fragile ou trompeuse

- **Taille du jeu de test réduite** : les performances sont calculées sur seulement 75 étudiants, dont 15 seulement sont réellement à risque. Un déplacement de 1 ou 2 cas dans la matrice de confusion changerait sensiblement les pourcentages de rappel et de précision. Les chiffres obtenus doivent donc être interprétés comme des ordres de grandeur, pas comme des valeurs absolues.
- **Déséquilibre des classes** : la classe « à risque » ne représente que 20 % des étudiants. Un modèle peut afficher une bonne accuracy tout en étant peu performant sur la classe minoritaire, qui est pourtant celle qui compte le plus médicalement. C'est pourquoi le rappel (80 %) est ici plus informatif que l'accuracy (96 %).
- **Deux variables seulement** : le modèle ne s'appuie que sur `FCR_bpm` et `PAS_mmHg`. D'autres facteurs cliniques non mesurés ici (antécédents, âge, mode de vie, etc.) pourraient améliorer la détection des cas à risque, notamment les 3 cas manqués.
- **Origine des données** : les données utilisées proviennent d'un générateur pseudo-aléatoire calibré sur un nom d'étudiant, et non d'un dépistage réel. Les relations entre variables et les proportions de risque observées sont donc représentatives du mécanisme de génération choisi par le groupe, et ne doivent pas être interprétées comme une réalité épidémiologique.
- **Stabilité du modèle** : les deux modèles donnent ici des résultats identiques, mais rien ne garantit que ce serait encore le cas sur un autre échantillon d'étudiants ou avec une autre répartition entraînement/test. Une validation croisée (non réalisée ici) donnerait une estimation plus robuste de la performance réelle.
- **Risque d'usage aveugle** : un tel système ne doit être vu que comme une **aide au tri**, jamais comme un substitut au jugement médical. Se fier uniquement à la prédiction automatique reviendrait à accepter qu'environ un étudiant à risque sur cinq ne soit pas orienté vers une prise en charge, sans qu'aucun professionnel ne revérifie les cas classés « non à risque ».

## 7. Conclusion pour le commanditaire

Un système de prédiction automatique du risque, basé sur la fréquence cardiaque et la pression artérielle systolique, est réalisable et présente de bonnes performances globales (96 % de bonnes réponses). Il peut être utilisé comme **outil de pré-tri rapide** lors des campagnes de dépistage de masse, à condition de ne jamais l'utiliser comme décision finale : environ un étudiant à risque sur cinq échapperait au repérage automatique. Un contrôle humain, au moins ponctuel, sur les cas classés « non à risque », reste recommandé avant toute généralisation du système.
