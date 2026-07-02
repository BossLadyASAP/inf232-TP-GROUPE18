import numpy as np
import pandas as pd
import hashlib
import os

def generate_seed_from_name(full_name):
    """
    Fonction obligatoire demandée par le prof : 
    Transforme le nom complet en une graine numérique reproductible.
    """
    # Nettoyage : Majuscules, pas d'espaces, pas d'accents (simplifié)
    clean_name = "".join(full_name.upper().split())
    
    # Hashage pour garantir l'unicité et le déterminisme
    hash_object = hashlib.sha256(clean_name.encode())
    seed = int(hash_object.hexdigest()[:8], 16)
    return seed

def generate_dataset(full_name, n_samples=250):
    """
    Générateur de données pour le Thème A (Santé Universitaire).
    Produit : FCR, PAS et l'étiquette de Risque.
    """
    seed = generate_seed_from_name(full_name)
    np.random.seed(seed)
    
    print(f"--- GÉNÉRATEUR GROUPE 18 ---")
    print(f"Nom du chef : {full_name}")
    print(f"Graine générée : {seed}")
    
    # 1. Indicateur physiologique 1 : Fréquence Cardiaque au Repos (FCR)
    # Distribution normale : moyenne 72, écart-type 10
    fcr = np.random.normal(72, 10, n_samples)
    
    # 2. Indicateur physiologique 2 : Pression Artérielle Systolique (PAS)
    # Liée à la FCR (corrélation positive) + un bruit aléatoire
    pas = 85 + 0.55 * fcr + np.random.normal(0, 7, n_samples)
    
    # Ajout de quelques cas extrêmes (Outliers) pour les analyses futures
    outlier_indices = np.random.choice(n_samples, 10, replace=False)
    fcr[outlier_indices[:5]] += 40
    pas[outlier_indices[5:]] += 50
    
    # 3. Étiquette de Risque (Classification)
    # Calcul d'un score de risque combiné
    risk_score = (fcr - 72) / 10 + (pas - 125) / 12 + np.random.normal(0, 0.4, n_samples)
    labels = (risk_score > 1.3).astype(int)
    
    # Création du DataFrame
    df = pd.DataFrame({
        'Etudiant_ID': range(1, n_samples + 1),
        'FCR_bpm': np.round(fcr, 1),
        'PAS_mmHg': np.round(pas, 1),
        'Risque': labels
    })
    
    # Sauvegarde pour les membres du groupe
    os.makedirs("data", exist_ok=True)
    file_path = "data/sante_etudiants.csv"
    df.to_csv(file_path, index=False)
    
    print(f"Succès : Fichier généré dans '{file_path}'")
    return df

if __name__ == "__main__":
    # Nom du chef de groupe (Chanel)
    CHEF = "MATAGNE DASSE PRESLIE CHANEL"
    generate_dataset(CHEF)
