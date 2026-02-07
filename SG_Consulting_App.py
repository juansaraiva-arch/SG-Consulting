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
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🛡️ SG Consulting: Sistema Maestro de Rescate")
st.markdown("**Metodología de Intervención Estratégica para PyMEs**")

# --- INPUTS GLOBALES (BARRA LATERAL) ---
with st.sidebar:
    st.header("1. Datos Financieros (Estado de Resultados)")
    st.info("Ingresa los datos mensuales o anuales.")
    
    ventas = st.number_input("Ventas Totales ($)", min_value=0.0, value=50000.0, step=1000.0)
    costo_ventas = st.number_input("Costo de Ventas (COGS) ($)", min_value=0.0, value=30000.0, step=1000.0)
    gastos_operativos = st.number_input("Gastos Operativos (OPEX) ($)", min_value=0.0, value=15000.0, step=500.0)
    depreciacion = st.number_input("Depreciaciones ($)", min_value=0.0, value=1500.0, step=100.0)
    intereses = st.number_input("Gastos Financieros ($)", min_value=0.0, value=500.0, step=100.0)
    impuestos = st.number_input("Impuestos ($)", min_value=0.0, value=1250.0, step=100.0)

# --- PESTAÑAS DE MÓDULOS ---
tab1, tab2 = st.tabs(["Módulo 1: Potencia (EBITDA)", "Módulo 2: Supervivencia (Punto de Equilibrio)"])

# ==========================================
# MÓDULO 1: LA CASCADA DE POTENCIA
# ==========================================
with tab1:
    st.subheader("💧 Análisis de Rentabilidad en Cascada")
    
    # Cálculos Módulo 1
    utilidad_bruta = ventas - costo_ventas
    ebitda = utilidad_bruta - gastos_operativos
    margen_ebitda = (ebitda / ventas) * 100 if ventas > 0 else 0
    ebit = ebitda - depreciacion
    utilidad_neta = ebit - intereses - impuestos
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico Cascada
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Flujo", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "subtotal", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Utilidad Bruta", "Gastos Op.", "EBITDA", "Otros Gastos", "Utilidad Neta"],
            text = [f"${x:,.0f}" for x in [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta]],
            y = [ventas, -costo_ventas, utilidad_bruta, -gastos_operativos, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#42a5f5"}}
        ))
        fig_waterfall.update_layout(title="Ruta del Dinero", height=400)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col2:
        # Tarjetas de KPI
        st.markdown(f"""
        <div class="metric-card">
            <h4>EBITDA (Caja Operativa)</h4>
            <h2 style="color: {'#2e7d32' if ebitda > 0 else '#c62828'}">${ebitda:,.2f}</h2>
            <p>Margen: <strong>{margen_ebitda:.1f}%</strong></p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        # Diagnóstico Rápido Texto
        if ebitda < 0:
            st.error("🚨 CRÍTICO: El negocio quema efectivo en su operación diaria.")
        elif margen_ebitda < 10:
            st.warning("⚠️ ALERTA: Margen operativo muy bajo. Vulnerable.")
        else:
            st.success("✅ SÓLIDO: La operación es saludable.")

# ==========================================
# MÓDULO 2: PUNTO DE EQUILIBRIO (NUEVO)
# ==========================================
with tab2:
    st.subheader("⚖️ La Línea de Supervivencia")
    st.markdown("Calcula cuánto necesitas vender para cubrir todos tus costos (Utilidad = 0).")
    
    # 1. CLASIFICACIÓN DE COSTOS (INPUTS ESPECÍFICOS MÓDULO 2)
    with st.expander("🛠️ Paso 1: Clasificar Costos (Fijos vs. Variables)", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### Costos Variables")
            st.caption("Cambian si vendes más (Materia prima, comisiones, envíos).")
            # Por defecto asumimos que el Costo de Ventas es 100% Variable
            costo_variable_total = st.number_input("Total Costos Variables ($)", value=costo_ventas, step=500.0, help="Usualmente es el Costo de Ventas + Comisiones de venta.")
        
        with col_b:
            st.markdown("##### Costos Fijos Totales")
            st.caption("No cambian si vendes cero (Alquiler, Nómina fija, Internet).")
            # Por defecto asumimos que Gastos Op + Intereses son Fijos
            costo_fijo_estimado = gastos_operativos + intereses
            costos_fijos_totales = st.number_input("Total Costos Fijos ($)", value=costo_fijo_estimado, step=500.0)

    # 2. CÁLCULOS
    if ventas > 0:
        # Margen de Contribución Global (%) = (Ventas - Costos Variables) / Ventas
        margen_contribucion_pct = (ventas - costo_variable_total) / ventas
        
        # Fórmula Maestra Punto de Equilibrio ($) = Costos Fijos / Margen Contribución %
        if margen_contribucion_pct > 0:
            punto_equilibrio = costos_fijos_totales / margen_contribucion_pct
        else:
            punto_equilibrio = 0 # Evitar división por cero si margen es negativo
            
        # Margen de Seguridad (%) = (Ventas Reales - PE) / Ventas Reales
        margen_seguridad = ((ventas - punto_equilibrio) / ventas) * 100
    else:
        punto_equilibrio = 0
        margen_seguridad = 0

    st.markdown("---")
    
    # 3. VISUALIZACIÓN Y DIAGNÓSTICO
    col_x, col_y = st.columns([1, 1])
    
    with col_x:
        st.markdown(f"### Tu Punto de Equilibrio es: **${punto_equilibrio:,.2f}**")
        st.markdown(f"Ventas Actuales: **${ventas:,.2f}**")
        
        delta = ventas - punto_equilibrio
        if delta > 0:
             st.success(f"✅ Estás **${delta:,.2f}** por ENCIMA del punto de equilibrio.")
        else:
             st.error(f"🚨 Estás **${abs(delta):,.2f}** por DEBAJO. Estás perdiendo dinero.")

        # Explicación para el cliente
        st.info(f"""
        **Interpretación para el Cliente:**
        "Para no perder ni ganar un centavo, su empresa necesita facturar **${punto_equilibrio:,.0f}**. 
        Todo lo que venda por encima de eso es ganancia; todo lo que venda por debajo sale de su bolsillo."
        """)

    with col_y:
        # Gráfico de Velocímetro (Gauge Chart) para Margen de Seguridad
        color_gauge = "red"
        if margen_seguridad > 20: color_gauge = "green"
        elif margen_seguridad > 10: color_gauge = "orange"
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = margen_seguridad,
            title = {'text': "Margen de Seguridad (%)"},
            delta = {'reference': 10, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [-50, 100]},
                'bar': {'color': color_gauge},
                'steps': [
                    {'range': [-50, 0], 'color': "#ffcdd2"}, # Zona Pérdida
                    {'range': [0, 10], 'color': "#fff9c4"},  # Zona Peligro
                    {'range': [10, 100], 'color': "#c8e6c9"} # Zona Seguridad
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # 4. ALERTA DEL MANUAL (SOURCE 2)
    st.write("#### 🧠 Diagnóstico Estratégico:")
    if margen_seguridad < 10:
        st.markdown("""
        <div class="alert-danger">
        <strong>⚠️ ZONA DE PELIGRO INMINENTE:</strong><br>
        Su Margen de Seguridad es inferior al 10%. Según el Manual de SG Consulting, esto significa que 
        <em>"Cualquier gripe del mercado (una huelga, una pandemia, un mal mes) mata a la empresa"</em>. 
        <br><strong>Acción Recomendada:</strong> Necesitamos reducir los Costos Fijos YA.
        </div>
        """, unsafe_allow_html=True)
    elif margen_seguridad < 25:
        st.markdown("""
        <div class="alert-warning">
        <strong>⚠️ ZONA DE PRECAUCIÓN:</strong><br>
        La empresa cubre sus costos, pero tiene poco espacio para maniobrar. No asuma nuevas deudas fijas.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
        <strong>✅ ZONA DE SEGURIDAD:</strong><br>
        La empresa tiene un colchón saludable para resistir crisis.
        </div>
        """, unsafe_allow_html=True)
