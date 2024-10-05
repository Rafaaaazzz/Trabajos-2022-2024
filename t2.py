import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Cargar el archivo Excel
file_path = 'DATOSCALLAO2024.1.xlsx'  # Asegúrate de que esta ruta sea accesible en tu entorno
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error('El archivo no se encuentra en la ruta especificada.')
    st.stop()

# Convertir las fechas del formato YYYYMMDD a datetime
date_columns = ['FECHA_CORTE', 'FECHA_REGISTRO', 'FECHA_HECHO', 'FECHA_NACIMIENTO']
for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], format='%Y%m%d', errors='coerce')

# Configurar la página para usar un layout amplio
st.set_page_config(layout="wide")

# Sidebar para filtros
st.sidebar.header('Filtros de Búsqueda')
tipo_denuncia = st.sidebar.selectbox('Tipo de Denuncia', [''] + df['TIPO_DE_DENUNCIA'].dropna().unique().tolist())
distrito = st.sidebar.selectbox('Distrito', [''] + df['DISTRITO'].dropna().unique().tolist())
estado_denuncia = st.sidebar.selectbox('Estado de la Denuncia', [''] + df['SITUACION_DENUNCIA'].dropna().unique().tolist())

# Filtros adicionales para gráficos
st.sidebar.header('Opciones de Visualización')
graficos = st.sidebar.multiselect('Selecciona los gráficos que quieres mostrar:', [
    'Distribución de Denuncias por Tipo',
    'Evolución de Denuncias a lo Largo del Tiempo',
    'Denuncias por Distrito',
    'Denuncias por Estado de Denuncia',
    'Distribución de Edades de las Personas',
    'Denuncias por Sexo',
    'Denuncias por Estado Civil',
    'Denuncias por Grado de Instrucción',
    'Denuncias por Ocupación',
    'Distribución de Nacionalidades',
    'Denuncias por Mes',
    'Box Plot de Edades',
    'Scatter Plot de Longitud vs Latitud',
    'Heatmap de Correlaciones',
    'Pie Chart de Denuncias por Categoría',
    'Violin Plot de Edades por Tipo de Denuncia'
])

# Filtros adicionales para gráficos de pastel
st.sidebar.header('Opciones de Gráfico de Pastel')
categorias_pie = st.sidebar.selectbox('Categoría para Gráfico de Pastel', [''] + [
    'TIPO_DE_DENUNCIA', 'DISTRITO', 'SITUACION_DENUNCIA', 'SEXO', 'ESTADO_CIVIL', 'GRADO_INSTRUCCION',
    'OCUPACION', 'PAIS_NATAL', 'MES', 'DEPARTAMENTO', 'PROVINCIA'
])

# Filtrar el dataframe basado en las entradas
filtro = pd.Series([True] * len(df))
if tipo_denuncia:
    filtro &= (df['TIPO_DE_DENUNCIA'] == tipo_denuncia)
if distrito:
    filtro &= (df['DISTRITO'] == distrito)
if estado_denuncia:
    filtro &= (df['SITUACION_DENUNCIA'] == estado_denuncia)

resultados = df[filtro]

# Mostrar los resultados filtrados
st.subheader('Resultados de la Búsqueda')
columns_to_show = [
    'FECHA_CORTE', 'FECHA_REGISTRO', 'ID_DOC_DENUNCIA', 'UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
    'TIPO_DE_DENUNCIA', 'SITUACION_DENUNCIA', 'TIPO', 'SUBTIPO', 'MODALIDAD', 'FECHA_HECHO', 'HORA_HECHO',
    'UBICACION', 'DESCRIPCION', 'FECHA_NACIMIENTO', 'EDAD_PERSONA', 'SEXO', 'ESTADO_CIVIL',
    'GRADO_INSTRUCCION', 'OCUPACION', 'PAIS_NATAL', 'MES', 'LONGITUD', 'LATITUD'
]
st.dataframe(resultados[columns_to_show])

# Función para generar gráficos
def generar_graficos():
    if 'Distribución de Denuncias por Tipo' in graficos and not resultados.empty:
        st.subheader('Distribución de Denuncias por Tipo')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='TIPO_DE_DENUNCIA', order=resultados['TIPO_DE_DENUNCIA'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Evolución de Denuncias a lo Largo del Tiempo' in graficos and not resultados.empty:
        st.subheader('Evolución de Denuncias a lo Largo del Tiempo')
        fig, ax = plt.subplots()
        resultados.groupby(resultados['FECHA_HECHO'].dt.to_period("M")).size().plot(kind='line', ax=ax)
        ax.set_title('Número de Denuncias por Mes')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Número de Denuncias')
        st.pyplot(fig)
    
    if 'Denuncias por Distrito' in graficos and not resultados.empty:
        st.subheader('Denuncias por Distrito')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='DISTRITO', order=resultados['DISTRITO'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Denuncias por Estado de Denuncia' in graficos and not resultados.empty:
        st.subheader('Denuncias por Estado de Denuncia')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='SITUACION_DENUNCIA', order=resultados['SITUACION_DENUNCIA'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Distribución de Edades de las Personas' in graficos and not resultados.empty:
        st.subheader('Distribución de Edades de las Personas')
        fig, ax = plt.subplots()
        sns.histplot(resultados['EDAD_PERSONA'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_xlabel('Edad')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)
    
    if 'Denuncias por Sexo' in graficos and not resultados.empty:
        st.subheader('Denuncias por Sexo')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='SEXO', order=resultados['SEXO'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Denuncias por Estado Civil' in graficos and not resultados.empty:
        st.subheader('Denuncias por Estado Civil')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='ESTADO_CIVIL', order=resultados['ESTADO_CIVIL'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Denuncias por Grado de Instrucción' in graficos and not resultados.empty:
        st.subheader('Denuncias por Grado de Instrucción')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='GRADO_INSTRUCCION', order=resultados['GRADO_INSTRUCCION'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Denuncias por Ocupación' in graficos and not resultados.empty:
        st.subheader('Denuncias por Ocupación')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='OCUPACION', order=resultados['OCUPACION'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Distribución de Nacionalidades' in graficos and not resultados.empty:
        st.subheader('Distribución de Nacionalidades')
        fig, ax = plt.subplots()
        sns.countplot(data=resultados, x='PAIS_NATAL', order=resultados['PAIS_NATAL'].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    if 'Denuncias por Mes' in graficos and not resultados.empty:
        st.subheader('Denuncias por Mes')
        fig, ax = plt.subplots()
        resultados.groupby(resultados['MES']).size().plot(kind='bar', ax=ax)
        ax.set_title('Número de Denuncias por Mes')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Número de Denuncias')
        st.pyplot(fig)
    
    if 'Box Plot de Edades' in graficos and not resultados.empty:
        st.subheader('Box Plot de Edades')
        fig, ax = plt.subplots()
        sns.boxplot(data=resultados, y='EDAD_PERSONA', ax=ax)
        ax.set_ylabel('Edad')
        st.pyplot(fig)
    
    if 'Scatter Plot de Longitud vs Latitud' in graficos and not resultados.empty:
        st.subheader('Scatter Plot de Longitud vs Latitud')
        fig, ax = plt.subplots()
        sns.scatterplot(data=resultados, x='LONGITUD', y='LATITUD', ax=ax)
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        st.pyplot(fig)
    
    if 'Heatmap de Correlaciones' in graficos and not resultados.empty:
        st.subheader('Heatmap de Correlaciones')
        numeric_cols = resultados.select_dtypes(include='number').columns
        corr = resultados[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    
    if 'Pie Chart de Denuncias por Categoría' in graficos and not resultados.empty and categorias_pie:
        st.subheader(f'Pie Chart de Denuncias por {categorias_pie.replace("_", " ").title()}')
        fig, ax = plt.subplots()
        resultados[categorias_pie].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    
    if 'Violin Plot de Edades por Tipo de Denuncia' in graficos and not resultados.empty:
        st.subheader('Violin Plot de Edades por Tipo de Denuncia')
        fig, ax = plt.subplots()
        sns.violinplot(data=resultados, x='TIPO_DE_DENUNCIA', y='EDAD_PERSONA', ax=ax)
        ax.set_xlabel('Tipo de Denuncia')
        ax.set_ylabel('Edad')
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Generar los gráficos seleccionados
generar_graficos()
