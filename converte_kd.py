import os
import re
import pandas as pd

# Caminhos dos arquivos e pastas
index_file = r'C:\Users\luiza\Downloads\figuras_novas\analises\INDEX_general_PN.2020'  # Arquivo de entrada
output_csv = r'C:\Users\luiza\Downloads\figuras_novas\analises\binding_data.csv'      # Arquivo CSV de saída
arquivos_final = r'C:\Users\luiza\Downloads\figuras_novas\analises\arquivos_finais'   # Pasta contendo os arquivos .pdb

# Expressão regular para capturar os dados de binding data no formato Kd=valor(unidade)
kd_pattern = re.compile(r'Kd=([\d\.]+)([a-zA-Z]+)')

# Função para converter os valores de Kd para micromolar (uM)
def convert_kd_to_um(value, unit):
    conversion_factors = {'pM': 1e-6, 'nM': 1e-3, 'uM': 1, 'mM': 1e3, 'fM': 1e-9}
    return float(value) * conversion_factors.get(unit, 1)  # Conversão padrão é uM

# Função para processar o arquivo INDEX_general_PN.txt
def process_index_file(index_file):
    pdb_data = {}  # Dicionário para armazenar os dados de PDB e Kd
    
    with open(index_file, 'r') as file:
        for line in file:
            columns = line.split()
            if len(columns) >= 4:
                pdb_id = columns[0]
                binding_data = line.split()[3]
                match = kd_pattern.search(binding_data)
                if match:
                    value, unit = match.groups()  # Extrai valor e unidade do Kd
                    kd_in_um = convert_kd_to_um(value, unit)  # Converte para uM
                    pdb_data[pdb_id] = kd_in_um  # Armazena no dicionário
    return pdb_data

# Função para comparar os PDBs na pasta arquivos_final
def filter_pdbs_with_binding_data(pdb_data, arquivos_final):
    final_pdbs = [f.split('.')[0] for f in os.listdir(arquivos_final) if f.endswith('.pdb')]
    filtered_data = {pdb: kd for pdb, kd in pdb_data.items() if pdb in final_pdbs}
    return filtered_data

# Processar o arquivo INDEX_general_PN.txt
pdb_data = process_index_file(index_file)

# Filtrar os PDBs presentes na pasta arquivos_final
filtered_pdb_data = filter_pdbs_with_binding_data(pdb_data, arquivos_final)

# Criar um DataFrame e arredondar os valores de Kd para 3 casas decimais
df = pd.DataFrame(list(filtered_pdb_data.items()), columns=['PDB ID', 'Kd (uM)'])
df['Kd (uM)'] = df['Kd (uM)'].round(3)  # Arredondar para 3 casas decimais

# Salvar o arquivo CSV
df.to_csv(output_csv, index=False)

print(f"CSV salvo com {len(df)} PDBs e seus valores de Kd em uM (arredondados para 3 casas decimais).")
