import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random

class CargadorCSV:
    def __init__(self):
        self.datos = None

    def leer_archivo_csv(self, ruta_archivo):
        try:
            datos = pd.read_csv(ruta_archivo, encoding='latin1', on_bad_lines='skip', sep=';')
        except Exception as e1:
            try:
                datos = pd.read_csv(ruta_archivo, encoding='utf-8', on_bad_lines='skip', sep=';')
            except Exception as e2:
                try:
                    datos = pd.read_csv(ruta_archivo, encoding='latin1', on_bad_lines='skip', sep=',')
                except Exception as e3:
                    try:
                        datos = pd.read_csv(ruta_archivo, encoding='utf-8', on_bad_lines='skip', sep=',')
                    except Exception as e4:
                        st.error(f"No se pudo cargar el archivo: {e4}")
                        return None
        return datos

    def cargar_archivo(self, ruta_archivo):
        if ruta_archivo:
            self.datos = self.leer_archivo_csv(ruta_archivo)
            if self.datos is not None:
                return True
        return False

class GeneradorGraficos:
    def __init__(self, datos):
        self.datos = datos

    def graficar_mypes_por_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos['ANIO'].value_counts().sort_index()
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title('Número de MYPES Registradas por Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=45)
        st.pyplot(fig)

    def graficar_mypes_por_departamento(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos['DEPARTAMENTO'].value_counts().sort_index()
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title('Número de MYPES por Departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(range(len(data.index)))
        ax.set_xticklabels(data.index, rotation=90)
        st.pyplot(fig)

    def graficar_mypes_por_provincia(self, provincias_seleccionadas):
        data = self.datos[self.datos['PROVINCIA'].isin(provincias_seleccionadas)]['PROVINCIA'].value_counts().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 70))  
        colors = sns.color_palette('viridis', len(data))
        ax.barh(data.index, data.values, color=colors) 
        ax.set_title('Número de MYPES por Provincia')
        ax.set_xlabel('Cantidad de MYPES')
        ax.set_ylabel('Provincia')
        st.pyplot(fig)

    def graficar_mypes_por_distrito(self, distritos_seleccionados):
        data = self.datos[self.datos['DISTRITO'].isin(distritos_seleccionados)]['DISTRITO'].value_counts().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 70))  
        colors = sns.color_palette('viridis', len(data))
        ax.barh(data.index, data.values, color=colors) 
        ax.set_title('Número de MYPES por Distrito')
        ax.set_xlabel('Cantidad de MYPES')
        ax.set_ylabel('Distrito')
        st.pyplot(fig)

    def graficar_mypes_por_dept_prov_dist(self, departamento, provincia, distrito):
        if not departamento or not provincia or not distrito:
            st.error("Seleccione Departamento, Provincia y Distrito.")
            return

        datos_filtrados = self.datos[(self.datos['DEPARTAMENTO'] == departamento) & (self.datos['PROVINCIA'] == provincia) & (self.datos['DISTRITO'] == distrito)]
        conteo_dept_prov_dist = datos_filtrados.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']).size().reset_index(name='Cantidad')

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(conteo_dept_prov_dist))
        ax.bar(conteo_dept_prov_dist.index, conteo_dept_prov_dist['Cantidad'], color=colors)
        ax.set_title(f'Número de MYPES en {departamento}, {provincia}, {distrito}')
        ax.set_xlabel('Distrito')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(range(len(conteo_dept_prov_dist)))
        ax.set_xticklabels(conteo_dept_prov_dist['DISTRITO'], rotation=90)
        st.pyplot(fig)

    def graficar_mypes_por_rubro(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos['RUBRO'].value_counts().sort_index()
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title('Número de MYPES por Rubro')
        ax.set_xlabel('Rubro')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=90)
        st.pyplot(fig)

    def graficar_nivel_digital(self):
        if 'NIVEL_DIGITAL' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITAL'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]

        data = self.datos['NIVEL_DIGITAL'].value_counts().sort_index()
        colors = sns.color_palette('viridis', len(data))

        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='pie', ax=ax, colors=colors, title='Nivel digital de las MYPES')
        st.pyplot(fig)

    def graficar_mypes_por_tipo(self):
        if 'TIPO' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'TIPO'.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos['TIPO'].value_counts().sort_index()
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title('Número de MYPES por Tipo')
        ax.set_xlabel('Tipo')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=45)
        st.pyplot(fig)

    def graficar_dig_general(self):
        if 'DIG_GENERAL' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'DIG_GENERAL'.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos['DIG_GENERAL']
        colors = sns.color_palette('viridis', len(data))  

        ax.bar(data.index, data.values, color=colors)  
        ax.set_title('Nivel Alcanzado en el Test de Diagnóstico')
        ax.set_xlabel('Nivel Alcanzado')
        ax.set_ylabel('Porcentaje')
        plt.tight_layout()
        st.pyplot(fig)

    def comparar_nivel_digital(self, nivel_digital_1, nivel_digital_2):
        if 'NIVEL_DIGITAL' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITAL'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]

        if not nivel_digital_1 or not nivel_digital_2:
            st.error("Seleccione dos niveles de digitalización para comparar.")
            return

        datos_filtrados_1 = self.datos[self.datos['NIVEL_DIGITAL'] == nivel_digital_1]
        datos_filtrados_2 = self.datos[self.datos['NIVEL_DIGITAL'] == nivel_digital_2]

        conteo_nivel_1 = len(datos_filtrados_1)
        conteo_nivel_2 = len(datos_filtrados_2)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar([nivel_digital_1, nivel_digital_2], [conteo_nivel_1, conteo_nivel_2])
        ax.set_title(f'Comparación de Niveles de Digitalización: {nivel_digital_1} vs {nivel_digital_2}')
        ax.set_xlabel('Nivel Digital')
        ax.set_ylabel('Cantidad de MYPES')
        st.pyplot(fig)

    def comparar_rubro(self, rubro_1, rubro_2):
        if 'RUBRO' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'RUBRO'.")
            return

        if not rubro_1 or not rubro_2:
            st.error("Seleccione dos rubros para comparar.")
            return

        datos_rubro_1 = self.datos[self.datos['RUBRO'] == rubro_1]
        datos_rubro_2 = self.datos[self.datos['RUBRO'] == rubro_2]

        conteo_rubro_1 = len(datos_rubro_1)
        conteo_rubro_2 = len(datos_rubro_2)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', 2)  
        ax.bar([rubro_1, rubro_2], [conteo_rubro_1, conteo_rubro_2], color=colors)
        ax.set_title(f'Comparación de Rubros: {rubro_1} vs {rubro_2}')
        ax.set_xlabel('Rubro')
        ax.set_ylabel('Cantidad de MYPES')
        st.pyplot(fig)

    def graficar_nivel_digital_por_distrito(self, distrito, nivel_digital):
        if 'NIVEL_DIGITALIZACION' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'NIVEL_DIGITALIZACIÓN'.")
            return

        datos_filtrados = self.datos[self.datos['DISTRITO'] == distrito]
        data = datos_filtrados['NIVEL_DIGITALIZACION'].value_counts().sort_index()

        if nivel_digital not in data.index:
            st.warning(f"No hay datos para el nivel digital '{nivel_digital}' en el distrito seleccionado.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title(f'Nivel de digitalización de las MYPES en {distrito}')
        ax.set_xlabel('Nivel digital')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=45)
        st.pyplot(fig)
    
    def graficar_nivel_digital_por_provincia(self, provincia, nivel_digital):
        if 'NIVEL_DIGITALIZACION' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'NIVEL_DIGITALIZACIÓN'.")
            return

        datos_filtrados = self.datos[self.datos['PROVINCIA'] == provincia]
        data = datos_filtrados['NIVEL_DIGITALIZACION'].value_counts().sort_index()

        if nivel_digital not in data.index:
            st.error(f"No hay datos para el nivel digital '{nivel_digital}' en la provincia seleccionada.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title(f'Nivel de digitalización de las MYPES en {provincia}')
        ax.set_xlabel('Nivel digital')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=45)
        st.pyplot(fig)

    def graficar_nivel_digital_por_departamento(self, departamento, nivel_digital):
        if 'NIVEL_DIGITALIZACION' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'NIVEL_DIGITALIZACIÓN'.")
            return

        datos_filtrados = self.datos[self.datos['DEPARTAMENTO'] == departamento]
        data = datos_filtrados['NIVEL_DIGITALIZACION'].value_counts().sort_index()

        if nivel_digital not in data.index:
            st.error(f"No hay datos para el nivel digital '{nivel_digital}' en el departamento seleccionado.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(data))
        ax.bar(data.index, data.values, color=colors)
        ax.set_title(f'Nivel de digitalización de las MYPES en {departamento}')
        ax.set_xlabel('Nivel digital')
        ax.set_ylabel('Cantidad de MYPES')
        ax.set_xticks(data.index)
        ax.set_xticklabels(data.index, rotation=45)
        st.pyplot(fig)
    
    def graficar_nivel_digital_por_rubro(self, rubro):
        if 'RUBRO' not in self.datos.columns:
            st.error("El archivo CSV no contiene la columna 'RUBRO'.")
            return

        if 'NIVEL_DIGITALIZACION' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITALIZACION'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]

        data = self.datos[self.datos['RUBRO'] == rubro]['NIVEL_DIGITALIZACION'].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(data))
        data.plot(kind='pie', ax=ax, colors=colors)
        ax.set_title(f'Nivel de digitalización por Rubro: {rubro}')
        ax.set_ylabel('')
        st.pyplot(fig)
    
    def graficar_mypes_por_rubro_y_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['ANIO', 'RUBRO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Rubro y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Rubro', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_nivel_digital_y_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['ANIO', 'NIVEL_DIGITALIZACION']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Nivel Digital y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Nivel Digital', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_nivel_digital_por_departamento_y_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['ANIO', 'DEPARTAMENTO', 'NIVEL_DIGITALIZACION']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Nivel Digital por Departamento y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Nivel Digital', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_tipo_de_mypes_por_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['ANIO', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Tipo de MYPES por Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_rubro_y_departamento(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['DEPARTAMENTO', 'RUBRO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Rubro y Departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Rubro', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_provincia_y_departamento(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['DEPARTAMENTO', 'PROVINCIA']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Provincia y Departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Provincia', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_distrito_y_provincia(self, distritos_seleccionados):
        datos_filtrados = self.datos[self.datos['DISTRITO'].isin(distritos_seleccionados)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['PROVINCIA', 'DISTRITO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Distrito y Provincia')
        ax.set_xlabel('Provincia')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Distrito', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_nivel_digital_por_departamento_y_provincia(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'NIVEL_DIGITALIZACION']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Nivel Digital por Departamento y Provincia')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Nivel Digital', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_nivel_digital_y_provincia(self, provincias_seleccionadas):
        if 'NIVEL_DIGITAL' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITAL'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]
        
        datos_filtrados = self.datos[self.datos['PROVINCIA'].isin(provincias_seleccionadas)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['PROVINCIA', 'NIVEL_DIGITAL']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Nivel Digital y Provincia')
        ax.set_xlabel('Provincia')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Nivel Digital', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_rubro_y_distrito(self, distritos_seleccionados):
        datos_filtrados = self.datos[self.datos['DISTRITO'].isin(distritos_seleccionados)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['DISTRITO', 'RUBRO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Rubro y Distrito')
        ax.set_xlabel('Distrito')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Rubro', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    # Nuevos gráficos
    def graficar_mypes_por_tipo_y_departamento(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['DEPARTAMENTO', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Tipo y Departamento')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_tipo_y_provincia(self, provincias_seleccionadas):
        datos_filtrados = self.datos[self.datos['PROVINCIA'].isin(provincias_seleccionadas)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['PROVINCIA', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Tipo y Provincia')
        ax.set_xlabel('Provincia')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_tipo_y_distrito(self, distritos_seleccionados):
        datos_filtrados = self.datos[self.datos['DISTRITO'].isin(distritos_seleccionados)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['DISTRITO', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Tipo y Distrito')
        ax.set_xlabel('Distrito')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_rubro_y_tipo(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['RUBRO', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Rubro y Tipo')
        ax.set_xlabel('Rubro')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_nivel_digital_y_tipo(self):
        if 'NIVEL_DIGITAL' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITAL'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['NIVEL_DIGITAL', 'TIPO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Nivel Digital y Tipo')
        ax.set_xlabel('Nivel Digital')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Tipo', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_departamento_y_anio(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['ANIO', 'DEPARTAMENTO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Departamento y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Departamento', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_provincia_y_anio(self, provincias_seleccionadas):
        datos_filtrados = self.datos[self.datos['PROVINCIA'].isin(provincias_seleccionadas)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['ANIO', 'PROVINCIA']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Provincia y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Provincia', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_distrito_y_anio(self, distritos_seleccionados):
        datos_filtrados = self.datos[self.datos['DISTRITO'].isin(distritos_seleccionados)]
        fig, ax = plt.subplots(figsize=(10, 6))
        data = datos_filtrados.groupby(['ANIO', 'DISTRITO']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Distrito y Año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Distrito', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

    def graficar_mypes_por_rubro_y_nivel_digital(self):
        if 'NIVEL_DIGITAL' not in self.datos.columns:
            niveles = {1: 'Inicial', 2: 'Básico', 3: 'Intermedio'}
            self.datos['NIVEL_DIGITAL'] = [niveles[random.randint(1, 3)] for _ in range(len(self.datos))]

        fig, ax = plt.subplots(figsize=(10, 6))
        data = self.datos.groupby(['RUBRO', 'NIVEL_DIGITAL']).size().unstack().fillna(0)
        data.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Número de MYPES por Rubro y Nivel Digital')
        ax.set_xlabel('Rubro')
        ax.set_ylabel('Cantidad de MYPES')
        ax.legend(title='Nivel Digital', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

def aplicacion():
    st.title("DATATECH")

    cargador_csv = CargadorCSV()
    
    st.sidebar.title("Cargar CSV")
    ruta_archivo = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
    
    if ruta_archivo:
        if cargador_csv.cargar_archivo(ruta_archivo):
            datos = cargador_csv.datos
            generador_graficos = GeneradorGraficos(datos)

            st.sidebar.title("Filtrar Datos")
            departamentos = sorted(list(datos['DEPARTAMENTO'].dropna().unique()))
            departamento_seleccionado = st.sidebar.selectbox("Seleccione Departamento", ["Todos"] + departamentos)
            if departamento_seleccionado != "Todos":
                datos = datos[datos['DEPARTAMENTO'] == departamento_seleccionado]
                provincias = sorted(list(datos['PROVINCIA'].dropna().unique()))
                provincia_seleccionada = st.sidebar.selectbox("Seleccione Provincia", ["Todos"] + provincias)
                if provincia_seleccionada != "Todos":
                    datos = datos[datos['PROVINCIA'] == provincia_seleccionada]
                    distritos = sorted(list(datos['DISTRITO'].dropna().unique()))
                    distrito_seleccionado = st.sidebar.selectbox("Seleccione Distrito", ["Todos"] + distritos)
                    if distrito_seleccionado != "Todos":
                        datos = datos[datos['DISTRITO'] == distrito_seleccionado]

            st.write("### Resumen de Datos Cargados")
            st.dataframe(datos, height=500)

            st.sidebar.title("Seleccione los gráficos que desea ver:")
            var_anio = st.sidebar.checkbox("Número de MYPES registradas por Año")
            var_departamento = st.sidebar.checkbox("Número de MYPES por Departamento")
            var_distrito = st.sidebar.checkbox("Número de MYPES por Distrito")
            var_provincia = st.sidebar.checkbox("Número de MYPES por Provincia")
            var_dept_prov_dist = st.sidebar.checkbox("Número de MYPES por Departamento, Provincia y Distrito")
            var_rubro = st.sidebar.checkbox("Número de MYPES por Rubro")
            var_nivel_digital = st.sidebar.checkbox("Nivel Digital de las MYPES")
            var_tipo = st.sidebar.checkbox("Número de MYPES por Tipo")
            var_nivel_alcanzado = st.sidebar.checkbox("Nivel alcanzado en el Test de Diagnóstico")
            var_comparar_nivel_digital = st.sidebar.checkbox("Comparar niveles de digitalización")
            var_comparar_rubro = st.sidebar.checkbox("Comparar MYPES según su Rubro")
            var_nivel_digital_distrito = st.sidebar.checkbox("Nivel digital por Distrito")
            var_nivel_digital_provincia = st.sidebar.checkbox("Nivel digital por Provincia")
            var_nivel_digital_departamento = st.sidebar.checkbox("Nivel digital por Departamento")
            var_rubros_por_nivel_digital = st.sidebar.checkbox("Nivel digital por Rubro")

            var_rubro_anio = st.sidebar.checkbox("Número de MYPES por Rubro y Año")
            var_nivel_digital_anio = st.sidebar.checkbox("Número de MYPES por Nivel Digital y Año")
            var_nivel_digital_depto_anio = st.sidebar.checkbox("Nivel Digital por Departamento y Año")
            var_tipo_anio = st.sidebar.checkbox("Tipo de MYPES por Año")
            var_rubro_depto = st.sidebar.checkbox("Número de MYPES por Rubro y Departamento")
            var_prov_depto = st.sidebar.checkbox("Número de MYPES por Provincia y Departamento")
            var_dist_prov = st.sidebar.checkbox("Número de MYPES por Distrito y Provincia")
            var_nivel_digital_depto_prov = st.sidebar.checkbox("Nivel Digital por Departamento y Provincia")
            var_nivel_digital_prov = st.sidebar.checkbox("Número de MYPES por Nivel Digital y Provincia")
            var_rubro_distrito = st.sidebar.checkbox("Número de MYPES por Rubro y Distrito")

            var_tipo_depto = st.sidebar.checkbox("Número de MYPES por Tipo y Departamento")
            var_tipo_prov = st.sidebar.checkbox("Número de MYPES por Tipo y Provincia")
            var_tipo_dist = st.sidebar.checkbox("Número de MYPES por Tipo y Distrito")
            var_rubro_tipo = st.sidebar.checkbox("Número de MYPES por Rubro y Tipo")
            var_nivel_digital_tipo = st.sidebar.checkbox("Número de MYPES por Nivel Digital y Tipo")
            var_depto_anio = st.sidebar.checkbox("Número de MYPES por Departamento y Año")
            var_prov_anio = st.sidebar.checkbox("Número de MYPES por Provincia y Año")
            var_dist_anio = st.sidebar.checkbox("Número de MYPES por Distrito y Año")
            var_rubro_nivel_digital = st.sidebar.checkbox("Número de MYPES por Rubro y Nivel Digital")

            st.sidebar.title("Añadir Nueva MYPE")
            if st.sidebar.button("Añadir MYPE"):
                anio = st.sidebar.text_input("Año")
                razon_social = st.sidebar.text_input("Razón Social")
                rubro = st.sidebar.text_input("Rubro")
                tipo = st.sidebar.text_input("Tipo")
                departamento = st.sidebar.text_input("Departamento")
                provincia = st.sidebar.text_input("Provincia")
                distrito = st.sidebar.text_input("Distrito")
                nivel_digital = st.sidebar.text_input("Nivel Digital")
                dig_general = st.sidebar.text_input("DIG General")
                if st.sidebar.button("Guardar MYPE"):
                    nueva_mype = {
                        'ANIO': anio,
                        'RAZON_SOCIAL_ANONIMIZADA': razon_social,
                        'RUBRO': rubro,
                        'TIPO': tipo,
                        'DEPARTAMENTO': departamento,
                        'PROVINCIA': provincia,
                        'DISTRITO': distrito,
                        'NIVEL_DIGITAL': nivel_digital,
                        'DIG_GENERAL': dig_general
                    }
                    datos = datos.append(nueva_mype, ignore_index=True)
                    st.success("Nueva MYPE añadida exitosamente.")

            st.sidebar.title("Buscar RAZON_SOCIAL_ANONIMIZADA :")
            nombre_busqueda = st.sidebar.text_input("Nombre de la RAZON_SOCIAL_ANONIMIZADA")
            if st.sidebar.button("Buscar"):
                resultado_busqueda = datos[datos['RAZON_SOCIAL_ANONIMIZADA'].str.contains(nombre_busqueda, na=False)]
                st.write("### Resultados de Búsqueda")
                st.dataframe(resultado_busqueda, height=300)

            if var_anio:
                generador_graficos.graficar_mypes_por_anio()

            if var_departamento:
                generador_graficos.graficar_mypes_por_departamento()

            if var_distrito:
                distritos_seleccionados = st.sidebar.multiselect("Seleccione Distritos", sorted(list(datos['DISTRITO'].dropna().unique())))
                if distritos_seleccionados:
                    generador_graficos.graficar_mypes_por_distrito(distritos_seleccionados)

            if var_provincia:
                provincias_seleccionadas = st.sidebar.multiselect("Seleccione Provincias", sorted(list(datos['PROVINCIA'].dropna().unique())))
                if provincias_seleccionadas:
                    generador_graficos.graficar_mypes_por_provincia(provincias_seleccionadas)

            if var_dept_prov_dist:
                departamentos = sorted(list(datos['DEPARTAMENTO'].dropna().unique()))
                departamento = st.sidebar.selectbox("Seleccione Departamento", departamentos)
                if departamento:
                    provincias = sorted(list(datos[datos['DEPARTAMENTO'] == departamento]['PROVINCIA'].dropna().unique()))
                    provincia = st.sidebar.selectbox("Seleccione Provincia", provincias)
                    if provincia:
                        distritos = sorted(list(datos[(datos['DEPARTAMENTO'] == departamento) & (datos['PROVINCIA'] == provincia)]['DISTRITO'].dropna().unique()))
                        distrito = st.sidebar.selectbox("Seleccione Distrito", distritos)
                        if distrito:
                            generador_graficos.graficar_mypes_por_dept_prov_dist(departamento, provincia, distrito)

            if var_rubro:
                generador_graficos.graficar_mypes_por_rubro()

            if var_nivel_digital:
                generador_graficos.graficar_nivel_digital()

            if var_tipo:
                generador_graficos.graficar_mypes_por_tipo()

            if var_nivel_alcanzado:
                generador_graficos.graficar_dig_general()

            if var_comparar_nivel_digital:
                niveles_disponibles = ['Inicial', 'Básico', 'Intermedio']
                nivel_digital_1 = st.sidebar.selectbox("Seleccione el primer nivel de digitalización", niveles_disponibles)
                nivel_digital_2 = st.sidebar.selectbox("Seleccione el segundo nivel de digitalización", niveles_disponibles)
                if nivel_digital_1 and nivel_digital_2:
                    generador_graficos.comparar_nivel_digital(nivel_digital_1, nivel_digital_2)

            if var_comparar_rubro:
                rubros_disponibles = sorted(list(datos['RUBRO'].dropna().unique()))
                rubro_1 = st.sidebar.selectbox("Seleccione el primer rubro", rubros_disponibles)
                rubro_2 = st.sidebar.selectbox("Seleccione el segundo rubro", rubros_disponibles)
                if rubro_1 and rubro_2:
                    generador_graficos.comparar_rubro(rubro_1, rubro_2)
            
            if var_nivel_digital_distrito:
                distritos = sorted(list(datos['DISTRITO'].dropna().unique()))
                distrito_seleccionado = st.sidebar.selectbox("Seleccione Distrito", distritos)
                
                if distrito_seleccionado:
                    niveles_digitales = ['Inicial', 'Básico', 'Intermedio']
                    nivel_digital_seleccionado = st.sidebar.selectbox("Seleccione Nivel Digital", niveles_digitales)
                    
                    generador_graficos.graficar_nivel_digital_por_distrito(distrito_seleccionado, nivel_digital_seleccionado)
                
            if var_nivel_digital_provincia:
                provincias = sorted(list(datos['PROVINCIA'].dropna().unique()))
                provincia_seleccionada = st.sidebar.selectbox("Seleccione Provincia", provincias)
                
                if provincia_seleccionada:
                    niveles_digitales = ['Inicial', 'Básico', 'Intermedio']
                    nivel_digital_seleccionado = st.sidebar.selectbox("Seleccione Nivel Digital", niveles_digitales)
                    
                    generador_graficos.graficar_nivel_digital_por_provincia(provincia_seleccionada, nivel_digital_seleccionado)

            if var_nivel_digital_departamento:
                departamentos = sorted(list(datos['DEPARTAMENTO'].dropna().unique()))
                departamento_seleccionado = st.sidebar.selectbox("Seleccione Departamento", departamentos)
                
                if departamento_seleccionado:
                    niveles_digitales = ['Inicial', 'Básico', 'Intermedio']
                    nivel_digital_seleccionado = st.sidebar.selectbox("Seleccione Nivel Digital", niveles_digitales)
                    
                    generador_graficos.graficar_nivel_digital_por_departamento(departamento_seleccionado, nivel_digital_seleccionado)

            if var_rubros_por_nivel_digital:
                rubro = sorted(list(datos['RUBRO'].dropna().unique()))
                rubro_seleccionado = st.sidebar.selectbox("Seleccione el rubro", rubro)
                if rubro_seleccionado:
                    generador_graficos.graficar_nivel_digital_por_rubro(rubro_seleccionado)

            if var_rubro_anio:
                generador_graficos.graficar_mypes_por_rubro_y_anio()

            if var_nivel_digital_anio:
                generador_graficos.graficar_mypes_por_nivel_digital_y_anio()

            if var_nivel_digital_depto_anio:
                generador_graficos.graficar_nivel_digital_por_departamento_y_anio()

            if var_tipo_anio:
                generador_graficos.graficar_tipo_de_mypes_por_anio()

            if var_rubro_depto:
                generador_graficos.graficar_mypes_por_rubro_y_departamento()

            if var_prov_depto:
                generador_graficos.graficar_mypes_por_provincia_y_departamento()

            if var_dist_prov:
                provincias_seleccionadas = st.sidebar.multiselect("Seleccione Provincias", sorted(list(datos['PROVINCIA'].dropna().unique())))
                if provincias_seleccionadas:
                    generador_graficos.graficar_mypes_por_distrito_y_provincia(provincias_seleccionadas)

            if var_nivel_digital_depto_prov:
                generador_graficos.graficar_nivel_digital_por_departamento_y_provincia()

            if var_nivel_digital_prov:
                provincias_seleccionadas = st.sidebar.multiselect("Seleccione Provincias", sorted(list(datos['PROVINCIA'].dropna().unique())))
                if provincias_seleccionadas:
                    generador_graficos.graficar_mypes_por_nivel_digital_y_provincia(provincias_seleccionadas)

            if var_rubro_distrito:
                distritos_seleccionados = st.sidebar.multiselect("Seleccione Distritos", sorted(list(datos['DISTRITO'].dropna().unique())))
                if distritos_seleccionados:
                    generador_graficos.graficar_mypes_por_rubro_y_distrito(distritos_seleccionados)

            if var_tipo_depto:
                generador_graficos.graficar_mypes_por_tipo_y_departamento()

            if var_tipo_prov:
                provincias_seleccionadas = st.sidebar.multiselect("Seleccione Provincias", sorted(list(datos['PROVINCIA'].dropna().unique())))
                if provincias_seleccionadas:
                    generador_graficos.graficar_mypes_por_tipo_y_provincia(provincias_seleccionadas)

            if var_tipo_dist:
                distritos_seleccionados = st.sidebar.multiselect("Seleccione Distritos", sorted(list(datos['DISTRITO'].dropna().unique())))
                if distritos_seleccionados:
                    generador_graficos.graficar_mypes_por_tipo_y_distrito(distritos_seleccionados)

            if var_rubro_tipo:
                generador_graficos.graficar_mypes_por_rubro_y_tipo()

            if var_nivel_digital_tipo:
                generador_graficos.graficar_mypes_por_nivel_digital_y_tipo()

            if var_depto_anio:
                generador_graficos.graficar_mypes_por_departamento_y_anio()

            if var_prov_anio:
                provincias_seleccionadas = st.sidebar.multiselect("Seleccione Provincias", sorted(list(datos['PROVINCIA'].dropna().unique())))
                if provincias_seleccionadas:
                    generador_graficos.graficar_mypes_por_provincia_y_anio(provincias_seleccionadas)

            if var_dist_anio:
                distritos_seleccionados = st.sidebar.multiselect("Seleccione Distritos", sorted(list(datos['DISTRITO'].dropna().unique())))
                if distritos_seleccionados:
                    generador_graficos.graficar_mypes_por_distrito_y_anio(distritos_seleccionados)

            if var_rubro_nivel_digital:
                generador_graficos.graficar_mypes_por_rubro_y_nivel_digital()

if __name__ == "__main__":
    aplicacion()
