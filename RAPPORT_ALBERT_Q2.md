          # RAPPORT DE TP: Analyse de la relation entre Frequence Cardiaque et Pression Arterielle



       Contexte: **Theme A- Service de sante universitaire
       **Etudiant: **Albert

                  **Objectif: **Verifier si la Frequence Cardiaque et la Pression Arterielle  Systolique sont liees, et voir si l'on peut estimer l,une par rapport a l'autre.

        ---

          ## 1. Donnees brutes et Statistiques Descriptives.

          L'etude a ete realisee sur un echantillon de **250 etudiants**.Les variables ainsi etudiees sont:
           * ** Variable explicative(X):** Frequence Cardiaque au repos(FCR_bpm).
           * ** Variables a expliquer (Y): **Pression Arterielle Systolique (PAS_mmHg).

           ### Indicateurs cles calcules :
           * **Moyenne de X(FC):**72,34 bmp
           (Ecart-type:11,38)
           * **Moyenne de Y(PAS):**124,99 mmHg
           (Ecart-type:11,39)

           ---


           ## 2. Resultats de la modelisation Lineaire

           ### 2.1. Analyse de la Correlation 
           Le coefficient de la Correelation de Pearson obtenu est **r = o,4135**
           * **Interpretation :** Il existe une correlation positive moderee**.
           Lorsque la FC augmente, la PAS augmente egalement en tendance, mais le lien lineaire n'est pas tres fort.

           ### 2.2. Equation de la droite de regression
           La formule mathematique permanante d'estimer la PAS en fonction de la FC est:
           $$PAS = O,4126\times FC + 95,1374$$

           Ci-dessous le graphique du nuage de points incluant la droite de regression


           ![Nuage de points et regression](rapport/nuage_regression.png)

           ---

           ## 3. Fiabilite et Limites du Modele

           ### 3.1. Qualites de la prediction (RxR)
           Le coefficient de determinaton est :
           **RXR = 0,1710** (soit **17,1 %**).
           * **Interpretation : ** Seulement 17 % des variables de la FC. Les 83 % restants dependent d'autres facteurs comme le stress, la genetique ou le poids. L'estimation est donc techniquement possible mais avec une **grande marge d'erreur**.

           ### 3.2. Detection des Outiliers(Valeurs aberrantes)
           En utilisant un seuil critique de 2 fois l'ecart-type (soit 20,6848), **6 etudiants outiliers** ont ete detectes. Le graphique des residus  ci-dessous met en evidence ces ecarts majeurs:


           ![Analyse des residus](rapport/residus.png)
           
           Pour ces 6 etudiants la formule mathematique donne un resultat tres trompeur.

           ---

           ## 4. Conclusion et Consignes de securite Medicale

           1. **Plage de validite :** La formule ne doit jamais etre utilisee en dehors des valeurs observees dans l'echantillon (FC entre 41,9 et 120,1 bmp).
           
           2. **Regle d'or une estimation mathematique ne possede pas la fiabilite necessaire pour un usage medical pricis et **ne remplecera jamais une mesure directe** de la tension par un professionnel de sante.
             



