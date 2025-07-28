import pandas as pd
import os

# 📌 Remplace par le nom de ton fichier Excel
excel_file = "bridgeemployeerole.xlsx"

# Lecture des colonnes A-C pour les champs à sélectionner
df = pd.read_excel(excel_file, engine='openpyxl', header=0, usecols="A:C")
df.columns = ['alias', 'column', 'table']
df = df.dropna(subset=['column', 'table'])

# Lecture des colonnes G-H pour les jointures
df_joins = pd.read_excel(excel_file, engine='openpyxl', header=0, usecols="G:H")
df_joins.columns = ['join_from', 'join_to']
df_joins = df_joins.dropna(how='any')  # ignore les lignes incomplètes

# Construction de la clause SELECT
select_clauses = [
    f"{row['table']}.{row['column']} AS {row['alias']}"
    for _, row in df.iterrows()
]

def extract_table_name(full_reference):
    parts = full_reference.replace('[', '').replace(']', '').split('.')
    if len(parts) >= 2:
        return parts[-2]  # nom de la table uniquement
    return parts[0]


def extract_full_table_path(full_reference):
    parts = full_reference.strip().split('.')
    if len(parts) >= 2:
        return '.'.join(parts[:-1])  # tout sauf la colonne
    return parts[0]  # fallback


# 📌 Détection automatique de la bonne table principale
tables_in_select = df['table'].tolist()
join_targets = [
    extract_table_name(j)
    for j in df_joins['join_to'].dropna()
]
main_table_candidates = [t for t in tables_in_select if t not in join_targets]
main_table = main_table_candidates[0] if main_table_candidates else df['table'].iloc[0]

# Construction des JOINs
join_clauses = []
joined_tables = set()




for _, row in df_joins.iterrows():
    join_from = row['join_from']
    join_to = row['join_to']
    right_table_path = extract_full_table_path(join_to)
    join_statement = f"JOIN {right_table_path} ON {join_from} = {join_to}"

    if join_statement not in join_clauses:
        join_clauses.append(join_statement)
        joined_tables.add(right_table_path.split('.')[-1])

# Assemblage final
sql_query = f"""SELECT
    {',\n    '.join(select_clauses)}
FROM
    {main_table}
"""

if join_clauses:
    sql_query += '\n' + '\n'.join(join_clauses)

# Écriture dans le fichier query.txt
output_file = os.path.join(os.path.dirname(__file__), 'query.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(sql_query)

print(f"✅ Requête SQL générée et enregistrée dans : {output_file}")
