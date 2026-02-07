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
    .alert-box { padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid; }
    .alert-danger { background-color: #fdecea; color: #c62828; border-color: #c62828; }
    .alert-warning { background-color: #fff8e1; color: #ef6c00; border-color: #ef6c00; }
    .alert-success { background-color: #e8f5e9; color: #2e7d32; border-color: #2e7d32; }
    .level-header { font-size: 18px; font-weight: bold; color: #1565c0; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia** y **Línea de Supervivencia**")

# --- BARRA LATERAL: INPUT DE VARIABLES (COINCIDEN CON LA METODOLOGÍA) ---
with st.sidebar:
    st.header("1. Datos Financieros (Mes Actual)")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        st.info("Ingresa los datos para calcular los 4 Niveles de Potencia.")
        ventas_actual = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0)
        costo_ventas = st.number_input("Costo de Ventas (Variable)", value=30000.0, step=1000.0, help="Materia prima, mano de obra directa.")
        gastos_operativos = st.number_input("Gastos Operativos (Opex)", value=12000.0, step=500.0, help="Renta, nómina administrativa, luz, marketing.")
        depreciacion = st.number_input("Depreciaciones + Amortizaciones", value=2000.0, step=100.0, help="Desgaste de activos.")
        intereses = st.number_input("Intereses (Gastos Financieros)", value=1000.0, step=100.0)
        impuestos = st.number_input("Impuestos", value=1500.0, step=100.0)

    with st.expander("B. Balance General (Para Flujo de Caja)", expanded=False):
        activo_corriente = st.number_input("Activo Corriente", value=80000.0)
        pasivo_corriente = st.number_input("Pasivo Corriente", value=60000.0)
        inventario = st.number_input("Inventario ($)", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar ($)", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar ($)", value=10000.0)

# --- CÁLCULOS: LA CASCADA DE POTENCIA (4 NIVELES) ---

# NIVEL 1: Potencia Comercial
utilidad_bruta = ventas_actual - costo_ventas
margen_bruto = (utilidad_bruta / ventas_actual) * 100 if ventas_actual > 0 else 0

# NIVEL 2: Potencia Operativa (El Corazón)
ebitda = utilidad_bruta - gastos_operativos
margen_ebitda = (ebitda / ventas_actual) * 100 if ventas_actual > 0 else 0

# NIVEL 3: Potencia de Activos (EBIT) - ¡AGREGADO!
ebit = ebitda - depreciacion
margen_ebit = (ebit / ventas_actual) * 100 if ventas_actual > 0 else 0

# NIVEL 4: Potencia Patrimonial
utilidad_neta = ebit - intereses - impuestos
margen_neto = (utilidad_neta / ventas_actual) * 100 if ventas_actual > 0 else 0

# --- CÁLCULOS: SUPERVIVENCIA Y OXÍGENO ---

# Punto de Equilibrio (Módulo 2)
# Costos Fijos Totales = Gastos Operativos (Planilla, Alquiler) + Intereses (Seguros, Servicios)
# Nota: Según el texto, Costos Fijos incluye Planilla base, Alquiler. Asumimos Opex + Intereses.
costos_fijos_totales = gastos_operativos + intereses 
margen_contribucion_pct = (utilidad_bruta / ventas_actual) if ventas_actual > 0 else 0
punto_equilibrio = costos_fijos_totales / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad = ventas_actual - punto_equilibrio

# Ciclo de Caja (Módulo 3)
dias_calle = (cuentas_cobrar / ventas_actual) * 30 if ventas_actual > 0 else 0
dias_inventario = (inventario / costo_ventas) * 30 if costo_ventas > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas) * 30 if costo_ventas > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

# --- DASHBOARD VISUAL ---

tab1, tab2, tab3 = st.tabs(["💎 La Cascada de Potencia", "⚖️ Línea de Supervivencia", "🫁 El Oxígeno (Caja)"])

# MÓDULO 1: CASCADA DE POTENCIA
with tab1:
    st.subheader("Diagnóstico de los 4 Niveles de Potencia")
    
    col_main, col_chart = st.columns([1.5, 1])
    
    with col_main:
        # NIVEL 1
        st.markdown('<p class="level-header">Nivel 1: Potencia Comercial (Utilidad Bruta)</p>', unsafe_allow_html=True)
        st.write(f"**${utilidad_bruta:,.2f}** (Margen: {margen_bruto:.1f}%)")
        if margen_bruto < 30: # Umbral de ejemplo
            st.markdown("""<div class="alert-box alert-warning">
            ⚠️ <strong>SÍNTOMA:</strong> Margen bajo. No culpes a la administración. 
            El problema es que compras caro o vendes barato.<br>
            👉 <strong>ACCIÓN:</strong> Renegociar proveedores o subir precios.</div>""", unsafe_allow_html=True)
        else:
            st.success("✅ Modelo de precios y proveedores saludable.")

        # NIVEL 2
        st.markdown('<p class="level-header">Nivel 2: Potencia Operativa (EBITDA) - El Corazón</p>', unsafe_allow_html=True)
        st.write(f"**${ebitda:,.2f}** (Margen: {margen_ebitda:.1f}%)")
        if ebitda < 0:
            st.markdown("""<div class="alert-box alert-danger">
            🚨 <strong>SÍNTOMA:</strong> EBITDA Negativo. El negocio está enfermo de muerte.<br>
            👉 <strong>ACCIÓN:</strong> Necesita cirugía mayor (recortes de estructura/personal) inmediato.</div>""", unsafe_allow_html=True)
        else:
             st.success("✅ El corazón del negocio late fuerte. La operación genera dinero puro.")

        # NIVEL 3
        st.markdown('<p class="level-header">Nivel 3: Potencia de Activos (EBIT)</p>', unsafe_allow_html=True)
        st.write(f"**${ebit:,.2f}** (Margen: {margen_ebit:.1f}%)")
        if ebitda > 0 and ebit < (ebitda * 0.2): # Si el EBIT es muy bajo comparado al EBITDA
             st.markdown("""<div class="alert-box alert-warning">
            ⚠️ <strong>SÍNTOMA:</strong> EBITDA alto pero EBIT bajo.<br>
            👉 <strong>DIAGNÓSTICO:</strong> Tienes activos muy costosos o viejos (Depreciación alta) que se comen la ganancia operativa.</div>""", unsafe_allow_html=True)

        # NIVEL 4
        st.markdown('<p class="level-header">Nivel 4: Potencia Patrimonial (Utilidad Neta)</p>', unsafe_allow_html=True)
        st.write(f"**${utilidad_neta:,.2f}** (Margen: {margen_neto:.1f}%)")
        if ebit > 0 and utilidad_neta < 0:
             st.markdown("""<div class="alert-box alert-danger">
            🚨 <strong>SÍNTOMA:</strong> EBIT bueno pero Neta roja.<br>
            👉 <strong>DIAGNÓSTICO:</strong> El problema es Financiero (mucha deuda).<br>
            👉 <strong>ACCIÓN:</strong> Reestructuración de deuda (ir al banco con los números en mano).</div>""", unsafe_allow_html=True)
        elif utilidad_neta > 0:
             st.success("✅ Potencia Patrimonial positiva. El dueño gana dinero.")

    with col_chart:
        # Gráfico Cascada EXACTO con los 4 niveles
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "subtotal", "relative", "subtotal", "relative", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Ut. Bruta", "Gastos Op.", "EBITDA", "Depreciación", "EBIT", "Intereses", "Impuestos", "Ut. Neta"],
            y = [ventas_actual, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -depreciacion, ebit, -intereses, -impuestos, utilidad_neta],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#1565c0"}}
        ))
        fig_waterfall.update_layout(title="Cascada de Potencia (Visual)", showlegend=False, height=600)
        st.plotly_chart(fig_waterfall, use_container_width=True)

# MÓDULO 2: SUPERVIVENCIA
with tab2:
    st.subheader("La Línea de Supervivencia")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Punto de Equilibrio ($)", f"${punto_equilibrio:,.2f}")
        st.metric("Ventas Actuales", f"${ventas_actual:,.2f}")
        
        # Margen de Seguridad
        if margen_seguridad > 0:
            st.success(f"✅ Margen de Seguridad: ${margen_seguridad:,.2f}")
        else:
            st.error(f"🚨 Faltan ${abs(margen_seguridad):,.2f} para no perder dinero.")
            
    with col2:
        # Diagnóstico de Estratega
        porcentaje_seguridad = (margen_seguridad / ventas_actual) * 100
        st.write("#### 🧠 Interpretación de Estratega:")
        
        if porcentaje_seguridad < 10:
             st.markdown("""<div class="alert-box alert-danger">
            ⚠️ <strong>ZONA DE PELIGRO:</strong><br>
            La brecha es pequeña (menor al 10%).<br>
            <strong>Cualquier caída del mercado te quiebra.</strong></div>""", unsafe_allow_html=True)
        else:
             st.markdown("""<div class="alert-box alert-success">
            ✅ <strong>ZONA SEGURA:</strong><br>
            Tienes colchón para resistir caídas de ventas.</div>""", unsafe_allow_html=True)

# MÓDULO 3: OXÍGENO
with tab3:
    st.subheader("El Ciclo de Conversión de Efectivo (CCC)")
    st.write("Cómo desbloquear el dinero atrapado.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("1. Días Calle (DSO)", f"{dias_calle:.0f} días")
    c2.metric("2. Días Inventario (DIO)", f"{dias_inventario:.0f} días")
    c3.metric("3. Días Proveedor (DPO)", f"{dias_proveedor:.0f} días")
    
    st.metric("Ciclo de Caja (CCC)", f"{ccc:.0f} días", delta_color="inverse")
    
    st.markdown("---")
    st.write("#### 🔧 Las 3 Palancas de Rescate:")
    
    # Palanca 1
    if dias_calle > 60:
        st.warning(f"⚠️ **Problema (DSO):** Clientes pagan a {dias_calle:.0f} días.")
        st.info("👉 **Solución:** Descuento por pronto pago (2% a 10 días) o Factoring.")
    else:
        st.success("✅ Cobranza eficiente.")
        
    # Palanca 2
    if dias_inventario > 60:
        st.warning(f"⚠️ **Problema (DIO):** Bodega llena ({dias_inventario:.0f} días). Producto no rota.")
        st.info("👉 **Solución:** Remate de inventario muerto para hacer caja inmediata.")
    else:
        st.success("✅ Inventario rota bien.")
        
    # Palanca 3
    if dias_proveedor < 30:
        st.warning(f"⚠️ **Problema (DPO):** Pagas a {dias_proveedor:.0f} días (muy rápido).")
        st.info("👉 **Solución:** Renegociar plazos más largos usando tu volumen de compra.")
    else:
        st.success("✅ Buen apalancamiento con proveedores.")

# --- GENERADOR PDF (ACTUALIZADO CON 4 NIVELES) ---
def create_pdf_strategic():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SG CONSULTING | Diagnóstico de Potencia", ln=True, align="C")
    pdf.ln(5)
    
    # Sección Cascada
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. LA CASCADA DE POTENCIA (4 NIVELES)", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    
    pdf.cell(0, 8, f"Nivel 1 (Comercial - Ut. Bruta): ${utilidad_bruta:,.2f}", ln=True)
    pdf.cell(0, 8, f"Nivel 2 (Operativa - EBITDA): ${ebitda:,.2f}", ln=True)
    pdf.cell(0, 8, f"Nivel 3 (Activos - EBIT): ${ebit:,.2f}", ln=True)
    pdf.cell(0, 8, f"Nivel 4 (Patrimonial - Ut. Neta): ${utilidad_neta:,.2f}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "DIAGNOSTICO AUTOMATICO:", ln=True)
    pdf.set_font("Arial", "", 10)
    
    if ebitda < 0:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 6, "ALERTA: EBITDA Negativo. Negocio enfermo de muerte. Requiere recortes inmediatos.")
    elif ebitda > 0 and utilidad_neta < 0:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 6, "ALERTA: Problema Financiero. EBIT positivo pero Neta negativa. Requiere reestructurar deuda.")
    else:
        pdf.set_text_color(0, 100, 0)
        pdf.multi_cell(0, 6, "ESTADO: Negocio saludable en sus niveles de potencia.")
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Sección Supervivencia
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. LINEA DE SUPERVIVENCIA", ln=True, fill=False)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Punto de Equilibrio: ${punto_equilibrio:,.2f}", ln=True)
    pdf.cell(0, 8, f"Margen de Seguridad: ${margen_seguridad:,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Generado por SG Rescue App", ln=True, align="C")
    
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar Diagnóstico Maestro"):
    pdf_bytes = create_pdf_strategic()
    st.sidebar.download_button("💾 Guardar PDF", data=pdf_bytes, file_name="Diagnostico_Potencia_SG.pdf", mime="application/pdf")
