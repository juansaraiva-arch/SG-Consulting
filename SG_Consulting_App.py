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
    .veredicto { font-style: italic; font-weight: bold; color: #555; padding: 10px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #333; }
    .level-header { font-size: 18px; font-weight: bold; color: #1565c0; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Simulación**")

# --- BARRA LATERAL: INPUT DE VARIABLES ---
with st.sidebar:
    st.header("1. Datos Financieros (Mes Actual)")
    
    with st.expander("A. Estado de Resultados (Desglosado)", expanded=True):
        st.info("Ingresa los datos para calcular los Niveles de Potencia y Eficiencia.")
        ventas_actual = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0)
        costo_ventas = st.number_input("Costo de Ventas (Variable)", value=30000.0, step=1000.0, help="Materia prima, comisiones, costo directo.")
        
        st.markdown("---")
        st.markdown("**Desglose de Gastos Operativos (OPEX):**")
        # DESGLOSE CLAVE PARA LOS RATIOS
        gasto_alquiler = st.number_input("1. Alquiler + Mantenimiento (CAM)", value=5000.0, step=100.0, help="Renta del local y cuotas de mantenimiento.")
        gasto_planilla = st.number_input("2. Planilla / Nómina Total", value=8000.0, step=500.0, help="Sueldos administrativos y operativos fijos.")
        gasto_otros = st.number_input("3. Otros Gastos Operativos", value=2000.0, step=100.0, help="Luz, agua, internet, marketing, etc.")
        
        # CÁLCULO AUTO DE OPEX TOTAL
        gastos_operativos = gasto_alquiler + gasto_planilla + gasto_otros
        st.write(f"**Total OPEX:** ${gastos_operativos:,.2f}")
        st.markdown("---")

        depreciacion = st.number_input("Depreciaciones + Amortizaciones", value=2000.0, step=100.0)
        intereses = st.number_input("Intereses (Gastos Financieros)", value=1000.0, step=100.0)
        impuestos = st.number_input("Impuestos", value=1500.0, step=100.0)

    with st.expander("B. Balance General (Para Flujo de Caja)", expanded=False):
        inventario = st.number_input("Inventario ($)", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar ($)", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar ($)", value=10000.0)

# --- CÁLCULOS PRINCIPALES ---

# NIVEL 1: Potencia Comercial
utilidad_bruta = ventas_actual - costo_ventas
margen_bruto = (utilidad_bruta / ventas_actual) * 100 if ventas_actual > 0 else 0

# NIVEL 2: Potencia Operativa
ebitda = utilidad_bruta - gastos_operativos
margen_ebitda = (ebitda / ventas_actual) * 100 if ventas_actual > 0 else 0

# NIVEL 3 & 4
ebit = ebitda - depreciacion
margen_ebit = (ebit / ventas_actual) * 100 if ventas_actual > 0 else 0
utilidad_neta = ebit - intereses - impuestos
margen_neto = (utilidad_neta / ventas_actual) * 100 if ventas_actual > 0 else 0

# CÁLCULOS DE RATIOS DE EFICIENCIA (NUEVO)
# A. Ratio Alquiler = Alquiler / Ventas
ratio_alquiler = (gasto_alquiler / ventas_actual) * 100 if ventas_actual > 0 else 0

# B. Ratio Planilla = Planilla / Utilidad Bruta (¡OJO: Sobre Utilidad Bruta, no Ventas!)
ratio_planilla = (gasto_planilla / utilidad_bruta) * 100 if utilidad_bruta > 0 else 0

# Puntos de Equilibrio y Caja
costos_fijos_totales = gastos_operativos + intereses 
margen_contribucion_pct = (utilidad_bruta / ventas_actual) if ventas_actual > 0 else 0
punto_equilibrio = costos_fijos_totales / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad = ventas_actual - punto_equilibrio

dias_calle = (cuentas_cobrar / ventas_actual) * 30 if ventas_actual > 0 else 0
dias_inventario = (inventario / costo_ventas) * 30 if costo_ventas > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas) * 30 if costo_ventas > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

# --- DASHBOARD VISUAL ---

tab1, tab2, tab3, tab4 = st.tabs(["💎 Cascada de Potencia", "🚦 Semáforo de Eficiencia", "⚖️ Supervivencia", "🫁 Oxígeno (Caja)"])

# MÓDULO 1: CASCADA DE POTENCIA
with tab1:
    st.subheader("Diagnóstico de los 4 Niveles de Potencia")
    col_main, col_chart = st.columns([1.5, 1])
    
    with col_main:
        # NIVEL 1
        st.markdown(f'<p class="level-header">1. Potencia Comercial: ${utilidad_bruta:,.2f} ({margen_bruto:.1f}%)</p>', unsafe_allow_html=True)
        if margen_bruto < 30: st.warning("⚠️ Margen bajo. Revisa precios o proveedores.")
        else: st.success("✅ Modelo de precios saludable.")

        # NIVEL 2
        st.markdown(f'<p class="level-header">2. Potencia Operativa (EBITDA): ${ebitda:,.2f} ({margen_ebitda:.1f}%)</p>', unsafe_allow_html=True)
        if ebitda < 0: st.error("🚨 EBITDA NEGATIVO. El negocio quema efectivo.")
        else: st.success("✅ Corazón operativo fuerte.")

        # NIVEL 3
        st.markdown(f'<p class="level-header">3. Potencia Activos (EBIT): ${ebit:,.2f}</p>', unsafe_allow_html=True)
        
        # NIVEL 4
        st.markdown(f'<p class="level-header">4. Potencia Patrimonial (Neta): ${utilidad_neta:,.2f}</p>', unsafe_allow_html=True)
        if utilidad_neta < 0: st.error("🚨 PÉRDIDA NETA. Revisa estructura financiera.")

    with col_chart:
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "relative", "relative", "subtotal", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Ut. Bruta", "Alquiler", "Planilla", "Otros Gastos", "EBITDA", "Otros (Dep+Int+Imp)", "Ut. Neta"],
            y = [ventas_actual, -costo_ventas, utilidad_bruta, -gasto_alquiler, -gasto_planilla, -gasto_otros, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#1565c0"}}
        ))
        fig_waterfall.update_layout(title="Cascada Detallada", showlegend=False, height=500)
        st.plotly_chart(fig_waterfall, use_container_width=True)

# MÓDULO 4: SEMÁFORO DE EFICIENCIA & SIMULADOR (NUEVO)
with tab2:
    st.subheader("🚦 Semáforo de Eficiencia y Veredictos")
    st.markdown("Análisis de la estructura de costos fijos claves: **Alquiler** y **Talento**.")

    col_renta, col_nomina = st.columns(2)

    # --- INDICADOR DE ALQUILER ---
    with col_renta:
        st.markdown("### 🏢 Ratio de Alquiler")
        st.write("(Alquiler / Ventas)")
        
        # Definir color y mensaje
        color_renta = "green"
        mensaje_renta = "✅ Estructura Óptima. Tu local es un activo productivo."
        if ratio_alquiler >= 10 and ratio_alquiler <= 15:
            color_renta = "orange"
            mensaje_renta = "⚠️ Estructura Pesada. Zona de vigilancia. Revisa si la ubicación trae suficientes clientes."
        elif ratio_alquiler > 15:
            color_renta = "red"
            mensaje_renta = "🚨 ALERTA CRÍTICA. El local está consumiendo tu utilidad. Es un ancla, no un activo."

        fig_gauge_renta = go.Figure(go.Indicator(
            mode = "gauge+number", value = ratio_alquiler,
            title = {'text': "Esfuerzo Inmobiliario (%)"},
            gauge = {
                'axis': {'range': [None, 30]},
                'bar': {'color': color_renta},
                'steps': [
                    {'range': [0, 10], 'color': "#e8f5e9"},
                    {'range': [10, 15], 'color': "#fff3e0"},
                    {'range': [15, 30], 'color': "#ffebee"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 15}
            }
        ))
        fig_gauge_renta.update_layout(height=250)
        st.plotly_chart(fig_gauge_renta, use_container_width=True)
        
        st.markdown(f'<div class="veredicto">👩‍💼 Veredicto Estratega:<br>{mensaje_renta}</div>', unsafe_allow_html=True)

    # --- INDICADOR DE PLANILLA ---
    with col_nomina:
        st.markdown("### 👥 Eficiencia de Planilla")
        st.write("(Planilla / Utilidad Bruta)")
        
        color_nomina = "green"
        mensaje_nomina = "✅ Personal Altamente Productivo. Tu equipo se paga solo."
        if ratio_planilla >= 30 and ratio_planilla <= 40:
            color_nomina = "orange"
            mensaje_nomina = "⚠️ Zona de Vigilancia. Evalúa procesos y automatización."
        elif ratio_planilla > 40:
            color_nomina = "red"
            mensaje_nomina = "🚨 ALERTA DE ESTRUCTURA OBESA. Riesgo de insolvencia. Tu equipo consume demasiado margen."

        fig_gauge_nomina = go.Figure(go.Indicator(
            mode = "gauge+number", value = ratio_planilla,
            title = {'text': "Peso de Nómina (%)"},
            gauge = {
                'axis': {'range': [None, 60]},
                'bar': {'color': color_nomina},
                'steps': [
                    {'range': [0, 30], 'color': "#e8f5e9"},
                    {'range': [30, 40], 'color': "#fff3e0"},
                    {'range': [40, 60], 'color': "#ffebee"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}
            }
        ))
        fig_gauge_nomina.update_layout(height=250)
        st.plotly_chart(fig_gauge_nomina, use_container_width=True)
        
        st.markdown(f'<div class="veredicto">👩‍💼 Veredicto Estratega:<br>{mensaje_nomina}</div>', unsafe_allow_html=True)

    # --- SIMULADOR WHAT-IF ---
    st.markdown("---")
    st.subheader("🔮 Simulador de Rescate: 'La Palanca de Futuro'")
    st.info("Mueve los controles para ver cuánto dinero recuperarías optimizando estos gastos.")

    col_sim_controls, col_sim_results = st.columns(2)

    with col_sim_controls:
        st.write("**Metas de Reducción:**")
        meta_alquiler = st.slider("Reducir Alquiler en (%):", 0, 50, 0, step=5)
        meta_planilla = st.slider("Optimizar Planilla en (%):", 0, 50, 0, step=5)

    with col_sim_results:
        # Cálculos de Simulación
        ahorro_alquiler = gasto_alquiler * (meta_alquiler/100)
        ahorro_planilla = gasto_planilla * (meta_planilla/100)
        total_recuperado = ahorro_alquiler + ahorro_planilla
        
        nuevo_ebitda = ebitda + total_recuperado
        nueva_neta = utilidad_neta + total_recuperado # Asumiendo impacto directo

        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 Dinero Recuperado (Mensual)</h4>
            <h2 style="color: #2e7d32">+${total_recuperado:,.2f}</h2>
            <hr>
            <p>Nuevo EBITDA Proyectado: <strong>${nuevo_ebitda:,.2f}</strong></p>
            <p>Nueva Utilidad Neta: <strong>${nueva_neta:,.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    if total_recuperado > 0:
        st.success(f"💡 **Pitch de Venta:** 'Si implementamos el plan de 90 días para lograr estas reducciones, tu empresa ganará ${total_recuperado*12:,.0f} extras al año. ¿Empezamos?'")

# MÓDULO 2 Y 3 (MANTENIDOS IGUALES PERO EN NUEVAS PESTAÑAS)
with tab3:
    st.subheader("Línea de Supervivencia")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Punto de Equilibrio ($)", f"${punto_equilibrio:,.2f}")
        if margen_seguridad > 0:
            st.success(f"✅ Margen de Seguridad: ${margen_seguridad:,.2f}")
        else:
            st.error(f"🚨 Faltan ${abs(margen_seguridad):,.2f} para cubrir costos.")
    with col2:
        porcentaje_seguridad = (margen_seguridad / ventas_actual) * 100 if ventas_actual > 0 else 0
        fig_gauge_safe = go.Figure(go.Indicator(
             mode = "gauge+number", value = porcentaje_seguridad, title={'text':"Seguridad (%)"},
             gauge = {'axis': {'range': [-50, 100]}, 'bar': {'color': "green" if porcentaje_seguridad > 10 else "red"}}
        ))
        fig_gauge_safe.update_layout(height=250)
        st.plotly_chart(fig_gauge_safe, use_container_width=True)

with tab4:
    st.subheader("Ciclo de Conversión de Efectivo (CCC)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Días Calle", f"{dias_calle:.0f}")
    c2.metric("Días Inventario", f"{dias_inventario:.0f}")
    c3.metric("Días Proveedor", f"{dias_proveedor:.0f}")
    c4.metric("Ciclo de Caja", f"{ccc:.0f} días", delta_color="inverse")
    
    st.info("Si el Ciclo de Caja es positivo, tus proveedores cobran antes de que tú recuperes el dinero.")

# ==========================================
# GENERADOR DE REPORTE PROFESIONAL (SG CONSULTING)
# ==========================================

def create_professional_pdf():
    class PDF(FPDF):
        def header(self):
            # Franja superior de color
            self.set_fill_color(21, 101, 192) # Azul SG Consulting
            self.rect(0, 0, 210, 20, 'F')
            self.set_y(5)
            self.set_font('Arial', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, 'SG CONSULTING | Informe Estratégico', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Página {self.page_no()} - Generado por SG Strategic Dashboard el {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- 1. RESUMEN EJECUTIVO (SEMAFORIZADO) ---
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, '1. RESUMEN EJECUTIVO DE SIGNOS VITALES', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Línea separadora
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "Este informe analiza la salud financiera bajo la metodología de Potencia y Eficiencia. A continuación, el diagnóstico de los signos vitales críticos:")
    pdf.ln(5)
    
    # Tabla de Resumen
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 8, "INDICADOR", 1, 0, 'C', fill=True)
    pdf.cell(40, 8, "RESULTADO", 1, 0, 'C', fill=True)
    pdf.cell(90, 8, "DIAGNOSTICO", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 10)
    
    # Fila EBITDA
    diag_ebitda = "CRÍTICO (Inviable)" if ebitda < 0 else "VULNERABLE" if margen_ebitda < 10 else "SALUDABLE"
    pdf.cell(60, 8, "Potencia Operativa (EBITDA)", 1)
    pdf.cell(40, 8, f"${ebitda:,.0f} ({margen_ebitda:.1f}%)", 1)
    pdf.set_font('Arial', 'B', 10)
    if ebitda < 0: pdf.set_text_color(194, 24, 7) # Rojo
    else: pdf.set_text_color(0, 100, 0) # Verde
    pdf.cell(90, 8, diag_ebitda, 1, 1, 'C')
    pdf.set_text_color(0, 0, 0) # Reset
    
    # Fila Alquiler
    diag_renta = "OPTIMO"
    if ratio_alquiler > 15: diag_renta = "ALERTA CRITICA (Ancla)"
    elif ratio_alquiler > 10: diag_renta = "PESADO (Vigilancia)"
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(60, 8, "Ratio de Alquiler", 1)
    pdf.cell(40, 8, f"{ratio_alquiler:.1f}% de Ventas", 1)
    pdf.set_font('Arial', 'B', 10)
    if ratio_alquiler > 15: pdf.set_text_color(194, 24, 7)
    elif ratio_alquiler > 10: pdf.set_text_color(255, 140, 0)
    else: pdf.set_text_color(0, 100, 0)
    pdf.cell(90, 8, diag_renta, 1, 1, 'C')
    pdf.set_text_color(0, 0, 0)

    # Fila Planilla
    diag_nomina = "PRODUCTIVO"
    if ratio_planilla > 40: diag_nomina = "OBESO (Riesgo Insolvencia)"
    elif ratio_planilla > 30: diag_nomina = "ALERTA (Automatizar)"
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(60, 8, "Eficiencia de Nomina", 1)
    pdf.cell(40, 8, f"{ratio_planilla:.1f}% de Ut. Bruta", 1)
    pdf.set_font('Arial', 'B', 10)
    if ratio_planilla > 40: pdf.set_text_color(194, 24, 7)
    elif ratio_planilla > 30: pdf.set_text_color(255, 140, 0)
    else: pdf.set_text_color(0, 100, 0)
    pdf.cell(90, 8, diag_nomina, 1, 1, 'C')
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(10)

    # --- 2. ANALISIS DE EFICIENCIA Y ESTRATEGIA ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. ANALISIS DE EFICIENCIA Y RECOMENDACIONES', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    # Veredicto Alquiler
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f"A. Esfuerzo Inmobiliario (Ratio: {ratio_alquiler:.1f}%)", 0, 1)
    pdf.set_font('Arial', '', 11)
    veredicto_renta_txt = "Su estructura de local es optima. Mantenga este nivel."
    if ratio_alquiler > 15:
        veredicto_renta_txt = "VEREDICTO: El local esta consumiendo su utilidad. No es un activo, es un ancla financiera. Se recomienda renegociar contrato o evaluar reubicacion inmediata."
    elif ratio_alquiler > 10:
        veredicto_renta_txt = "VEREDICTO: Estructura pesada. Se debe revisar si la ubicacion actual justifica el costo con trafico de clientes."
    pdf.multi_cell(0, 6, veredicto_renta_txt)
    pdf.ln(5)

    # Veredicto Planilla
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f"B. Productividad de Talento (Ratio: {ratio_planilla:.1f}%)", 0, 1)
    pdf.set_font('Arial', '', 11)
    veredicto_nomina_txt = "Su equipo es altamente productivo. El retorno sobre talento es positivo."
    if ratio_planilla > 40:
        veredicto_nomina_txt = "VEREDICTO: Alerta de Estructura Obesa. Su equipo consume demasiado margen bruto, dejando a la empresa sin oxigeno para otros gastos. Riesgo alto de insolvencia."
    elif ratio_planilla > 30:
        veredicto_nomina_txt = "VEREDICTO: Zona de Vigilancia. Considere automatizar tareas administrativas o auditar la productividad por empleado."
    pdf.multi_cell(0, 6, veredicto_nomina_txt)
    pdf.ln(10)

    # --- 3. SUPERVIVENCIA Y CAJA ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. SUPERVIVENCIA Y FLUJO DE CAJA', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 8, f"Punto de Equilibrio (Meta Minima): ${punto_equilibrio:,.2f}", 0, 1)
    
    margen_seguridad_txt = f"${margen_seguridad:,.2f}"
    if margen_seguridad < 0:
        pdf.set_text_color(194, 24, 7)
        pdf.cell(100, 8, f"Deficit Actual (Perdida): {margen_seguridad_txt}", 0, 1)
    else:
        pdf.set_text_color(0, 100, 0)
        pdf.cell(100, 8, f"Colchon de Seguridad: {margen_seguridad_txt}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, f"Ciclo de Conversion de Efectivo: {ccc:.0f} dias", 0, 1)
    pdf.set_font('Arial', '', 11)
    if ccc > 0:
        pdf.multi_cell(0, 6, f"ALERTA DE CAJA: Sus proveedores cobran antes de que usted recupere el dinero. Usted financia la operacion por {ccc:.0f} dias con su propio bolsillo. Accion: Renegociar plazos o Factoring.")
    else:
        pdf.multi_cell(0, 6, "EXCELENTE: Su ciclo de caja es negativo o financiado. Usted trabaja con el dinero de sus proveedores.")

    # --- 4. ADVERTENCIA LEGAL ---
    pdf.ln(15)
    pdf.set_draw_color(194, 24, 7)
    pdf.set_fill_color(255, 235, 238)
    pdf.rect(10, pdf.get_y(), 190, 25, 'DF')
    pdf.set_xy(12, pdf.get_y()+2)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(194, 24, 7)
    pdf.cell(0, 6, "ADVERTENCIA DE RESPONSABILIDAD GERENCIAL Y FIDUCIARIA", 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 4, "Este reporte constituye una herramienta de diagnostico interno. Operar consistentemente con margenes operativos negativos o insolvencia tecnica puede acarrear responsabilidades patrimoniales para los administradores segun la legislacion mercantil vigente en Panama. Si los indicadores estan en ROJO, se recomienda la implementacion inmediata de un Plan de Estabilizacion.", align='C')

    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- BOTÓN DE DESCARGA ---
st.sidebar.markdown("---")
st.sidebar.header("📥 Entregable Profesional")

if st.sidebar.button("📄 Generar Informe Consultivo"):
    pdf_bytes = create_professional_pdf()
    st.sidebar.download_button(
        label="💾 Descargar PDF de SG Consulting",
        data=pdf_bytes,
        file_name=f"Informe_Estrategico_SG_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
