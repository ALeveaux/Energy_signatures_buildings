import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier Excel
chemin_fichier_excel = 'satec_b06_15.xlsx'
df = pd.read_excel(chemin_fichier_excel)

# Convertir la colonne Date en format de date
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')

# Calculer la différence entre chaque ligne à partir de la troisième ligne
df['Diff_kWhImport'] = df['kWhImport'].diff(periods=1)

# Mettre à la valeur précédente les valeurs de Diff_kWhImport supérieures à 2000/4
df['Diff_kWhImport'] = df['Diff_kWhImport'].where(df['Diff_kWhImport'] <= 2000/4, df['Diff_kWhImport'].shift(1))

# Multiplier la colonne 'kWhImport' par 4
df['Diff_kWhImport'] = df['Diff_kWhImport'] * 4




#METTRE EN COMMENTAIRE SI ON VEUT FAIRE LES AUTRES GRAPHES
# Tracer le graphique à partir de la troisième ligne
plt.figure(figsize=(10, 6))
plt.plot(df['Date'][2:], df['Diff_kWhImport'][2:])

# Formater l'axe des abscisses pour afficher uniquement les noms des mois
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%B'))





#POUR AFFICHER SEULEMENT LE MOIS DE JANVIER (JUIN C'EST ==6)
# Filtrer les données pour ne conserver que celles du mois de janvier
#df_janvier = df[df['Date'].dt.month == 1]

# Tracer le graphique
#plt.figure(figsize=(10, 6))
#plt.plot(df_janvier['Date'], df_janvier['Diff_kWhImport'])






#POUR AFFICHER UN SEUL JOUR
# Filtrer les données pour ne conserver que celles du 01/01/2022
#date_specifique = pd.to_datetime('01/01/2022', format='%d/%m/%Y')
#df_jour_specifique = df[df['Date'].dt.date == date_specifique.date()]

# Tracer le graphique
#plt.figure(figsize=(10, 6))
#plt.plot(df_jour_specifique['Date'], df_jour_specifique['Diff_kWhImport'])



# Ajouter des étiquettes et un titre
plt.xlabel('Time [months]')
plt.ylabel('Power consumption [kW]')
plt.title('Electrical power consumption of B06 in 2022')

# Afficher le graphique
plt.show()
