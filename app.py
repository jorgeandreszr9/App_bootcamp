import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from io import BytesIO

# Estilo HTML y CSS para títulos y subtítulos con degradado en las letras (azul eléctrico y gris)
st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    background: linear-gradient(100deg, #02AC66, #C0C0C0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: black; /* Cambio realizado */
}

.subheader {
    font-size: 24px;
    font-weight: bold;
    background: linear-gradient(180deg, #00008B, #C0C0C0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: black; /* Cambio realizado */
}

</style>
""", unsafe_allow_html=True)


# Título principal
st.markdown('<h1 class="title">Aplicación Oil and Gas</h1>', unsafe_allow_html=True)

# Selección del módulo
module = st.sidebar.selectbox("Selecciona el módulo", ["Módulo 1: Calculadora", "Módulo 2: Producción y Mapa", "Módulo 3: Exportación y Cálculo de IPR"])

if module == "Módulo 1: Calculadora":
    st.markdown('<h2 class="subheader">Módulo 1: Calculadora de Unidades</h2>', unsafe_allow_html=True)

    # Agregar imagen a la barra lateral
    st.sidebar.image("Escala_API.png", use_column_width=True)


    # Selección del tipo de cálculo
    calculation_type = st.radio("¿Qué desea calcular?", ("Gravedad específica a partir de API", "API a partir de gravedad específica"))

    if calculation_type == "Gravedad específica a partir de API":
        st.subheader("Conversión de gravedad API a gravedad específica")
        st.latex(r"\text{Gravedad específica} = \frac{141.5}{131.5 + \text{API}}") # Sintaxis para mostrar ecuación
        #st.latex(r'''S_w = \sqrt{ \frac{a \cdot R_w}{\phi^m \cdot R_t} }''')
        try:
            api_gravity = st.number_input("Ingrese la gravedad API", min_value=0.0)
            specific_gravity = 141.5 / (131.5 + api_gravity)
            st.write(f"Gravedad específica: {specific_gravity:.4f}")
            
            # Clasificación del tipo de fluido
            if api_gravity < 10:
                fluid_type = "Petróleo extrapesado"
            elif api_gravity == 10:
                fluid_type = "Petróleo pesado (posiblemente agua)"
            elif api_gravity < 22.3:
                fluid_type = "Petróleo pesado"
            elif api_gravity < 31.1:
                fluid_type = "Petróleo medio"
            elif api_gravity < 39:
                fluid_type = "Petróleo ligero"
            else:
                fluid_type = "Petróleo superligero"
            
            st.write(f"Tipo de fluido: **{fluid_type}**")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.subheader("Conversión de gravedad específica a API")
        st.latex(r"\text{API} = \frac{141.5}{\text{Gravedad específica}} - 131.5")
        try:
            specific_gravity = st.number_input("Ingrese la gravedad específica", min_value=0.0)
            api_gravity = 141.5 / specific_gravity - 131.5
            st.write(f"Gravedad API: {api_gravity:.2f}")
            
            # Clasificación del tipo de fluido
            if api_gravity < 10:
                fluid_type = "Petróleo extrapesado"
            elif api_gravity == 10:
                fluid_type = "Petróleo pesado (posiblemente agua)"
            elif api_gravity < 22.3:
                fluid_type = "Petróleo pesado"
            elif api_gravity < 31.1:
                fluid_type = "Petróleo medio"
            elif api_gravity < 39:
                fluid_type = "Petróleo ligero"
            else:
                fluid_type = "Petróleo superligero"
            
            st.write(f"Tipo de fluido: **{fluid_type}**")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

elif module == "Módulo 2: Producción y Mapa":
    st.markdown('<h2 class="subheader">Módulo 2: Producción y Mapa</h2>', unsafe_allow_html=True)

    # Agregar imagen a la barra lateral
    st.sidebar.image("Módulo2.png", use_column_width=True)

    
    # Selección de días de producción
    days = st.number_input("Número de días de producción", min_value=1, max_value=365, value=30)

    # Generar o actualizar los datos de producción con ruido
    wells = ["Pozo 1", "Pozo 2", "Pozo 3"]

    # Simulación de datos de producción
    np.random.seed(42)  # Para reproducibilidad
    production_data = {
        "Día": np.arange(1, days + 1),
        "Pozo 1 Petróleo": np.linspace(500, 100, days) + np.random.normal(0, 20, days),
        "Pozo 1 Agua": np.linspace(50, 300, days) + np.random.normal(0, 10, days),
        "Pozo 2 Petróleo": np.linspace(600, 150, days) + np.random.normal(0, 25, days),
        "Pozo 2 Agua": np.linspace(60, 350, days) + np.random.normal(0, 15, days),
        "Pozo 3 Petróleo": np.linspace(400, 80, days) + np.random.normal(0, 15, days),
        "Pozo 3 Agua": np.linspace(40, 250, days) + np.random.normal(0, 10, days),
    }

    production_df = pd.DataFrame(production_data)

    st.write(production_df)

    # Visualización de datos
    st.subheader("Gráfico de producción")
    selected_well = st.selectbox("Seleccione el pozo", ["Pozo 1", "Pozo 2", "Pozo 3"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=production_df["Día"], y=production_df[f"{selected_well} Petróleo"], mode='lines', name='Petróleo'))
    fig.add_trace(go.Scatter(x=production_df["Día"], y=production_df[f"{selected_well} Agua"], mode='lines', name='Agua'))
    fig.update_layout(title=f'Producción diaria - {selected_well}', xaxis_title='Día', yaxis_title='Producción (bbl/día)')
    st.plotly_chart(fig)

    # Mapa de Producción usando Plotly
    st.subheader("Mapa de Producción")
    coordinates = {"Pozo 1": (29.7, -95.3), "Pozo 2": (29.6, -95.2), "Pozo 3": (29.8, -95.4)}

    # Normalización de coordenadas
    latitudes = [coord[0] for coord in coordinates.values()]
    longitudes = [coord[1] for coord in coordinates.values()]
    lat_min, lat_max = min(latitudes), max(latitudes)
    lon_min, lon_max = min(longitudes), max(longitudes)

    # Ajustar el rango para que esté dentro de [0, 1]
    normalized_coords = {
        well: (
            (lat - lat_min) / (lat_max - lat_min) * 0.9 + 0.05,  # Escalando para evitar valores fuera del rango
            (lon - lon_min) / (lon_max - lon_min) * 0.9 + 0.05   # Escalando para evitar valores fuera del rango
        )
        for well, (lat, lon) in coordinates.items()
    }

    # Widget para seleccionar el día y mostrar la distribución de petróleo y agua
    day_selected = st.slider("Selecciona el día", 1, days, 1)

    fig_map = go.Figure()

    # Agregar un scatter plot para mostrar la malla de coordenadas
    fig_map.add_trace(go.Scatter(
        x=[coord[1] for coord in coordinates.values()],
        y=[coord[0] for coord in coordinates.values()],
        mode='markers+text',
        text=[well for well in coordinates.keys()],
        textposition='top center',
        marker=dict(size=10, color='red'),
        name='Ubicación de Pozos'
    ))

    for well, coord in normalized_coords.items():
        oil_prod = production_df.loc[production_df["Día"] == day_selected, f"{well} Petróleo"].values[0]
        water_prod = production_df.loc[production_df["Día"] == day_selected, f"{well} Agua"].values[0]
        fig_map.add_trace(go.Pie(labels=['Petróleo', 'Agua'], values=[oil_prod, water_prod], name=well, hole=.3,
                                 domain=dict(x=[coord[1] - 0.05, coord[1] + 0.05], y=[coord[0] - 0.05, coord[0] + 0.05])))

    fig_map.update_layout(
        title=f'Distribución de Producción de Petróleo y Agua - Día {day_selected}',
        showlegend=False,
        xaxis=dict(showgrid=True, zeroline=False),  # Mostrar grilla en el eje x
        yaxis=dict(showgrid=True, zeroline=False),  # Mostrar grilla en el eje y
        xaxis_title="Longitud (normalizada)",
        yaxis_title="Latitud (normalizada)",
    )
    st.plotly_chart(fig_map)

elif module == "Módulo 3: Exportación y Cálculo de IPR":
    st.markdown('<h2 class="subheader">Módulo 3: Exportación y Cálculo de IPR</h2>', unsafe_allow_html=True)

    st.subheader("Cálculo de IPR (Inflow Performance Relationship) usando el Método Generalizado")

# Agregar imagen a la barra lateral
    st.sidebar.image("Balancín.png", use_column_width=True)

    # Ingreso de parámetros necesarios
    pws = st.number_input("Ingrese la presión de fondo estática \(P_{ws}\) (psia)", min_value=0.0)
    pwf_test = st.number_input("Ingrese la presión de fondo fluyente durante la prueba \(P_{wf}\) (psia)", min_value=0.0)
    qo_test = st.number_input("Ingrese el caudal a la \(P_{wf}\) de la prueba \(Q_o\) (bbl/día)", min_value=0.0)
    pb = st.number_input("Ingrese la presión de burbuja \(P_b\) (psia)", min_value=0.0)
    ef = st.number_input("Ingrese la eficiencia de flujo \(EF)", min_value=1.0)
    
    # Funciones de cálculo
    def j(qo_test, pwf_test, pws, pb, ef=1):
        if ef == 1:
            if pwf_test >= pb:
                J = qo_test / (pws - pwf_test)
            else:
                J = qo_test / ((pws - pb) + (pb / 1.8) * \
                          (1 - 0.2 * (pwf_test / pb) - 0.8 * (pwf_test / pb)**2))
        elif ef != 1:
            st.warning("Eficiencia de flujo diferente de 1 no está completamente manejada.")
        return J

    def Qb(qo_test, pwf_test, pws, pb, ef=1):
        qb = j(qo_test, pwf_test, pws, pb, ef) * (pws - pb)
        return qb

    def aof(qo_test, pwf_test, pws, pb, ef=1):
        if ef == 1:
            if pws > pb:  # Yac. subsaturado
                if pwf_test >= pb:
                    AOF = j(qo_test, pwf_test, pws, pb) * pws
                elif pwf_test <  pb:
                    AOF = Qb(qo_test, pwf_test, pws, pb, ef=1) + ((j(qo_test, pwf_test, pws, pb) * pb) / (1.8))
            elif pws <= pb:  # Yac. Saturado
                AOF = qo_test / (1 - 0.2 * (pwf_test / pws) - 0.8 * (pwf_test / pws)**2)
        return AOF

    def qo_darcy(qo_test, pwf_test, pws, pwf, pb):
        qo = j(qo_test, pwf_test, pws, pb) * (pws - pwf)
        return qo

    def qo_vogel(q_test, pwf_test, pws, pwf, pb):
        if pws <= pb:  # Yac. Saturado
            qo = aof(qo_test, pwf_test, pws, pb) * \
                 (1 - 0.2 * (pwf / pws) - 0.8 * (pwf / pws)**2)
        return qo

    def qo_ipr_compuesto(qo_test, pwf_test, pws, pwf, pb):
        if pws > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(qo_test, pwf_test, pws, pwf, pb)
            elif pwf < pb: 
                qo = Qb(qo_test, pwf_test, pws, pb) + \
                     ((j(qo_test, pwf_test, pws, pb) * pb) / (1.8)) * \
                     (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb)**2)
        elif pws <= pb:  # Yac. Saturado
            qo = aof(qo_test, pwf_test, pws, pb) * \
                 (1 - 0.2 * (pwf / pws) - 0.8 * (pwf / pws)**2)
        return qo

    def generate_ipr_curve(pws, pb, qo_test, pwf_test, steps=50):
        steps = int(steps)  # Asegurarse de que 'steps' sea un entero
        pressures = np.linspace(pws, 0, steps)
        rates = []
        
        for pwf in pressures:
            qo = qo_ipr_compuesto(qo_test, pwf_test, pws, pwf, pb)  # Uso de la función correcta
            rates.append(qo)
        
        return pressures, rates

    if st.button("Calcular IPR"):
        try:
            pressures, rates = generate_ipr_curve(pws, pb, qo_test, pwf_test)
            
            # Gráfica de la curva IPR continua
            plt.figure(figsize=(10, 6))
            plt.plot(rates, pressures, marker='o')
            plt.title('Curva IPR usando el Método Generalizado')
            plt.xlabel('Caudal de Producción \(Q_o\) (bbl/día)')
            plt.ylabel('Presión de Fondo Fluyente \(P_{wf}\) (psia)')
            plt.grid(True)

            # Línea entrecortada en la presión de burbuja
            plt.axhline(y=pb, color='red', linestyle='--')
            plt.axvline(x=Qb(qo_test, pwf_test, pws, pb), color='red', linestyle='--')
            plt.text(Qb(qo_test, pwf_test, pws, pb), pb, 'Punto de burbuja', color='red', ha='right')

            st.pyplot(plt)

            # Resultados en un DataFrame
            result_data = pd.DataFrame({
                "Caudal de Producción \(Q_o\) (bbl/día)": rates,
                "Presión de Fondo Fluyente \(P_{wf}\) (psia)": pressures
            })
            
            st.write(result_data)

            # Determinar el tipo de yacimiento
            if pws > pb:
                tipo_yacimiento = "Subsaturado"
                razon = "porque la presión de fondo estática es mayor que la presión de burbuja."
            else:
                tipo_yacimiento = "Saturado"
                razon = "porque la presión de fondo estática es menor o igual que la presión de burbuja."

            st.write(f"**Tipo de yacimiento:** {tipo_yacimiento} ({razon})")

            # Cálculo del caudal máximo y el índice de productividad
            Q_bp = Qb(qo_test, pwf_test, pws, pb, ef=1)
            q_max = aof(qo_test, pwf_test, pws, pb)
            ip = j(qo_test, pwf_test, pws, pb)

            st.write(f"**Caudal al punto de burbuja (Qb):** {Q_bp:.2f} bbl/día")
            st.write(f"**Caudal máximo (AOF) cuando Pwf = 0:** {q_max:.2f} bbl/día")
            st.write(f"**Índice de Productividad (IP):** {ip:.4f} bbl/día/psia")

            # Función para exportar resultados a Excel
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='IPR Resultados')
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            # Botones para exportar resultados
            if st.button("Exportar a Excel"):
                st.download_button(label="Descargar Excel", data=to_excel(result_data), file_name='IPR_resultados.xlsx')

            if st.button("Exportar a CSV"):
                st.download_button(label="Descargar CSV", data=result_data.to_csv(index=False).encode('utf-8'), file_name='IPR_resultados.csv')

            if st.button("Exportar a PDF"):
                st.warning("Funcionalidad PDF no implementada en esta versión.")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
