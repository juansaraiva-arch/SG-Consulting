import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Strategic Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- 1. INICIALIZACIÓN DE MEMORIA (SESSION STATE) ---
if 'lab_precios' not in st.session_state:
    st.session_state.lab_precios = []

# --- 2. ESTILOS VISUALES (CSS) ---
st.markdown("""
    <style>
    /* Estilos Generales */
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* Cajas de Diagnóstico (Tab 1) */
    .power-level-title { font-size: 16px; font-weight: bold; color: #1565c0; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; }
    .power-value { font-size: 22px; font-weight: bold; color: #000000; margin-bottom: 5px; }
    
    .check-box-success { 
        background-color: #2e7d32; color: white; padding: 10px; border-radius: 5px; 
        font-weight: bold; display: flex; align-items: center; margin-bottom: 10px; border-left: 5px solid #1b5e20;
    }
    .check-box-warning { 
        background-color: #fbc02d; color: black; padding: 10px; border-radius: 5px; 
        font-weight: bold; display: flex; align-items: center; margin-bottom: 10px; border-left: 5px solid #f57f17;
    }
    .check-box-danger { 
        background-color: #c62828; color: white; padding: 10px; border-radius: 5px; 
        font-weight: bold; display: flex; align-items: center; margin-bottom: 10px; border-left: 5px solid #b71c1c;
    }

    /* Estilos Nuevos */
    .verdict-box { background-color: #263238; color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 8px solid #ffca28; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .money-trap { background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #c62828; }
    .valuation-box { background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    .veredicto { font-style: italic; font-weight: bold; color: #555; padding: 10px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #333; }
    .legal-footer { font-size: 10px; color: #777; margin-top: 10px; font-style: italic; border-top: 1px solid #ddd; padding-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Laboratorio de Precios**")

# --- 3. BARRA LATERAL: INPUTS ---
with st.sidebar:
    st.header("1. Configuración")
    
    # Selector de Modo
    modo_analisis = st.radio(
        "Modo de Datos:", 
        ["Mensual (Flash)", "Anual (Estratega)"],
        help="Mensual: Datos de un solo mes. Anual: Datos acumulados de 12 meses."
    )
    
    st.header("2. Datos Financieros")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        st.info(f"Ingresa los valores {'del MES' if 'Mensual' in modo_analisis else 'TOTALES del AÑO'}.")
        
        ventas_input = st.number_input("Ventas Totales ($)", value=600000.0 if 'Anual' in modo_analisis else 50000.0, step=1000.0)
        costo_ventas_input = st.number_input("Costo de Ventas (Variable)", value=360000.0 if 'Anual' in modo_analisis else 30000.0, step=1000.0)
        
        st.markdown("**Gastos Operativos (OPEX):**")
        gasto_alquiler_input = st.number_input("1. Alquiler + CAM", value=60000.0 if 'Anual' in modo_analisis else 5000.0, step=100.0)
        gasto_planilla_input = st.number_input("2. Planilla Total", value=96000.0 if 'Anual' in modo_analisis else 8000.0, step=500.0)
        gasto_otros_input = st.number_input("3. Otros Gastos Operativos", value=24000.0 if 'Anual' in modo_analisis else 2000.0, step=100.0)
        
        st.markdown("---")
        depreciacion_input = st.number_input("Depreciaciones + Amortizaciones", value=24000.0 if 'Anual' in modo_analisis else 2000.0, step=100.0)
        intereses_input = st.number_input("Intereses (Gastos Financieros)", value=12000.0 if 'Anual' in modo_analisis else 1000.0, step=100.0)
        impuestos_input = st.number_input("Impuestos", value=18000.0 if 'Anual' in modo_analisis else 1500.0, step=100.0)

    with st.expander("B. Balance General (FOTO)", expanded=True):
        st.warning("⚠️ Ingresa el SALDO FINAL (Lo que hay hoy). No dividas ni sumes.")
        inventario = st.number_input("Inventario (Saldo Final $)", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar (Saldo Final $)", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar (Saldo Final $)", value=10000.0)

# --- 4. LÓGICA DE NORMALIZACIÓN ---
if 'modo_analisis' in locals() and "Anual" in modo_analisis:
    divisor = 12
    st.sidebar.success("✅ Modo Anual: Datos convertidos a promedio mensual.")
else:
    divisor = 1

# Normalización de P&L
ventas_mes = ventas_input / divisor
costo_ventas_mes = costo_ventas_input / divisor
gasto_alquiler_mes = gasto_alquiler_input / divisor
gasto_planilla_mes = gasto_planilla_input / divisor
gasto_otros_mes = gasto_otros_input / divisor
gastos_operativos_mes = gasto_alquiler_mes + gasto_planilla_mes + gasto_otros_mes

depreciacion_mes = depreciacion_input / divisor
intereses_mes = intereses_input / divisor
impuestos_mes = impuestos_input / divisor

# --- 5. CÁLCULOS PRINCIPALES ---

# Potencia
utilidad_bruta_mes = ventas_mes - costo_ventas_mes
margen_bruto = (utilidad_bruta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebitda_mes = utilidad_bruta_mes - gastos_operativos_mes
margen_ebitda = (ebitda_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebit_mes = ebitda_mes - depreciacion_mes
utilidad_neta_mes = ebit_mes - intereses_mes - impuestos_mes
margen_neto = (utilidad_neta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

# Ratios Eficiencia
ratio_alquiler = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
ratio_planilla = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0

# Supervivencia
costos_fijos_totales_mes = gastos_operativos_mes + intereses_mes
margen_contribucion_pct = (utilidad_bruta_mes / ventas_mes) if ventas_mes > 0 else 0
punto_equilibrio_mes = costos_fijos_totales_mes / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad_mes = ventas_mes - punto_equilibrio_mes

# Oxígeno (CCC)
dias_calle = (cuentas_cobrar / ventas_mes) * 30 if ventas_mes > 0 else 0
dias_inventario = (inventario / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

dinero_atrapado_total = cuentas_cobrar + inventario

# Valoración Base (Para Tab 1)
valor_empresa_actual = (ebitda_mes * 12) * 3 if ebitda_mes > 0 else 0

# Juez Digital
veredicto_final = ""
icono_veredicto = "⚖️"
if ebitda_mes < 0:
    veredicto_final = "INTERVENCIÓN DE EMERGENCIA NECESARIA. El modelo de negocio está consumiendo capital. Problema Estructural."
    icono_veredicto = "🚨"
elif ccc > 60:
    veredicto_final = "SÍNDROME DE 'AGUJERO NEGRO'. Rentable pero insolvente. Prioridad: COBRAR."
    icono_veredicto = "🕳️"
elif ratio_alquiler > 15:
    veredicto_final = "RIESGO INMOBILIARIO. Estás trabajando para pagar el local."
    icono_veredicto = "🏢"
else:
    veredicto_final = "EMPRESA SALUDABLE Y ESCALABLE. Listo para crecer."
    icono_veredicto = "✅"

# --- 6. DASHBOARD VISUAL (TABS) ---

# Veredicto
st.markdown(f"""<div class="verdict-box"><h3>{icono_veredicto} Veredicto de la Estratega:</h3><p style="font-size: 18px;">"{veredicto_final}"</p></div>""", unsafe_allow_html=True)

# TABS PRINCIPALES
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💎 Cascada", "🚦 Semáforo", "⚖️ Supervivencia", "🫁 Oxígeno", "📈 Valoración", "🧪 Lab de Precios"])

# =========================================================
# TAB 1: LOS 4 NIVELES DE POTENCIA (DISEÑO EXTENDIDO RESTAURADO)
# =========================================================
with tab1:
    col_main, col_chart = st.columns([1.2, 1])
    
    with col_main:
        st.subheader("Diagnóstico de los 4 Niveles de Potencia")
        st.caption("Análisis de salud financiera capa por capa.")
        
        # --- SECCIÓN VALORACIÓN BASE ---
        if valor_empresa_actual > 0:
            st.markdown(f"""
            <div class="valuation-box">
                <h4>Valor Ref. (Base 3x):</h4>
                <h1 style="color: #1b5e20;">${valor_empresa_actual:,.2f}</h1>
                <p><em>Ve a la Pestaña 5 para personalizar el múltiplo.</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Tu empresa hoy vale $0.00 para un inversor (EBITDA Negativo).")
            
        st.markdown("---")
        
        # --- NIVEL 1: POTENCIA COMERCIAL ---
        st.markdown('<div class="power-level-title">Nivel 1: Potencia Comercial (Utilidad Bruta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_bruta_mes:,.2f} (Margen: {margen_bruto:.1f}%)</div>', unsafe_allow_html=True)
        
        if margen_bruto > 30:
            st.markdown('<div class="check-box-success">✅ <strong>Saludable:</strong> Tienes un modelo de precios y costos de venta correcto.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="check-box-warning">⚠️ <strong>Alerta:</strong> Tu margen bruto es bajo. Revisa precios o proveedores.</div>', unsafe_allow_html=True)

        # --- NIVEL 2: POTENCIA OPERATIVA ---
        st.markdown('<div class="power-level-title">Nivel 2: Potencia Operativa (EBITDA) - El Corazón</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebitda_mes:,.2f} (Margen: {margen_ebitda:.1f}%)</div>', unsafe_allow_html=True)

        if ebitda_mes > 0 and margen_ebitda > 10:
             st.markdown('<div class="check-box-success">✅ <strong>Fuerte:</strong> El corazón de tu negocio late con fuerza. Generas caja operativa.</div>', unsafe_allow_html=True)
        elif ebitda_mes > 0:
             st.markdown('<div class="check-box-warning">⚠️ <strong>Vulnerable:</strong> Generas dinero pero el margen es muy estrecho (< 10%).</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 <strong>CRÍTICO:</strong> El negocio quema efectivo cada mes. Requiere intervención inmediata.</div>', unsafe_allow_html=True)

        # --- NIVEL 3: POTENCIA DE ACTIVOS ---
        st.markdown('<div class="power-level-title">Nivel 3: Potencia de Activos (EBIT)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebit_mes:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)
        st.caption("Resultado después de depreciaciones (desgaste de equipos).")

        # --- NIVEL 4: POTENCIA PATRIMONIAL ---
        st.markdown('<div class="power-level-title">Nivel 4: Potencia Patrimonial (Utilidad Neta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_neta_mes:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)
        
        if utilidad_neta_mes > 0:
             st.markdown('<div class="check-box-success">✅ <strong>Ganancia Real:</strong> El dueño está ganando dinero después de todo.</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 <strong>Pérdida:</strong> El dueño está perdiendo dinero o trabajando gratis.</div>', unsafe_allow_html=True)

    with col_chart:
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "relative", "relative", "subtotal", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Ut. Bruta", "Alquiler", "Planilla", "Otros Gastos", "EBITDA", "Otros", "Ut. Neta"],
            y = [ventas_mes, -costo_ventas_mes, utilidad_bruta_mes, -gasto_alquiler_mes, -gasto_planilla_mes, -gasto_otros_mes, ebitda_mes, -(depreciacion_mes+intereses_mes+impuestos_mes), utilidad_neta_mes],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#1565c0"}}
        ))
        fig_waterfall.update_layout(title="Cascada Detallada (Mensual)", showlegend=False, height=600)
        st.plotly_chart(fig_waterfall, use_container_width=True)

# TAB 2: SEMÁFORO
with tab2:
    col_renta, col_nomina = st.columns(2)
    with col_renta:
        color_renta = "green" if ratio_alquiler < 10 else "orange" if ratio_alquiler < 15 else "red"
        st.markdown(f"**Ratio Alquiler:** {ratio_alquiler:.1f}%")
        st.progress(min(ratio_alquiler/30, 1.0))
        if color_renta == "red": st.markdown('<p class="alert-danger">🚨 El local es un ancla financiera.</p>', unsafe_allow_html=True)
        else: st.success("Estructura OK")

    with col_nomina:
        color_nomina = "green" if ratio_planilla < 30 else "orange" if ratio_planilla < 40 else "red"
        st.markdown(f"**Eficiencia Planilla:** {ratio_planilla:.1f}%")
        st.progress(min(ratio_planilla/60, 1.0))
        if color_nomina == "red": st.markdown('<p class="alert-danger">🚨 Estructura obesa.</p>', unsafe_allow_html=True)
        else: st.success("Productividad OK")

    st.markdown("---")
    st.subheader("🔮 Simulador de Rescate")
    c_sim_1, c_sim_2 = st.columns(2)
    with c_sim_1:
        meta_alquiler = st.slider("Reducir Alquiler (%)", 0, 50, 0, step=5)
        meta_planilla = st.slider("Optimizar Planilla (%)", 0, 50, 0, step=5)
    with c_sim_2:
        ahorro = (gasto_alquiler_mes * meta_alquiler/100) + (gasto_planilla_mes * meta_planilla/100)
        nuevo_ebitda = ebitda_mes + ahorro
        st.markdown(f"""<div class="metric-card"><h4>Impacto</h4><p>Ahorro Mensual: <strong style="color:green">+${ahorro:,.2f}</strong></p><p>Nuevo EBITDA: <strong>${nuevo_ebitda:,.2f}</strong></p></div>""", unsafe_allow_html=True)

# TAB 3: SUPERVIVENCIA
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Punto Equilibrio (Mes)", f"${punto_equilibrio_mes:,.2f}")
        if margen_seguridad_mes > 0: st.success(f"✅ Zona Segura: ${margen_seguridad_mes:,.2f}")
        else: st.error(f"🚨 Faltan: ${abs(margen_seguridad_mes):,.2f}")
    with c2:
        pct_safe = (margen_seguridad_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
        fig = go.Figure(go.Indicator(mode="gauge+number", value=pct_safe, title={'text':"Seguridad %"}, gauge={'axis':{'range':[-50,100]}, 'bar':{'color':"green" if pct_safe>10 else "red"}}))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: OXÍGENO
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Ciclo de Caja", f"{ccc:.0f} días")
        if ccc > 0: st.warning(f"Tardas {ccc:.0f} días en recuperar tu dinero.")
        else: st.success("Ciclo Negativo (Financiado).")
    with c2:
        st.markdown(f"""<div class="money-trap"><h4>💸 Efectivo Atrapado</h4><p>Total: <strong>${dinero_atrapado_total:,.2f}</strong></p></div>""", unsafe_allow_html=True)

# TAB 5: VALORACIÓN DE MERCADO
with tab5:
    st.subheader("📈 Calculadora de Valoración")
    ebitda_anualizado = ebitda_mes * 12
    c_input, c_result = st.columns([1, 1])
    
    with c_input:
        st.info("Fórmula: (EBITDA Mes x 12) x Múltiplo")
        st.metric("EBITDA Anualizado", f"${ebitda_anualizado:,.2f}")
        multiplo_seleccionado = st.selectbox("Factor Multiplicador:", options=[2, 3, 4, 5, 6], index=1)
    
    with c_result:
        valor_mercado_final = ebitda_anualizado * multiplo_seleccionado
        if valor_mercado_final > 0:
            st.markdown(f"""<div class="valuation-box" style="text-align: center;"><h3>Tu Empresa Vale:</h3><h1 style="color: #1b5e20;">${valor_mercado_final:,.2f}</h1><p>(EBITDA Anual x {multiplo_seleccionado})</p></div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ EBITDA Negativo.")
    st.markdown("""<div class="legal-footer">* Nota Legal: Estimación basada en Múltiplos. Uso estratégico.</div>""", unsafe_allow_html=True)

# =========================================================
# TAB 6: LABORATORIO DE PRECIOS (3 BLOQUES VERTICALES)
# =========================================================
with tab6:
    st.subheader("🧪 Laboratorio de Ingeniería de Precios")
    st.caption("Calculadora 'Bottom-Up': Define tus costos unitarios para encontrar el precio de venta real.")

    # --- BLOQUE 1: CALCULADORA DE COSTOS (INPUTS) ---
    st.markdown("### 1. Calculadora de Costos Unitarios")
    col_inputs_A, col_inputs_B = st.columns(2)
    
    with col_inputs_A:
        nombre_producto = st.text_input("Nombre del Producto:", placeholder="Ej. Hamburguesa Especial")
        st.markdown("**A. Materiales (Receta)**")
        df_mat = pd.DataFrame([{"Ingrediente": "Insumo 1", "Costo ($)": 0.0}, {"Ingrediente": "Insumo 2", "Costo ($)": 0.0}])
        edited_df = st.data_editor(df_mat, num_rows="dynamic", use_container_width=True)
        costo_materiales = edited_df["Costo ($)"].sum()
        st.write(f"💰 Costo Materiales: **${costo_materiales:,.2f}**")

    with col_inputs_B:
        st.markdown("**B. Mano de Obra y Fijos**")
        salario = st.number_input("Salario Operario ($)", value=600.0)
        horas_mes = st.number_input("Horas Laborales/Mes", value=192)
        mins_unidad = st.number_input("Minutos/Unidad", value=15)
        costo_mod = (salario / (horas_mes*60)) * mins_unidad
        st.write(f"👷 Costo MOD: **${costo_mod:,.2f}**")
        
        capacidad = st.number_input("Capacidad Mensual (Unds)", value=1000)
        gastos_fijos_ref = gastos_operativos_mes if 'gastos_operativos_mes' in locals() else 5000.0
        costo_fijo_u = gastos_fijos_ref / capacidad if capacidad > 0 else 0
        st.write(f"🏭 Costo Fijo Unit.: **${costo_fijo_u:,.2f}**")

    costo_total_u = costo_materiales + costo_mod + costo_fijo_u
    st.info(f"📊 **COSTO TOTAL UNITARIO: ${costo_total_u:,.2f}**")
    st.markdown("---")

    # --- BLOQUE 2: ESTRATEGIA (MÁRGENES) ---
    st.markdown("### 2. Definidor de Estrategia")
    c_strat_1, c_strat_2 = st.columns(2)
    
    with c_strat_1:
        margen_deseado = st.slider("Margen Deseado (%)", 10, 60, 30)
        comision_plat = st.slider("Comisión Plataforma (%)", 0, 40, 5)
    
    with c_strat_2:
        denom = 1 - ((margen_deseado + comision_plat) / 100)
        precio_sugerido = costo_total_u / denom if denom > 0 else 0
        itbms = precio_sugerido * 0.07
        precio_final = precio_sugerido + itbms
        
        st.markdown(f"""
        <div style="background-color: #f1f8e9; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #33691e;">
            <p style="margin:0;">Precio Sugerido</p>
            <h2 style="color: #33691e; margin:0;">${precio_sugerido:,.2f}</h2>
            <p>+ ITBMS: ${itbms:,.2f} | <strong>Total: ${precio_final:,.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Ver Desglose del Dinero"):
        ganancia_real = precio_sugerido * (margen_deseado/100)
        st.write(f"Precio: ${precio_sugerido:,.2f} | Costo: -${costo_total_u:,.2f} | Comis.: -${precio_sugerido*(comision_plat/100):,.2f} | Ganancia: ${ganancia_real:,.2f}")

    st.markdown("---")

    # --- BLOQUE 3: MATRIZ COMPARATIVA ---
    st.markdown("### 3. Matriz de Comparación")
    col_btns_1, col_btns_2 = st.columns([1, 4])
    with col_btns_1:
        if st.button("➕ Agregar Producto"):
            if nombre_producto and precio_sugerido > 0:
                st.session_state.lab_precios.append({
                    "Producto": nombre_producto,
                    "Costo": f"${costo_total_u:,.2f}",
                    "Precio": f"${precio_sugerido:,.2f}",
                    "Margen": f"{margen_deseado}%",
                    "Ganancia": f"${precio_sugerido*(margen_deseado/100):,.2f}"
                })
    with col_btns_2:
        if st.button("🗑️ Borrar Tabla"):
            st.session_state.lab_precios = []
            st.experimental_rerun()

    if len(st.session_state.lab_precios) > 0:
        st.table(pd.DataFrame(st.session_state.lab_precios))
    else:
        st.info("Agrega productos para comparar.")

# --- PDF GENERATOR ---
def create_professional_pdf():
    class PDF(FPDF):
        def header(self):
            self.set_fill_color(21, 101, 192); self.rect(0, 0, 210, 20, 'F')
            self.set_y(5); self.set_font('Arial', 'B', 16); self.set_text_color(255)
            self.cell(0, 10, 'SG CONSULTING | Informe', 0, 1, 'C'); self.ln(10)
    pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Veredicto: {veredicto_final}", 0, 1)
    
    # Valoración en PDF
    m_pdf = multiplo_seleccionado if 'multiplo_seleccionado' in globals() else 3
    val_pdf = (ebitda_mes * 12) * m_pdf
    pdf.cell(0, 10, f"Valoración ({m_pdf}x): ${val_pdf:,.2f}", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar PDF"):
    st.sidebar.download_button("💾 Guardar", data=create_professional_pdf(), file_name="SG_Informe.pdf", mime="application/pdf")
