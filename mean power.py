import pandas as pd
from matplotlib.pyplot import pyplot as plt
import numpy as np
from scipy import stats


###############################################################################################################
#Calcule la puissance consommée par jour pour les batiments

# Charge le fichier Excel
df = pd.read_excel("B06e_c.xlsx")

# Étape 1 : Multiplie la colonne "P" par 60
df["P*60"] = df["P"] * 60

# Étape 2 : Convertit la colonne "DATETIME" en type datetime
df["DATETIME"] = pd.to_datetime(df["DATETIME"])

# Étape 3 : Crée une colonne "Date" avec la date seule (sans l'heure)
df["Date"] = df["DATETIME"].dt.date

# Étape 4 : Calcule la somme de "P*60" pour chaque jour
daily_consumption = df.groupby("Date")["P*60"].sum().reset_index()
daily_consumption.rename(columns={"P*60": ""}, inplace=True)

# Insère la colonne "P per day" à la 7e position
df.insert(6, "P per day", daily_consumption[""])

# Sauvegarde le fichier Excel modifié
df.to_excel("B06e_c_with_vector.xlsx", index=False)

# Convertit la colonne "P per day" en un vecteur Python
P_mean = df["P per day"].values

print('Le fichier Excel est créé et disponible.')
print('Le vecteur Python "p_per_day_vector" a été créé.')


###############################################################################################################
# Uniformisation des dates du fichier
# Chargez le fichier Excel
file_path = "Building_Data_Template_Agora1+2.xlsx"
df = pd.read_excel(file_path, sheet_name="Meteo")

# Convertissez toutes les dates en format "2021-01-01 00:00:00"
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Sauvegardez les données mises à jour dans le fichier Excel
df.to_excel(file_path, sheet_name="Meteo", index=False)

print("Format de date uniformisé avec succès.")

# Calcule de la température moyenne par jour
# Convertissez la colonne "Date" en datetime si ce n'est pas déjà fait
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')

# Calculez la moyenne de la température par jour
daily_temperature_avg = df.groupby(df['Date'].dt.date)['Temperature'].mean().reset_index()

# Renommez la colonne "Temperature" en "Daily_Temperature_Avg"
daily_temperature_avg = daily_temperature_avg.rename(columns={'Temperature': 'Daily_Temperature_Avg'})

# Créez une nouvelle colonne "Mean temperature" pour stocker les moyennes quotidiennes
df['Mean temperature'] = daily_temperature_avg['Daily_Temperature_Avg']

# Sauvegardez les données mises à jour dans le fichier Excel
df.to_excel(file_path, sheet_name="Meteo", index=False)

print("Moyennes de température quotidiennes calculées et ajoutées avec succès.")

mean_temperature_vector = df['Mean temperature'].to_numpy()

print("Moyennes de température quotidiennes calculées et ajoutées avec succès.")
print('Le vecteur Python "mean_temperature_vector" a été créé.')

#modification ALeveaux
def Energy_signature_plot (Daily_Temperature_Avg , P_mean)

    tolerance = 0.1
    m = 0
    k= 0
    for i in range len(Daily_Temperature_Avg): #évaluation de la taille des tableaux pour régression linéaire

        if P_mean[i]< tolerance:
            m+=1
        
        else:
            k+=1

    first_part= np.zeros(k)
    second_part= np.zeros(m)
    k = 0
    m = 0
    i=0

    for i in range len(Daily_Temperature_Avg):

        if P_mean[i]< tolerance:
            second_part_P[m] = P_mean[i]
            second_part_T[m] = Daily_Temperature_Avg[i]
            m += 1

        else:
            first_part_P[k] = P_mean[i]
            first_part_T[k] = Daily_Temperature_Avg[i]
            k += 1
    
    slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(first_part_T, first_part_P)

    slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(second_part_T, second_part_P)

    def interp1(x)
        return slope1*x + intercept1

     def interp2(x)
        return slope2*x + intercept2

plt.scatter(Daily_Temperature_Avg, P_mean)
plt.plot()


