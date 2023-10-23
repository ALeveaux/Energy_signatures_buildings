# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:56:57 2023

@author: Antoine Verheyden
"""

import pandas as pd

# Charger le fichier Excel
fichier_entree = 'B06D_CHA_CC.xlsx'
df = pd.read_excel(fichier_entree)

# Convertir la colonne "DATETIME" en objets datetime
df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%d-%m-%Y %H:%M:%S')

# Calculer la moyenne de la colonne "P" par jour
moyennes_par_jour = df.groupby(df['DATETIME'].dt.date)['P'].mean().reset_index()
moyennes_par_jour.columns = ['Date', 'P_mean']

# Charger le fichier Excel de sortie
fichier_sortie = 'B06D_CHA_CC.xlsx'

# Copier les données existantes dans le fichier de sortie
writer = pd.ExcelWriter(fichier_sortie, engine='openpyxl')
writer.book = writer.book
writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

# Ajouter la moyenne quotidienne à la colonne "G" du fichier de sortie
moyennes_par_jour.to_excel(writer, index=False, header=False, sheet_name='Feuil1', startcol=6)

# Enregistrer les modifications dans le fichier Excel de sortie
writer.save()

print("Moyennes quotidiennes ajoutées avec succès dans le fichier", fichier_sortie)
