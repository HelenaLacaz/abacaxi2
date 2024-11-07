import streamlit as st
import pandas as pd
import datetime
from collections import Counter 
import re
from unidecode import unidecode
import altair as alt


st.set_page_config(
    layout='wide',
    page_icon='Avatar Matriculados'
)

@st.cache_data
def load_data(file, page):
    df = pd.read_excel(file, sheet_name=page)
    return df

df_inscritos_atuais = load_data('Planilha Geral - IMM2025_2.xlsx','Preencheu Pesquisa')

columns_inscritos_atuais = list(df_inscritos_atuais.columns.values.tolist())


columns_inscritos_atuais[1] = 'Nome'
columns_inscritos_atuais[2] = 'Probabilidade de Matricula' #
columns_inscritos_atuais[3] = 'Email' #
columns_inscritos_atuais[5] = 'Idade' #
columns_inscritos_atuais[6] = 'Genero' #
columns_inscritos_atuais[7] = 'Civil' #
columns_inscritos_atuais[8] = 'Filhos' #
columns_inscritos_atuais[9] = 'Escolaridade' #
columns_inscritos_atuais[10] = 'Renda' #
columns_inscritos_atuais[11] = 'Profissao' #
columns_inscritos_atuais[12] = 'Seguidor' #
columns_inscritos_atuais[22] = 'Imersao' #


df_inscritos_atuais.columns = columns_inscritos_atuais
df_final = df_inscritos_atuais

#df_inscritos_atuais[['Email','Idade','Genero','Civil','Filhos','Escolaridade','Renda','Profissao','Seguidor','Imersao']]


#--------- Logo & Titulo --------
st.image('logo1-1.png', width=220)
#st.image('logo2-2.png', width=150)
st.markdown('## Respostas da Pesquisa')

#---------------SIDEBAR--------------
st.sidebar.markdown('## Filtros')

#---------------FILTROS--------
#select all filter

#por imersao
imersoes = df_final['Imersao'].value_counts().index.tolist()
imersoes.insert(0, 'Todas') #add 'Select All' option to the top 
selected_imersao = st.sidebar.multiselect('Participará da Imersão?', imersoes, default='Sim')

# if select all is chosen, select all artists
if 'Todas' in selected_imersao :
	df_resp_filtered = df_final
else:
#st.write(artist_dropdown)
    df_resp_filtered = df_final[df_final['Imersao'].isin(selected_imersao)]

#por renda
rendas = df_resp_filtered['Renda'].value_counts().index.tolist()
rendas.insert(0, 'Todas') #add 'Select All' option to the top 
selected_renda = st.sidebar.multiselect('Faixa de Renda', rendas, default='Todas')

# if select all is chosen, select all artists
if 'Todas' in selected_renda :
	df_resp_filtered1 = df_resp_filtered
else:
#st.write(artist_dropdown)
    df_resp_filtered1 = df_resp_filtered[df_resp_filtered['Renda'].isin(selected_renda)]

#por profissao
profissoes = df_resp_filtered1['Profissao'].value_counts().index.tolist()
profissoes.insert(0, 'Todas') #add 'Select All' option to the top 
selected_profissoes = st.sidebar.multiselect('Profissão',profissoes, default='Todas')

if 'Todas' in selected_profissoes :
	df_resp_filtered2 = df_resp_filtered1
else:
    df_resp_filtered2 = df_resp_filtered1[df_resp_filtered1['Profissao'].isin(selected_profissoes)]

#por genero 
generos = df_resp_filtered2['Genero'].value_counts().index.tolist()
generos.insert(0, 'Todos') #add 'Select All' option to the top 
selected_genero = st.sidebar.multiselect('Gênero', generos, default='Todos')

# if select all is chosen, select all artists
if 'Todos' in selected_genero :
	df_resp_filtered3 = df_resp_filtered2
else:
#st.write(artist_dropdown)
    df_resp_filtered3 = df_resp_filtered2[df_resp_filtered2['Genero'].isin(selected_genero)]

#por seguidor
seguidores = df_resp_filtered3['Seguidor'].value_counts().index.tolist()
seguidores.insert(0, 'Todas') #add 'Select All' option to the top 
selected_seguidores = st.sidebar.multiselect('Seguidor',seguidores, default='Todas')

if 'Todas' in selected_seguidores :
	df_resp_filtered4 = df_resp_filtered3
else:
    df_resp_filtered4 = df_resp_filtered3[df_resp_filtered3['Seguidor'].isin(selected_seguidores)]




#----------Presentation-----
st.sidebar.markdown('Desenvolvido por **Lacaz Data Services**🎲')
st.sidebar.markdown('Dashboard desenvolvido para [Natlhalia Carvalho e Jaque França](https://nathaliamarketingmedico.com/formacao-med10k/?utm_source=Instagram&utm_medium=Bio&utm_id=SVMM+-+LC1)')


#-----------Gráficos-------------------
# Renda
contagem_renda = df_resp_filtered4['Renda'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_renda.columns = ['Faixa de Renda', 'Contagem']
contagem_renda = contagem_renda.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_renda = alt.Chart(contagem_renda).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Faixa de Renda:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Faixa de Renda'
).interactive()


# Idade
contagem_idade = df_resp_filtered4['Idade'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_idade.columns = ['Idade', 'Contagem']
contagem_idade = contagem_idade.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_idade = alt.Chart(contagem_idade).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Idade:N', sort='-y', title=None),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Faixa de Idade'
).interactive()


# Escolaridade
contagem_escol = df_resp_filtered4['Escolaridade'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_escol.columns = ['Escolaridade', 'Contagem']
contagem_escol = contagem_escol.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_escol = alt.Chart(contagem_escol).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Escolaridade:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Escolaridade',
    height=450 
).interactive()


#Profissao
contagem_profissao = df_resp_filtered4['Profissao'].value_counts()[:10].reset_index() #contagem da coluna de interesse y
contagem_profissao.columns = ['Profissao', 'Contagem']
contagem_profissao = contagem_profissao.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_profissao= alt.Chart(contagem_profissao).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Profissao', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Profissão Top10',
    height=450 
).interactive()


# Seguidor
contagem_seguidor = df_resp_filtered4['Seguidor'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_seguidor.columns = ['Seguidor', 'Contagem']
contagem_seguidor = contagem_seguidor.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_seguidor = alt.Chart(contagem_seguidor).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Seguidor:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Seguidor a quanto tempo?',
    height=450 
).interactive()


# Genero
contagem_genero = df_resp_filtered4['Genero'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_genero.columns = ['Genero', 'Contagem']
contagem_genero = contagem_genero.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_genero = alt.Chart(contagem_genero).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Contagem:Q'),
    color = alt.Color('Genero:N', legend=alt.Legend(orient='bottom', direction='horizontal'), title=None)
).properties(
    title='Gênero'
).interactive()


# Filhos
contagem_filhos = df_resp_filtered4['Filhos'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_filhos.columns = ['Filhos', 'Contagem']
contagem_filhos = contagem_filhos.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_filhos = alt.Chart(contagem_filhos).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Contagem:Q'),
    color = alt.Color('Filhos:N', legend=alt.Legend(orient='bottom', direction='horizontal'), title=None)
).properties(
    title='Tem Filhos?'
).interactive()

#Civil
contagem_civil = df_resp_filtered4['Civil'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_civil.columns = ['Civil', 'Contagem']
contagem_civil = contagem_civil.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_civil = alt.Chart(contagem_civil).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Civil:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Estado Civil',
    height=450 
).interactive()




col1, col2 = st.columns(2)
col1.altair_chart(chart_renda, use_container_width=True)
col2.altair_chart(chart_idade, use_container_width=True)

col1, col2 = st.columns(2)
col1.altair_chart(chart_profissao, use_container_width=True)
col2.altair_chart(chart_escol, use_container_width=True)


st.altair_chart(chart_seguidor, use_container_width=True)


col1, col2, col3 = st.columns(3)
col1.altair_chart(chart_genero, use_container_width=True)
col2.altair_chart(chart_civil, use_container_width=True)
col3.altair_chart(chart_filhos, use_container_width=True)



st.markdown('## Tabela Detalhada')
st.markdown('Coluna Probabilidade de Matrícula - Acurácia do Modelo : 62% ')

df_resp_filtered4['Probabilidade de Matricula'] = df_resp_filtered4['Probabilidade de Matricula']*100


st.dataframe(df_resp_filtered4,
             column_config={
                 "Probabilidade de Matricula": st.column_config.ProgressColumn(
                     "Probabilidade de Matricula", format="%d", min_value=0, max_value=100
                 )
             })

