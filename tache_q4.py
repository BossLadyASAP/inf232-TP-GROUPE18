import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

def classification_supervisee():
    """
    Q4 - classification supervisee pour predire la colonne 'Risque'
    """
    print("=" * 60)
    print("Q4 - CLASSIFICATION SUPERVISEE")
    print("=" * 60)

    # Chargement des donnees
    df = pd.read_csv("data/sante_etudiants.csv")
    print(f"\nDonnees chargees : {df.shape[0]} etudiants, {df.shape[1]} colonnes")

    # Separation facture/target
    X = df[['FCR_bpm', 'PAS_mmHg']]
    y = df['Risque']

    print(f"\nDistribution de la cible 'Risque' :")
    print(y.value_counts())
    print(f"Pourcentage de classe 1 (Risque) : {y.mean()*100:.2f}%")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"\nSplit : {X_train.shape[0]} entrainement, {X_test.shape[0]} test")

    # Modele 1 : Regression logique
    print("\n" + "-" * 60)
    print("Modele 1 : REGRESSION LOGIQUE")
    print("-" * 60)
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)

    print("\nCoefficient du modele :")
    print(f"FCR_bpm : {lr_model.coef_[0][0]:.4f}")
    print(f"PAS_mmHg : {lr_model.coef_[0][1]:.4f}")
    print(f"Intercept : {lr_model.intercept_[0]:.4f}")

    # Modele 2 : Random Forest
    print("n" + "-" * 60)
    print("MODELE 2 : RANDOM FOREST")
    print("-" * 60)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    print("\nImportance des factures :")
    print(f"FCR_bpm : {rf_model.feature_importances_[0]:.4f}")
    print(f"PAS_mmHg : {rf_model.feature_importances_[1]:.4f}")

    # Evaluation des modeles
    print("\n" + "=" * 60)
    print("EVALUATION DES MODELES")
    print("=" * 60)

    print("\n--- Regression Logique ---")
    print(f"Accuracy : {accuracy_score(y_test, y_pred_lr):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred_lr):.4f}")
    print(f"Recall : {f1_score(y_test, y_pred_lr):.4f}")
    print(f"F1-Score : {f1_score(y_test, y_pred_lr):.4f}")

    print("\n--- Random Forest ---")
    print(f"Accuracy : {accuracy_score(y_test, y_pred_rf):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred_rf):.4f}")
    print(f"recall : {recall_score(y_test, y_pred_rf):.4f}")
    print(f"F1-Score : {f1_score(y_test, y_pred_rf):.4f}")

    # Rapport detaille
    print("\n" + "=" * 60)
    print("RESULTAT DE CLASSIFICATION (RANDOM FOREST)")
    print("=" * 60)
    print(classification_report(y_test, y_pred_rf))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred_rf)
    print("\nMatrice de confusion :")
    print(cm)

    # Creation du dossier rapport
    os.makedirs("resultat", exist_ok=True)

    # Visualisation de la matrice de confusion
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Pas de risque', 'Risque'],
                yticklabels=['PAS de risque', 'Risque'])
    plt.title('Matrice de Confusion _ Random Forest')
    plt.ylabel('Classe reelle')
    plt.xlabel('Classe predite')
    plt.savefig('rapport/matrice_confusion_q4.png', dpi=150, bbox_inches='tight')
    print(f"\nGraphique sauvegarde : rapport/matrice_confusion_q4.png")

    # Visualisation des frontieres de decision
    plt.figure(figsize=(12, 5))

    # Regression logique
    plt.subplot(1, 2, 1)
    x_min, x_max = X['FCR_bpm'].min() - 5, X['FCR_bpm'].max() + 5
    y_min, y_max = X['PAS_mmHg'].min() -5, X['PAS_mmHg'].max() + 5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 1),
                         np.arange(y_min, y_max, 1))
    Z = lr_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
    scatter = plt.scatter(X['FCR_bpm'], X['PAS_mmHg'], c=y, cmap='RdYlBu', alpha=0.7)
    plt.xlabel('FCR_bpm')
    plt.ylabel('PAS_mmHg')
    plt.title('Regression Logique')
    plt.colorbar(scatter)

    # Rendom Forest
    plt.subplot(1, 2, 2)
    Z = rf_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
    scatter = plt.scatter(X['FCR_bpm'], X['PAS_mmHg'], c=y, cmap='RdYlBu', alpha=0.7)
    plt.xlabel('FCR_bpm')
    plt.ylabel('PAS_mmHg')
    plt.title('Random Forest')
    plt.colorbar(scatter)

    plt.tight_layout()
    plt.savefig('rapport/frontieres_decision_q4.png', dpi=150, bbox_inches='tight')
    print(f"Graphique sauvegarde : rapport/frontieres_decision_q4.png")

    # Sauvegarde du rapport texte
    with open('rapport/resultat_classification_q4.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("Q4 - RAPPORT DE CLASSIFICATION SUPERVISEE\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Donnees : {df.shape[0]} etudiants\n")
        f.write(f"Factures : FCR_bpm, PAS_mmHg\n")
        f.write(f"Cible : Risque (0/1)\n\n")
        f.write(f"Distribution : {y.value_counts().to_dict()}\n\n")
        f.write("-" * 60 + "\n")
        f.write("REGRESSION LOGIQUE\n")
        f.write("-" * 60 + "\n")
        f.write(f"Accuracy : {accuracy_score(y_test, y_pred_lr):.4f}\n")
        f.write(f"Precision : {precision_score(y_test, y_pred_lr):.4f}\n")
        f.write(f"Precision : {precision_score(y_test, y_pred_lr):.4f}\n")
        f.write(f"Recall : {recall_score(y_test, y_pred_lr):.4f}\n")
        f.write(f"F1-Score : {f1_score(y_test, y_pred_lr):.4f}\n\n")
        f.write("-" * 60 + "\n")
        f.write("RANDOM FOREST\n")
        f.write("-" * 60 + "\n")
        f.write(f"Accuracy : {accuracy_score(y_test, y_pred_rf):.4f}\n")
        f.write(f"Precision : {precision_score(y_test, y_pred_rf):.4f}\n")
        f.write(f"Recall : {recall_score(y_test, y_pred_rf):.4f}\n")
        f.write(f"F1-Score : {f1_score(y_test, y_pred_rf):.4f}\n\n")
        f.write("Matrice de confusion (Random Forest) :\n")
        f.write(str(cm) + "\n")

    print(f"Rapport texte sauvegarde : resultat_classification_q4.png.txt")
    print("\n" + "=" * 60)
    print("CLASSIFICATION TERMINEE AVEC SUCCES")
    print("=" * 60)

    return lr_model, rf_model

if __name__ == "__main__":
    classification_supervisee()
