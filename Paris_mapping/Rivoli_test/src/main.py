import pandas as pd

df = pd.read_csv(r'Points.csv', sep=';') #Importation des points

dataCSV = pd.DataFrame(df, columns=['X', 'Y']) #On veut que X et Y


string = ""

for index, row in dataCSV.iterrows() : #Pour toutes les lignes
    string = string + '\n' + '= [' + str(row['X']) + "," + str(row['Y']) + '];'

print(string)
