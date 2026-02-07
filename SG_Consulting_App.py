import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Rescue | Diagnóstico Financiero", layout="wide")

# --- ESTILOS VISUALES (BRANDING SG CONSULTING) ---
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    .alert-danger { background-color: #ffebee; padding: 10px; border-radius: 5px; color: #c62828; border: 1px solid #c62828;}
    .alert-warning { background-color: #fff3e0; padding: 10px; border-radius: 5px; color: #ef6c00; border: 1px solid #ef6c00;}
    .alert-success { background-color: #e8f5e9; padding: 10px; border-radius: 5px; color: #2e7d32; border: 1px solid #2e7d32;}
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO Y ENCABEZADO ---
st.title("🛡️ SG Consulting: Sistema de Rescate Financiero")
st.markdown("### Módulo 1: La Cascada de Potencia (Diagnóstico de EBITDA)")
st.markdown("---")

# --- BARRA LATERAL (INPUTS DE SORAYA) ---
with st.sidebar:
    st.header("1. Ingresa los Datos Financieros")
    st.info("Introduce los valores anuales o mensuales del Estado de Resultados.")
    
    # Entradas de datos
    ventas = st.number_input("Ventas Totales ($)", min_value=0.0, value=500000.0, step=1000.0)
    costo_ventas = st.number_input("Costo de Ventas / Mercancía ($)", min_value=0.0, value=300000.0, step=1000.0)
    gastos_operativos = st.number_input("Gastos Operativos (OPEX) ($)", min_value=0.0, value=130000.0, step=1000.0, help="Incluye nómina, alquiler, luz, marketing.")
    depreciacion = st.number_input("Depreciaciones y Amortizaciones ($)", min_value=0.0, value=15000.0, step=500.0)
    intereses = st.number_input("Gastos Financieros / Intereses ($)", min_value=0.0, value=5000.0, step=500.0)
    impuestos = st.number_input("Impuestos ($)", min_value=0.0, value=12500.0, step=500.0)

# --- LÓGICA DE CÁLCULO (ALGORITMO SG CONSULTING) ---

# 1. Utilidad Bruta [cite: 351]
utilidad_bruta = ventas - costo_ventas
margen_bruto = (utilidad_bruta / ventas) * 100 if ventas > 0 else 0

# 2. EBITDA (La Verdad Operativa) [cite: 354, 457]
ebitda = utilidad_bruta - gastos_operativos
margen_ebitda = (ebitda / ventas) * 100 if ventas > 0 else 0

# 3. EBIT (Potencia de Activos) [cite: 304, 463]
ebit = ebitda - depreciacion

# 4. Utilidad Neta (Potencia Patrimonial) [cite: 316, 467]
utilidad_neta = ebit - intereses - impuestos
margen_neto = (utilidad_neta / ventas) * 100 if ventas > 0 else 0

# --- VISUALIZACIÓN PRINCIPAL ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 La Cascada de Rentabilidad")
    
    # Gráfico de Cascada (Waterfall) - Clave para entender la "dilución" del dinero
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "subtotal", "relative", "subtotal", "relative", "relative", "relative", "total"],
        x = ["Ventas", "Costo Ventas", "Utilidad Bruta", "Gastos Op (OPEX)", "EBITDA", "Depreciación", "EBIT", "Intereses e Imp.", "Utilidad Neta"],
        textposition = "outside",
        text = [f"${x/1000:.1f}k" for x in [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -depreciacion, ebit, -(intereses+impuestos), utilidad_neta]],
        y = [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -depreciacion, ebit, -(intereses+impuestos), utilidad_neta],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#ef5350"}}, # Rojo para gastos
        increasing = {"marker":{"color":"#66bb6a"}}, # Verde para ingresos
        totals = {"marker":{"color":"#42a5f5"}}       # Azul para subtotales
    ))
    fig.update_layout(title = "De la Venta a la Utilidad (Flujo Visual)", showlegend = False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("KPIs Estratégicos")
    
    # Tarjeta EBITDA
    st.markdown(f"""
    <div class="metric-card">
        <h3>EBITDA (Caja Operativa)</h3>
        <h2 style="color: {'#2e7d32' if ebitda > 0 else '#c62828'}">${ebitda:,.2f}</h2>
        <p>Margen: {margen_ebitda:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Espaciador
    
    # Tarjeta Utilidad Neta
    st.metric(label="Utilidad Neta Final", value=f"${utilidad_neta:,.2f}", delta=f"{margen_neto:.1f}% Margen")
    st.metric(label="Punto de Equilibrio (Estimado)", value="Calculando en Módulo 2...")

# --- DIAGNÓSTICO INTELIGENTE (EL CEREBRO DE LA APP) ---
st.markdown("---")
st.header("🧠 Diagnóstico del Consultor (SG Consulting)")

# Lógica de Diagnóstico basada en Manual Maestro

# 1. Análisis de Potencia Comercial (Margen Bruto) [cite: 453]
with st.expander("1. Diagnóstico Comercial (Utilidad Bruta)", expanded=True):
    if margen_bruto < 30: # Umbral de ejemplo, ajustable por sector
        st.markdown(f'<div class="alert-warning">⚠️ <strong>Margen Bruto Bajo ({margen_bruto:.1f}%):</strong> El problema puede ser de PRECIOS (muy bajos) o de COMPRAS (proveedores caros). La administración no es la culpable aquí.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">✅ <strong>Potencia Comercial Sana:</strong> Tu producto tiene un buen margen ({margen_bruto:.1f}%) antes de gastos operativos.</div>', unsafe_allow_html=True)

# 2. Análisis de EBITDA (El Corazón) [cite: 356, 359, 459]
with st.expander("2. Diagnóstico Operativo (EBITDA)", expanded=True):
    if ebitda < 0:
        st.markdown('<div class="alert-danger">🚨 <strong>ALERTA ROJA (EBITDA NEGATIVO):</strong> El corazón del negocio no late. El modelo de negocio no funciona. Se requiere cirugía mayor inmediata (recorte de personal o cierre de líneas de negocio).</div>', unsafe_allow_html=True)
    elif margen_ebitda < 10:
        st.markdown(f'<div class="alert-warning">⚠️ <strong>Fragilidad Operativa ({margen_ebitda:.1f}%):</strong> La empresa genera caja pero es muy vulnerable. Cualquier caída en ventas te llevará a números rojos.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">✅ <strong>Motor Operativo Fuerte ({margen_ebitda:.1f}%):</strong> La empresa sabe hacer dinero. Si falta efectivo en el banco, el problema NO es operativo (revisar cobros o deudas).</div>', unsafe_allow_html=True)

# 3. Análisis Financiero y Legal [cite: 469, 528]
with st.expander("3. Diagnóstico Financiero y Legal", expanded=True):
    if ebitda > 0 and utilidad_neta < 0:
        st.markdown('<div class="alert-warning">⚖️ <strong>El Problema es la Deuda:</strong> Tu negocio operativo es bueno (EBITDA +), pero los intereses o impuestos se están comiendo toda la ganancia. <strong>Acción:</strong> Reestructuración de deuda urgente.</div>', unsafe_allow_html=True)
    
    # Advertencia de Responsabilidad Fiduciaria (Contexto Panamá)
    if utilidad_neta < 0:
         st.markdown("""
         <div class="alert-danger" style="margin-top: 10px;">
         <strong>⚖️ ADVERTENCIA LEGAL (RESPONSABILIDAD FIDUCIARIA):</strong> 
         La empresa está destruyendo valor patrimonial. Seguir endeudándose sin un plan de corrección puede acarrear responsabilidades legales para los administradores. Es vital detener la hemorragia hoy.
         </div>
         """, unsafe_allow_html=True)

# --- BOTÓN DE ACCIÓN ---
st.markdown("---")
st.button("📥 Generar Informe PDF para Cliente")