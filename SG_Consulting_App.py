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
    /* NUEVOS ESTILOS PARA LAS NUEVAS FUNCIONES */
    .verdict-box { background-color: #263238; color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 8px solid #ffca28; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .money-trap { background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #c62828; }
    .valuation-box { background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    .veredicto { font-style: italic; font-weight: bold; color: #555; padding: 10px; background-color: #f5f5f5; border-radius: 5px; border-left: 4px solid #333; }
    .level-header { font-size: 18px; font-weight: bold; color: #1565c0; margin-top: 20px; }
    /* --- PEGA ESTO DENTRO DE TU <style> --- */
    
    /* Títulos de Nivel (Azulito como en la foto) */
    .power-level-title { 
        font-size: 16px; 
        font-weight: bold; 
        color: #42a5f5; 
        margin-top: 15px; 
        margin-bottom: 5px; 
        text-transform: uppercase; 
    }
    
    /* Valores Grandes */
    .power-value { 
        font-size: 22px; 
        font-weight: bold; 
        color: #000000; 
        margin-bottom: 5px; 
    }
    
    /* Cajas de Diagnóstico (Verde, Amarillo, Rojo) */
    .check-box-success { 
        background-color: #2e7d32; 
        color: white; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold;
        display: flex; align-items: center;
        margin-bottom: 15px;
    }
    .check-box-warning { 
        background-color: #fbc02d; 
        color: black; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold;
        display: flex; align-items: center;
        margin-bottom: 15px;
    }
    .check-box-danger { 
        background-color: #c62828; 
        color: white; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold;
        display: flex; align-items: center;
        margin-bottom: 15px;
    }
    /* Estilo para la Nota al Pie de Valoración */
    .legal-footer { font-size: 10px; color: #777; margin-top: 10px; font-style: italic; border-top: 1px solid #ddd; padding-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Valoración Patrimonial**")

# --- BARRA LATERAL: INPUT DE VARIABLES ---
# --- BARRA LATERAL: INPUT DE VARIABLES ---
with st.sidebar:
    st.header("1. Configuración")
    
    # SELECTOR DE MODO (CRÍTICO PARA LA LÓGICA DE CÁLCULO)
    modo_analisis = st.radio(
        "Modo de Datos:", 
        ["Mensual (Flash)", "Anual (Estratega)"],
        help="Mensual: Datos de un solo mes. Anual: Datos acumulados de 12 meses."
    )
    
    st.header("2. Datos Financieros")
    
    with st.expander("A. Estado de Resultados (P&L)", expanded=True):
        st.info(f"Ingresa los valores {'del MES' if 'Mensual' in modo_analisis else 'TOTALES del AÑO'}.")
        # Usamos variables temporales (_input) para luego procesarlas
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

# --- PUENTE DE NORMALIZACIÓN (AQUÍ OCURRE LA MAGIA) ---
if "Anual" in modo_analisis:
    divisor = 12
    st.sidebar.success("✅ Modo Anual: P&L convertido a promedio mensual.")
else:
    divisor = 1

# Convertimos inputs anuales a base mensual operativa (SOLO P&L)
ventas_actual = ventas_input / divisor
costo_ventas = costo_ventas_input / divisor
gasto_alquiler = gasto_alquiler_input / divisor
gasto_planilla = gasto_planilla_input / divisor
gasto_otros = gasto_otros_input / divisor
gastos_operativos = gasto_alquiler + gasto_planilla + gasto_otros # Recalculamos total
depreciacion = depreciacion_input / divisor
intereses = intereses_input / divisor
impuestos = impuestos_input / divisor

# NOTA: Inventario, Cuentas por Cobrar y Pagar NO se tocan (Son Saldos).

# --- CÁLCULOS PRINCIPALES (MANTENIENDO TODOS LOS ANTERIORES) ---

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

# CÁLCULOS DE RATIOS DE EFICIENCIA
ratio_alquiler = (gasto_alquiler / ventas_actual) * 100 if ventas_actual > 0 else 0
ratio_planilla = (gasto_planilla / utilidad_bruta) * 100 if utilidad_bruta > 0 else 0

# Puntos de Equilibrio y Caja
costos_fijos_totales = gastos_operativos + intereses 
margen_contribucion_pct = (utilidad_bruta / ventas_actual) if ventas_actual > 0 else 0
punto_equilibrio = costos_fijos_totales / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad = ventas_actual - punto_equilibrio

# CCC (Días)
dias_calle = (cuentas_cobrar / ventas_actual) * 30 if ventas_actual > 0 else 0
dias_inventario = (inventario / costo_ventas) * 30 if costo_ventas > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas) * 30 if costo_ventas > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

# --- NUEVOS CÁLCULOS: VALORACIÓN Y DINERO ATRAPADO ---
# 6. Valoración Actual (CORRECCIÓN TEMPORAL)
# Usamos un múltiplo base de 3x aquí para que el resto de la App (como la Tab 1) no falle.
# La valoración dinámica real controlada por el usuario estará en la Pestaña 5.
valor_empresa_actual = (ebitda * 12) * 3 if ebitda > 0 else 0

# Dinero Atrapado
dinero_atrapado_total = cuentas_cobrar + inventario

# --- EL JUEZ DIGITAL: LOGICA DE VEREDICTO AUTOMÁTICO ---
veredicto_final = ""
icono_veredicto = "⚖️"

if ebitda < 0:
    veredicto_final = "INTERVENCIÓN DE EMERGENCIA NECESARIA. El modelo de negocio está consumiendo capital. Su problema no es de ventas, es estructural. Se requiere corte inmediato de gastos (Cirugía Mayor)."
    icono_veredicto = "🚨"
elif ccc > 60:
    veredicto_final = "SÍNDROME DE 'AGUJERO NEGRO'. Su empresa es rentable (EBITDA Positivo) pero insolvente. Estás financiando a tus clientes con tu propio sudor. Tu prioridad #1 no es vender, es COBRAR."
    icono_veredicto = "🕳️"
elif ratio_alquiler > 15:
    veredicto_final = "RIESGO INMOBILIARIO. Estás trabajando para pagar el local. Tu estructura de costos fijos es demasiado pesada para tu nivel de ventas actual."
    icono_veredicto = "🏢"
else:
    veredicto_final = "EMPRESA SALUDABLE Y ESCALABLE. Tienes control operativo y flujo de caja. Estás listo para invertir en crecimiento o preparar una venta estratégica."
    icono_veredicto = "✅"


# --- DASHBOARD VISUAL ---

# 1. VEREDICTO DE LA ESTRATEGA (AL TOPE - NUEVO)
st.markdown(f"""
<div class="verdict-box">
    <h3>{icono_veredicto} Veredicto de la Estratega:</h3>
    <p style="font-size: 18px;">"{veredicto_final}"</p>
</div>
""", unsafe_allow_html=True)

# TABS PRINCIPALES
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💎 Cascada & Potencia", "🚦 Semáforo & Simulador", "⚖️ Supervivencia", "🫁 Oxígeno & Dinero Atrapado", "📈 Valoración de Mercado"])

# MÓDULO 1: CASCADA DE POTENCIA + VALORACIÓN (ACTUALIZADO)
# --- REEMPLAZA TODO EL BLOQUE 'with tab1:' CON ESTO ---

# TAB 1: LOS 4 NIVELES DE POTENCIA (CORREGIDO)
with tab1:
    col_main, col_chart = st.columns([1.2, 1])
    
    with col_main:
        st.subheader("Diagnóstico de los 4 Niveles de Potencia")
        st.caption(f"Datos mostrados en base mensual promedio.")

        # --- SECCIÓN VALORACIÓN BASE (CORREGIDA) ---
        # Usamos el valor seguro calculado previamente (3x)
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

# MÓDULO 2: SEMÁFORO DE EFICIENCIA & SIMULADOR (CON IMPACTO EN VALOR)
with tab2:
    st.subheader("🚦 Semáforo de Eficiencia y Veredictos")
    col_renta, col_nomina = st.columns(2)

    # --- INDICADOR DE ALQUILER ---
    with col_renta:
        # Definir color y mensaje
        color_renta = "green"
        mensaje_renta = "✅ Estructura Óptima."
        if ratio_alquiler >= 10 and ratio_alquiler <= 15:
            color_renta = "orange"
            mensaje_renta = "⚠️ Estructura Pesada."
        elif ratio_alquiler > 15:
            color_renta = "red"
            mensaje_renta = "🚨 ALERTA CRÍTICA (Ancla)."

        fig_gauge_renta = go.Figure(go.Indicator(
            mode = "gauge+number", value = ratio_alquiler,
            title = {'text': "Ratio Alquiler (%)"},
            gauge = {
                'axis': {'range': [None, 30]},
                'bar': {'color': color_renta},
                'steps': [{'range': [0, 10], 'color': "#e8f5e9"}, {'range': [10, 15], 'color': "#fff3e0"}, {'range': [15, 30], 'color': "#ffebee"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 15}
            }
        ))
        fig_gauge_renta.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge_renta, use_container_width=True)
        st.markdown(f'<div class="veredicto">{mensaje_renta}</div>', unsafe_allow_html=True)

    # --- INDICADOR DE PLANILLA ---
    with col_nomina:
        color_nomina = "green"
        mensaje_nomina = "✅ Productivo."
        if ratio_planilla >= 30 and ratio_planilla <= 40:
            color_nomina = "orange"
            mensaje_nomina = "⚠️ Zona Vigilancia."
        elif ratio_planilla > 40:
            color_nomina = "red"
            mensaje_nomina = "🚨 ALERTA OBESA."

        fig_gauge_nomina = go.Figure(go.Indicator(
            mode = "gauge+number", value = ratio_planilla,
            title = {'text': "Eficiencia Planilla (%)"},
            gauge = {
                'axis': {'range': [None, 60]},
                'bar': {'color': color_nomina},
                'steps': [{'range': [0, 30], 'color': "#e8f5e9"}, {'range': [30, 40], 'color': "#fff3e0"}, {'range': [40, 60], 'color': "#ffebee"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}
            }
        ))
        fig_gauge_nomina.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge_nomina, use_container_width=True)
        st.markdown(f'<div class="veredicto">{mensaje_nomina}</div>', unsafe_allow_html=True)

    # --- SIMULADOR WHAT-IF (MEJORADO CON VALORACIÓN) ---
    st.markdown("---")
    st.subheader("🔮 Simulador de Rescate: 'La Palanca de Futuro'")
    
    col_sim_controls, col_sim_results = st.columns(2)

    with col_sim_controls:
        st.write("**Metas de Reducción:**")
        meta_alquiler = st.slider("Reducir Alquiler en (%):", 0, 50, 0, step=5)
        meta_planilla = st.slider("Optimizar Planilla en (%):", 0, 50, 0, step=5)

    with col_sim_results:
        # Cálculos de Simulación
        ahorro_alquiler = gasto_alquiler * (meta_alquiler/100)
        ahorro_planilla = gasto_planilla * (meta_planilla/100)
        total_recuperado_mes = ahorro_alquiler + ahorro_planilla
        
        nuevo_ebitda = ebitda + total_recuperado_mes
        nuevo_valor_empresa = nuevo_ebitda * 12 * multiplo_industria
        plusvalia = nuevo_valor_empresa - valor_empresa_actual

        st.markdown(f"""
        <div class="metric-card">
            <h4>Impacto Patrimonial</h4>
            <p>Dinero Recuperado (Mes): <strong style="color:green">+${total_recuperado_mes:,.2f}</strong></p>
            <p>Nuevo EBITDA Proyectado: <strong>${nuevo_ebitda:,.2f}</strong></p>
            <hr>
            <h3>Tu Empresa Valdría: <span style="color: #2e7d32">${nuevo_valor_empresa:,.2f}</span></h3>
            <p>Ganancia de Valor (Plusvalía): <strong>+${plusvalia:,.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    if total_recuperado_mes > 0:
        st.success(f"💡 **Pitch de Venta:** 'Bajar estos gastos aumenta tu patrimonio en ${plusvalia:,.0f}. Mi consultoría se paga sola con el primer mes de ahorro'.")

# MÓDULO 3: SUPERVIVENCIA (MANTENIDO)
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

# MÓDULO 4: OXÍGENO & DINERO ATRAPADO (ACTUALIZADO)
with tab4:
    st.subheader("Ciclo de Conversión de Efectivo (CCC)")
    
    col_kpi_cash, col_trap = st.columns(2)
    
    with col_kpi_cash:
        st.metric("Ciclo de Caja (Días)", f"{ccc:.0f} días")
        c1, c2, c3 = st.columns(3)
        c1.metric("Calle", f"{dias_calle:.0f}")
        c2.metric("Inv.", f"{dias_inventario:.0f}")
        c3.metric("Prov.", f"{dias_proveedor:.0f}")
        
        if ccc > 0:
            st.warning(f"Tardas {ccc:.0f} días en recuperar tu dinero.")
        else:
            st.success("Tu ciclo es negativo (Financiado por proveedores).")

    with col_trap:
        # CÁLCULO DE DINERO ATRAPADO (NUEVO VISUAL)
        st.markdown("""
        <div class="money-trap">
            <h4>💸 ¿Dónde está tu dinero? (Efectivo Atrapado)</h4>
            <p>Dinero en la Calle (Clientes): <strong>${:,.2f}</strong></p>
            <p>Dinero en Bodega (Inventario): <strong>${:,.2f}</strong></p>
            <hr>
            <h3>Total Atrapado: <strong>${:,.2f}</strong></h3>
        </div>
        """.format(cuentas_cobrar, inventario, dinero_atrapado_total), unsafe_allow_html=True)
        
        if dinero_atrapado_total > 20000: 
            st.info("💡 **Consultor:** 'No necesitas vender más para tener liquidez, necesitas liberar esos fondos atrapados mediante Factoring o Remates'.")

# TAB 5: VALORACIÓN DE MERCADO (NUEVA PESTAÑA DINÁMICA)
with tab5:
    st.subheader("📈 Calculadora de Valoración de Mercado")
    
    # 1. Backend: Calculamos el EBITDA Anualizado automáticamente
    ebitda_anualizado = ebitda * 12
    
    col_val_input, col_val_result = st.columns([1, 1])
    
    with col_val_input:
        st.info("💡 Fórmula: (EBITDA Promedio Mensual x 12) x Múltiplo")
        st.metric("EBITDA Anualizado (Base)", f"${ebitda_anualizado:,.2f}")
        
        # 2. Frontend: El Selector (Dato Modificable)
        # Aquí creamos el Dropdown que pediste
        multiplo_seleccionado = st.selectbox(
            "Selecciona el Factor Multiplicador:",
            options=[2, 3, 4, 5, 6], # Tus opciones sugeridas
            index=1, # Esto hace que por defecto arranque en '3' (posición 1 de la lista)
            help="Industrias tradicionales: 2x-3x. Tecnología/Escalables: 4x-6x."
        )
    
    with col_val_result:
        # 3. Resultado Visual (Se actualiza en tiempo real al mover el selector)
        valor_mercado_dinamico = ebitda_anualizado * multiplo_seleccionado
        
        if valor_mercado_dinamico > 0:
            st.markdown(f"""
            <div class="valuation-box" style="text-align: center;">
                <h3>Valor Estimado de la Empresa</h3>
                <h1 style="font-size: 48px; color: #1b5e20;">${valor_mercado_dinamico:,.2f}</h1>
                <p>Múltiplo aplicado: <strong>{multiplo_seleccionado}x EBITDA</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No se puede valorar una empresa con EBITDA negativo por este método.")

    # 4. Nota al pie (Tu explicación de mentora)
    st.markdown("""
    <div class="legal-footer">
    * Nota: Estimación basada en método de Múltiplos de EBITDA. Uso estrictamente estratégico. 
    El Balance General se comporta diferente al P&L (Foto vs Película). Esta valoración asume continuidad operativa.
    </div>
    """, unsafe_allow_html=True)
    
# ==========================================
# GENERADOR DE REPORTE PROFESIONAL (ACTUALIZADO)
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
    
    # LÓGICA DE CONEXIÓN:
    # Intentamos tomar el valor del selector (multiplo_seleccionado).
    # Si por alguna razón no está definido (ej. no ha cargado la pestaña), usamos 3 por defecto.
    multiplo_pdf = multiplo_seleccionado if 'multiplo_seleccionado' in globals() else 3
    
    # Calculamos el valor final para el PDF usando ese múltiplo
    val_estimado_pdf = (ebitda * 12) * multiplo_pdf
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"EBITDA Anualizado: ${(ebitda*12):,.2f}", 0, 1)
    pdf.cell(0, 8, f"Multiplo Aplicado: {multiplo_pdf}x", 0, 1)
    
    pdf.set_font('Arial', 'B', 14); pdf.set_text_color(27, 94, 32)
    pdf.cell(0, 10, f"Valor Estimado: ${val_estimado_pdf:,.2f}", 0, 1)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, "Estimacion basada en metodo de Multiplos de EBITDA.", 0, 1)
    
    pdf.ln(10); pdf.set_font('Arial', 'I', 8)
    pdf.multi_cell(0, 5, "ADVERTENCIA FIDUCIARIA: Informe de uso interno. El Balance General se comporta diferente al P&L (Foto vs Pelicula).")
    
    return pdf.output(dest='S').encode('latin-1', 'replace')


