import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Configuración de la página
st.set_page_config(page_title='Análisis de Datos', layout='wide')
st.title('Análisis de Datos, Factor de Potencia')

# Sidebar para ingresar datos CSV
st.sidebar.header('Pegar datos CSV')
csv_data = st.sidebar.text_area('Pega aquí los datos en formato CSV')

if csv_data:
    column_names = "DateTime,FP,Rango de Cumplimiento 0.95 (low),Rango de Cumplimiento 0.95 (high),Rango de Cumplimiento 0.97 (low),Rango de Cumplimiento 0.97 (high)\n"
    csv_data = column_names + csv_data
    data = StringIO(csv_data)
    df = pd.read_csv(data)

    # Llenar valores faltantes
    df.fillna({
        'Rango de Cumplimiento 0.95 (low)': 0.95,
        'Rango de Cumplimiento 0.95 (high)': 1,
        'Rango de Cumplimiento 0.97 (low)': 0.97,
        'Rango de Cumplimiento 0.97 (high)': 1
    }, inplace=True)

    # Calcular cumplimiento
    df['Cumple 0.95'] = df.apply(lambda row: 'Cumple' if row['FP'] >= row['Rango de Cumplimiento 0.95 (low)'] and row['FP'] <= row['Rango de Cumplimiento 0.95 (high)'] else 'No Cumple', axis=1)
    df['Cumple 0.97'] = df.apply(lambda row: 'Cumple' if row['FP'] >= row['Rango de Cumplimiento 0.97 (low)'] and row['FP'] <= row['Rango de Cumplimiento 0.97 (high)'] else 'No Cumple', axis=1)

    # Mostrar datos y cumplimiento
    st.subheader('Datos del Archivo CSV')
    st.dataframe(df[['DateTime', 'FP', 'Cumple 0.95', 'Cumple 0.97']])

    # Datos totales esperados y datos actuales
    total_data_points = 8928
    current_data_count = len(df)
    pending_data_points = total_data_points - current_data_count

    # Calcular porcentajes
    cumple_95_pct = (df['Cumple 0.95'] == 'Cumple').mean() * 100
    cumple_97_pct = (df['Cumple 0.97'] == 'Cumple').mean() * 100

    # Análisis estadístico
    st.subheader('Análisis Estadístico del Factor de Potencia')
    stats = df['FP'].describe()
    st.write(stats)

    # Mostrar porcentajes exactos de cumplimiento
    st.subheader('Porcentajes Exactos de Cumplimiento')
    st.write(f'Porcentaje de datos que cumplen el cuantil 0.95: {cumple_95_pct:.2f}%')
    st.write(f'Porcentaje de datos que cumplen el cuantil 0.97: {cumple_97_pct:.2f}%')

    # Gráficos de pastel para visualizar cumplimiento y proyecciones
    fig_pie_95 = px.pie(values=[cumple_95_pct, 100 - cumple_95_pct, pending_data_points * 100 / total_data_points],
                        names=['Cumple', 'No Cumple', 'Todavía no ha pasado'],
                        title='Proyección de Cumplimiento 0.95')
    fig_pie_97 = px.pie(values=[cumple_97_pct, 100 - cumple_97_pct, pending_data_points * 100 / total_data_points],
                        names=['Cumple', 'No Cumple', 'Todavía no ha pasado'],
                        title='Proyección de Cumplimiento 0.97')
    st.plotly_chart(fig_pie_95)
    st.plotly_chart(fig_pie_97)

    # Gráfico de líneas para FP
    fig_line = px.line(df, x='DateTime', y='FP', title='Evolución del Factor de Potencia (FP)')
    st.plotly_chart(fig_line)

    # Histograma de FP
    fig_hist = px.histogram(df, x='FP', nbins=30, title='Distribución del Factor de Potencia (FP)')
    st.plotly_chart(fig_hist)

else:
    st.info('Por favor, pega los datos en formato CSV en el recuadro de la barra lateral para comenzar.')
