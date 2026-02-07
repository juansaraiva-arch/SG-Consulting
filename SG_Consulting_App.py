import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Rescue | App de Diagnóstico", layout="wide")

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #1e88e5; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .alert-danger { background-color: #ffebee; padding: 15px; border-radius: 5px; color: #c62828; border: 1px solid #c62828; font-weight: bold;}
    .alert-warning { background-color: #fff3e0; padding: 15px; border-radius: 5px; color: #ef6c00; border: 1px solid #ef6c00; font-weight: bold;}
    .alert-success { background-color: #e8f5e9; padding: 15px; border-radius: 5px; color: #2e7d32; border: 1px solid #2e7d32; font-weight: bold;}
    .recommendation-box { background-color: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 5px solid #2196f3; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🛡️ SG Consulting: Sistema Maestro de Rescate")
st.markdown("**Metodología de Intervención Estratégica para PyMEs**")

# --- INPUTS GLOBALES (BARRA LATERAL) ---
with st.sidebar:
    st.header("1. Estado de Resultados (Anual)")
    ventas = st.number_input("Ventas Totales ($)", min_value=0.0, value=500000.0, step=1000.0)
    costo_ventas = st.number_input("Costo de Ventas (COGS) ($)", min_value=0.0, value=300000.0, step=1000.0)
    gastos_operativos = st.number_input("Gastos Operativos (OPEX) ($)", min_value=0.0, value=130000.0, step=500.0)
    depreciacion = st.number_input("Depreciaciones ($)", min_value=0.0, value=15000.0, step=100.0)
    intereses = st.number_input("Gastos Financieros ($)", min_value=0.0, value=5000.0, step=100.0)
    impuestos = st.number_input("Impuestos ($)", min_value=0.0, value=12500.0, step=100.0)
    
    st.markdown("---")
    st.header("2. Balance General (Actual)")
    st.info("Datos clave para el Flujo de Caja")
    cuentas_por_cobrar = st.number_input("Cuentas por Cobrar ($)", min_value=0.0, value=50000.0, step=500.0, help="Dinero que te deben los clientes.")
    inventario = st.number_input("Valor del Inventario ($)", min_value=0.0, value=60000.0, step=500.0, help="Mercancía parada en bodega.")
    cuentas_por_pagar = st.number_input("Cuentas por Pagar ($)", min_value=0.0, value=25000.0, step=500.0, help="Dinero que debes a proveedores.")

# --- PESTAÑAS DE MÓDULOS ---
tab1, tab2, tab3 = st.tabs(["Módulo 1: Potencia (EBITDA)", "Módulo 2: Supervivencia (PE)", "Módulo 3: Oxígeno (Flujo de Caja)"])

# ==========================================
# MÓDULO 1: LA CASCADA DE POTENCIA
# ==========================================
with tab1:
    st.subheader("💧 Análisis de Rentabilidad en Cascada")
    # Cálculos
    utilidad_bruta = ventas - costo_ventas
    ebitda = utilidad_bruta - gastos_operativos
    margen_ebitda = (ebitda / ventas) * 100 if ventas > 0 else 0
    ebit = ebitda - depreciacion
    utilidad_neta = ebit - intereses - impuestos
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Flujo", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "subtotal", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Utilidad Bruta", "Gastos Op.", "EBITDA", "Otros Gastos", "Utilidad Neta"],
            text = [f"${x/1000:.1f}k" for x in [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta]],
            y = [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#42a5f5"}}
        ))
        fig_waterfall.update_layout(title="Ruta del Dinero", height=400)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col2:
        st.metric(label="EBITDA (Caja Operativa)", value=f"${ebitda:,.0f}", delta=f"{margen_ebitda:.1f}% Margen")
        if ebitda < 0:
            st.error("🚨 CRÍTICO: El negocio quema efectivo.")
        elif margen_ebitda < 10:
            st.warning("⚠️ ALERTA: Margen operativo muy bajo.")
        else:
            st.success("✅ SÓLIDO: Operación saludable.")

# ==========================================
# MÓDULO 2: PUNTO DE EQUILIBRIO
# ==========================================
with tab2:
    st.subheader("⚖️ La Línea de Supervivencia")
    # Cálculos
    costo_variable_total = costo_ventas # Simplificación para el modelo
    costos_fijos_totales = gastos_operativos + intereses
    margen_contribucion_pct = (ventas - costo_variable_total) / ventas if ventas > 0 else 0
    
    if margen_contribucion_pct > 0:
        punto_equilibrio = costos_fijos_totales / margen_contribucion_pct
    else:
        punto_equilibrio = 0
            
    margen_seguridad = ((ventas - punto_equilibrio) / ventas) * 100 if ventas > 0 else 0

    col_x, col_y = st.columns(2)
    with col_x:
        st.metric("Punto de Equilibrio ($)", f"${punto_equilibrio:,.2f}")
        if ventas < punto_equilibrio:
             st.error(f"🚨 Estás perdiendo dinero. Faltan ${punto_equilibrio - ventas:,.0f} para cubrir costos.")
        else:
             st.success(f"✅ Cubres costos y ganas dinero.")

    with col_y:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = margen_seguridad,
            title = {'text': "Margen de Seguridad (%)"},
            gauge = {'axis': {'range': [-50, 100]}, 'bar': {'color': "green" if margen_seguridad > 10 else "red"}}
        ))
        fig_gauge.update_layout(height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)

# ==========================================
# MÓDULO 3: EL OXÍGENO (FLUJO DE CAJA) - NUEVO
# ==========================================
with tab3:
    st.subheader("🫁 El Oxígeno del Negocio (Ciclo de Conversión de Efectivo)")
    st.markdown("Diagnóstico de Liquidez: ¿Por qué no tengo dinero en el banco?")
    
    # --- CÁLCULOS DEL TRIÁNGULO DE PODER ---
    # Días Calle (DSO) = (CXC / Ventas) * 365
    dias_calle = (cuentas_por_cobrar / ventas) * 365 if ventas > 0 else 0
    
    # Días Inventario (DIO) = (Inventario / Costo Ventas) * 365
    dias_inventario = (inventario / costo_ventas) * 365 if costo_ventas > 0 else 0
    
    # Días Proveedor (DPO) = (CXP / Costo Ventas) * 365
    dias_proveedor = (cuentas_por_pagar / costo_ventas) * 365 if costo_ventas > 0 else 0
    
    # Ciclo de Conversión de Efectivo (CCC)
    ciclo_efectivo = dias_calle + dias_inventario - dias_proveedor

    # --- VISUALIZACIÓN DE MÉTRICAS ---
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.metric("Días Calle (Cobro)", f"{dias_calle:.0f} días", help="Tiempo que tardas en cobrar a clientes.")
    with col4:
        st.metric("Días Inventario", f"{dias_inventario:.0f} días", help="Tiempo que la mercancía está parada.")
    with col5:
        st.metric("Días Proveedor (Pago)", f"{dias_proveedor:.0f} días", help="Tiempo que tardas en pagar proveedores.")
    with col6:
        st.metric("Ciclo de Caja (CCC)", f"{ciclo_efectivo:.0f} días", 
                 delta_color="inverse", delta=f"{'⚠️ ALERTA' if ciclo_efectivo > 0 else '✅ EXCELENTE'}")

    st.markdown("---")

    # --- GRÁFICO COMPARATIVO ---
    col_chart, col_diag = st.columns([1, 1])
    
    with col_chart:
        # Gráfico de barras horizontales para comparar tiempos
        fig_cash = go.Figure()
        fig_cash.add_trace(go.Bar(
            y=['Días Calle (Cobro)', 'Días Inventario', 'Ciclo Total (Financiamiento)'],
            x=[dias_calle, dias_inventario, ciclo_efectivo],
            name='Tu Dinero Atrapado', orientation='h', marker_color='#ef5350'
        ))
        fig_cash.add_trace(go.Bar(
            y=['Días Proveedor (Pago)'],
            x=[dias_proveedor],
            name='Financiamiento Proveedor', orientation='h', marker_color='#66bb6a'
        ))
        fig_cash.update_layout(title="Tu Dinero vs. Dinero del Proveedor", barmode='group')
        st.plotly_chart(fig_cash, use_container_width=True)

    # --- DIAGNÓSTICO INTELIGENTE Y RECOMENDACIONES ---
    with col_diag:
        st.subheader("🩺 Diagnóstico de Liquidez")
        
        # Regla Maestra: (Calle + Inventario) > Proveedor
        tiempo_recuperacion = dias_calle + dias_inventario
        
        if tiempo_recuperacion > dias_proveedor:
            brecha = tiempo_recuperacion - dias_proveedor
            st.markdown(f"""
            <div class="alert-danger">
            <strong>🚨 ALERTA DE AHOGO FINANCIERO</strong><br>
            Tardas <strong>{tiempo_recuperacion:.0f} días</strong> en recuperar tu dinero, pero debes pagar en <strong>{dias_proveedor:.0f} días</strong>.
            <br><br>
            Tienes una <strong>Brecha de {brecha:.0f} días</strong> que estás financiando con tu propio bolsillo (o deuda bancaria).
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 💊 Receta de Intervención (SG Consulting):")
            
            # Recomendaciones dinámicas según dónde esté el problema
            if dias_calle > 45:
                st.info("📉 **Problema: Cobras muy lento.**\n\n*Acción:* Implementa descuento por pronto pago (ej. 2% a 10 días) o usa Factoring.")
            
            if dias_inventario > 60:
                st.info("📦 **Problema: Inventario estancado.**\n\n*Acción:* Haz un 'Remate de Inventario Muerto' para liberar efectivo ya.")
            
            if dias_proveedor < 30:
                st.info("🤝 **Problema: Pagas muy rápido.**\n\n*Acción:* Negocia con proveedores pagar a 45 o 60 días.")
                
        else:
            st.markdown(f"""
            <div class="alert-success">
            <strong>✅ NIRVANA FINANCIERO</strong><br>
            ¡Felicidades! Cobras y vendes antes de tener que pagar. Estás trabajando con el dinero de tus proveedores (Ciclo Negativo o financiado).
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# GENERADOR DE REPORTE PDF (SG CONSULTING)
# ==========================================
from fpdf import FPDF
from datetime import datetime

def create_pdf(ventas, ebitda, margen_ebitda, punto_equilibrio, margen_seguridad, 
               dias_calle, dias_inventario, dias_proveedor, ciclo_efectivo):
    
    class PDF(FPDF):
        def header(self):
            # Título / Membrete
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'SG CONSULTING | Informe de Diagnóstico Financiero', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'Estrategia, Intervención y Rentabilidad', 0, 1, 'C')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()} - Generado por SG Rescue App el {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 1. RESUMEN EJECUTIVO
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(200, 220, 255) # Azul claro
    pdf.cell(0, 10, ' 1. RESUMEN EJECUTIVO DE SIGNOS VITALES', 1, 1, 'L', fill=True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    
    # Evaluar estado general para el texto
    estado_ebitda = "CRÍTICO" if ebitda < 0 else "VULNERABLE" if margen_ebitda < 10 else "SÓLIDO"
    estado_caja = "AHOGO FINANCIERO" if ciclo_efectivo > 0 else "LIQUIDEZ ÓPTIMA"
    
    pdf.multi_cell(0, 7, f"El presente diagnóstico evalúa la salud financiera de la empresa con base en la metodología de Rentabilidad y Flujo de Caja. El estado actual del negocio es: {estado_ebitda} en Operación y presenta un cuadro de {estado_caja}.")
    pdf.ln(5)

    # 2. DETALLE DE POTENCIA (EBITDA)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, ' 2. ANÁLISIS DE POTENCIA (MÓDULO 1)', 1, 1, 'L', fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.ln(2)
    
    pdf.cell(50, 8, f"Ventas Totales:", 0)
    pdf.cell(50, 8, f"${ventas:,.2f}", 0, 1)
    pdf.cell(50, 8, f"EBITDA (Caja Operativa):", 0)
    
    # Color rojo si es negativo (simulado con texto)
    if ebitda < 0:
        pdf.set_text_color(194, 24, 7) # Rojo
    else:
        pdf.set_text_color(0, 100, 0) # Verde
        
    pdf.cell(50, 8, f"${ebitda:,.2f} ({margen_ebitda:.1f}%)", 0, 1)
    pdf.set_text_color(0, 0, 0) # Reset color
    
    if ebitda < 0:
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 6, "ALERTA: El modelo de negocio no es viable. Los gastos operativos superan a la utilidad bruta. Se requiere reestructuración inmediata de personal o costos fijos.")
    pdf.ln(5)

    # 3. LÍNEA DE SUPERVIVENCIA (PUNTO DE EQUILIBRIO)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, ' 3. LÍNEA DE SUPERVIVENCIA (MÓDULO 2)', 1, 1, 'L', fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.ln(2)
    
    pdf.cell(60, 8, f"Punto de Equilibrio (Meta):", 0)
    pdf.cell(50, 8, f"${punto_equilibrio:,.2f}", 0, 1)
    pdf.cell(60, 8, f"Margen de Seguridad:", 0)
    pdf.cell(50, 8, f"{margen_seguridad:.1f}%", 0, 1)
    
    if margen_seguridad < 10:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 6, "RIESGO ALTO: La empresa está en zona de peligro. Cualquier caída leve en ventas resultará en pérdidas netas. 'Cualquier gripe del mercado mata a la empresa'.")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # 4. OXÍGENO Y CAJA (MÓDULO 3)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, ' 4. CICLO DEL DINERO (MÓDULO 3)', 1, 1, 'L', fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.ln(2)
    
    pdf.cell(60, 8, f"Días Calle (Cobro):", 0)
    pdf.cell(50, 8, f"{dias_calle:.0f} días", 0, 1)
    pdf.cell(60, 8, f"Días Inventario:", 0)
    pdf.cell(50, 8, f"{dias_inventario:.0f} días", 0, 1)
    pdf.cell(60, 8, f"Días Proveedor (Pago):", 0)
    pdf.cell(50, 8, f"{dias_proveedor:.0f} días", 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(60, 8, f"CICLO DE CAJA (CCC):", 0)
    pdf.cell(50, 8, f"{ciclo_efectivo:.0f} días", 0, 1)
    pdf.set_font('Arial', '', 11)
    
    # Recomendaciones Automáticas
    pdf.ln(3)
    pdf.set_font('Arial', 'I', 10)
    rec_text = "RECOMENDACIONES ESTRATÉGICAS:\n"
    if dias_calle > 45:
        rec_text += "- Implementar política de 'Descuento por Pronto Pago' o Factoring para acelerar cobros.\n"
    if dias_inventario > 60:
        rec_text += "- Ejecutar estrategia de 'Remate de Inventario Muerto' para liberar efectivo atrapado.\n"
    if ciclo_efectivo > 0:
        rec_text += "- La empresa financia la operación con recursos propios. Prioridad: Negociar plazos con proveedores."
    
    pdf.multi_cell(0, 6, rec_text)
    pdf.ln(10)

    # 5. NOTA LEGAL (DISCLAIMER)
    pdf.set_draw_color(194, 24, 7)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(0, 5, "ADVERTENCIA DE RESPONSABILIDAD GERENCIAL Y FIDUCIARIA", 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    pdf.multi_cell(0, 4, "Este reporte constituye una herramienta de diagnóstico interno. Operar con márgenes negativos o insolvencia técnica puede acarrear responsabilidades patrimoniales para los administradores según la legislación mercantil vigente. Se recomienda la implementación inmediata del plan de estabilización.")

    return pdf.output(dest='S').encode('latin-1')

# --- BOTÓN DE DESCARGA EN LA BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.header("📥 Entregable")

if st.sidebar.button("Generar PDF de Diagnóstico"):
    # Generamos el PDF pasando todas las variables calculadas en los módulos anteriores
    pdf_bytes = create_pdf(ventas, ebitda, margen_ebitda, punto_equilibrio, margen_seguridad, 
                           dias_calle, dias_inventario, dias_proveedor, ciclo_efectivo)
    
    st.sidebar.download_button(
        label="💾 Descargar Reporte SG Consulting",
        data=pdf_bytes,
        file_name="Diagnostico_SG_Consulting.pdf",
        mime="application/pdf"
    )
