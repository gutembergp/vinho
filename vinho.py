import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Títulos
st.write('# Grupo 69')
st.write('# Exportação Brasil')

st.set_option('deprecation.showPyplotGlobalUse', False)

# Subindo e tratandos os dados
exp_vinho = pd.read_csv("ExpVinho.csv", encoding='utf-8',
            sep=";")

exp_espumante = pd.read_csv("ExpEspumantes.csv", encoding='utf-8',
            sep=";")

# Creating a function which will remove extra leading
# and tailing whitespace from the data.
# pass dataframe as a parameter here
def whitespace_remover(dataframe):

    # iterating over the columns
    for i in dataframe.columns:

        # checking datatype of each columns
        if dataframe[i].dtype == 'object':

            # applying strip function on column
            dataframe[i] = dataframe[i].map(str.strip)

        else:

            # if condn. is False then it will do nothing.
            pass

# Creating a function which will remove '/n'
# pass dataframe as a parameter here
def n_remover(dataframe):

    # iterating over the columns
    for i in dataframe.columns:

        # checking datatype of each columns
        if dataframe[i].dtype == 'object':

            # applying xx function on column
            dataframe[i] = dataframe[i].str.replace("\n", "")

        else:

            # if condn. is False then it will do nothing.
            pass

# Creating a function which will remove '.' dot
# pass dataframe as a parameter here
def dot_remover(dataframe):

    # iterating over the columns
    for i in dataframe.columns:

        # checking datatype of each columns
        if dataframe[i].dtype == 'object':

            # applying strip function on column
            dataframe[i] = dataframe[i].str.replace('.', '')

        else:

            # if condn. is False then it will do nothing.
            pass


# Formartar a coluna Quantidade de 2008 a 2022

anos = []
for i in range(1, 16):
  ano = 2007 + i
  anos.append(str(ano))

# Formatar a Coluna de Valor 2008.1 a 2022.1

anos_val = []
for i in range(1, 16):
  ano = 2007 + i
  anos_val.append(str(ano)+'.1')

#Cabecalho Quantidade
cabecalho = anos
cabecalho.insert(0,'País')

#Cabecalho Valor
cabecalho_val = anos_val
cabecalho_val.insert(0,'País')

# Tratamento do data frame Vinho
whitespace_remover(exp_vinho)
n_remover(exp_vinho)

whitespace_remover(exp_vinho)
n_remover(exp_vinho)

exp_vinho_qtd = exp_vinho[cabecalho]
exp_vinho_qtd = exp_vinho_qtd.set_axis(cabecalho, axis=1)
exp_vinho_val = exp_vinho[cabecalho_val]
exp_vinho_val = exp_vinho_val.set_axis(cabecalho, axis=1)

# Trasforma colunas de exp_vinho_qtd para float
exp_vinho[anos] = exp_vinho[anos].apply(pd.to_numeric, errors='coerce')
exp_vinho[anos] = exp_vinho[anos].astype(float)

exp_vinho_total_ano = exp_vinho_qtd.sum()


# Tratamento do dataframe Espumante
whitespace_remover(exp_espumante)
n_remover(exp_espumante)

exp_espumante_qtd = exp_espumante[cabecalho]
exp_espumante_qtd = exp_espumante_qtd.set_axis(cabecalho, axis=1)
exp_espumante_val = exp_espumante[cabecalho_val]
exp_espumante_val = exp_espumante_val.set_axis(cabecalho_val, axis=1)

exp_espumante_qtd.set_index("País", inplace = True)
exp_espumante_total_ano = exp_espumante_qtd.sum()

exp_vinho_qtd.set_index("País", inplace = True)
exp_vinho_qtd_total_ano = exp_vinho_qtd.sum()

#Produção 
producao = pd.read_csv("Producao.csv", encoding='utf-8', sep=";")

whitespace_remover(producao)
dot_remover(producao)

# Formartar a coluna anos 2007 a 2021
anos = []
for i in range(1, 16):
  ano = 2006 + i
  anos.append(str(ano))

# Transfroma as colunas Ano para numerico float
producao[anos] = producao[anos].apply(pd.to_numeric, errors='coerce')
producao[anos] = producao[anos].astype(float)

# Substitui valores NaN por 0.00
producao.fillna(0,inplace=True)


# Elimina Coluna Index e 2 finais e anos <> 2008-2022
producao = producao.drop(producao.columns[[0, -1, -2 ]],axis = 1)
cab = producao.columns[1:(54-15)].tolist()
producao = producao.drop(cab,axis = 1)

prod = producao.set_index("produto")

# Consumo 
consumo = pd.read_csv("wine-consumption-per-person.csv", encoding='utf-8',
            sep=",")

# Wine consumption per person, 1960 to 2019
#Average per capita consumption of wine, as measured in liters of pure alcohol per year. 1 liter of wine contains around
# 0.12 liters of pure alcohol.

consumo.rename(columns={"Entity": "País", consumo.columns[-1]: "alchool"}, inplace=True)
consumo_2019 = pd.DataFrame(consumo.query(" Year == 2019"))
consumo_2019['vinho'] = (consumo_2019['alchool'] / 0.12)
consumo_2019.drop('Year', inplace=True, axis=1)

populacao = pd.read_csv("world_population.csv", encoding='utf-8',
            sep=",")
populacao.drop(populacao.columns[[0,3,4,6]], inplace=True, axis=1)
populacao.drop(populacao.columns[3:], inplace=True, axis=1)

populacao.rename(columns={"CCA3": "Code", "País": "alchool", "2022 Population" : "Population"}, inplace=True)

# Juntar Populacao e Consumo 2019

consumo_vinho = pd.merge(populacao, consumo_2019, left_on='Code', right_on='Code')
consumo_vinho['consumo'] = consumo_vinho['Population'] * consumo_vinho['alchool']
consumo_vinho = consumo_vinho.sort_values( by = 'consumo', ascending = False)
consumo_vinho.reset_index(drop=True)
consumo_vinho_15 = consumo_vinho.iloc[:15]

# Processamento Vinho Fino

proc_viniferas = pd.read_csv("ProcessaViniferas.csv", encoding='utf-8', sep="\t")
proc_viniferas = proc_viniferas.query("cultivar == 'TINTAS' or cultivar == 'BRANCAS E ROSADAS'")
proc_viniferas = proc_viniferas.drop(proc_viniferas.columns[[0, 1]],axis = 1)
proc_viniferas.rename(columns={'cultivar': 'FINO'}, inplace = True)
proc_viniferas = proc_viniferas.set_index("FINO")

# Transformar as celulas Quantidade de Processamento para Float
anos = proc_viniferas.columns[2:53].tolist()
proc_viniferas[anos] = proc_viniferas[anos].apply(pd.to_numeric, errors='coerce')
proc_viniferas[anos] = proc_viniferas[anos].astype(float)

proc_viniferas_total = proc_viniferas.T
proc_viniferas_total['Fino Total'] = proc_viniferas_total['TINTAS'] + proc_viniferas_total['BRANCAS E ROSADAS']
proc_viniferas_total.rename(columns={'TINTAS': 'Fino Tintas'}, inplace = True)
proc_viniferas_total.rename(columns={'BRANCAS E ROSADAS': 'Fino Brancas'}, inplace = True)

# Processamento Vinho de Mesa

proc_americanas = pd.read_csv("ProcessaAmericanas.csv", encoding='utf-8',
            sep=";")
proc_americanas = proc_americanas.query("cultivar == 'TINTAS' or cultivar == 'BRANCAS E ROSADAS'")
proc_americanas = proc_americanas.drop(proc_americanas.columns[[0, 1]],axis = 1)
proc_americanas.rename(columns={'cultivar': 'MESA'}, inplace = True)
proc_americanas = proc_americanas.set_index("MESA")

# Transformar as celulas Quantidade de Processamento para Float
anos = proc_americanas.columns[2:53].tolist()

proc_americanas[anos] = proc_americanas[anos].apply(pd.to_numeric, errors='coerce')
proc_americanas[anos] = proc_americanas[anos].astype(float)

proc_americana_total = proc_americanas.T
proc_americana_total['Mesa Total'] = proc_americana_total['TINTAS'] + proc_americana_total['BRANCAS E ROSADAS']

proc_americana_total.rename(columns={'TINTAS': 'Mesa Tintas'}, inplace = True)
proc_americana_total.rename(columns={'BRANCAS E ROSADAS': 'Mesa Brancas'}, inplace = True)

proc_viniferas_total = pd.DataFrame(proc_viniferas_total)

# Processamento Total (Fino e Mesa) 

proc_total = pd.concat([proc_americana_total, proc_viniferas_total], axis=1)
proc_total = proc_total[["Mesa Total" ,"Fino Total"] ]


# Criando o layout da aplicação
tab0, tab1, tab2, tab3  = st.tabs(["Consumo Mundial", "Exportação", "Produção e Processamento", "Conclusão"])

with tab0:
    st.write('### 15 Maiores Paises consumidores de vinhos')

    x = consumo_vinho_15['País']
    y = np.float64 (consumo_vinho_15['consumo'])
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    eixo = plt.bar(x, y, color ='blue', width = 0.4)
    from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
    plt.xlabel("Paises")
    plt.xticks(rotation=90)
    plt.ylabel("Consumo Litros")
    plt.title("15 Maiores Paises consumidores de vinhos")
    plt.show()
    st.pyplot(fig)

with tab1:

    df_vinho = pd.DataFrame (exp_vinho_qtd_total_ano, columns =['vinho'])
    df_espumante = pd.DataFrame (exp_espumante_total_ano, columns =['espumante'])
    df_total = df_vinho.join(df_espumante)

    st.write('### Exportação Brasil')
    st.write('##### 15 Anos (2008-2022)')
    st.bar_chart(df_total)
 
    st.write('### Exportação de Espumante')
    st.bar_chart(exp_espumante_total_ano)
   
    st.write('### Exportação Espumante por País')
    st.write('### Acumulado (2008-2022)')
    # Tabela de Quantidade Espumante Exportada pelo Brasil
    exp_espumante_qtd.reset_index(inplace=True)
    exp_espumante_qtd = exp_espumante_qtd.melt(id_vars='País')
    # Tabela de Valor Espumante Exportado pelo Brasil
    exp_espumante_val.reset_index(inplace=True)
    exp_espumante_val = exp_espumante_val.melt(id_vars='País')
    exp_espumante_qtd.rename(columns={"variable": "anos"}, inplace=True)
    exp_espumante_qtd.rename(columns={"value": "qtd"}, inplace=True)
    exp_espumante_val.rename(columns={"variable": "anos"}, inplace=True)
    exp_espumante_val.rename(columns={"value": "val"}, inplace=True)
    exp_brasil_espumante = exp_espumante_qtd
    exp_brasil_espumante['val'] =  exp_espumante_val['val']
    exp_brasil_espumante.drop(exp_brasil_espumante[exp_brasil_espumante['qtd'] == 0].index, inplace = True)
    exp_espumante_pais = exp_brasil_espumante.groupby('País').agg({'qtd': 'sum','val': 'sum'}).sort_values('qtd', ascending=False)
    exp_espumante_pais = exp_espumante_pais[:10]

    from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
    fig, ax = plt.subplots(figsize=(10,5))
    tam = len(exp_espumante_pais)
    x = np.arange(tam)
    width = 0.4
    plt.bar(x-0.2, exp_espumante_pais['qtd'],
            width, color='tab:red', label='Quantidade (Litros)')
    plt.bar(x+0.2, exp_espumante_pais['val'],
            width, color='gold', label='Valor US$')
    plt.title('TOP10 Importadores de Espumante', fontsize=10)
    labels = exp_espumante_pais.index
    plt.xticks(x, labels, rotation ='vertical') 
    plt.yticks(fontsize=10)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    sns.despine(bottom=True)
    ax.grid(False)
    ax.tick_params(bottom=False, left=True)
    plt.legend(frameon=False, fontsize=15)

    st.pyplot(fig)

    st.write('### Exportação de Vinho')
    st.bar_chart(exp_vinho_total_ano)

    st.write('### Exportação Vinho por País')
    st.write('### Acumulado (2008-2022)')
    # Tabela de Quantidade vinho Exportada pelo Brasil
    exp_vinho_qtd.reset_index(inplace=True)
    exp_vinho_qtd = exp_vinho_qtd.melt(id_vars='País')
    # Tabela de Valor vinho Exportado pelo Brasil
    exp_vinho_val.reset_index(inplace=True)
    exp_vinho_val = exp_vinho_val.melt(id_vars='País')
    exp_vinho_qtd.rename(columns={"variable": "anos"}, inplace=True)
    exp_vinho_qtd.rename(columns={"value": "qtd"}, inplace=True)
    exp_vinho_val.rename(columns={"variable": "anos"}, inplace=True)
    exp_vinho_val.rename(columns={"value": "val"}, inplace=True)
    exp_brasil_vinho = exp_vinho_qtd
    exp_brasil_vinho['val'] =  exp_vinho_val['val']
    exp_brasil_vinho.drop(exp_brasil_vinho[exp_brasil_vinho['qtd'] == 0].index, inplace = True)
    exp_vinho_pais = exp_brasil_vinho.groupby('País').agg({'qtd': 'sum','val': 'sum'}).sort_values('qtd', ascending=False)
    exp_vinho_pais = exp_vinho_pais[:10]

    from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
    fig, ax = plt.subplots(figsize=(10,5))
    tam = len(exp_vinho_pais)
    x = np.arange(tam)
    width = 0.4
    plt.bar(x-0.2, exp_vinho_pais['qtd'],
            width, color='tab:red', label='Quantidade (Litros)')
    plt.bar(x+0.2, exp_vinho_pais['val'],
            width, color='gold', label='Valor US$')
    plt.title('TOP10 Importadores de Vinho', fontsize=10)
    labels = exp_vinho_pais.index
    plt.xticks(x, labels, rotation ='vertical') 
    plt.yticks(fontsize=10)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    sns.despine(bottom=True)
    ax.grid(False)
    ax.tick_params(bottom=False, left=True)
    plt.legend(frameon=False, fontsize=15)

    st.pyplot(fig)

with tab2:

    st.write('### Processamento de Vinhos Finos e Mesa')

    fig = plt.figure(figsize=(10,5))
    eixo = fig.add_axes([0,0,1,1])
    eixo.plot(proc_total)
    eixo.axhline(y=np.nanmean(proc_total['Mesa Total']),color = 'b')
    eixo.axhline(y=np.nanmean(proc_total['Fino Total']), color = 'g')
    eixo.set_title('Processamento Vinho \n Rio Grande do Sul (1970 a 2021) ', fontsize=25)
    eixo.set_ylabel('Litros', fontsize=20)
    eixo.set_xlabel('Anos', fontsize=20)
    eixo.legend(loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=15)
    eixo.yaxis.set_major_formatter(FormatStrFormatter('%.f'))
    plt.xticks(rotation ='vertical', fontsize=10) 
    plt.legend(loc='upper left')
    st.pyplot(fig)
  
with tab3:
    st.write('### A Exportação de vinhos do Brasil que gera um maior valor comercial em relação ao volume produzido é a venda de espumantes finos que utilizam uvas brancas e rosadas na sua produção.')
    st.write('### O vinho Brasileiro ainda precisa se estabelecer em mercados internacionais e criar referências nos maiores mercados consumidores de vinho.') 
    st.write('### Com estratégia a Vinícola deveria focar seus esforços e investimentos na produção, melhoria e exportação de espumantes finos para o mercado americano (EUA) nos próximos anos.')
