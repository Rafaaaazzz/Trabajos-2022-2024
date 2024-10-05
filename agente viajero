import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

def generar_matriz_simetrica(n):
    matriz = np.random.randint(1, 100, size=(n, n))
    matriz = (matriz + matriz.T) // 2
    np.fill_diagonal(matriz, 0)
    return matriz

def vecino_mas_cercano(matriz, n):
    visitado = [False] * n
    ciclo = [0]
    visitado[0] = True
    nodo_actual = 0
    distancia_total = 0

    for _ in range(n - 1):
        distancia_min = float('inf')
        siguiente_nodo = None
        for i in range(n):
            if not visitado[i] and 0 < matriz[nodo_actual][i] < distancia_min:
                distancia_min = matriz[nodo_actual][i]
                siguiente_nodo = i
        ciclo.append(siguiente_nodo)
        visitado[siguiente_nodo] = True
        distancia_total += distancia_min
        nodo_actual = siguiente_nodo
    
    distancia_total += matriz[nodo_actual][0]
    ciclo.append(0)
    
    return ciclo, distancia_total

def optimizacion_2_opt(matriz, ciclo, n, max_iteraciones=100):
    def intercambiar_2opt(ruta, i, k):
        return ruta[:i] + ruta[i:k+1][::-1] + ruta[k+1:]

    mejor_ciclo = ciclo
    mejora = True
    iteraciones = 0
    while mejora and iteraciones < max_iteraciones:
        mejora = False
        mejor_distancia = calcular_distancia(matriz, mejor_ciclo)
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                nuevo_ciclo = intercambiar_2opt(mejor_ciclo, i, k)
                nueva_distancia = calcular_distancia(matriz, nuevo_ciclo)
                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_ciclo = nuevo_ciclo
                    mejora = True
        iteraciones += 1
    return mejor_ciclo, mejor_distancia

def calcular_distancia(matriz, ciclo):
    distancia_total = 0
    for i in range(len(ciclo) - 1):
        distancia_total += matriz[ciclo[i]][ciclo[i+1]]
    return distancia_total

def graficar_ruta_interactiva(matriz, ciclo, nombres, titulo, n, color_ruta):
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=matriz[i][j])

    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    edge_x = []
    edge_y = []
    edge_text = []
    annotations = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_text.append(f'{nombres[edge[0]]} - {nombres[edge[1]]}: {matriz[edge[0]][edge[1]]}')
        
        annotations.append(dict(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=str(matriz[edge[0]][edge[1]]),
            showarrow=False,
            font=dict(color='white', size=14),
            align="center",
            ax=0, ay=0
        ))
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#A0A0A0'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=nombres,
        textposition="top center",
        marker=dict(
            showscale=False,
            color='rgb(255,165,0)',
            size=16,
            line_width=3))

    ciclo_x = []
    ciclo_y = []
    for i in range(len(ciclo) - 1):
        x0, y0 = pos[ciclo[i]]
        x1, y1 = pos[ciclo[i+1]]
        ciclo_x.append(x0)
        ciclo_x.append(x1)
        ciclo_x.append(None)
        ciclo_y.append(y0)
        ciclo_y.append(y1)
        ciclo_y.append(None)

    ciclo_trace = go.Scatter(
        x=ciclo_x, y=ciclo_y,
        line=dict(width=6, color=color_ruta),
        hoverinfo='none',
        mode='lines')

    fig = go.Figure(data=[edge_trace, ciclo_trace, node_trace],
                    layout=go.Layout(
                        title=dict(
                            text=titulo,
                            x=0.5,
                            xanchor='center',
                            font=dict(size=24, color='white')
                        ),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=20, r=20, t=60),
                        annotations=annotations,
                        paper_bgcolor='black',
                        plot_bgcolor='black',
                        xaxis=dict(showgrid=False, zeroline=False, visible=False),
                        yaxis=dict(showgrid=False, zeroline=False, visible=False)))

    st.plotly_chart(fig)

st.markdown("<h1 style='text-align: left; color: #FF6347;'>Problema del Agente Viajero (TSP) 🚗</h1>", unsafe_allow_html=True)

st.write("Selecciona un contexto para aplicar el TSP en Perú:")

opciones = ['Turismo en Perú', 'Transporte de mercancías', 'Recolección de basura', 
            'Transporte público', 'Rutas médicas en zonas rurales', 'Agricultura', 'Ingresar manualmente']

contexto = st.selectbox("Contexto de Aplicación", opciones)

if contexto == 'Ingresar manualmente':
    num_puntos = st.slider("Número de puntos", min_value=3, max_value=10)
    nombres = []
    for i in range(num_puntos):
        nombre = st.text_input(f"Nombre del punto {i+1}", f"Punto {i+1}")
        nombres.append(nombre)
    
    matriz = np.zeros((num_puntos, num_puntos), dtype=int)
    
    for i in range(num_puntos):
        for j in range(i + 1, num_puntos):
            valor = st.number_input(f"Distancia entre {nombres[i]} y {nombres[j]}", min_value=1, max_value=100)
            matriz[i][j] = valor
            matriz[j][i] = valor
    
    np.fill_diagonal(matriz, 0)
    st.dataframe(pd.DataFrame(matriz, index=nombres, columns=nombres))

else:
    if contexto == 'Turismo en Perú':
        nombres = ['Lima', 'Cusco', 'Machu Picchu', 'Nazca', 'Arequipa', 'Valle del Colca']
    elif contexto == 'Transporte de mercancías':
        nombres = ['Lima', 'Arequipa', 'Trujillo', 'Chiclayo', 'Piura', 'Cusco']
    elif contexto == 'Recolección de basura':
        nombres = ['Miraflores', 'San Isidro', 'Surco', 'La Molina', 'San Borja']
    elif contexto == 'Transporte público':
        nombres = ['Ruta 1', 'Ruta 2', 'Ruta 3', 'Ruta 4', 'Ruta 5']
    elif contexto == 'Rutas médicas en zonas rurales':
        nombres = ['Localidad A', 'Localidad B', 'Localidad C', 'Localidad D']
    elif contexto == 'Agricultura':
        nombres = ['Parcela 1', 'Parcela 2', 'Parcela 3', 'Parcela 4', 'Parcela 5']

    matriz = generar_matriz_simetrica(len(nombres))
    st.dataframe(pd.DataFrame(matriz, index=nombres, columns=nombres))

color_ruta = st.color_picker("Selecciona el color para la ruta optimizada", "#33FF57")

if st.button("Optimizar Ruta"):
    ciclo, distancia = vecino_mas_cercano(matriz, len(matriz))
    st.write(f"Ruta Optimizada: {' -> '.join([nombres[i] for i in ciclo])}")
    st.write(f"Distancia total optimizada: {distancia}")
    graficar_ruta_interactiva(matriz, ciclo, nombres, f"Ruta Optimizada ({contexto})", len(matriz), color_ruta)
