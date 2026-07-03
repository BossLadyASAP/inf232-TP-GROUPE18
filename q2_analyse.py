# q2_analyse.py
# Auteur : KARIS ZOGO EMMANUEL
# Devoir : TP INF232
# Objectif : Q2 - Corrélation + Régression linéaire (Thème A)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. CHARGER LES DONNÉES
df = pd.read_csv('data/sante_etudiants.csv')
print("Aperçu des données :")
print(df.head())

# 2. EXTRAIRE LES VARIABLES
# X = Fréquence Cardiaque (FCR_bpm), Y = Pression Artérielle (PAS_mmHg)
X = df[['FCR_bpm']].values  # doit être en 2D pour sklearn
y = df['PAS_mmHg'].values   # 1D

# 3. STATISTIQUES DESCRIPTIVES (pour le rapport)
print("\n--- Statistiques descriptives ---")
print(f"Moyenne de la FC (bpm) : {np.mean(X):.2f}")
print(f"Écart-type de la FC (bpm) : {np.std(X):.2f}")
print(f"Moyenne de la PAS (mmHg) : {np.mean(y):.2f}")
print(f"Écart-type de la PAS (mmHg) : {np.std(y):.2f}")

# 4. CORRÉLATION
correlation = np.corrcoef(X.flatten(), y)[0, 1]
print(f"\nCoefficient de corrélation de Pearson (r) : {correlation:.4f}")

# 5. RÉGRESSION LINÉAIRE
modele = LinearRegression()
modele.fit(X, y)

# Coefficients
a = modele.coef_[0]          # pente
b = modele.intercept_        # ordonnée à l'origine
print(f"Équation de la droite : PAS = {a:.4f} * FC + {b:.4f}")

# Prédictions et R²
y_pred = modele.predict(X)
r2 = r2_score(y, y_pred)
print(f"Coefficient de détermination (R²) : {r2:.4f}")

# 6. RÉSIDUS (pour détecter les outliers)
residus = y - y_pred
seuil = 2 * np.std(residus)   # on considère outlier si résidu > 2 écarts-types
outliers = np.abs(residus) > seuil
nb_outliers = np.sum(outliers)
print(f"Nombre d'outliers détectés : {nb_outliers} sur {len(df)}")

# 7. GRAPHIQUE : Nuage de points + droite de régression
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X.flatten(), y=y, label='Données observées', alpha=0.6)
plt.plot(X.flatten(), y_pred, color='red', linewidth=2, label='Droite de régression')
plt.xlabel('Fréquence Cardiaque (bpm)')
plt.ylabel('Pression Artérielle Systolique (mmHg)')
plt.title('Relation entre FC et PAS chez les étudiants')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Sauvegarder le graphique
plt.savefig('rapport/nuage_regression.png', dpi=300, bbox_inches='tight')
plt.show()

# 8. GRAPHIQUE : Résidus
plt.figure(figsize=(10, 4))
plt.scatter(X.flatten(), residus, alpha=0.6)
plt.axhline(y=0, color='red', linestyle='--')
plt.axhline(y=seuil, color='orange', linestyle=':', label=f'Seuil +2σ ({seuil:.2f})')
plt.axhline(y=-seuil, color='orange', linestyle=':', label=f'Seuil -2σ ({-seuil:.2f})')
plt.xlabel('Fréquence Cardiaque (bpm)')
plt.ylabel('Résidus (PAS observée - PAS prédite)')
plt.title('Analyse des résidus')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('rapport/residus.png', dpi=300, bbox_inches='tight')
plt.show()

# 9. EXPORT DES RÉSULTATS POUR LE RAPPORT (pour Albert)
with open('resultats_q2.txt', 'w') as f:
    f.write("=== RÉSULTATS Q2 - CORRÉLATION ET RÉGRESSION ===\n\n")
    f.write(f"Taille de l'échantillon : {len(df)}\n")
    f.write(f"Moyenne FC (bpm) : {np.mean(X):.2f}\n")
    f.write(f"Écart-type FC (bpm) : {np.std(X):.2f}\n")
    f.write(f"Moyenne PAS (mmHg) : {np.mean(y):.2f}\n")
    f.write(f"Écart-type PAS (mmHg) : {np.std(y):.2f}\n\n")
    f.write(f"Coefficient de corrélation (r) : {correlation:.4f}\n")
    f.write(f"Coefficient de détermination (R²) : {r2:.4f}\n\n")
    f.write(f"Équation de la droite : PAS = {a:.4f} * FC + {b:.4f}\n\n")
    f.write(f"Nombre d'outliers détectés : {nb_outliers}\n")
    f.write(f"Seuil utilisé pour les outliers : 2 * écart-type = {seuil:.4f}\n")

print("\n Analyse terminée. Résultats sauvegardés dans 'resultats_q2.txt'.")
