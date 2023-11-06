import pandas as pd
from matplotlib.pyplot import pyplot as plt
import numpy as np
from scipy import stats


def building_conso(Area, Floors, Occupation, Ligthning):
############################################################################################################### 
#Calcule la puissance consommée par jour pour les batiments 
 
# Charge le fichier Excel, /!\ NE PAS OUBLIER DE METTRE LA SURFACE CHAUFFÉE DU BÂTIMENT EN QUESTION
    df = pd.read_excel("B05c_c.xlsx") 
 
# Étape 1 : Diviser la colonne P par le nombre de m^2 chauffés
    df["P/m^2"] = df["P"]/(Area*Floors)
 
# Étape 2 : Convertit la colonne "DATETIME" en type datetime 
    df["DATETIME"] = pd.to_datetime(df["DATETIME"]) 
 
# Étape 3 : Crée une colonne "Date" avec la date seule (sans l'heure) 
    df["Date"] = df["DATETIME"].dt.date 
 
# Étape 4 : Calcule la moyenne de "P/m^2" pour chaque jour 
    daily_consumption = df.groupby("Date")["P/m^2"].sum().reset_index() 
    daily_consumption.rename(columns={"P/m^2": ""}, inplace=True) 
 
# Insère la colonne "P per day" à la 7e position 
    df.insert(6, "P per day", daily_consumption[""]) 
 
# Sauvegarde le fichier Excel modifié 
    #df.to_excel("B06e_c_with_vector.xlsx", index=False) 
 
# Convertit la colonne "P per day" en un vecteur Python 
    P_mean_tot = df["P per day"].values 
    
    if Occupation == 1:
        file_path = "Building_Data_Template_Agora1+2.xlsx" 
        df = pd.read_excel(file_path, sheet_name="Occupation")
        Occ = df['B5c'].to_numpy()
    
    
        Occ_day = np.sum(Occ[4:29])*Occ[0]/24
        
    else: 
        
        Occ_day = 0
    
    if Ligthning == 1:
        
        file_path = "Building_Data_Template_Agora1+2.xlsx" 
        df = pd.read_excel(file_path, sheet_name="Lights")
        Lights = df['B5c'].to_numpy()
        
        Lights_day = np.sum(Lights[4:29])*Lights[0]/24
    
    else: 
        
        Lights_day = 0
    
    
    P_mean = np.zeros(365)
    for i in range (365):
        P_mean[i] = P_mean_tot[i]*60*1000/(3600*24)
        
        if P_mean[i]>0.1:
            
            P_mean[i] += Occ_day/Floors + Lights_day/Floors
    
    
    return P_mean

 
############################################################################################################### 
# Uniformisation des dates du fichier 
# Chargez le fichier Excel 
#file_path = "Building_Data_Template_Agora1+2.xlsx" 
#df = pd.read_excel(file_path, sheet_name="Meteo") 
 
# Convertissez toutes les dates en format "2021-01-01 00:00:00" 
#df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d %H:%M:%S') 
#df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S') 
 
# Sauvegardez les données mises à jour dans le fichier Excel 
#df.to_excel(file_path, sheet_name="Meteo", index=False) 
 
#print("Format de date uniformisé avec succès.") 
 
# Calcule de la température moyenne par jour 
# Convertissez la colonne "Date" en datetime si ce n'est pas déjà fait 
#df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S') 
 
# Calculez la moyenne de la température par jour 
#daily_temperature_avg = df.groupby(df['Date'].dt.date)['Temperature'].mean().reset_index() 
 
# Renommez la colonne "Temperature" en "Daily_Temperature_Avg" 
#daily_temperature_avg = daily_temperature_avg.rename(columns={'Temperature': 'Daily_Temperature_Avg'}) 
 
# Créez une nouvelle colonne "Mean temperature" pour stocker les moyennes quotidiennes 
#df['Mean temperature'] = daily_temperature_avg['Daily_Temperature_Avg'] 
 
# Sauvegardez les données mises à jour dans le fichier Excel 
#df.to_excel(file_path, sheet_name="Meteo", index=False) 
 
#print("Moyennes de température quotidiennes calculées et ajoutées avec succès.") 
 
#mean_temperature_vector = df['Mean temperature'].to_numpy() 
 
#print("Moyennes de température quotidiennes calculées et ajoutées avec succès.") 
#print('Le vecteur Python "mean_temperature_vector" a été créé.') 

def temp_vect():
    
    file_path = "Building_Data_Template_Agora1+2.xlsx" 
    df = pd.read_excel(file_path, sheet_name="Meteo")
    total_col_temp = df['O'].to_numpy()
    mean_temperature_vector = np.zeros(365)
    
    i=0
    
    for i in range(365):
        mean_temperature_vector[i] = total_col_temp[i]
    
    
    return mean_temperature_vector

#modification ALeveaux 
def Energy_signature_plot (mean_temperature_vector , P_mean):
 
    tolerance = 0.1 
    m = 0 
    k= 0 
    for i in range (len(mean_temperature_vector)): #évaluation de la taille des tableaux pour régression linéaire 
        
        if P_mean[i]< tolerance: 
            m+=1 
         
        else: 
            k+=1 
 
    first_part_P= np.zeros(k) 
    first_part_T= np.zeros(k)
    second_part_P= np.zeros(m) 
    second_part_T = np.zeros(m)
    k = 0 
    m = 0 
    i=0 
 
    for i in range (len(mean_temperature_vector)): 
 
        if P_mean[i]< tolerance: 
            second_part_P[m] = P_mean[i] 
            second_part_T[m] = mean_temperature_vector[i] 
            m += 1 
 
        else: 
            first_part_P[k] = P_mean[i] 
            first_part_T[k] = mean_temperature_vector[i] 
            k += 1 
    
    slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(first_part_T, first_part_P) 
 
    slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(second_part_T, second_part_P) 
 
    i = 0
    
    
    
    for i in range (len(first_part_T)):
        
        if  -intercept1/slope1 < first_part_T[i]:
            
            first_part_T[i] = -intercept1/slope1
        
    for i in range (len(second_part_T)):
        
        if second_part_T[i] < -intercept1/slope1:
            
            second_part_T[i] = -intercept1/slope1
            
            
    def interp1(x):
        return slope1*x + intercept1 
 
    def interp2(x):
        return (0*x)
 
    
    plt.scatter(mean_temperature_vector, P_mean) 
    plt.plot(first_part_T, interp1(first_part_T), color = "red") 
    plt.plot(second_part_T,interp2(second_part_T), color = "red")
    plt.ylabel('consumption (W/$m^2$)')
    plt.xlabel('Temperature (C)')
    plt.title('Energy signature B05c')
    

