import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Strategic Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .alert-box { padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .alert-danger { background-color: #fdecea; color: #c62828; border: 1px solid #c62828; }
    .alert-warning { background-color: #fff8e1; color: #ef6c00; border: 1px solid #ef6c00; }
    .alert-success { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico Empresarial: **Rentabilidad, Liquidez y Tendencias**")

# --- BARRA LATERAL: INPUT DE DATOS ---
with st.sidebar:
    st.header("1. Cierre del Mes Actual")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        ventas_actual = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0, key="v_act")
        costo_ventas = st.number_input("Costo de Ventas (Variables)", value=30000.0, step=1000.0, key="c_act")
        gastos_operativos = st.number_input("Gastos Operativos (Fijos)", value=15000.0, step=500.0, key="g_act")
        depreciacion = st.number_input("Depreciaciones", value=1500.0, key="d_act")
        intereses = st.number_input("Gastos Financieros", value=500.0, key="i_act")
        impuestos = st.number_input("Impuestos", value=900.0, key="imp_act")

    with st.expander("B. Balance General (Liquidez)", expanded=False):
        activo_corriente = st.number_input("Activo Corriente", value=80000.0)
        pasivo_corriente = st.number_input("Pasivo Corriente", value=60000.0)
        inventario = st.number_input("Inventario", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar", value=10000.0)

    st.header("2. Histórico (Tendencias)")
    st.info("Ingresa los datos pasados para calcular el EBITDA real de cada mes.")
    
    # --- LOGICA DINÁMICA DE MESES ---
    num_meses = st.number_input("Meses a comparar (sin incluir actual)", min_value=1, max_value=6, value=2, step=1)
    
    historial_ventas = []
    historial_ebitda = []
    meses_labels = []

    # Bucle para pedir datos de cada mes histórico
    for i in range(num_meses):
        # Etiqueta del mes (Ej: Mes -1, Mes -2)
        idx_mes = num_meses - i
        label_mes = f"Mes Anterior (-{idx_mes})"
        meses_labels.append(label_mes)
        
        with st.expander(f"Datos: {label_mes}", expanded=False):
            # Pedimos los 3 componentes para calcular EBITDA
            col_h1, col_h2, col_h3 = st.columns(3)
            
            # Valores por defecto para agilizar la demo
            def_v = 40000.0 + (i * 2000)
            def_c = 25000.0 + (i * 1000)
            def_g = 12000.0
            
            v_hist = col_h1.number_input("Ventas", value=def_v, key=f"v_{i}")
            c_hist = col_h2.number_input("Costos (Var)", value=def_c, key=f"c_{i}")
            g_hist = col_h3.number_input("Gastos (Fij)", value=def_g, key=f"g_{i}")
            
            # CÁLCULO AUTOMÁTICO DEL EBITDA HISTÓRICO
            ebitda_calc = v_hist - c_hist - g_hist
            st.markdown(f"**EBITDA Calculado:** :green[${ebitda_calc:,.0f}]")
            
            historial_ventas.append(v_hist)
            historial_ebitda.append(ebitda_calc)

    # Agregamos el mes actual al final de las listas para la gráfica completa
    ebitda_actual_calc = ventas_actual - costo_ventas - gastos_operativos
    
    meses_labels.append("Mes Actual")
    historial_ventas.append(ventas_actual)
    historial_ebitda.append(ebitda_actual_calc)

# --- CÁLCULOS ESTRATÉGICOS GLOBALES ---
# Rentabilidad Actual
utilidad_bruta = ventas_actual - costo_ventas
margen_ebitda = (ebitda_actual_calc / ventas_actual) * 100 if ventas_actual > 0 else 0
utilidad_neta = ebitda_actual_calc - depreciacion - intereses - impuestos

# Liquidez
razon_circulante = activo_corriente / pasivo_corriente if pasivo_corriente > 0 else 0
ccc = ((cuentas_cobrar / ventas_actual) * 30) + ((inventario / costo_ventas) * 30) - ((cuentas_pagar / costo_ventas) * 30)

# Punto de Equilibrio
costos_fijos_totales = gastos_operativos + intereses
margen_contribucion_pct = (utilidad_bruta / ventas_actual) if ventas_actual > 0 else 0
punto_equilibrio = costos_fijos_totales / margen_contribucion_pct if margen_contribucion_pct > 0 else 0

# --- DASHBOARD VISUAL ---

tab1, tab2, tab3 = st.tabs(["📈 Tendencia & Potencia", "⚖️ Equilibrio Maestro", "💰 Liquidez (Cash Flow)"])

# MÓDULO 1: TENDENCIA & POTENCIA
with tab1:
    st.subheader(f"Análisis de Evolución ({num_meses + 1} Periodos)")
    
    # GRÁFICO DE TENDENCIA
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=meses_labels, y=historial_ventas, mode='lines+markers+text', name='Ventas', 
                                   text=[f"${x/1000:.0f}k" for x in historial_ventas], textposition="top center",
                                   line=dict(color='#1e88e5', width=3)))
    fig_trend.add_trace(go.Scatter(x=meses_labels, y=historial_ebitda, mode='lines+markers+text', name='EBITDA (Real)', 
                                   text=[f"${x/1000:.0f}k" for x in historial_ebitda], textposition="top center",
                                   line=dict(color='#43a047', width=3), fill='tozeroy'))
    
    fig_trend.update_layout(title="Ventas vs. Rentabilidad Real (Calculada)", height=450, hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

    # CÁLCULO DE CRECIMIENTO (Inicio vs Fin)
    inicio_v = historial_ventas[0]
    fin_v = historial_ventas[-1]
    inicio_e = historial_ebitda[0]
    fin_e = historial_ebitda[-1]
    
    crecimiento_ventas = ((fin_v - inicio_v) / inicio_v) * 100 if inicio_v > 0 else 0
    crecimiento_ebitda = ((fin_e - inicio_e) / inicio_e) * 100 if inicio_e > 0 else 0
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric("Crecimiento Ventas", f"{crecimiento_ventas:.1f}%", help="Variación desde el primer mes registrado hasta hoy.")
    with col_t2:
        st.metric("Crecimiento EBITDA", f"{crecimiento_ebitda:.1f}%", help="Variación de la utilidad operativa real.")
    with col_t3:
        st.metric("Margen EBITDA Actual", f"{margen_ebitda:.1f}%", help="Eficiencia del mes actual.")

    st.markdown("---")
    st.write("#### 🧠 Diagnóstico de Tendencia (SG Consulting):")
    
    if crecimiento_ventas > 0 and crecimiento_ebitda < 0:
        st.markdown("""<div class="alert-box alert-danger">
        🚨 <strong>ALERTA DE INEFICIENCIA:</strong> Cuidado. Tus ventas han subido, pero tu EBITDA ha bajado. 
        Estás gastando más de lo que ingresas extra. Revisa Costos Variables y Gastos Fijos históricos.</div>""", unsafe_allow_html=True)
    elif crecimiento_ventas > crecimiento_ebitda:
        st.markdown("""<div class="alert-box alert-warning">
        ⚠️ <strong>CRECIMIENTO PESADO:</strong> El negocio crece, pero la estructura de costos crece más rápido. 
        El EBITDA no sigue el ritmo de las ventas.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="alert-box alert-success">
        ✅ <strong>ESCALAMIENTO RENTABLE:</strong> Tu EBITDA crece saludablemente junto con tus ventas. 
        Estás optimizando la operación mes a mes.</div>""", unsafe_allow_html=True)

# MÓDULO 2: PUNTO DE EQUILIBRIO
with tab2:
    st.subheader("Mapa de Supervivencia (Mes Actual)")
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.metric("Ventas Actuales", f"${ventas_actual:,.0f}")
        st.metric("Punto de Equilibrio", f"${punto_equilibrio:,.0f}")
        
        if punto_equilibrio > 0:
            pct_meta = (ventas_actual / punto_equilibrio) * 100
        else:
            pct_meta = 0
        
        if ventas_actual > punto_equilibrio:
            st.success(f"Cubres costos al {pct_meta:.0f}%")
        else:
            st.error(f"Faltan ventas para cubrir costos.")
        
    with c2:
        fig_eq = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = ventas_actual,
            title = {'text': "Ventas vs Meta Mínima"},
            gauge = {
                'axis': {'range': [None, punto_equilibrio * 1.5]},
                'bar': {'color': "#1565c0"},
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': punto_equilibrio}
            }
        ))
        st.plotly_chart(fig_eq, use_container_width=True)

# MÓDULO 3: LIQUIDEZ
with tab3:
    st.subheader("Indicadores de Caja")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Razón Circulante", f"{razon_circulante:.2f}")
        if razon_circulante < 1:
            st.error("PELIGRO: Pasivos superan Activos a corto plazo.")
        else:
            st.success("Solvencia adecuada.")
    with col_b:
        st.metric("Ciclo de Caja (CCC)", f"{ccc:.0f} días")
        st.caption("Días que financias la operación.")

# --- GENERADOR DE REPORTE PDF V4 ---
def create_pdf_v4():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SG CONSULTING | Reporte Estrategico", ln=True, align="C")
    pdf.ln(5)
    
    # Sección Tendencia
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"1. ANALISIS DE TENDENCIA ({num_meses + 1} Meses)", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    
    pdf.cell(0, 8, f"Crecimiento Ventas: {crecimiento_ventas:.1f}%", ln=True)
    pdf.cell(0, 8, f"Crecimiento EBITDA: {crecimiento_ebitda:.1f}%", ln=True)
    
    if crecimiento_ventas > crecimiento_ebitda:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 8, "ALERTA: Las ventas crecen mas rapido que la utilidad. El negocio pierde eficiencia operativa.")
    else:
        pdf.set_text_color(0, 100, 0)
        pdf.multi_cell(0, 8, "TENDENCIA POSITIVA: El negocio escala saludablemente, mejorando margenes.")
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Sección Actual
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. ESTADO ACTUAL (Cierre de Mes)", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Ventas Actuales: ${ventas_actual:,.2f}", ln=True)
    pdf.cell(0, 8, f"EBITDA Actual: ${ebitda_actual_calc:,.2f} ({margen_ebitda:.1f}%)", ln=True)
    pdf.cell(0, 8, f"Punto de Equilibrio: ${punto_equilibrio:,.2f}", ln=True)
    
    # Sección Liquidez
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. LIQUIDEZ Y SOLVENCIA", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Razon Circulante: {razon_circulante:.2f}", ln=True)
    pdf.cell(0, 8, f"Ciclo de Caja: {ccc:.0f} dias", ln=True)
    
    if razon_circulante < 1:
         pdf.set_text_color(194, 24, 7)
         # AQUÍ ESTABA EL ERROR: Texto largo corregido en una sola línea
         pdf.multi_cell(0, 8, "RIESGO CRITICO: La empresa no tiene activos suficientes para cubrir sus deudas inmediatas.")
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Generado por SG Rescue App - Uso Confidencial", ln=True, align="C")
    
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar Reporte Completo"):
    pdf_bytes = create_pdf_v4()
    st.sidebar.download_button("💾 Guardar PDF", data=pdf_bytes, file_name="Reporte_SG_Consulting.pdf", mime="application/pdf")
