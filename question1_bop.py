# =============================================================================
# INF232 - TP Statistiques et Analyse de Données
# THEME A : Service de santé universitaire de MBOUDA
# QUESTION 1 : Analyse univariée du premier indicateur physiologique
#              -> Fréquence Cardiaque au Repos (FCR, en battements/minute)
# =============================================================================
#
# Rappel de la question posée par le directeur du service de santé :
# "Comment se répartit le premier indicateur physiologique mesuré, quelles
#  sont les valeurs typiques, y a-t-il des étudiants dont la mesure sort du
#  lot, et comment présenter cela simplement à une équipe médicale non
#  formée en statistique ?"
#
# Notion du cours mobilisée : STATISTIQUE UNIVARIEE (une seule variable
# étudiée ici : la FCR). On y applique les mesures de tendance centrale,
# les mesures de dispersion, la détection de valeurs atypiques, et les
# représentations graphiques adaptées (histogramme, boîte à moustaches).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
# CONSTANTES DU SCRIPT
# -----------------------------------------------------------------------
CHEMIN_FICHIER_DONNEES = "data/sante_etudiants.csv"
NOM_COLONNE_ETUDIEE = "FCR_bpm"          # premier indicateur physiologique
UNITE_MESURE = "battements/minute"
DOSSIER_SORTIE_GRAPHIQUES = "resultats"
COEFFICIENT_MOUSTACHE = 1.5              # coefficient standard de la boîte à moustaches


# -----------------------------------------------------------------------
# 1) CHARGEMENT DES DONNEES
# -----------------------------------------------------------------------
def charger_donnees(chemin_fichier: str) -> pd.DataFrame:
    """
    Charge le fichier CSV généré par le pôle 0 et retourne un DataFrame pandas.
    """
    donnees = pd.read_csv(chemin_fichier)
    return donnees


# -----------------------------------------------------------------------
# 2) MESURES DE TENDANCE CENTRALE
# -----------------------------------------------------------------------
def calculer_tendance_centrale(serie: pd.Series) -> dict:
    """
    Calcule les mesures de tendance centrale vues en cours :
    moyenne, médiane et mode.

    Rôle de chaque mesure :
      - la moyenne donne une valeur centrale globale, mais est sensible
        aux valeurs extrêmes (cf. cours, exemple des 3 groupes G1/G2/G3) ;
      - la médiane est plus robuste car elle donne le centre réel de la
        distribution, peu influencée par les cas extrêmes ;
      - le mode (ici, valeur arrondie la plus fréquente) donne la valeur
        la plus courante, utile pour compléter le portrait de la série.
    """
    moyenne = serie.mean()
    mediane = serie.median()
    # Le mode est calculé sur les valeurs arrondies à l'entier, car la FCR
    # est une variable continue : sans arrondi, chaque valeur serait unique
    mode_arrondi = serie.round(0).mode()[0]

    return {
        "moyenne": round(moyenne, 2),
        "mediane": round(mediane, 2),
        "mode_arrondi": mode_arrondi,
    }


# -----------------------------------------------------------------------
# 3) MESURES DE DISPERSION
# -----------------------------------------------------------------------
def calculer_dispersion(serie: pd.Series) -> dict:
    """
    Calcule les mesures de dispersion vues en cours :
    étendue, variance, écart-type, quartiles et distance interquartile.

    Rôle : ces mesures indiquent à quel point les valeurs sont dispersées
    autour du centre de la distribution. L'écart-type en particulier
    permet de dire "la plupart des étudiants ont une FCR comprise entre
    (moyenne - écart-type) et (moyenne + écart-type)".
    """
    etendue = serie.max() - serie.min()

    # ddof=0 : on utilise la variance de la population (formule du cours,
    # division par n), et non celle d'un échantillon (division par n-1)
    variance = serie.var(ddof=0)
    ecart_type = serie.std(ddof=0)

    premier_quartile = serie.quantile(0.25)
    troisieme_quartile = serie.quantile(0.75)
    distance_interquartile = troisieme_quartile - premier_quartile

    return {
        "etendue": round(etendue, 2),
        "variance": round(variance, 2),
        "ecart_type": round(ecart_type, 2),
        "premier_quartile": round(premier_quartile, 2),
        "troisieme_quartile": round(troisieme_quartile, 2),
        "distance_interquartile": round(distance_interquartile, 2),
    }


# -----------------------------------------------------------------------
# 4) DETECTION DES VALEURS ATYPIQUES (methode de la boite a moustaches)
# -----------------------------------------------------------------------
def detecter_valeurs_atypiques(serie: pd.Series, mesures_dispersion: dict) -> pd.DataFrame:
    """
    Applique la méthode vue en cours pour détecter les valeurs extrêmes :
        borne_basse  = Q1 - 1.5 * distance_interquartile
        borne_haute  = Q3 + 1.5 * distance_interquartile

    Toute valeur en dehors de [borne_basse, borne_haute] est considérée
    comme une valeur atypique (un point isolé sur la boîte à moustaches).
    C'est la méthode retenue ici car elle est plus robuste que le z-score
    (elle ne dépend pas de la moyenne, qui est elle-même sensible aux
    valeurs extrêmes qu'on cherche justement à détecter).
    """
    q1 = mesures_dispersion["premier_quartile"]
    q3 = mesures_dispersion["troisieme_quartile"]
    iq = mesures_dispersion["distance_interquartile"]

    borne_basse = q1 - COEFFICIENT_MOUSTACHE * iq
    borne_haute = q3 + COEFFICIENT_MOUSTACHE * iq

    masque_atypique = (serie < borne_basse) | (serie > borne_haute)
    etudiants_atypiques = donnees.loc[masque_atypique, ["Etudiant_ID", NOM_COLONNE_ETUDIEE]]

    print(f"Bornes de la boîte à moustaches : [{borne_basse:.2f} ; {borne_haute:.2f}]")
    return etudiants_atypiques


# -----------------------------------------------------------------------
# 5) NOMBRE DE CLASSES POUR L'HISTOGRAMME (regle de Sturges)
# -----------------------------------------------------------------------
def calculer_nombre_classes_sturges(nombre_observations: int) -> int:
    """
    Applique la règle de Sturges vue en cours pour estimer un nombre de
    classes raisonnable pour l'histogramme : J = 1 + 3.3 * log10(n)
    """
    nombre_classes = 1 + 3.3 * np.log10(nombre_observations)
    return round(nombre_classes)


# -----------------------------------------------------------------------
# 6) GRAPHIQUES
# -----------------------------------------------------------------------
def tracer_histogramme(serie: pd.Series, nombre_classes: int, chemin_sortie: str) -> None:
    """
    Trace l'histogramme des effectifs de la FCR, regroupée en classes.
    Rôle : montrer la FORME globale de la distribution (est-elle
    symétrique ? y a-t-il un pic net ? etc.), plus lisible qu'un long
    tableau de chiffres pour l'équipe médicale.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(serie, bins=nombre_classes, color="#4C72B0", edgecolor="black")
    plt.title("Répartition de la Fréquence Cardiaque au Repos (FCR)")
    plt.xlabel(f"FCR ({UNITE_MESURE})")
    plt.ylabel("Nombre d'étudiants (effectif)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(chemin_sortie, dpi=150)
    plt.close()


def tracer_boite_moustaches(serie: pd.Series, chemin_sortie: str) -> None:
    """
    Trace la boîte à moustaches de la FCR.
    Rôle : c'est LE graphique le plus adapté pour répondre en un coup
    d'œil à la question du directeur sur les valeurs atypiques, car il
    montre en même temps la médiane, la dispersion (boîte = 50% central
    des étudiants) et les valeurs extrêmes (points isolés).
    """
    plt.figure(figsize=(6, 5))
    plt.boxplot(serie, vert=True, patch_artist=True,
                boxprops=dict(facecolor="#DD8452"),
                medianprops=dict(color="black", linewidth=2))
    plt.title("Boîte à moustaches de la FCR")
    plt.ylabel(f"FCR ({UNITE_MESURE})")
    plt.xticks([1], ["Étudiants dépistés"])
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(chemin_sortie, dpi=150)
    plt.close()


# -----------------------------------------------------------------------
# 7) MESSAGE DESTINE AU DIRECTEUR (langage non statisticien)
# -----------------------------------------------------------------------
def rediger_message_pour_directeur(tendance: dict, dispersion: dict,
                                    etudiants_atypiques: pd.DataFrame,
                                    nombre_total_etudiants: int) -> str:
    """
    Construit automatiquement, à partir des résultats calculés, un
    paragraphe de synthèse en langage simple, destiné à l'équipe médicale
    (3e volet de la question du directeur).
    """
    nombre_atypiques = len(etudiants_atypiques)
    liste_ids_atypiques = ", ".join(str(i) for i in etudiants_atypiques["Etudiant_ID"].tolist())

    message = (
        f"Sur les {nombre_total_etudiants} étudiants dépistés, la fréquence "
        f"cardiaque au repos moyenne est de {tendance['moyenne']} battements/minute, "
        f"et la moitié des étudiants se situent entre {dispersion['premier_quartile']} "
        f"et {dispersion['troisieme_quartile']} battements/minute (leur médiane est de "
        f"{tendance['mediane']} bpm). La plupart des étudiants ont une FCR comprise "
        f"entre {round(tendance['moyenne'] - dispersion['ecart_type'], 1)} et "
        f"{round(tendance['moyenne'] + dispersion['ecart_type'], 1)} bpm.\n\n"
        f"Nous avons repéré {nombre_atypiques} étudiant(s) dont la fréquence cardiaque "
        f"sort nettement de cette norme (étudiant(s) n°{liste_ids_atypiques}) : "
        f"ils mériteraient un suivi individualisé."
    )
    return message


# -----------------------------------------------------------------------
# PROGRAMME PRINCIPAL
# -----------------------------------------------------------------------
if __name__ == "__main__":
    import os
    os.makedirs(DOSSIER_SORTIE_GRAPHIQUES, exist_ok=True)

    # Etape 1 : chargement des données
    donnees = charger_donnees(CHEMIN_FICHIER_DONNEES)
    serie_fcr = donnees[NOM_COLONNE_ETUDIEE]
    nombre_total_etudiants = len(serie_fcr)

    print("=" * 70)
    print("QUESTION 1 - ANALYSE UNIVARIEE DE LA FREQUENCE CARDIAQUE AU REPOS")
    print("=" * 70)
    print(f"Nombre d'étudiants dépistés : {nombre_total_etudiants}\n")

    # Etape 2 : mesures de tendance centrale
    resultats_tendance = calculer_tendance_centrale(serie_fcr)
    print("--- Mesures de tendance centrale ---")
    for nom_mesure, valeur in resultats_tendance.items():
        print(f"{nom_mesure} : {valeur}")

    # Etape 3 : mesures de dispersion
    resultats_dispersion = calculer_dispersion(serie_fcr)
    print("\n--- Mesures de dispersion ---")
    for nom_mesure, valeur in resultats_dispersion.items():
        print(f"{nom_mesure} : {valeur}")

    # Etape 4 : détection des valeurs atypiques
    print("\n--- Détection des valeurs atypiques (méthode boîte à moustaches) ---")
    etudiants_atypiques = detecter_valeurs_atypiques(serie_fcr, resultats_dispersion)
    print(f"Nombre d'étudiants atypiques détectés : {len(etudiants_atypiques)}")
    print(etudiants_atypiques.to_string(index=False))

    # Etape 5 : graphiques
    nombre_classes = calculer_nombre_classes_sturges(nombre_total_etudiants)
    print(f"\nNombre de classes retenu pour l'histogramme (règle de Sturges) : {nombre_classes}")

    tracer_histogramme(serie_fcr, nombre_classes,
                        os.path.join(DOSSIER_SORTIE_GRAPHIQUES, "histogramme_fcr.png"))
    tracer_boite_moustaches(serie_fcr,
                             os.path.join(DOSSIER_SORTIE_GRAPHIQUES, "boxplot_fcr.png"))
    print(f"\nGraphiques enregistrés dans le dossier '{DOSSIER_SORTIE_GRAPHIQUES}/'")

    # Etape 6 : message de synthèse pour le directeur
    message_directeur = rediger_message_pour_directeur(
        resultats_tendance, resultats_dispersion, etudiants_atypiques, nombre_total_etudiants
    )
    print("\n" + "=" * 70)
    print("MESSAGE DE SYNTHESE POUR LE DIRECTEUR (langage non statisticien)")
    print("=" * 70)
    print(message_directeur)

    # Etape 7 : rappel des limites à discuter dans le rapport
    print("\n" + "=" * 70)
    print("LIMITES A DISCUTER DANS LE RAPPORT")
    print("=" * 70)
    print(
        "- La moyenne peut être tirée vers le haut par quelques valeurs très élevées :\n"
        "  comparer avec la médiane permet de vérifier si la distribution est asymétrique.\n"
        "- La taille de l'échantillon (n={}) influence la fiabilité de la généralisation\n"
        "  à l'ensemble des étudiants de l'université.\n"
        "- Une valeur jugée 'atypique' au sens statistique n'est pas automatiquement une\n"
        "  anomalie médicale grave, et inversement : la significativité statistique ne\n"
        "  remplace pas l'avis clinique d'un médecin.".format(nombre_total_etudiants)
    )
