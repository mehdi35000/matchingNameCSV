import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Charger les fichiers CSV
df1 = pd.read_csv('namesFromAD.csv')
df2 = pd.read_csv('namesFromDWH.csv')

# Fonction pour trouver la meilleure correspondance pour un nom donné dans le deuxième DataFrame
def find_best_match(name, names_list):
    return process.extractOne(name, names_list, scorer=fuzz.token_sort_ratio)

# Nettoyer les espaces superflus dans les noms du premier fichier et convertir en minuscules
df1.columns = df1.columns.str.strip().str.lower()

# Nettoyer les espaces superflus dans les noms du deuxième fichier et convertir en minuscules
df2.columns = df2.columns.str.strip().str.lower()

# Créer un nouveau DataFrame pour le troisième fichier
df3 = pd.DataFrame(columns=['First name', 'Last name', 'Date of birth', 'Role'])

# Itérer sur les noms du premier fichier
for index, row in df1.iterrows():
    display_name = row['display names']
    role = row['role']

    # Trouver la meilleure correspondance dans le deuxième fichier
    result = find_best_match(display_name, df2['name'])
    best_match = result[0]
    score = result[1]

    # Si le score de correspondance est supérieur à un seuil donné
    if score > 50:  # Vous pouvez ajuster ce seuil selon vos besoins
        # Récupérer les informations nécessaires
        matched_row = df2[df2['name'] == best_match].iloc[0]

        # Utiliser le nom complet du df1 si la première lettre est une initiale
        if len(matched_row['name'].split()) == 1 and len(display_name.split()) > 1:
            first_name = ' '.join(display_name.split()[:-1])
            last_name = display_name.split()[-1]
        else:
            first_name = matched_row['name'].split()[0]
            last_name = ' '.join(matched_row['name'].split()[1:])

        df3 = df3._append({'First name': first_name,
                          'Last name': last_name,
                          'Date of birth': matched_row['date of birth'],
                          'Role': role}, ignore_index=True)

# Imprimer le contenu de df3
print("\nContenu de df3 :")
print(df3)

# Sauvegarder le résultat dans un nouveau fichier CSV
df3.to_csv('fusion.csv', index=False)
