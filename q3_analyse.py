# q3_analyse.py
# Auteur : FOKOU KELEFACK KERIANE KIANELLE
# Devoir : TP INF232
# Objectif : Q3 - Clustering K-Means (Thème A)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# 1. CHARGER LES DONNÉES
df = pd.read_csv('data/sante_etudiants.csv')
print("Aperçu des données :")
print(df.head())

# 2. EXTRAIRE LES VARIABLES
# On applique K-Means sur les deux indicateurs physiologiques : FCR_bpm et PAS_mmHg
X = df[['FCR_bpm', 'PAS_mmHg']].values

# 3. STANDARDISATION
# Indispensable car FCR et PAS n'ont pas la même échelle -> on centre-réduit
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. MÉTHODE DU COUDE (choix du nombre optimal de clusters)
inerties = []
k_range = range(1, 9)
for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    inerties.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(list(k_range), inerties, marker='o')
plt.xlabel('Nombre de clusters (k)')
plt.ylabel('Inertie intra-cluster')
plt.title("Méthode du coude - Choix de k")
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('rapport/coude_kmeans.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. APPLICATION DE K-MEANS AVEC k = 3
# Choix justifié : on distingue un profil "sain", un profil "modéré"
# et un profil "à risque" (cohérent avec la variable Risque du dataset)
k_optimal = 3
modele = KMeans(n_clusters=k_optimal, init='k-means++', n_init=10, random_state=42)
clusters = modele.fit_predict(X_scaled)
df['Cluster'] = clusters

# 6. SCORE DE SILHOUETTE (qualité du clustering)
silhouette = silhouette_score(X_scaled, clusters)
print(f"\nScore de silhouette (k={k_optimal}) : {silhouette:.4f}")

# 7. CENTROÏDES (dans l'échelle d'origine, pour interprétation)
centroides_scaled = modele.cluster_centers_
centroides = scaler.inverse_transform(centroides_scaled)
print("\n--- Centroïdes des clusters (échelle réelle) ---")
for i, c in enumerate(centroides):
    print(f"Cluster {i} : FCR = {c[0]:.2f} bpm | PAS = {c[1]:.2f} mmHg")

# 8. TAILLE ET PROFIL DE CHAQUE CLUSTER
print("\n--- Effectif et profil de chaque cluster ---")
profils = {}
for i in range(k_optimal):
    sous_groupe = df[df['Cluster'] == i]
    effectif = len(sous_groupe)
    part_risque = sous_groupe['Risque'].mean() * 100
    fcr_moy = sous_groupe['FCR_bpm'].mean()
    pas_moy = sous_groupe['PAS_mmHg'].mean()
    profils[i] = {
        'effectif': effectif,
        'fcr_moy': fcr_moy,
        'pas_moy': pas_moy,
        'part_risque': part_risque
    }
    print(f"Cluster {i} : {effectif} étudiants | FCR moy = {fcr_moy:.2f} | "
          f"PAS moy = {pas_moy:.2f} | % à risque = {part_risque:.1f}%")

# 9. ÉTIQUETAGE DES PROFILS (interprétation métier)
# On trie les clusters par PAS moyenne croissante pour nommer les profils
ordre = sorted(profils.keys(), key=lambda i: profils[i]['pas_moy'])
noms_profils = {ordre[0]: 'Profil sain', ordre[1]: 'Profil modéré', ordre[2]: 'Profil à risque'}
df['Profil'] = df['Cluster'].map(noms_profils)

print("\n--- Noms des profils attribués ---")
for c, nom in noms_profils.items():
    print(f"Cluster {c} -> {nom}")

# 10. GRAPHIQUE : Visualisation des clusters
plt.figure(figsize=(10, 6))
palette = {'Profil sain': 'green', 'Profil modéré': 'orange', 'Profil à risque': 'red'}
sns.scatterplot(
    data=df, x='FCR_bpm', y='PAS_mmHg', hue='Profil',
    palette=palette, alpha=0.7, s=60
)
plt.scatter(
    centroides[:, 0], centroides[:, 1],
    c='black', marker='X', s=200, label='Centroïdes'
)
plt.xlabel('Fréquence Cardiaque au Repos (bpm)')
plt.ylabel('Pression Artérielle Systolique (mmHg)')
plt.title(f'Clustering K-Means des étudiants (k={k_optimal})')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('rapport/clusters_kmeans.png', dpi=300, bbox_inches='tight')
plt.show()

# 11. EXPORT DES RÉSULTATS POUR LE RAPPORT (pour Elda)
with open('resultats_q3.txt', 'w') as f:
    f.write("=== RÉSULTATS Q3 - CLUSTERING K-MEANS ===\n\n")
    f.write(f"Taille de l'échantillon : {len(df)}\n")
    f.write(f"Variables utilisées : FCR_bpm, PAS_mmHg (standardisées)\n")
    f.write(f"Nombre de clusters (k) : {k_optimal}\n")
    f.write(f"Score de silhouette : {silhouette:.4f}\n\n")

    f.write("--- Centroïdes (échelle réelle) ---\n")
    for i, c in enumerate(centroides):
        f.write(f"Cluster {i} ({noms_profils[i]}) : FCR = {c[0]:.2f} bpm | PAS = {c[1]:.2f} mmHg\n")

    f.write("\n--- Détail des profils ---\n")
    for i in range(k_optimal):
        p = profils[i]
        f.write(f"Cluster {i} - {noms_profils[i]} : {p['effectif']} étudiants | "
                f"FCR moy = {p['fcr_moy']:.2f} bpm | PAS moy = {p['pas_moy']:.2f} mmHg | "
                f"% à risque (Risque=1) = {p['part_risque']:.1f}%\n")

    f.write("\n--- Interprétation ---\n")
    f.write("Le clustering K-Means fait apparaitre trois profils physiologiques distincts :\n")
    f.write("- Profil sain : FCR et PAS proches des valeurs normales, faible part d'étudiants a risque.\n")
    f.write("- Profil modere : valeurs intermediaires, part d'etudiants a risque plus elevee.\n")
    f.write("- Profil a risque : FCR et/ou PAS elevees, forte proportion d'etudiants classes a risque.\n")
    f.write("Ce resultat est coherent avec l'etiquette 'Risque' du jeu de donnees, sans que celle-ci\n")
    f.write("ait ete utilisee pour construire les clusters (apprentissage non supervise).\n")

print("\nAnalyse terminée. Résultats sauvegardés dans 'resultats_q3.txt'.")