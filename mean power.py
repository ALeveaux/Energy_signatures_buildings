import pandas as pd

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

