import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Strategic Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- ESTILOS VISUALES PREMIUM ---
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
    st.header("1. Datos del Mes Actual (Cierre)")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        ventas_actual = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0)
        costo_ventas = st.number_input("Costo de Ventas (Variables)", value=30000.0, step=1000.0)
        gastos_operativos = st.number_input("Gastos Operativos (Fijos)", value=15000.0, step=500.0)
        depreciacion = st.number_input("Depreciaciones", value=1500.0)
        intereses = st.number_input("Gastos Financieros", value=500.0)
        impuestos = st.number_input("Impuestos", value=900.0)

    with st.expander("B. Balance General (Liquidez)", expanded=False):
        activo_corriente = st.number_input("Activo Corriente", value=80000.0)
        pasivo_corriente = st.number_input("Pasivo Corriente", value=60000.0)
        inventario = st.number_input("Inventario", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar", value=10000.0)

    st.header("2. Análisis de Tendencia (Histórico)")
    
    # --- LOGICA DINÁMICA DE MESES ---
    num_meses = st.number_input("¿Cuántos meses quieres comparar?", min_value=2, max_value=12, value=3, step=1)
    
    historial_ventas = []
    historial_ebitda = []
    meses_labels = []

    st.markdown("Invgresa los datos desde el más antiguo hasta el actual:")
    
    with st.expander("Ingresar Datos Históricos", expanded=True):
        for i in range(num_meses):
            # Usamos columnas para ahorrar espacio en la barra lateral
            col_h1, col_h2 = st.columns(2)
            label_mes = f"Mes -{num_meses - i - 1}" if i < num_meses-1 else "Mes Actual"
            meses_labels.append(label_mes)
            
            with col_h1:
                # Si es el último mes (actual), tomamos el valor ya ingresado arriba por defecto
                val_v = ventas_actual if i == num_meses-1 else 40000.0 + (i*1000)
                v = st.number_input(f"Ventas {label_mes}", value=val_v, key=f"v_hist_{i}")
                historial_ventas.append(v)
            
            with col_h2:
                # Calculo simple por defecto para EBITDA
                val_e = (ventas_actual - costo_ventas - gastos_operativos) if i == num_meses-1 else (v * 0.15)
                e = st.number_input(f"EBITDA {label_mes}", value=val_e, key=f"e_hist_{i}")
                historial_ebitda.append(e)

# --- CÁLCULOS ESTRATÉGICOS (MES ACTUAL) ---
utilidad_bruta = ventas_actual - costo_ventas
ebitda_actual = utilidad_bruta - gastos_operativos
margen_ebitda = (ebitda_actual / ventas_actual) * 100 if ventas_actual > 0 else 0
utilidad_neta = ebitda_actual - depreciacion - intereses - impuestos

# Liquidez
razon_circulante = activo_corriente / pasivo_corriente if pasivo_corriente > 0 else 0
# Ciclo de Caja (Simplificado a base 30 días)
ccc = ((cuentas_cobrar / ventas_actual) * 30) + ((inventario / costo_ventas) * 30) - ((cuentas_pagar / costo_ventas) * 30)

# Punto de Equilibrio
costos_fijos = gastos_operativos + intereses
margen_contribucion_pct = (utilidad_bruta / ventas_actual) if ventas_actual > 0 else 0
punto_equilibrio = costos_fijos / margen_contribucion_pct if margen_contribucion_pct > 0 else 0


# --- DASHBOARD VISUAL ---

tab1, tab2, tab3 = st.tabs(["📈 Tendencia & Potencia", "⚖️ Equilibrio", "💰 Liquidez"])

# MÓDULO 1: TENDENCIA & POTENCIA
with tab1:
    st.subheader(f"Análisis de Tendencia de {num_meses} Meses")
    
    # CREACIÓN DEL GRÁFICO DE TENDENCIA
    fig_trend = go.Figure()
    
    # Línea de Ventas
    fig_trend.add_trace(go.Scatter(x=meses_labels, y=historial_ventas, mode='lines+markers', name='Ventas', line=dict(color='#1e88e5', width=3)))
    # Línea de EBITDA (Barra o Área)
    fig_trend.add_trace(go.Scatter(x=meses_labels, y=historial_ebitda, mode='lines+markers', name='EBITDA', line=dict(color='#43a047', width=3), fill='tozeroy'))
    
    fig_trend.update_layout(title="Comportamiento: Ventas vs. Rentabilidad Real", height=400, hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

    # ANÁLISIS DE LA TENDENCIA (LÓGICA AUTOMÁTICA)
    crecimiento_ventas = ((historial_ventas[-1] - historial_ventas[0]) / historial_ventas[0]) * 100
    crecimiento_ebitda = ((historial_ebitda[-1] - historial_ebitda[0]) / historial_ebitda[0]) * 100
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric("Crecimiento Ventas (Periodo)", f"{crecimiento_ventas:.1f}%", delta_color="normal")
    with col_t2:
        st.metric("Crecimiento EBITDA (Periodo)", f"{crecimiento_ebitda:.1f}%", delta_color="normal")

    st.markdown("---")
    st.write("#### 🧠 Diagnóstico de Tendencia:")
    
    if crecimiento_ventas > 0 and crecimiento_ebitda < 0:
        st.markdown("""<div class="alert-box alert-danger">
        🚨 <strong>CRECIMIENTO IMPRODUCTIVO:</strong> Tus ventas suben, pero tu EBITDA baja. 
        Estás "comprando ventas" (bajando precios o gastando mucho en marketing) pero destruyendo valor.</div>""", unsafe_allow_html=True)
    elif crecimiento_ventas > crecimiento_ebitda:
        st.markdown("""<div class="alert-box alert-warning">
        ⚠️ <strong>PÉRDIDA DE EFICIENCIA:</strong> El negocio crece, pero los gastos crecen más rápido que las ventas. 
        Revisa tu estructura de costos fijos.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="alert-box alert-success">
        ✅ <strong>ESCALAMIENTO SANO:</strong> Tu EBITDA crece al ritmo (o mejor) que tus ventas. Estás optimizando.</div>""", unsafe_allow_html=True)

# MÓDULO 2: PUNTO DE EQUILIBRIO
with tab2:
    st.subheader("Mapa de Supervivencia (Mes Actual)")
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.metric("Ventas Actuales", f"${ventas_actual:,.0f}")
        st.metric("Punto de Equilibrio", f"${punto_equilibrio:,.0f}")
        
        if ventas_actual > punto_equilibrio:
            st.success("Zona de Ganancia")
        else:
            st.error("Zona de Pérdida")
        
    with c2:
        fig_eq = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = ventas_actual,
            title = {'text': "Ventas vs Meta Mínima"},
            gauge = {
                'axis': {'range': [None, punto_equilibrio * 1.5]},
                'bar': {'color': "darkblue"},
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
            st.error("PELIGRO: No puedes cubrir deudas a corto plazo.")
    with col_b:
        st.metric("Ciclo de Caja (CCC)", f"{ccc:.0f} días")

# --- GENERADOR DE REPORTE PDF V3 ---
def create_pdf_v3():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SG CONSULTING | Reporte de Tendencias", ln=True, align="C")
    pdf.ln(5)
    
    # Sección Tendencia
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"1. ANALISIS DE TENDENCIA ({num_meses} Meses)", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    
    pdf.cell(0, 8, f"Crecimiento Ventas: {crecimiento_ventas:.1f}%", ln=True)
    pdf.cell(0, 8, f"Crecimiento EBITDA: {crecimiento_ebitda:.1f}%", ln=True)
    
    if crecimiento_ventas > crecimiento_ebitda:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 8, "ALERTA: Las ventas crecen mas rapido que la utilidad. El negocio pierde eficiencia.")
    else:
        pdf.set_text_color(0, 100, 0)
        pdf.multi_cell(0, 8, "TENDENCIA POSITIVA: El negocio escala saludablemente.")
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Sección Actual
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. ESTADO ACTUAL (Cierre de Mes)", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Ventas Actuales: ${ventas_actual:,.2f}", ln=True)
    pdf.cell(0, 8, f"EBITDA Actual: ${ebitda_actual:,.2f} ({margen_ebitda:.1f}%)", ln=True)
    pdf.cell(0, 8, f"Punto de Equilibrio: ${punto_equilibrio:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Generado por SG Rescue App - Uso Confidencial", ln=True, align="C")
    
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar Reporte de Tendencias"):
    pdf_bytes = create_pdf_v3()
    st.sidebar.download_button("💾 Guardar PDF", data=pdf_bytes, file_name="Reporte_Tendencias_SG.pdf", mime="application/pdf")
