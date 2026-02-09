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
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | Strategic Dashboard")
st.markdown("Diagnóstico basado en **La Cascada de Potencia**, **Semáforos de Eficiencia** y **Valoración Patrimonial**")

# --- BARRA LATERAL: INPUT DE VARIABLES ---
# --- LÓGICA DE NORMALIZACIÓN (EL PUENTE ENTRE SIDEBAR Y TABS) ---
# Detectamos si el usuario eligió Modo Anual para dividir entre 12
if 'modo_analisis' in locals() and "Anual" in modo_analisis:
    divisor = 12
    st.sidebar.success("✅ Modo Anual: Datos convertidos a promedio mensual.")
else:
    divisor = 1

# 1. Normalización de P&L (Todo a Base Mensual para evitar errores)
# Si no existen las variables _input (por si acaso), usamos valores por defecto
try:
    ventas_mes = ventas_input / divisor
    costo_ventas_mes = costo_ventas_input / divisor
    gasto_alquiler_mes = gasto_alquiler_input / divisor
    gasto_planilla_mes = gasto_planilla_input / divisor
    gasto_otros_mes = gasto_otros_input / divisor
    
    depreciacion_mes = depreciacion_input / divisor
    intereses_mes = intereses_input / divisor
    impuestos_mes = impuestos_input / divisor
except NameError:
    # Fallback de seguridad si la barra lateral no se actualizó bien
    ventas_mes = ventas_actual if 'ventas_actual' in locals() else 50000
    costo_ventas_mes = costo_ventas if 'costo_ventas' in locals() else 30000
    gasto_alquiler_mes = gasto_alquiler if 'gasto_alquiler' in locals() else 5000
    gasto_planilla_mes = gasto_planilla if 'gasto_planilla' in locals() else 8000
    gasto_otros_mes = gasto_otros if 'gasto_otros' in locals() else 2000
    depreciacion_mes = 2000
    intereses_mes = 1000
    impuestos_mes = 1500

gastos_operativos_mes = gasto_alquiler_mes + gasto_planilla_mes + gasto_otros_mes

# --- CÁLCULOS PRINCIPALES (AHORA SÍ GENERA LAS VARIABLES _mes) ---

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
# Usamos saldos finales (no se dividen)
inv_final = inventario if 'inventario' in locals() else 20000
cxc_final = cuentas_cobrar if 'cuentas_cobrar' in locals() else 15000
cxp_final = cuentas_pagar if 'cuentas_pagar' in locals() else 10000

dias_calle = (cxc_final / ventas_mes) * 30 if ventas_mes > 0 else 0
dias_inventario = (inv_final / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
dias_proveedor = (cxp_final / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor

dinero_atrapado_total = cxc_final + inv_final

# E. Valoración Base (Para que Tab 1 no falle)
valor_empresa_actual = (ebitda_mes * 12) * 3 if ebitda_mes > 0 else 0

# --- EL JUEZ DIGITAL ---
veredicto_final = ""
icono_veredicto = "⚖️"

if ebitda_mes < 0:
    veredicto_final = "INTERVENCIÓN DE EMERGENCIA NECESARIA. El modelo de negocio está consumiendo capital."
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

# 1. VEREDICTO DE LA ESTRATEGA (AL TOPE - NUEVO)
st.markdown(f"""
<div class="verdict-box">
    <h3>{icono_veredicto} Veredicto de la Estratega:</h3>
    <p style="font-size: 18px;">"{veredicto_final}"</p>
</div>
""", unsafe_allow_html=True)

# TABS PRINCIPALES
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💎 Cascada & Valoración", "🚦 Semáforo & Simulador", "⚖️ Supervivencia", "🫁 Oxígeno & Dinero Atrapado", "📈 Valoración de Mercado"])


# MÓDULO 1: CASCADA DE POTENCIA (CORREGIDO)
with tab1:
    col_main, col_chart = st.columns([1.2, 1])
    
    with col_main:
        # --- 1. SECCIÓN VALORACIÓN BASE (CORREGIDA) ---
        st.markdown("### 🏆 Valoración Patrimonial")
        
        # Aquí estaba el error. Ahora usamos texto fijo porque la variable ya no existe en sidebar.
        if valor_empresa_actual > 0:
            st.markdown(f"""
            <div class="valuation-box">
                <h4>Valor Ref. de la Empresa (Base 3x):</h4>
                <h1 style="color: #1b5e20;">${valor_empresa_actual:,.2f}</h1>
                <p>Basado en 3.0x EBITDA Anual. <br><em>(Ve a la Pestaña 5 para personalizar el múltiplo)</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Tu empresa hoy vale $0.00 para un inversor (EBITDA Negativo).")
            
        st.markdown("---")
        
        # --- 2. SECCIÓN POTENCIA (DISEÑO FOTO) ---
        st.subheader("Diagnóstico de los 4 Niveles de Potencia")
        
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
             st.markdown('<div class="check-box-success">✅ El corazón del negocio late fuerte. La operación genera dinero puro.</div>', unsafe_allow_html=True)
        elif ebitda_mes > 0:
             st.markdown('<div class="check-box-warning">⚠️ Genera dinero pero es vulnerable (Margen < 10%).</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 ALERTA ROJA: El negocio quema efectivo.</div>', unsafe_allow_html=True)

        # NIVEL 3
        st.markdown('<div class="power-level-title">Nivel 3: Potencia de Activos (EBIT)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebit_mes:,.2f}</div>', unsafe_allow_html=True)

        # NIVEL 4
        st.markdown('<div class="power-level-title">Nivel 4: Potencia Patrimonial (Utilidad Neta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_neta_mes:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)
        
        if utilidad_neta_mes > 0:
             st.markdown('<div class="check-box-success">✅ Potencia Patrimonial positiva. El dueño gana dinero.</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="check-box-danger">🚨 El dueño pierde dinero (Revisar Deuda/Impuestos).</div>', unsafe_allow_html=True)

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

# ==========================================
# TAB 5: CALCULADORA DE VALORACIÓN DE MERCADO
# ==========================================
with tab5:
    st.subheader("📈 Calculadora de Valoración de Empresa")
    
    # 1. Lógica del Cálculo (Backend)
    # Tomamos el EBITDA mensual (calculado en la cascada) y lo anualizamos
    ebitda_anualizado = ebitda * 12
    
    col_val_input, col_val_result = st.columns([1, 1])
    
    with col_val_input:
        st.info("💡 La Fórmula: (EBITDA Promedio Mensual x 12) x Múltiplo")
        
        # Dato Automático
        st.metric("EBITDA Mensual Actual", f"${ebitda:,.2f}")
        st.metric("EBITDA Anualizado (Base)", f"${ebitda_anualizado:,.2f}", help="Es tu EBITDA mensual multiplicado por 12 meses.")
        
        st.markdown("---")
        
        # 2. Dato Modificable (El Selector / Dropdown)
        multiplo_seleccionado = st.selectbox(
            "Selecciona el Factor Multiplicador:",
            options=[2, 3, 4, 5, 6], # Opciones sugeridas
            index=1, # El índice 1 es el número '3' (posición: 0, [1], 2, 3...) -> Default 3x
            help="Industrias tradicionales: 2x-3x. Tecnología/Escalables: 4x-6x."
        )
    
    with col_val_result:
        # 3. El Resultado Visual (Cálculo Dinámico)
        # Se actualiza apenas cambias el Dropdown
        valor_mercado_final = ebitda_anualizado * multiplo_seleccionado
        
        if valor_mercado_final > 0:
            st.markdown(f"""
            <div class="valuation-box" style="text-align: center; border: 2px solid #2e7d32; background-color: #f1f8e9;">
                <h3 style="color: #555;">Tu Empresa Vale:</h3>
                <h1 style="font-size: 50px; color: #1b5e20; margin: 0;">${valor_mercado_final:,.2f}</h1>
                <p style="margin-top: 10px; font-weight: bold;">(EBITDA Anual x {multiplo_seleccionado})</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mensaje de refuerzo positivo
            incremento = valor_mercado_final - (ebitda_anualizado * 2) # Comparado contra el escenario pesimista
            st.success(f"💰 **Visión de Estratega:** Subir el múltiplo aumenta tu patrimonio. Una empresa organizada y sin dependencia del dueño vale más (cerca de 5x-6x).")
            
        else:
            st.warning("⚠️ No se puede valorar una empresa con EBITDA negativo por el método de Múltiplos. Primero debemos sanear la operación (Módulo 1).")

    # 4. Nota al pie
    st.markdown("""
    <div style="font-size: 11px; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 5px;">
    * <strong>Nota Legal:</strong> Estimación basada en método de Múltiplos de EBITDA. Uso estrictamente estratégico. 
    El Balance General se comporta de forma totalmente diferente al Estado de Resultados (P&L). 
    Si sumas los Balances de 12 meses, cometerás un error garrafal y la App dará datos locos.
    </div>
    """, unsafe_allow_html=True)


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




