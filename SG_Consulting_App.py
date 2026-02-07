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
    .big-font { font-size:20px !important; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .alert-box { padding: 15px; border-radius: 5px; margin-bottom: 10px; border: 1px solid transparent; }
    .alert-danger { background-color: #fdecea; color: #c62828; border-color: #c62828; }
    .alert-warning { background-color: #fff8e1; color: #ef6c00; border-color: #ef6c00; }
    .alert-success { background-color: #e8f5e9; color: #2e7d32; border-color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico Empresarial de Alto Nivel: **Rentabilidad, Liquidez y Eficiencia**")

# --- BARRA LATERAL: INPUT DE DATOS (ESTRUCTURADO) ---
with st.sidebar:
    st.header("1. Datos del Mes Actual")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        ventas = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0)
        # Separación estricta de costos vs gastos
        costo_ventas = st.number_input("Costo de Ventas (Variables)", value=30000.0, step=1000.0, help="Solo lo que se mueve con la venta (insumos, comisiones).")
        gastos_operativos = st.number_input("Gastos Operativos (Fijos)", value=15000.0, step=500.0, help="Renta, sueldos fijos, software.")
        depreciacion = st.number_input("Depreciaciones", value=1500.0)
        intereses = st.number_input("Gastos Financieros", value=500.0)
        impuestos = st.number_input("Impuestos", value=900.0)

    with st.expander("B. Balance General (Liquidez)", expanded=False):
        activo_corriente = st.number_input("Activo Corriente", value=80000.0, help="Efectivo + Cuentas por Cobrar + Inventario")
        pasivo_corriente = st.number_input("Pasivo Corriente", value=60000.0, help="Deudas a pagar en menos de un año")
        inventario = st.number_input("Inventario", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar", value=10000.0)

    st.header("2. Benchmarking (Comparativa)")
    with st.expander("C. Mes Anterior (MoM)", expanded=False):
        ventas_anterior = st.number_input("Ventas Mes Pasado", value=45000.0)
        ebitda_anterior = st.number_input("EBITDA Mes Pasado", value=4000.0)

# --- CÁLCULOS ESTRATÉGICOS ---

# 1. Rentabilidad
utilidad_bruta = ventas - costo_ventas
margen_bruto = (utilidad_bruta / ventas) * 100 if ventas > 0 else 0

ebitda = utilidad_bruta - gastos_operativos
margen_ebitda = (ebitda / ventas) * 100 if ventas > 0 else 0

utilidad_neta = ebitda - depreciacion - intereses - impuestos
margen_neto = (utilidad_neta / ventas) * 100 if ventas > 0 else 0

# 2. Benchmarking (Deltas)
delta_ventas = ventas - ventas_anterior
delta_ebitda = ebitda - ebitda_anterior

# 3. Punto de Equilibrio
costos_fijos = gastos_operativos + intereses + depreciacion
margen_contribucion_pct = (utilidad_bruta / ventas) if ventas > 0 else 0
punto_equilibrio = costos_fijos / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad = ((ventas - punto_equilibrio) / ventas) * 100 if ventas > 0 else 0

# 4. Liquidez (Cash is King)
razon_circulante = activo_corriente / pasivo_corriente if pasivo_corriente > 0 else 0
# Ciclo de Caja
dias_calle = (cuentas_cobrar / ventas) * 30 if ventas > 0 else 0 # Base mensual
dias_inventario = (inventario / costo_ventas) * 30 if costo_ventas > 0 else 0
dias_pagar = (cuentas_pagar / costo_ventas) * 30 if costo_ventas > 0 else 0
ccc = dias_calle + dias_inventario - dias_pagar

# --- DASHBOARD VISUAL ---

tab1, tab2, tab3 = st.tabs(["📊 Potencia & Benchmarking", "⚖️ Equilibrio Maestro", "💰 Liquidez (Cash is King)"])

# MÓDULO 1: POTENCIA & COMPARATIVA
with tab1:
    st.subheader("Análisis de Eficiencia Operativa (MoM)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ventas Totales", f"${ventas:,.0f}", f"{delta_ventas:,.0f} vs Mes Pasado")
    with col2:
        st.metric("EBITDA (Operación)", f"${ebitda:,.0f}", f"{delta_ebitda:,.0f} vs Mes Pasado")
    with col3:
        st.metric("Margen EBITDA %", f"{margen_ebitda:.1f}%", help="¿Cuánto te queda de cada dólar operativo?")

    st.markdown("---")
    
    # LÓGICA DE DIAGNÓSTICO (Tus reglas de experto)
    st.write("#### 🧠 Diagnóstico del Consultor:")
    
    # Regla 1: Utilidad Bruta
    if margen_bruto < 30: # Umbral ejemplo
        st.markdown(f"""<div class="alert-box alert-warning">
        ⚠️ <strong>Margen Bruto Bajo ({margen_bruto:.1f}%):</strong> Tu problema es de <strong>PRECIO</strong> o <strong>COSTO</strong>. 
        Estás comprando caro o vendiendo muy barato. Revisa tu lista de precios o proveedores.</div>""", unsafe_allow_html=True)
    
    # Regla 2: EBITDA Negativo o Bajo
    if ebitda < 0:
        st.markdown(f"""<div class="alert-box alert-danger">
        🚨 <strong>EBITDA NEGATIVO:</strong> Tu modelo operativo es ineficiente. 
        Tienes demasiada estructura (gastos fijos) para el volumen de ventas actual. ¡Corta grasa ya!</div>""", unsafe_allow_html=True)
    elif delta_ventas > 0 and delta_ebitda < 0:
        st.markdown(f"""<div class="alert-box alert-warning">
        📉 <strong>ALERTA DE EFICIENCIA:</strong> Cuidado. Vendiste más que el mes pasado (${delta_ventas:,.0f}), 
        pero ganaste menos EBITDA (${delta_ebitda:,.0f}). Te estás volviendo ineficiente al crecer.</div>""", unsafe_allow_html=True)

    # Regla 3: EBITDA vs Neta
    if ebitda > 0 and utilidad_neta <= 0:
        st.markdown(f"""<div class="alert-box alert-danger">
        💸 <strong>DRENAJE FINANCIERO:</strong> Tu operación es buena (EBITDA +), pero tus <strong>DEUDAS</strong> (Intereses) 
        o tu carga fiscal te están comiendo el esfuerzo. Reestructura pasivos.</div>""", unsafe_allow_html=True)

    if ebitda > 0 and utilidad_neta > 0 and margen_bruto > 30:
        st.markdown(f"""<div class="alert-box alert-success">
        ✅ <strong>SALUDABLE:</strong> El negocio opera con eficiencia. Enfócate en escalar ventas.</div>""", unsafe_allow_html=True)

# MÓDULO 2: PUNTO DE EQUILIBRIO
with tab2:
    st.subheader("Mapa de Supervivencia")
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.metric("Meta Mínima de Ventas", f"${punto_equilibrio:,.0f}")
        st.metric("Ventas Actuales", f"${ventas:,.0f}")
        
        pct_cumplimiento = (ventas / punto_equilibrio) * 100
        st.write(f"Estás al **{pct_cumplimiento:.1f}%** de tu meta mínima.")
        
    with c2:
        # Gráfico de termómetro
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ventas,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Ventas vs Equilibrio"},
            delta = {'reference': punto_equilibrio, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, punto_equilibrio * 1.5]},
                'bar': {'color': "darkblue"},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': punto_equilibrio
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"💡 **Estrategia:** Necesitas vender **${punto_equilibrio:,.0f}** solo para no perder dinero (pagar costos fijos y variables). Todo lo que vendas arriba de esto es ganancia.")

# MÓDULO 3: LIQUIDEZ (CASH IS KING)
with tab3:
    st.subheader("Indicadores de Solvencia y Caja")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 1. Razón Circulante (Solvencia)")
        st.metric("Ratio de Liquidez", f"{razon_circulante:.2f}")
        
        if razon_circulante < 1:
            st.markdown(f"""<div class="alert-box alert-danger">
            🛑 <strong>PELIGRO DE QUIEBRA TÉCNICA:</strong> Tienes ${razon_circulante:.2f} por cada $1.00 de deuda. 
            No tienes con qué pagar tus obligaciones a corto plazo. ¡Inyecta capital o vende activos!</div>""", unsafe_allow_html=True)
        elif razon_circulante < 1.5:
             st.markdown(f"""<div class="alert-box alert-warning">
            ⚠️ <strong>LIQUIDEZ AJUSTADA:</strong> Tienes capacidad de pago, pero cualquier retraso de clientes te pone en problemas.</div>""", unsafe_allow_html=True)
        else:
             st.markdown(f"""<div class="alert-box alert-success">
            ✅ <strong>SOLVENCIA SÓLIDA:</strong> Tienes capacidad de sobra para pagar deudas.</div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("#### 2. Ciclo de Caja (Eficiencia)")
        st.metric("Ciclo de Conversión (CCC)", f"{ccc:.0f} días")
        st.caption("Días que financias tu operación con tu propio dinero.")
        
        if ccc > 60:
             st.warning("Tu dinero pasa demasiado tiempo atrapado en la calle o bodega.")
        else:
             st.success("Tu ciclo de efectivo es eficiente.")

# --- GENERADOR DE REPORTE PDF V2 ---
def create_pdf_v2():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SG CONSULTING | Informe Estrategico", ln=True, align="C")
    pdf.ln(10)
    
    # Resumen
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. DIAGNOSTICO OPERATIVO (P&L)", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Ventas: ${ventas:,.2f} (Delta vs Mes Pasado: ${delta_ventas:,.2f})", ln=True)
    pdf.cell(0, 8, f"EBITDA: ${ebitda:,.2f} (Margen: {margen_ebitda:.1f}%)", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. DIAGNOSTICO DE LIQUIDEZ", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Razon Circulante: {razon_circulante:.2f}", ln=True)
    pdf.cell(0, 8, f"Punto de Equilibrio: ${punto_equilibrio:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, "Este reporte es una herramienta de toma de decisiones. Si la Razon Circulante es menor a 1, la empresa esta en riesgo inminente de impago.")
    
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar Reporte Estratégico"):
    pdf_bytes = create_pdf_v2()
    st.sidebar.download_button("💾 Guardar PDF", data=pdf_bytes, file_name="Reporte_Estrategico_SG.pdf", mime="application/pdf")
