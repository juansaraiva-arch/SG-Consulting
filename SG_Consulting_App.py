import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SG Strategic Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- INICIALIZACIÓN DE MEMORIA (SESSION STATE) ---
if 'lab_precios' not in st.session_state:
    st.session_state.lab_precios = []

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .alert-box { padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid; }
    .alert-danger { background-color: #fdecea; color: #c62828; border-color: #c62828; }
    .alert-warning { background-color: #fff8e1; color: #ef6c00; border-color: #ef6c00; }
    .alert-success { background-color: #e8f5e9; color: #2e7d32; border-color: #2e7d32; }
    
    /* ESTILOS NUEVOS */
    .verdict-box { background-color: #263238; color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 8px solid #ffca28; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .money-trap { background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #c62828; }
    .valuation-box { background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    .veredicto { font-style: italic; font-weight: bold; color: #555; padding: 10px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #333; }
    
    /* NIVELES DE POTENCIA */
    .power-level-title { font-size: 16px; font-weight: bold; color: #42a5f5; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; }
    .power-value { font-size: 22px; font-weight: bold; color: #000000; margin-bottom: 5px; }
    .check-box-success { background-color: #2e7d32; color: white; padding: 10px; border-radius: 5px; font-weight: bold; display: flex; align-items: center; margin-bottom: 15px; }
    .check-box-warning { background-color: #fbc02d; color: black; padding: 10px; border-radius: 5px; font-weight: bold; display: flex; align-items: center; margin-bottom: 15px; }
    .check-box-danger { background-color: #c62828; color: white; padding: 10px; border-radius: 5px; font-weight: bold; display: flex; align-items: center; margin-bottom: 15px; }
    
    /* NOTA LEGAL */
    .legal-footer { font-size: 10px; color: #777; margin-top: 10px; font-style: italic; border-top: 1px solid #ddd; padding-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Valoración Patrimonial**")

# --- BARRA LATERAL: INPUT DE VARIABLES ---
with st.sidebar:
    st.header("1. Configuración")
    
    # SELECTOR DE MODO
    modo_analisis = st.radio(
        "Modo de Datos:", 
        ["Mensual (Flash)", "Anual (Estratega)"],
        help="Mensual: Datos de un solo mes. Anual: Datos acumulados de 12 meses."
    )
    
    st.header("2. Datos Financieros")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        st.info(f"Ingresa los valores {'del MES' if 'Mensual' in modo_analisis else 'TOTALES del AÑO'}.")
        
        # DEFINICIÓN DE VARIABLES _INPUT
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
        # El Balance NO cambia de nombre de variable porque siempre es Saldo Final
        inventario = st.number_input("Inventario (Saldo Final $)", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar (Saldo Final $)", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar (Saldo Final $)", value=10000.0)

# --- LÓGICA DE NORMALIZACIÓN (EL PUENTE ENTRE SIDEBAR Y TABS) ---
if 'modo_analisis' in locals() and "Anual" in modo_analisis:
    divisor = 12
    st.sidebar.success("✅ Modo Anual: Datos convertidos a promedio mensual.")
else:
    divisor = 1

# 1. Normalización de P&L
ventas_mes = ventas_input / divisor
costo_ventas_mes = costo_ventas_input / divisor
gasto_alquiler_mes = gasto_alquiler_input / divisor
gasto_planilla_mes = gasto_planilla_input / divisor
gasto_otros_mes = gasto_otros_input / divisor
gastos_operativos_mes = gasto_alquiler_mes + gasto_planilla_mes + gasto_otros_mes

depreciacion_mes = depreciacion_input / divisor
intereses_mes = intereses_input / divisor
impuestos_mes = impuestos_input / divisor

# --- CÁLCULOS PRINCIPALES ---

# A. Potencia
utilidad_bruta_mes = ventas_mes - costo_ventas_mes
margen_bruto = (utilidad_bruta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebitda_mes = utilidad_bruta_mes - gastos_operativos_mes
margen_ebitda = (ebitda_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebit_mes = ebitda_mes - depreciacion_mes
utilidad_neta_mes = ebit_mes - intereses_mes - impuestos_mes
margen_neto = (utilidad_neta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

# B. Ratios Eficiencia
ratio_alquiler = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
ratio_planilla = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0

# C. Supervivencia
costos_fijos_totales_mes = gastos_operativos_mes + intereses_mes
margen_contribucion_pct = (utilidad_bruta_mes / ventas_mes) if ventas_mes > 0 else 0
punto_equilibrio_mes = costos_fijos_totales_mes / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad_mes = ventas_mes - punto_equilibrio_mes

# D. Oxígeno (CCC)
dias_calle = (cuentas_cobrar / ventas_mes) * 30 if ventas_mes > 0 else 0
dias_inventario = (inventario / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

dinero_atrapado_total = cuentas_cobrar + inventario

# E. Valoración Base (Para Tab 1 - Evita errores)
valor_empresa_actual = (ebitda_mes * 12) * 3 if ebitda_mes > 0 else 0

# --- EL JUEZ DIGITAL ---
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

# --- DASHBOARD VISUAL ---

# Veredicto Principal
st.markdown(f"""
<div class="verdict-box">
    <h3>{icono_veredicto} Veredicto de la Estratega:</h3>
    <p style="font-size: 18px;">"{veredicto_final}"</p>
</div>
""", unsafe_allow_html=True)

# TABS PRINCIPALES (AHORA SON 6)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💎 Cascada", "🚦 Semáforo", "⚖️ Supervivencia", "🫁 Oxígeno", "📈 Valoración", "🧪 Lab de Precios"])

# TAB 1: LOS 4 NIVELES DE POTENCIA
with tab1:
    col_main, col_chart = st.columns([1.2, 1])
    
    with col_main:
        st.subheader("Diagnóstico de los 4 Niveles de Potencia")
        st.caption(f"Datos mostrados en base mensual promedio.")

        # --- SECCIÓN VALORACIÓN BASE ---
        if valor_empresa_actual > 0:
            st.markdown(f"""
            <div class="valuation-box">
                <h4>Valor Ref. de la Empresa (Base 3x):</h4>
                <h1 style="color: #1b5e20;">${valor_empresa_actual:,.2f}</h1>
                <p>Basado en 3.0x EBITDA Anual. <br><em>(Ve a la Pestaña 5 para personalizar el múltiplo)</em></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # NIVEL 1
        st.markdown('<div class="power-level-title">Nivel 1: Potencia Comercial (Utilidad Bruta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_bruta_mes:,.2f} (Margen: {margen_bruto:.1f}%)</div>', unsafe_allow_html=True)
        if margen_bruto > 30:
            st.markdown('<div class="check-box-success">✅ Modelo de precios y proveedores saludable.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="check-box-warning">⚠️ Margen bajo. Revisa precios o costo de compra.</div>', unsafe_allow_html=True)

        # NIVEL 2
        st.markdown('<div class="power-level-title">Nivel 2: Potencia Operativa (EBITDA) - El Corazón</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebitda_mes:,.2f} (Margen: {margen_ebitda:.1f}%)</div>', unsafe_allow_html=True)
        if ebitda_mes > 0 and margen_ebitda > 10:
             st.markdown('<div class="check-box-success">✅ El corazón del negocio late fuerte.</div>', unsafe_allow_html=True)
        elif ebitda_mes > 0:
             st.markdown('<div class="check-box-warning">⚠️ Genera dinero pero es vulnerable (< 10%).</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 ALERTA ROJA: El negocio quema efectivo.</div>', unsafe_allow_html=True)

        # NIVEL 3
        st.markdown('<div class="power-level-title">Nivel 3: Potencia de Activos (EBIT)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebit_mes:,.2f}</div>', unsafe_allow_html=True)

        # NIVEL 4
        st.markdown('<div class="power-level-title">Nivel 4: Potencia Patrimonial (Utilidad Neta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_neta_mes:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)
        if utilidad_neta_mes > 0:
             st.markdown('<div class="check-box-success">✅ El dueño gana dinero.</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 El dueño pierde dinero.</div>', unsafe_allow_html=True)

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
        else: st.success("Estructura Inmobiliaria OK")

    with col_nomina:
        color_nomina = "green" if ratio_planilla < 30 else "orange" if ratio_planilla < 40 else "red"
        st.markdown(f"**Eficiencia Planilla:** {ratio_planilla:.1f}%")
        st.progress(min(ratio_planilla/60, 1.0))
        if color_nomina == "red": st.markdown('<p class="alert-danger">🚨 Estructura obesa.</p>', unsafe_allow_html=True)
        else: st.success("Productividad de Talento OK")

    st.markdown("---")
    st.subheader("🔮 Simulador de Rescate")
    c_sim_1, c_sim_2 = st.columns(2)
    with c_sim_1:
        meta_alquiler = st.slider("Reducir Alquiler (%)", 0, 50, 0, step=5)
        meta_planilla = st.slider("Optimizar Planilla (%)", 0, 50, 0, step=5)
    with c_sim_2:
        ahorro_mensual = (gasto_alquiler_mes * meta_alquiler/100) + (gasto_planilla_mes * meta_planilla/100)
        nuevo_ebitda_proyectado = ebitda_mes + ahorro_mensual
        st.markdown(f"""
        <div class="metric-card">
            <h4>Impacto en Flujo</h4>
            <p>Ahorro Mensual: <strong style="color:green">+${ahorro_mensual:,.2f}</strong></p>
            <p>Nuevo EBITDA Mensual: <strong>${nuevo_ebitda_proyectado:,.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: SUPERVIVENCIA
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Punto de Equilibrio (Mes)", f"${punto_equilibrio_mes:,.2f}")
        if margen_seguridad_mes > 0: st.success(f"✅ Zona Segura por ${margen_seguridad_mes:,.2f}")
        else: st.error(f"🚨 Faltan ${abs(margen_seguridad_mes):,.2f}")
    with col2:
         pct_safe = (margen_seguridad_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
         fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = pct_safe, title={'text':"Seguridad (%)"}, gauge = {'axis': {'range': [-50, 100]}, 'bar': {'color': "green" if pct_safe > 10 else "red"}}))
         fig_gauge.update_layout(height=250)
         st.plotly_chart(fig_gauge, use_container_width=True)

# TAB 4: DINERO ATRAPADO
with tab4:
    col_kpi_cash, col_trap = st.columns(2)
    with col_kpi_cash:
        st.metric("Ciclo de Caja (CCC)", f"{ccc:.0f} días")
        if ccc > 0: st.warning(f"Tardas {ccc:.0f} días en recuperar tu dinero.")
        else: st.success("Ciclo Negativo (Financiado).")
    with col_trap:
        st.markdown(f"""
        <div class="money-trap">
            <h4>💸 Efectivo Atrapado (Foto Balance)</h4>
            <p>En Calle + Bodega: <strong>${dinero_atrapado_total:,.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)

# TAB 5: VALORACIÓN DE MERCADO
with tab5:
    st.subheader("📈 Calculadora de Valoración de Empresa")
    
    # 1. Dato Automático (Backend)
    ebitda_anualizado = ebitda_mes * 12
    
    col_val_input, col_val_result = st.columns([1, 1])
    
    with col_val_input:
        st.info("💡 La Fórmula: (EBITDA Promedio Mensual x 12) x Múltiplo")
        st.metric("EBITDA Anualizado (Base)", f"${ebitda_anualizado:,.2f}")
        
        # 2. Dato Modificable (Dropdown)
        multiplo_seleccionado = st.selectbox(
            "Selecciona el Factor Multiplicador:",
            options=[2, 3, 4, 5, 6],
            index=1, # Default 3x
            help="Industrias tradicionales: 2x-3x. Tecnología/Escalables: 4x-6x."
        )
    
    with col_val_result:
        # 3. Resultado Visual
        valor_mercado_final = ebitda_anualizado * multiplo_seleccionado
        
        if valor_mercado_final > 0:
            st.markdown(f"""
            <div class="valuation-box" style="text-align: center; border: 2px solid #2e7d32; background-color: #f1f8e9;">
                <h3 style="color: #555;">Tu Empresa Vale:</h3>
                <h1 style="font-size: 50px; color: #1b5e20; margin: 0;">${valor_mercado_final:,.2f}</h1>
                <p style="margin-top: 10px; font-weight: bold;">(EBITDA Anual x {multiplo_seleccionado})</p>
            </div>
            """, unsafe_allow_html=True)
            st.success(f"💰 Visión de Estratega: Subir el múltiplo aumenta tu patrimonio.")
        else:
            st.warning("⚠️ No se puede valorar una empresa con EBITDA negativo.")

    st.markdown("""<div class="legal-footer">* Nota Legal: Estimación basada en método de Múltiplos de EBITDA. Uso estrictamente estratégico.</div>""", unsafe_allow_html=True)

# TAB 6: LABORATORIO DE PRECIOS (NUEVO)
with tab6:
    st.subheader("🧪 Laboratorio de Ingeniería de Precios")
    st.caption("Calculadora 'Bottom-Up': Define tus costos unitarios para encontrar el precio de venta real.")

    # --- BLOQUE 1: CALCULADORA DE COSTOS (INPUTS) ---
    col_lab_inputs, col_lab_strategy = st.columns([1, 1.2])
    
    with col_lab_inputs:
        st.markdown("### 1. Estructura de Costos (Unitario)")
        nombre_producto = st.text_input("Nombre del Producto / Servicio:", placeholder="Ej. Hamburguesa Especial")
        
        # A. MATERIALES (Directos)
        st.markdown("**A. Materiales e Insumos**")
        df_materiales_default = pd.DataFrame([
            {"Ingrediente": "Insumo Principal", "Costo ($)": 0.00},
            {"Ingrediente": "Insumo Secundario", "Costo ($)": 0.00},
            {"Ingrediente": "Empaque/Otros", "Costo ($)": 0.00}
        ])
        edited_df = st.data_editor(df_materiales_default, num_rows="dynamic", use_container_width=True)
        costo_materiales = edited_df["Costo ($)"].sum()
        st.write(f"💰 *Costo Materiales: ${costo_materiales:,.2f}*")

        # B. MANO DE OBRA DIRECTA (MOD)
        st.markdown("**B. Mano de Obra Directa (MOD)**")
        with st.expander("Calcular MOD Unitario"):
            salario_operario = st.number_input("Salario Mensual Operario ($)", value=600.0, step=50.0)
            horas_mes = st.number_input("Horas Laborales al Mes", value=192, help="48h semanales x 4 semanas")
            minutos_por_unidad = st.number_input("Minutos para producir 1 unidad", value=15, step=5)
            
            costo_minuto = salario_operario / (horas_mes * 60)
            costo_mod_unitario = costo_minuto * minutos_por_unidad
            st.write(f"⏱️ Costo por Minuto: ${costo_minuto:.3f}")
        st.write(f"👷 *Costo MOD: ${costo_mod_unitario:,.2f}*")

        # C. INDIRECTOS Y FIJOS (Capacidad)
        st.markdown("**C. Asignación de Costos Fijos**")
        gastos_fijos_ref = gastos_operativos_mes if 'gastos_operativos_mes' in locals() else 5000.0
        
        capacidad_mensual = st.number_input("Capacidad de Producción Mensual (Unidades)", value=1000, help="¿Cuántas unidades puedes vender al mes con tu estructura actual?")
        costo_fijo_unitario = gastos_fijos_ref / capacidad_mensual if capacidad_mensual > 0 else 0
        
        st.write(f"🏭 *Costo Fijo Asignado: ${costo_fijo_unitario:,.2f}*")
        
        # COSTO TOTAL UNITARIO
        costo_total_unitario = costo_materiales + costo_mod_unitario + costo_fijo_unitario
        st.markdown("---")
        st.metric("COSTO TOTAL UNITARIO", f"${costo_total_unitario:,.2f}")

    # --- BLOQUE 2: ESTRATEGIA DE PRECIO ---
    with col_lab_strategy:
        st.markdown("### 2. Definición de Precio y Margen")
        
        # A. FUGAS (Comisiones)
        comision_plataforma_pct = st.slider("Comisión Plataforma/Tarjeta (%)", 0, 40, 5)
        
        # B. MARGEN DESEADO
        margen_deseado_pct = st.select_slider(
            "Margen de Ganancia Real Deseado (%)",
            options=[10, 15, 20, 25, 30, 35, 40, 50, 60],
            value=30
        )
        
        # C. FÓRMULA MAESTRA
        denominador = 1 - ((margen_deseado_pct + comision_plataforma_pct) / 100)
        
        if denominador <= 0:
            st.error("🚨 ERROR: Margen + Comisión supera el 100%.")
            precio_sugerido = 0
        else:
            precio_sugerido = costo_total_unitario / denominador
        
        # ITBMS
        impuesto_pct = 0.07
        precio_con_impuesto = precio_sugerido * (1 + impuesto_pct)
        
        # D. VISUALIZACIÓN DEL TICKET
        st.markdown(f"""
        <div style="background-color: #f1f8e9; padding: 20px; border-radius: 10px; border: 2px solid #33691e; text-align: center;">
            <p style="margin:0;">Precio Sugerido (Antes de Impuestos)</p>
            <h1 style="color: #33691e; margin:0;">${precio_sugerido:,.2f}</h1>
            <hr>
            <p style="font-size: 14px;">
            + ITBMS (7%): ${precio_sugerido*impuesto_pct:,.2f}<br>
            <strong>PRECIO FINAL EN ETIQUETA: ${precio_con_impuesto:,.2f}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        ganancia_neta_unitaria = precio_sugerido * (margen_deseado_pct/100)
        pago_comisiones = precio_sugerido * (comision_plataforma_pct/100)
        
        with st.expander("Ver Desglose del Dinero"):
            st.write(f"💵 **Ingreso Neto:** ${precio_sugerido:,.2f}")
            st.write(f"🔴 **Menos Costo:** -${costo_total_unitario:,.2f}")
            st.write(f"💳 **Menos Comisión:** -${pago_comisiones:,.2f}")
            st.write(f"🟢 **Ganancia Real:** ${ganancia_neta_unitaria:,.2f}")

    # --- BLOQUE 3: MATRIZ COMPARATIVA ---
    st.markdown("---")
    st.markdown("### 3. Matriz de Comparación")
    
    col_btn_add, col_btn_clear = st.columns([1, 4])
    
    with col_btn_add:
        if st.button("➕ Agregar a Tabla"):
            if nombre_producto and precio_sugerido > 0:
                st.session_state.lab_precios.append({
                    "Producto": nombre_producto,
                    "Costo Unit.": f"${costo_total_unitario:,.2f}",
                    "Precio Venta": f"${precio_sugerido:,.2f}",
                    "Margen %": f"{margen_deseado_pct}%",
                    "Ganancia $": f"${ganancia_neta_unitaria:,.2f}",
                    "Comisión Plat.": f"{comision_plataforma_pct}%"
                })
                st.success("Agregado")
            else:
                st.warning("Calcula un precio válido primero.")

    with col_btn_clear:
        if st.button("🗑️ Limpiar Tabla"):
            st.session_state.lab_precios = []
            st.experimental_rerun()

    if len(st.session_state.lab_precios) > 0:
        df_comparativo = pd.DataFrame(st.session_state.lab_precios)
        st.table(df_comparativo)
    else:
        st.info("La tabla está vacía. Agrega productos arriba para comparar.")

# ==========================================
# GENERADOR DE REPORTE PROFESIONAL (PDF)
# ==========================================
def create_professional_pdf():
    class PDF(FPDF):
        def header(self):
            self.set_fill_color(21, 101, 192)
            self.rect(0, 0, 210, 20, 'F')
            self.set_y(5); self.set_font('Arial', 'B', 16); self.set_text_color(255, 255, 255)
            self.cell(0, 10, 'SG CONSULTING | Informe Estratégico', 0, 1, 'C'); self.ln(10)
        def footer(self):
            self.set_y(-15); self.set_font('Arial', 'I', 8); self.set_text_color(128)
            self.cell(0, 10, f'Pag {self.page_no()}', 0, 0, 'C')

    pdf = PDF(); pdf.add_page(); pdf.set_auto_page_break(auto=True, margin=15)
    
    # Contenido PDF
    pdf.set_font('Arial', 'B', 14); pdf.set_text_color(0)
    pdf.cell(0, 10, '1. VEREDICTO', 0, 1); pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(255, 248, 225); pdf.multi_cell(0, 8, veredicto_final, 1, 'L', True); pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 14); pdf.cell(0, 10, '2. DIAGNOSTICO DE POTENCIA (BASE MENSUAL)', 0, 1)
    pdf.set_font('Arial', '', 11)
    # Tabla simple
    pdf.cell(60, 8, "Nivel", 1); pdf.cell(40, 8, "Resultado", 1); pdf.cell(90, 8, "Estado", 1, 1)
    pdf.cell(60, 8, "1. Comercial (Bruta)", 1); pdf.cell(40, 8, f"${utilidad_bruta_mes:,.0f}", 1); pdf.cell(90, 8, "Saludable" if margen_bruto > 30 else "Revisar", 1, 1)
    pdf.cell(60, 8, "2. Operativa (EBITDA)", 1); pdf.cell(40, 8, f"${ebitda_mes:,.0f}", 1); pdf.cell(90, 8, "Fuerte" if ebitda_mes > 0 else "CRITICO", 1, 1)
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 14); pdf.cell(0, 10, '3. VALORACION DE MERCADO', 0, 1)
    
    # Recálculo para PDF
    multiplo_pdf = multiplo_seleccionado if 'multiplo_seleccionado' in globals() else 3
    val_estimado_pdf = (ebitda_mes * 12) * multiplo_pdf
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"EBITDA Anualizado: ${(ebitda_mes*12):,.2f}", 0, 1)
    pdf.cell(0, 8, f"Multiplo Aplicado: {multiplo_pdf}x", 0, 1)
    pdf.set_font('Arial', 'B', 14); pdf.set_text_color(27, 94, 32)
    pdf.cell(0, 10, f"Valor Estimado: ${val_estimado_pdf:,.2f}", 0, 1)
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, "Estimacion basada en metodo de Multiplos de EBITDA.", 0, 1)
    
    pdf.ln(10); pdf.set_font('Arial', 'I', 8)
    pdf.multi_cell(0, 5, "ADVERTENCIA FIDUCIARIA: Informe de uso interno. El Balance General se comporta diferente al P&L (Foto vs Pelicula).")
    
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
