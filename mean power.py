import pandas as pd

###############################################################################################################
#Calcule la moyenne des puissances pour les batiments
# Charger le fichier Excel
fichier_entree = 'Our_name.xlsx' #nom de notre fichier excel pour nos batiments
df = pd.read_excel(fichier_entree)

# Convertir la colonne "DATETIME" en objets datetime
df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%d-%m-%Y %H:%M:%S')

# Calculer la moyenne de la colonne "P" par jour
moyennes_par_jour = df.groupby(df['DATETIME'].dt.date)['P'].mean().reset_index()
moyennes_par_jour.columns = ['Date', 'P_mean']

# Charger le fichier Excel de sortie
fichier_sortie = 'Our_name.xlsx'

# Copier les données existantes dans le fichier de sortie
writer = pd.ExcelWriter(fichier_sortie, engine='openpyxl')
writer.book = writer.book
writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

# Ajouter la moyenne quotidienne à la colonne "G" du fichier de sortie
moyennes_par_jour.to_excel(writer, index=False, header=False, sheet_name='Feuil1', startcol=6)

# Enregistrer les modifications dans le fichier Excel de sortie
writer.save()

print("Moyennes quotidiennes ajoutées avec succès dans le fichier", fichier_sortie)




###############################################################################################################
#Uniformisation des dates du fichier"
# Chargez le fichier Excel
file_path = "Building_Data_Template_Agora1+2.xlsx"
df = pd.read_excel(file_path, sheet_name="Meteo")

# Convertissez toutes les dates en format "2021-01-01 00:00:00"
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Sauvegardez les données mises à jour dans le fichier Excel
df.to_excel(file_path, sheet_name="Meteo", index=False)

print("Format de date uniformisé avec succès.")





###############################################################################################################
#Calcule de la température moyenne par jour
# Calculez la moyenne de la température par jour
daily_temperature_avg = df.groupby(df['Date'].dt.date)['Temperature'].mean().reset_index()

# Renommez la colonne "Temperature" en "Daily_Temperature_Avg"
daily_temperature_avg = daily_temperature_avg.rename(columns={'Temperature': 'Daily_Temperature_Avg'})

# Créez une nouvelle colonne "O" pour stocker les moyennes quotidiennes
df['Mean temperature'] = daily_temperature_avg['Daily_Temperature_Avg']

# Sauvegardez les données mises à jour dans le fichier Excel
df.to_excel(file_path, sheet_name="Meteo", index=False)

print("Moyennes de température quotidiennes calculées et ajoutées avec succès.")

