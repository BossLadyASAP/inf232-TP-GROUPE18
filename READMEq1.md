# INF232 — TP Statistiques et Analyse de Données
## Thème A : Service de santé universitaire de MBOUDA

Groupe 18 — Chef de groupe : MATAGNE DASSE PRESLIE CHANEL

---

## 1. Contexte

Le service de santé de l'Université de MBOUDA a mené un dépistage de
routine sur un échantillon d'étudiants. Pour chaque étudiant, deux
indicateurs physiologiques ont été mesurés, ainsi qu'une étiquette de
risque ("à risque" / "non à risque"). Le directeur du service pose 4
questions auxquelles ce projet répond, une par une, à l'aide des outils
statistiques vus en cours (statistique univariée, bivariée,
classification non supervisée, classification supervisée).

**Indicateurs choisis et justification :**

| Variable | Nom complet | Unité | Justification |
|---|---|---|---|
| `FCR_bpm` | Fréquence Cardiaque au Repos | battements/minute | Mesure rapide et non invasive, standard en dépistage de masse |
| `PAS_mmHg` | Pression Artérielle Systolique | mmHg | Indicateur classique de risque cardiovasculaire, plausiblement lié à la FCR |
| `Risque` | Étiquette de risque | 0 = non à risque, 1 = à risque | Classement du service de santé, utilisé pour la classification supervisée (Q4) |

---

## 2. Génération des données (Pôle 0)

Les données sont **entièrement reproductibles** à partir du nom du chef
de groupe, conformément à la consigne du TP.

- **Nom transformé :** `MATAGNEDASSEPRESLIECHANEL`
- **Méthode de génération de la graine :** hachage SHA-256 du nom
  nettoyé (majuscules, sans espaces), dont les 8 premiers caractères
  hexadécimaux sont convertis en entier
- **Générateur :** `numpy.random.seed(graine)` (Mersenne Twister),
  garantissant que deux exécutions du script donnent toujours
  exactement le même jeu de données
- **Taille de l'échantillon :** n = 250 étudiants

Relancer le générateur reproduit systématiquement le même fichier
`data/sante_etudiants.csv`.

---

## 3. Structure du dossier

```
INF232_TP_GROUPE18/
├── README.md                     <- ce fichier
├── generateur_donnees.py         <- génère data/sante_etudiants.csv à partir du nom du chef
├── question1_fcr.py              <- Question 1 : analyse univariée de la FCR
├── question2_bivarie.py          <- Question 2 : lien FCR / PAS (à venir)
├── question3_non_supervise.py    <- Question 3 : profils naturels (à venir)
├── question4_supervise.py        <- Question 4 : prédiction du risque (à venir)
├── data/
│   └── sante_etudiants.csv       <- jeu de données généré
├── resultats/
│   ├── histogramme_fcr.png
│   └── boxplot_fcr.png
└── rapport/
    └── rapport_TP_groupe18.pdf   <- document "Rapport" du rendu
```

---

## 4. Prérequis

- Python 3.10 ou plus récent
- Bibliothèques : `pandas`, `numpy`, `matplotlib`

Installation :
```bash
pip install pandas numpy matplotlib
```

---

## 5. Mode d'emploi

**Étape 1 — Générer les données** (à faire une seule fois, ou pour
vérifier la reproductibilité) :
```bash
python3 generateur_donnees.py
```
→ crée/écrase `data/sante_etudiants.csv` et affiche la graine du groupe
dans le terminal.

**Étape 2 — Lancer l'analyse de la Question 1** :
```bash
python3 question1_fcr.py
```
→ affiche dans le terminal les mesures de tendance centrale, de
dispersion, la liste des étudiants atypiques et un message de synthèse
en langage simple ; enregistre `histogramme_fcr.png` et `boxplot_fcr.png`
dans le dossier `resultats/`.

**Étapes suivantes (Q2, Q3, Q4)** : chaque script se lance de la même
façon, indépendamment, une fois `data/sante_etudiants.csv` généré.

---

## 6. Question 1 — Répartition de la FCR (résumé des résultats)

| Mesure | Valeur |
|---|---|
| Moyenne | 72,44 bpm |
| Médiane | 72,60 bpm |
| Écart-type | 11,76 bpm |
| Q1 / Q3 | 65,30 / 78,85 bpm |
| Bornes boîte à moustaches | [44,97 ; 99,17] |
| Étudiants atypiques | 7 (n° 48, 93, 148, 154, 182, 217, 246) |

Moyenne et médiane très proches → distribution globalement symétrique,
peu déformée par les valeurs extrêmes. Détails complets, limites et
interprétation dans `rapport/rapport_TP_groupe18.pdf`.

---

## 7. Équipe et répartition des pôles

| Pôle | Membres | Mission |
|---|---|---|
| 0 — Génération des données | | Graine, générateur, dataset |
| 1 — Q1 (univarié) | | Répartition de la FCR |
| 2 — Q2 (bivarié) | | Lien FCR / PAS |
| 3 — Q3 (non supervisé) | | Profils naturels d'étudiants |
| 4 — Q4 (supervisé) | | Prédiction du risque |
| 5 — Intégration & rapport | | Assemblage final |

---

## 8. Avertissement anti-fraude

Ce jeu de données est unique au groupe 18, généré déterministiquement à
partir du nom de son chef. Toute correspondance exacte avec les données
d'un autre groupe serait un cas de fraude au sens du règlement du TP.
