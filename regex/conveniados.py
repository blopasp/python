import fitz
import re
from fitz.utils import write_text
import pandas as pd

CAMINHO_PDF = "arquivos_entrada/Gmail - INDICAÇÃO DE LOCAL REFERENCIADO.pdf"

def write_txt_list(list, filename):
    with open(filename, 'w') as f:
        for ele in list:
            f.write(ele+'\n')

def extract_from_pdf(path_filename):
    with fitz.open(path_filename) as pdf:
        text = ""
        for page in pdf:
            text += page.getText()
    return text

if __name__ == '__main__':
    # extraindo texto do arquivo pdf
    texto = extract_from_pdf(CAMINHO_PDF)

    # Salvando arquivo original para um arquivo txt
    with open('arquivos_saida/conveniado.txt', 'a') as conv:
        conv.write(texto)

    # procurando padrao nos bairros e nas quantidades de ocorrencias
    bairros = re.findall(r'[A-Z][A-Z ]+\B\W\d{1,2}\W', texto)

    # salvando bairros para um arquivo txt
    write_txt_list(bairros, 'arquivos_saida/bairros.txt')

    # Procurando padrao para encontrar conveniada, endereco, complemento e bairro
    conveniados = re.findall(r'([A-Z][A-Z ]+\s)([A-Z ]+[,]\s[N]\S\s\d*)(|\s\W\d*)(\s\W\s[A-Z][A-Z ]+)', texto)
    
    # criando dicionario com os padroes encontrados
    cad = {
        'Conveniado':[row[0] for row in conveniados], 
        'Endereco':[row[1] for row in conveniados], 
        'Complemento':[row[2] for row in conveniados], 
        'Cidade':[row[3] for row in conveniados]
    }
    # Criando um dataframe para 
    df = pd.DataFrame(cad)

    # Tratando dataframe
    df['Conveniado'] = df['Conveniado'].apply(lambda x: x.replace('\n', ''))
    df['Cidade'] = df['Cidade'].apply(lambda x: x.replace(' - ', ''))
    df['Complemento'] = df['Complemento'].apply(lambda x: x.replace('-', ''))
    df['Numero'] = df['Endereco'].apply(lambda x: x.split(',')[1])
    df['Numero'] = df['Numero'].apply(lambda x: x.split(' ')[2])
    df['Endereco'] = df['Endereco'].apply(lambda x: x.split(',')[0])

    # Reordenando as colunas e salvando o arquivo
    df = df[['Conveniado', 'Endereco', 'Numero', 'Complemento', 'Cidade']]
    df.to_csv('arquivos_saida/Conveniado.csv', index=False)