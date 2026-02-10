import streamlit as st
import plotly.graph_objects as go
import pandas as pdst.tabs
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
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Valoración Patrimonial**")

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
        
    # --- NUEVO INPUT: VALORACIÓN ---
    with st.expander("C. Valoración de Negocio (Nuevo)", expanded=True):
        st.markdown("**El Legado:**")
        multiplo_industria = st.slider("Múltiplo EBITDA (Industria)", 2.0, 6.0, 3.0, 0.5, help="Por cuántos años de utilidad se vende una empresa en tu sector.")

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
# Valoración Actual (Anualizada)
valor_empresa_actual = ebitda * 12 * multiplo_industria if ebitda > 0 else 0

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💎 Cascada", "🚦 Semáforo", "⚖️ Supervivencia", "🫁 Oxígeno", "📈 Valoración", "🧪 Lab de Precios"])

# MÓDULO 1: CASCADA DE POTENCIA + VALORACIÓN (ACTUALIZADO)
# --- REEMPLAZA TODO EL BLOQUE 'with tab1:' CON ESTO ---

with tab1:
    col_main, col_chart = st.columns([1.2, 1])
    
    with col_main:
        # --- 1. SECCIÓN VALORACIÓN (NUEVA - LA MANTENEMOS) ---
        st.markdown("### 🏆 Valoración Patrimonial")
        if valor_empresa_actual > 0:
            st.markdown(f"""
            <div class="valuation-box">
                <h4>Valor Actual de la Empresa:</h4>
                <h1 style="color: #1b5e20;">${valor_empresa_actual:,.2f}</h1>
                <p>Basado en {multiplo_industria}x EBITDA Anual.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Tu empresa hoy vale $0.00 para un inversor (EBITDA Negativo).")
            
        st.markdown("---")
        
        # --- 2. SECCIÓN POTENCIA (RESTAURAMOS EL DISEÑO DE LA FOTO) ---
        st.subheader("Diagnóstico de los 4 Niveles de Potencia")
        
        # NIVEL 1: POTENCIA COMERCIAL
        st.markdown('<div class="power-level-title">Nivel 1: Potencia Comercial (Utilidad Bruta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_bruta:,.2f} (Margen: {margen_bruto:.1f}%)</div>', unsafe_allow_html=True)
        
        if margen_bruto > 30:
            st.markdown('<div class="check-box-success">✅ Modelo de precios y proveedores saludable.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="check-box-warning">⚠️ Margen bajo. Revisa precios o costo de compra.</div>', unsafe_allow_html=True)

        # NIVEL 2: POTENCIA OPERATIVA (EL CORAZÓN)
        st.markdown('<div class="power-level-title">Nivel 2: Potencia Operativa (EBITDA) - El Corazón</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebitda:,.2f} (Margen: {margen_ebitda:.1f}%)</div>', unsafe_allow_html=True)

        if ebitda > 0 and margen_ebitda > 10:
             st.markdown('<div class="check-box-success">✅ El corazón del negocio late fuerte. La operación genera dinero puro.</div>', unsafe_allow_html=True)
        elif ebitda > 0:
             st.markdown('<div class="check-box-warning">⚠️ Genera dinero pero es vulnerable (Margen < 10%).</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 ALERTA ROJA: El negocio quema efectivo.</div>', unsafe_allow_html=True)

        # NIVEL 3: POTENCIA DE ACTIVOS
        st.markdown('<div class="power-level-title">Nivel 3: Potencia de Activos (EBIT)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebit:,.2f} (Margen: {margen_ebit:.1f}%)</div>', unsafe_allow_html=True)

        # NIVEL 4: POTENCIA PATRIMONIAL
        st.markdown('<div class="power-level-title">Nivel 4: Potencia Patrimonial (Utilidad Neta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_neta:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)
        
        if utilidad_neta > 0:
             st.markdown('<div class="check-box-success">✅ Potencia Patrimonial positiva. El dueño gana dinero.</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 El dueño pierde dinero (Revisar Deuda/Impuestos).</div>', unsafe_allow_html=True)

    with col_chart:
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "subtotal", "relative", "relative", "relative", "subtotal", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Ut. Bruta", "Alquiler", "Planilla", "Otros Gastos", "EBITDA", "Otros", "Ut. Neta"],
            y = [ventas_actual, -costo_ventas, utilidad_bruta, -gasto_alquiler, -gasto_planilla, -gasto_otros, ebitda, -(depreciacion+intereses+impuestos), utilidad_neta],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#ef5350"}},
            increasing = {"marker":{"color":"#66bb6a"}},
            totals = {"marker":{"color":"#1565c0"}}
        ))
        fig_waterfall.update_layout(title="Cascada Detallada", showlegend=False, height=600)
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

# ==========================================
# TAB 6: LABORATORIO DE PRECIOS (INGENIERÍA DE MENÚ)
# ==========================================
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
        st.info("Lista los ingredientes y su costo *por la porción usada*.")
        
        # Data Editor simple para ingredientes
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
            horas_mes = st.number_input("Horas Laborales al Mes", value=192, help="Normalmente 48h semanales x 4 semanas")
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
        
        st.write(f"🏭 *Costo Fijo Asignado (Absorción): ${costo_fijo_unitario:,.2f}*")
        
        # COSTO TOTAL UNITARIO
        costo_total_unitario = costo_materiales + costo_mod_unitario + costo_fijo_unitario
        st.markdown("---")
        st.metric("COSTO TOTAL UNITARIO", f"${costo_total_unitario:,.2f}", help="Suma de Materiales + Mano de Obra + Carga Fabril Unitaria")

    # --- BLOQUE 2: ESTRATEGIA DE PRECIO ---
    with col_lab_strategy:
        st.markdown("### 2. Definición de Precio y Margen")
        
        # A. FUGAS (Comisiones)
        comision_plataforma_pct = st.slider("Comisión Plataforma/Tarjeta (%)", 0, 40, 5, help="UberEats, PedidosYa, Tarjeta de Crédito (Sobre Precio Final)")
        
        # B. MARGEN DESEADO
        margen_deseado_pct = st.select_slider(
            "Margen de Ganancia Real Deseado (%)",
            options=[10, 15, 20, 25, 30, 35, 40, 50, 60],
            value=30
        )
        
        # C. FÓRMULA MAESTRA (Backend)
        # Precio = Costo / (1 - (Margen% + Comision%))
        denominador = 1 - ((margen_deseado_pct + comision_plataforma_pct) / 100)
        
        if denominador <= 0:
            st.error("🚨 ERROR MATEMÁTICO: La suma de Margen + Comisión supera el 100%. Es imposible poner precio.")
            precio_sugerido = 0
        else:
            precio_sugerido = costo_total_unitario / denominador
        
        # ITBMS
        impuesto_pct = 0.07 # 7% ITBMS Panamá
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
        
        # DESGLOSE DE DINERO
        ganancia_neta_unitaria = precio_sugerido * (margen_deseado_pct/100)
        pago_comisiones = precio_sugerido * (comision_plataforma_pct/100)
        
        with st.expander("Ver Desglose del Dinero (¿Quién se lleva qué?)"):
            st.write(f"💵 **Ingreso Neto:** ${precio_sugerido:,.2f}")
            st.write(f"🔴 **Menos Costo:** -${costo_total_unitario:,.2f}")
            st.write(f"💳 **Menos Comisión:** -${pago_comisiones:,.2f}")
            st.write(f"🟢 **Ganancia Real:** ${ganancia_neta_unitaria:,.2f}")

    # --- BLOQUE 3: MATRIZ COMPARATIVA (SESSION STATE) ---
    st.markdown("---")
    st.markdown("### 3. Matriz de Comparación de Productos")
    
    col_btn_add, col_btn_clear = st.columns([1, 4])
    
    with col_btn_add:
        if st.button("➕ Agregar a Tabla"):
            if nombre_producto and precio_sugerido > 0:
                # Agregar a la lista en memoria
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

    # Mostrar Tabla si hay datos
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
    
    # --- 0. VEREDICTO PRINCIPAL (NUEVO EN PDF) ---
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, '1. VEREDICTO DE LA ESTRATEGA', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    # Fondo crema para el veredicto
    pdf.set_fill_color(255, 248, 225) 
    pdf.multi_cell(0, 8, veredicto_final, 1, 'L', True)
    pdf.ln(10)

    # --- 1. RESUMEN EJECUTIVO (SEMAFORIZADO) ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. SIGNOS VITALES', 0, 1, 'L')
    pdf.ln(2)
    
    # Tabla de Resumen
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 8, "INDICADOR", 1, 0, 'C', fill=True)
    pdf.cell(40, 8, "RESULTADO", 1, 0, 'C', fill=True)
    pdf.cell(90, 8, "DIAGNOSTICO", 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 10)
    
    # Fila EBITDA
    diag_ebitda = "CRITICO (Inviable)" if ebitda < 0 else "VULNERABLE" if margen_ebitda < 10 else "SALUDABLE"
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

    # --- 3. VALORACIÓN Y DINERO ATRAPADO (NUEVO EN PDF) ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. VALORACION Y EFECTIVO', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Valoración
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 8, f"Valor Actual de la Empresa (Base EBITDA {multiplo_industria}x):", 0, 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(46, 125, 50) # Verde
    pdf.cell(0, 8, f"${valor_empresa_actual:,.2f}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    
    # Dinero Atrapado
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 8, f"Efectivo Atrapado (Facturas + Bodega):", 0, 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(194, 24, 7) # Rojo
    pdf.cell(0, 8, f"${dinero_atrapado_total:,.2f}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    
    # CCC
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 8, f"Ciclo de Conversion de Efectivo:", 0, 0)
    pdf.cell(0, 8, f"{ccc:.0f} dias", 0, 1)

    pdf.ln(5)

    # --- 4. RECOMENDACIONES ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '4. RECOMENDACIONES DE LA ESTRATEGA', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    # Veredicto Alquiler
    veredicto_renta_txt = "Su estructura de local es optima. Mantenga este nivel."
    if ratio_alquiler > 15:
        veredicto_renta_txt = "ALQUILER: El local esta consumiendo su utilidad (Ancla financiera). Renegociar contrato o evaluar reubicacion."
    elif ratio_alquiler > 10:
        veredicto_renta_txt = "ALQUILER: Estructura pesada. Revisar trafico de clientes vs costo."
    pdf.multi_cell(0, 6, veredicto_renta_txt)
    pdf.ln(2)

    # Veredicto Planilla
    veredicto_nomina_txt = "PLANILLA: Su equipo es altamente productivo."
    if ratio_planilla > 40:
        veredicto_nomina_txt = "PLANILLA: Alerta de Estructura Obesa. Su equipo consume demasiado margen bruto. Riesgo alto de insolvencia."
    elif ratio_planilla > 30:
        veredicto_nomina_txt = "PLANILLA: Zona de Vigilancia. Considere automatizar tareas administrativas."
    pdf.multi_cell(0, 6, veredicto_nomina_txt)
    
    # Caja
    if ccc > 0:
        pdf.ln(2)
        pdf.multi_cell(0, 6, f"CAJA: Sus proveedores cobran antes de que usted recupere el dinero. Usted financia la operacion por {ccc:.0f} dias. Accion: Renegociar plazos o Factoring.")

    # --- 5. ADVERTENCIA LEGAL ---
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



