import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

def simuler_modele(alpha, beta, delta, gamma, population_initiale_lapin, population_initiale_renard):
    time = [0]
    lapin = [population_initiale_lapin]
    renard = [population_initiale_renard]
    
    step = 0.001
    for _ in range(0, 100_000):
        new_value_time = time[-1] + step
        new_value_lapin = (lapin[-1] * (alpha - beta * renard[-1])) * step + lapin[-1]
        new_value_renard = (renard[-1] * (delta * lapin[-1] - gamma)) * step + renard[-1]

        time.append(new_value_time)
        lapin.append(new_value_lapin)
        renard.append(new_value_renard)

    lapin = np.array(lapin)
    lapin *= 1000
    renard = np.array(renard)
    renard *= 1000    
    
    return time, lapin, renard

# Charger les données
csv = pd.read_csv("population.csv")
print("Données réelles :")
print(csv)

# Paramètres à tester
parametres = [1/3, 2/3, 1, 4/3]

# Variables pour garder trace des meilleurs paramètres
meilleure_erreur = float('inf')
meilleurs_params = None
meilleurs_resultats = None

# Population initiale depuis les données réelles
population_initiale_lapin = csv['proie'].iloc[0]/1000
population_initiale_renard = csv['predateur'].iloc[0]/1000

print("\nRecherche des meilleurs paramètres...")
# Tester toutes les combinaisons
for alpha in parametres:
    for beta in parametres:
        for delta in parametres:
            for gamma in parametres:
                # Simuler avec ces paramètres
                time, lapin, renard = simuler_modele(alpha, beta, delta, gamma, 
                                                   population_initiale_lapin, 
                                                   population_initiale_renard)
                
                # Calculer l'erreur avec les données réelles
                erreur_lapin = np.mean((lapin[:len(csv)] - csv['proie'])**2)
                erreur_renard = np.mean((renard[:len(csv)] - csv['predateur'])**2)
                erreur_totale = erreur_lapin + erreur_renard
                
                # Si c'est la meilleure combinaison jusqu'à présent
                if erreur_totale < meilleure_erreur:
                    meilleure_erreur = erreur_totale
                    meilleurs_params = (alpha, beta, delta, gamma)
                    meilleurs_resultats = (time, lapin, renard)
                
                print(f"Test α={alpha}, β={beta}, δ={delta}, γ={gamma}: erreur = {erreur_totale}")

# Afficher les meilleurs paramètres trouvés
print("\nMeilleurs paramètres trouvés:")
print(f"α = {meilleurs_params[0]}")
print(f"β = {meilleurs_params[1]}")
print(f"δ = {meilleurs_params[2]}")
print(f"γ = {meilleurs_params[3]}")
print(f"Erreur = {meilleure_erreur}")

# Tracer les résultats
plt.figure(figsize=(15, 6))
# Données réelles
plt.plot(csv.index, csv['proie'], 'b.', label='Lapins (données réelles)')
plt.plot(csv.index, csv['predateur'], 'r.', label='Renards (données réelles)')
# Modèle optimisé
time, lapin, renard = meilleurs_resultats
plt.plot(time[:len(csv)], lapin[:len(csv)], 'b-', label='Lapins (modèle)')
plt.plot(time[:len(csv)], renard[:len(csv)], 'r-', label='Renards (modèle)')

plt.xlabel('Temps (Mois)')
plt.ylabel('Population')
plt.legend()
plt.title('Comparaison modèle vs données réelles')
plt.show()