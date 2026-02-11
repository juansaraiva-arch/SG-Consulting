import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# ==========================================
# CONFIGURACIÓN INICIAL Y ESTILOS
# ==========================================
st.set_page_config(page_title="SG Consulting | Máquina de Verdad Financiera", layout="wide", initial_sidebar_state="expanded")

# Inicialización de Memoria (Session State)
if 'lab_precios' not in st.session_state:
    st.session_state.lab_precios = []

# ESTILOS CSS (DISEÑO VISUAL RECUPERADO)
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

    /* Estilos Nuevos V2.5 */
    .verdict-box { background-color: #263238; color: #ffffff; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 8px solid #ffca28; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .money-trap { background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #c62828; }
    .valuation-box { background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1565c0; }
    .legal-footer { font-size: 10px; color: #777; margin-top: 10px; font-style: italic; border-top: 1px solid #ddd; padding-top: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SG Consulting | La Máquina de Verdad Financiera")
st.markdown("**Versión 2.5:** Diagnóstico Flash, Tendencias 'Mandíbulas', Valoración Patrimonial e Ingeniería de Precios.")

# ==========================================
# BARRA LATERAL: MOTOR DE MODOS (A/B)
# ==========================================
with st.sidebar:
    st.header("1. Modo de Operación")
    
    # SELECTOR DE MODO
    modo_operacion = st.radio(
        "Selecciona el Terreno de Batalla:",
        ["Modo A: Diagnóstico Flash (Foto)", "Modo B: Estratega (Película)"],
        index=0,
        help="Flash: Input manual de un mes. Estratega: Carga masiva de 12 meses (Excel)."
    )
    
    st.header("2. Alimentación de Datos")
    
    # --- VARIABLES GLOBALES INICIALES ---
    ventas_mes = 0.0
    costo_ventas_mes = 0.0
    gasto_alquiler_mes = 0.0
    gasto_planilla_mes = 0.0
    gasto_otros_mes = 0.0
    depreciacion_mes = 0.0
    intereses_mes = 0.0
    impuestos_mes = 0.0
    
    df_historico = None 

    # --- LÓGICA MODO A: FLASH (INPUT MANUAL) ---
    if modo_operacion == "Modo A: Diagnóstico Flash (Foto)":
        st.info("📸 **Modo Flash:** Ingresa los datos de un mes representativo.")
        
        with st.expander("Datos del P&L (Mes)", expanded=True):
            ventas_mes = st.number_input("Ventas Totales ($)", value=50000.0, step=1000.0)
            costo_ventas_mes = st.number_input("Costo de Ventas (Variable)", value=30000.0, step=1000.0)
            st.markdown("**Gastos Operativos (OPEX):**")
            gasto_alquiler_mes = st.number_input("1. Alquiler + CAM", value=5000.0, step=100.0)
            gasto_planilla_mes = st.number_input("2. Planilla Total", value=8000.0, step=500.0)
            gasto_otros_mes = st.number_input("3. Otros Gastos", value=2000.0, step=100.0)
            st.markdown("---")
            depreciacion_mes = st.number_input("Depreciación", value=2000.0, step=100.0)
            intereses_mes = st.number_input("Intereses", value=1000.0, step=100.0)
            impuestos_mes = st.number_input("Impuestos", value=1500.0, step=100.0)

    # --- LÓGICA MODO B: ESTRATEGA (CARGA EXCEL) ---
    else:
        st.info("🎥 **Modo Estratega:** Analizamos la tendencia de 12 meses.")
        
        data_plantilla = {
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            'Ventas': [50000]*12, 'Costo_Ventas': [30000]*12,
            'Alquiler': [5000]*12, 'Planilla': [8000]*12, 'Otros_Gastos': [2000]*12,
            'Depreciacion': [2000]*12, 'Intereses': [1000]*12, 'Impuestos': [1500]*12
        }
        df_plantilla = pd.DataFrame(data_plantilla)
        csv = df_plantilla.to_csv(index=False).encode('utf-8')
        
        st.download_button("⬇️ Descargar Plantilla Excel (CSV)", data=csv, file_name="plantilla_sg_consulting.csv", mime="text/csv")
        
        archivo_subido = st.file_uploader("Sube tu archivo (CSV) con 12 meses", type=['csv'])
        
        if archivo_subido is not None:
            try:
                df_historico = pd.read_csv(archivo_subido)
                st.success("✅ Datos cargados exitosamente")
                
                # CÁLCULO DE PROMEDIOS PARA ALIMENTAR LA CASCADA
                ventas_mes = df_historico['Ventas'].mean()
                costo_ventas_mes = df_historico['Costo_Ventas'].mean()
                gasto_alquiler_mes = df_historico['Alquiler'].mean()
                gasto_planilla_mes = df_historico['Planilla'].mean()
                gasto_otros_mes = df_historico['Otros_Gastos'].mean()
                depreciacion_mes = df_historico['Depreciacion'].mean()
                intereses_mes = df_historico['Intereses'].mean()
                impuestos_mes = df_historico['Impuestos'].mean()
                
            except Exception as e:
                st.error(f"Error leyendo el archivo: {e}")
                st.stop()
        else:
            st.warning("⚠️ Esperando archivo... (Se usarán datos demo)")
            ventas_mes = 50000.0
            costo_ventas_mes = 30000.0
            gasto_alquiler_mes = 5000.0
            gasto_planilla_mes = 8000.0
            gasto_otros_mes = 2000.0
            depreciacion_mes = 2000.0
            intereses_mes = 1000.0
            impuestos_mes = 1500.0

# --- BALANCE GENERAL (ACTUALIZADO PARA SOLVENCIA) ---
    with st.expander("Balance General (Saldos & Deuda)", expanded=True):
        st.caption("FOTO ACTUAL (Liquidez y Obligaciones)")
        caja = st.number_input("Caja y Bancos ($)", value=5000.0, help="Dinero disponible ya.")
        cuentas_cobrar = st.number_input("Cuentas por Cobrar ($)", value=15000.0)
        inventario = st.number_input("Inventario ($)", value=20000.0)
        st.markdown("---")
        cuentas_pagar = st.number_input("Cuentas por Pagar (Proveedores) ($)", value=10000.0)
        deuda_bancaria = st.number_input("Deuda Bancaria Total ($)", value=15000.0)
    
    # --- MULTIPLO PARA SIMULADOR GLOBAL ---
    multiplo_global = st.number_input("Múltiplo EBITDA (Ref. Global)", value=3.0, step=0.5)

# ==========================================
# CÁLCULOS CENTRALES (BACKEND)
# ==========================================
gastos_operativos_mes = gasto_alquiler_mes + gasto_planilla_mes + gasto_otros_mes

# 1. Potencia
utilidad_bruta_mes = ventas_mes - costo_ventas_mes
margen_bruto = (utilidad_bruta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebitda_mes = utilidad_bruta_mes - gastos_operativos_mes
margen_ebitda = (ebitda_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

ebit_mes = ebitda_mes - depreciacion_mes
utilidad_neta_mes = ebit_mes - intereses_mes - impuestos_mes
margen_neto = (utilidad_neta_mes / ventas_mes) * 100 if ventas_mes > 0 else 0

# 2. Ratios
ratio_alquiler = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
ratio_planilla = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0

# 3. Supervivencia
costos_fijos_totales_mes = gastos_operativos_mes + intereses_mes
margen_contribucion_pct = (utilidad_bruta_mes / ventas_mes) if ventas_mes > 0 else 0
punto_equilibrio_mes = costos_fijos_totales_mes / margen_contribucion_pct if margen_contribucion_pct > 0 else 0
margen_seguridad_mes = ventas_mes - punto_equilibrio_mes

# 4. Oxígeno (CCC)
dias_calle = (cuentas_cobrar / ventas_mes) * 30 if ventas_mes > 0 else 0
dias_inventario = (inventario / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
dias_proveedor = (cuentas_pagar / costo_ventas_mes) * 30 if costo_ventas_mes > 0 else 0
ccc = dias_calle + dias_inventario - dias_proveedor
dinero_atrapado_total = cuentas_cobrar + inventario

# 5. Valoración Actual Base
valor_empresa_actual_base = (ebitda_mes * 12) * multiplo_global

# 6. Juez Digital
veredicto_final = ""
icono_veredicto = "⚖️"
if ebitda_mes < 0:
    veredicto_final = "INTERVENCIÓN DE EMERGENCIA. El negocio consume capital. Problema estructural."
    icono_veredicto = "🚨"
elif ccc > 60:
    veredicto_final = "AGUJERO NEGRO. Rentable pero insolvente. Prioridad: Cobrar."
    icono_veredicto = "🕳️"
elif ratio_alquiler > 15:
    veredicto_final = "RIESGO INMOBILIARIO. Trabajas para pagar el local."
    icono_veredicto = "🏢"
else:
    veredicto_final = "EMPRESA SALUDABLE Y ESCALABLE. Listo para crecer."
    icono_veredicto = "✅"

# ==========================================
# DASHBOARD VISUAL (TABS)
# ==========================================

st.markdown(f"""<div class="verdict-box"><h3>{icono_veredicto} Veredicto de la Estratega:</h3><p style="font-size: 18px;">"{veredicto_final}"</p></div>""", unsafe_allow_html=True)

# TABS PRINCIPALES
tabs = st.tabs(["💎 Cascada", "🦈 Mandíbulas (Tendencia)", "🚦 Semáforo & Simulador", "⚖️ Supervivencia", "🫁 Oxígeno", "🏆 Valoración V2.5", "🧪 Lab Precios"])

# --- TAB 1: CASCADA (DIAGNÓSTICO FOTO) ---
with tabs[0]:
    col_main, col_chart = st.columns([1.2, 1])
    with col_main:
        st.subheader("Diagnóstico de Potencia (Foto Promedio)")
        
        st.markdown('<div class="power-level-title">Nivel 1: Potencia Comercial (Bruta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_bruta_mes:,.2f} (Margen: {margen_bruto:.1f}%)</div>', unsafe_allow_html=True)
        if margen_bruto > 30: st.markdown('<div class="check-box-success">✅ Modelo Saludable.</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="check-box-warning">⚠️ Margen Bajo.</div>', unsafe_allow_html=True)

        st.markdown('<div class="power-level-title">Nivel 2: Potencia Operativa (EBITDA)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebitda_mes:,.2f} (Margen: {margen_ebitda:.1f}%)</div>', unsafe_allow_html=True)
        if ebitda_mes > 0 and margen_ebitda > 10: st.markdown('<div class="check-box-success">✅ Corazón Fuerte.</div>', unsafe_allow_html=True)
        elif ebitda_mes > 0: st.markdown('<div class="check-box-warning">⚠️ Vulnerable.</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="check-box-danger">🚨 Quema Efectivo.</div>', unsafe_allow_html=True)

        st.markdown('<div class="power-level-title">Nivel 3: Potencia Activos (EBIT)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebit_mes:,.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="power-level-title">Nivel 4: Potencia Patrimonial (Neta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_neta_mes:,.2f} (Margen: {margen_neto:.1f}%)</div>', unsafe_allow_html=True)

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
        fig_waterfall.update_layout(title="Cascada Detallada", height=600)
        st.plotly_chart(fig_waterfall, use_container_width=True)

# --- TAB 2: LAS MANDÍBULAS (TENDENCIAS ACTUALIZADAS V2.5) ---
with tabs[1]:
    st.subheader("🦈 Diagnóstico de Divergencia: Ventas vs Costos vs Utilidad")
    
    if modo_operacion == "Modo A: Diagnóstico Flash (Foto)":
        st.warning("⚠️ Esta visualización requiere datos históricos. Por favor, usa el 'Modo B: Estratega' subiendo un archivo CSV.")
    elif df_historico is not None:
        # 1. Preparación de Datos
        df = df_historico.copy()
        df['Costos_Totales'] = df['Costo_Ventas'] + df['Alquiler'] + df['Planilla'] + df['Otros_Gastos']
        df['Utilidad_Neta'] = df['Ventas'] - df['Costos_Totales']
        
        # 2. Lógica para el sombreado de "Ineficiencia" (Red > Blue)
        # Creamos una serie que solo contenga valores cuando los costos superan las ventas
        df['Costos_Exceso'] = df.apply(lambda x: x['Costos_Totales'] if x['Costos_Totales'] > x['Ventas'] else x['Ventas'], axis=1)

        fig_jaws = go.Figure()

        # A. BARRAS DE UTILIDAD (Base)
        fig_jaws.add_trace(go.Bar(
            x=df['Mes'], 
            y=df['Utilidad_Neta'],
            name='Spread (Utilidad)',
            marker_color=['#66bb6a' if u > 0 else '#ffa726' for u in df['Utilidad_Neta']],
            opacity=0.6,
            hovertemplate='Mes: %{x}<br>Utilidad: $%{y:,.2f}<extra></extra>'
        ))

        # B. LÍNEA DE VENTAS (Top Line)
        fig_jaws.add_trace(go.Scatter(
            x=df['Mes'], y=df['Ventas'],
            mode='lines+markers',
            name='Ventas',
            line=dict(color='#1565c0', width=4),
            hovertemplate='Ventas: $%{y:,.2f}'
        ))

        # C. LÍNEA DE COSTOS CON SOMBREADO
        fig_jaws.add_trace(go.Scatter(
            x=df['Mes'], y=df['Costos_Totales'],
            mode='lines+markers',
            name='Costos Totales',
            line=dict(color='#c62828', width=4),
            fill='tonexty', # Sombrea hacia la línea de ventas (que debe estar antes en el código)
            fillcolor='rgba(198, 40, 40, 0.2)', 
            hovertemplate='Costos: $%{y:,.2f}'
        ))

        # 3. DETECCIÓN DEL PUNTO DE INEFICIENCIA
        # Buscamos el primer mes donde Costos > Ventas
        punto_quiebre = df[df['Costos_Totales'] > df['Ventas']].first_valid_index()
        
        if punto_quiebre is not None:
            mes_q = df.loc[punto_quiebre, 'Mes']
            valor_q = df.loc[punto_quiebre, 'Costos_Totales']
            
            fig_jaws.add_annotation(
                x=mes_q, y=valor_q,
                text="⚠️ Punto de Ineficiencia",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#c62828",
                ax=0, ay=-40,
                font=dict(color="#ffffff", size=12),
                bgcolor="#c62828"
            )

        # Configuración del Layout
        fig_jaws.update_layout(
            height=600,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=80, b=20),
            hovermode="x unified",
            yaxis_title="Monto Financiero ($)"
        )

        st.plotly_chart(fig_jaws, use_container_width=True)
        
        st.info("""
        **Guía de Lectura:**
        * **Barras Verdes/Naranjas:** Representan el 'oxígeno' real que queda después de pagar todo.
        * **Sombreado Rojo:** Es la 'zona de quema'. Si las líneas se cruzan, estás en deseconomía de escala: vender más te está haciendo más pobre.
        """)

# --- TAB 3: SEMÁFORO & SIMULADOR (RECUPERADO VISUALMENTE) ---
with tabs[2]:
    st.subheader("🚦 Semáforo de Eficiencia y Veredictos")
    col_renta, col_nomina = st.columns(2)

    # --- INDICADOR DE ALQUILER (GAUGE) ---
    with col_renta:
        color_renta = "green"
        mensaje_renta = "✅ Estructura Óptima."
        if ratio_alquiler >= 10 and ratio_alquiler <= 15:
            color_renta = "orange"; mensaje_renta = "⚠️ Estructura Pesada."
        elif ratio_alquiler > 15:
            color_renta = "red"; mensaje_renta = "🚨 ALERTA CRÍTICA (Ancla)."

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
        fig_gauge_renta.update_layout(height=250)
        st.plotly_chart(fig_gauge_renta, use_container_width=True)
        st.markdown(f'<div class="veredicto">{mensaje_renta}</div>', unsafe_allow_html=True)

    # --- INDICADOR DE PLANILLA (GAUGE) ---
    with col_nomina:
        color_nomina = "green"
        mensaje_nomina = "✅ Productivo."
        if ratio_planilla >= 30 and ratio_planilla <= 40:
            color_nomina = "orange"; mensaje_nomina = "⚠️ Zona Vigilancia."
        elif ratio_planilla > 40:
            color_nomina = "red"; mensaje_nomina = "🚨 ALERTA OBESA."

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
        fig_gauge_nomina.update_layout(height=250)
        st.plotly_chart(fig_gauge_nomina, use_container_width=True)
        st.markdown(f'<div class="veredicto">{mensaje_nomina}</div>', unsafe_allow_html=True)

    # --- SIMULADOR DE RESCATE (RECUPERADO) ---
    st.markdown("---")
    st.subheader("🔮 Simulador de Rescate: 'La Palanca de Futuro'")
    
    col_sim_controls, col_sim_results = st.columns(2)

    with col_sim_controls:
        st.write("**Metas de Reducción:**")
        meta_alquiler = st.slider("Reducir Alquiler en (%):", 0, 50, 0, step=5)
        meta_planilla = st.slider("Optimizar Planilla en (%):", 0, 50, 0, step=5)

    with col_sim_results:
        # Cálculos de Simulación
        ahorro_alquiler = gasto_alquiler_mes * (meta_alquiler/100)
        ahorro_planilla = gasto_planilla_mes * (meta_planilla/100)
        total_recuperado_mes = ahorro_alquiler + ahorro_planilla
        
        nuevo_ebitda = ebitda_mes + total_recuperado_mes
        nuevo_valor_empresa = nuevo_ebitda * 12 * multiplo_global
        plusvalia = nuevo_valor_empresa - valor_empresa_actual_base

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

# --- TAB 4: SUPERVIVENCIA (índice 3) ---
# --- TAB 4: SUPERVIVENCIA (MAPA GRÁFICO CON META) ---
with tabs[3]:
    st.subheader("⚖️ Mapa de Supervivencia & Metas")

    # 1. PREPARACIÓN DE DATOS
    # Recálculo de ratios
    if ventas_mes > 0:
        cv_ratio = costo_ventas_mes / ventas_mes
        mc_ratio = 1 - cv_ratio # Margen de Contribución %
    else:
        cv_ratio = 0
        mc_ratio = 0

    # 2. ESTRUCTURA DE COLUMNAS
    col_kpi, col_graph = st.columns([1, 2.5])

    with col_kpi:
        # --- INPUT DE META (NUEVO) ---
        st.markdown("### 🎯 Define tu Objetivo")
        ganancia_deseada = st.number_input("¿Cuánto quieres ganar al mes? ($)", value=0.0, step=500.0)
        
        # CÁLCULO DE VENTA NECESARIA
        # Fórmula: (Fijos + Ganancia) / Margen Contribución
        if mc_ratio > 0:
            ventas_meta = (costos_fijos_totales_mes + ganancia_deseada) / mc_ratio
        else:
            ventas_meta = 0

        st.markdown("---")
        
        # KPI Numérico Principal
        st.metric("🧱 Punto de Equilibrio (Min)", f"${punto_equilibrio_mes:,.0f}")
        
        if ganancia_deseada > 0:
            st.metric("🏆 Venta para tu Meta", f"${ventas_meta:,.0f}", delta=f"${ventas_meta - ventas_mes:,.0f} vs Actual", delta_color="normal")
        else:
            st.metric("💵 Ventas Actuales", f"${ventas_mes:,.0f}")

        # Análisis de Estado Actual
        diferencia = ventas_mes - punto_equilibrio_mes
        if diferencia > 0:
            st.success(f"Estás en **ZONA DE UTILIDAD** (+${diferencia:,.0f}).")
        elif diferencia == 0:
            st.warning("Estás en **TABLAS**.")
        else:
            st.error(f"Estás en **ZONA DE PÉRDIDA** (-${abs(diferencia):,.0f}).")

    with col_graph:
        # 3. LÓGICA DEL GRÁFICO
        # Definir Rango de Proyección (Eje X) para incluir la Meta
        max_x = max(ventas_mes, punto_equilibrio_mes, ventas_meta) * 1.25
        if max_x == 0: max_x = 1000

        # Coordenadas
        eje_x = [0, max_x]
        y_ventas = [0, max_x]
        y_fijos = [costos_fijos_totales_mes, costos_fijos_totales_mes]
        y_totales = [costos_fijos_totales_mes, costos_fijos_totales_mes + (max_x * cv_ratio)]

        fig_be = go.Figure()

        # A. ZONAS DE SOMBRA (Pérdida/Ganancia)
        if punto_equilibrio_mes > 0:
            # Zona Roja
            fig_be.add_trace(go.Scatter(
                x=[0, punto_equilibrio_mes, punto_equilibrio_mes, 0],
                y=[costos_fijos_totales_mes, punto_equilibrio_mes, 0, 0],
                fill='toself', mode='none', name='Zona Pérdida',
                fillcolor='rgba(239, 83, 80, 0.1)', hoverinfo='skip'
            ))
            # Zona Verde
            y_fin_ventas = max_x
            y_fin_costos = costos_fijos_totales_mes + (max_x * cv_ratio)
            fig_be.add_trace(go.Scatter(
                x=[punto_equilibrio_mes, max_x, max_x, punto_equilibrio_mes],
                y=[punto_equilibrio_mes, y_fin_ventas, y_fin_costos, punto_equilibrio_mes],
                fill='toself', mode='none', name='Zona Ganancia',
                fillcolor='rgba(102, 187, 106, 0.1)', hoverinfo='skip'
            ))

        # B. LÍNEAS ESTRUCTURALES
        fig_be.add_trace(go.Scatter(x=eje_x, y=y_fijos, mode='lines', name='Costos Fijos', line=dict(color='firebrick', width=2, dash='dash')))
        fig_be.add_trace(go.Scatter(x=eje_x, y=y_totales, mode='lines', name='Costo Total', line=dict(color='orange', width=3)))
        fig_be.add_trace(go.Scatter(x=eje_x, y=y_ventas, mode='lines', name='Ventas', line=dict(color='royalblue', width=4)))

        # C. MARCADORES
        # 1. Punto de Equilibrio
        if punto_equilibrio_mes > 0:
            fig_be.add_trace(go.Scatter(
                x=[punto_equilibrio_mes], y=[punto_equilibrio_mes],
                mode='markers', name='Punto de Equilibrio',
                marker=dict(size=10, color='white', line=dict(color='black', width=2))
            ))

        # 2. Realidad Actual
        fig_be.add_trace(go.Scatter(
            x=[ventas_mes], y=[ventas_mes],
            mode='markers', name='Tu Realidad',
            marker=dict(size=15, color='green' if ventas_mes >= punto_equilibrio_mes else 'red', symbol='diamond'),
            hovertemplate='Hoy: $%{x:,.0f}<extra></extra>'
        ))

        # D. LÍNEA DE META (NUEVO FEATURE)
        if ganancia_deseada > 0 and ventas_meta > 0:
            # Línea Vertical
            fig_be.add_vline(x=ventas_meta, line_width=2, line_dash="dot", line_color="purple")
            
            # Marcador de Meta
            fig_be.add_trace(go.Scatter(
                x=[ventas_meta], y=[ventas_meta],
                mode='markers+text', name='META DESEADA',
                text=["🏆"], textposition="top center",
                marker=dict(size=15, color='purple', symbol='star'),
                hovertemplate='Meta: $%{x:,.0f}<br>Ganancia: $' + f'{ganancia_deseada:,.0f}<extra></extra>'
            ))
            
            # Anotación
            fig_be.add_annotation(
                x=ventas_meta, y=0,
                text=f"Meta: ${ventas_meta:,.0f}",
                showarrow=False, yshift=10, font=dict(color="purple")
            )

        # Configuración Final
        fig_be.update_layout(
            title="Mapa de Navegación Financiera",
            xaxis_title="Ventas ($)", yaxis_title="Dinero ($)",
            height=500, template="plotly_white",
            legend=dict(orientation="h", y=1.1)
        )

        st.plotly_chart(fig_be, use_container_width=True)
        
# --- TAB 5: OXÍGENO & SOLVENCIA (ACTUALIZADO) ---
with tabs[4]:
    st.subheader("🫁 Monitor de Oxígeno: Liquidez y Solvencia")
    
    # --- CÁLCULOS DE SOLVENCIA ---
    # 1. Prueba Ácida
    pasivo_circulante = cuentas_pagar # Asumimos CP es mayormente proveedores para este nivel
    if pasivo_circulante > 0:
        prueba_acida = (caja + cuentas_cobrar) / pasivo_circulante
    else:
        prueba_acida = 0 # Evitar div/0
    
    # 2. Diagnóstico de Reputación (DCP vs Inventario)
    # dias_inventario y dias_proveedor ya vienen calculados del backend
    alerta_reputacion = ""
    if dias_proveedor > 60 and dias_inventario > 60:
        alerta_reputacion = "⚠️ ALERTA DE REPUTACIÓN: Estás financiando inventario estancado a costa de tus proveedores. Riesgo de corte de suministro."
        estilo_alerta = "background-color: #ffebee; border-left: 5px solid #c62828; color: #b71c1c;"
    elif dias_proveedor > 60:
         alerta_reputacion = "⚠️ Cuidado: Estás estirando demasiado los pagos. Revisa tus acuerdos."
         estilo_alerta = "background-color: #fff3e0; border-left: 5px solid #ff9800; color: #e65100;"
    else:
        alerta_reputacion = "✅ Relación sana con proveedores."
        estilo_alerta = "background-color: #e8f5e9; border-left: 5px solid #2e7d32; color: #1b5e20;"

    # --- DISEÑO VISUAL ---
    col_liq, col_pyr = st.columns([1, 1.2])
    
    with col_liq:
        st.markdown("### 1. Ratio de Liquidez (Prueba Ácida)")
        
        # Semáforo de Supervivencia
        color_acida = "green"
        mensaje_acida = ""
        if prueba_acida > 1.1:
            color_acida = "#2e7d32" # Verde
            mensaje_acida = "🟢 TIENES OXÍGENO: Cubres tus deudas hoy sin problemas."
        elif 0.8 <= prueba_acida <= 1.1:
            color_acida = "#fbc02d" # Amarillo
            mensaje_acida = "🟡 AL LÍMITE: Cualquier retraso en cobranza te dejará impago."
        else:
            color_acida = "#c62828" # Rojo
            mensaje_acida = "🔴 INSOLVENCIA TÉCNICA: Debes más de lo que tienes líquido. Reestructuración urgente."

        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid {color_acida}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="color: {color_acida}; font-size: 48px; margin: 0;">{prueba_acida:.2f}</h2>
            <p style="font-weight: bold; color: {color_acida};">{mensaje_acida}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 2. Gestión de Proveedores")
        st.metric("Días Pago Proveedor (DCP)", f"{dias_proveedor:.0f} días", delta=f"{dias_inventario:.0f} días (Inv)", delta_color="inverse", help="Delta compara contra tus días de inventario")
        
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 5px; margin-top: 10px; {estilo_alerta}">
            <strong>Diagnóstico:</strong> {alerta_reputacion}
        </div>
        """, unsafe_allow_html=True)

    with col_pyr:
        st.markdown("### 🏛️ Pirámide de Obligaciones")
        # Preparamos datos para la pirámide
        # Estimamos Patrimonio (Capital Dueño) simplificado para el gráfico
        # Nota: En un balance real, Patrimonio = Activos - Pasivos. Aquí usamos el valor calculado en Tab Valoración o un estimado.
        patrimonio_estimado = (ebitda_mes * 12 * multiplo_global) - deuda_bancaria # Usamos valor empresa como proxy de equity
        if patrimonio_estimado < 0: patrimonio_estimado = 0
        
        fig_pyramid = go.Figure(go.Funnel(
            y = ["Deuda Patrimonial (Dueño)", "Deuda Financiera (Bancos)", "Deuda Operativa (Proveedores)"],
            x = [patrimonio_estimado, deuda_bancaria, cuentas_pagar],
            textinfo = "value+percent total",
            marker = {"color": ["#1565c0", "#f9a825", "#c62828"]},
            connector = {"line": {"color": "rgb(63, 63, 63)", "dash": "dot", "width": 1}}
        ))
        
        fig_pyramid.update_layout(
            title="¿A quién le pertenece el dinero?",
            showlegend=False,
            height=450,
            margin=dict(l=100) # Margen para leer las etiquetas
        )
        st.plotly_chart(fig_pyramid, use_container_width=True)
        
        st.info("💡 **Lectura:** La base (Roja) es la deuda más peligrosa porque paraliza la operación. La cima (Azul) es lo que realmente te pertenece.")

# --- TAB 6: VALORACIÓN V2.5 (PATRIMONIO NETO) ---
with tabs[5]:
    st.subheader("🏆 Motor de Riqueza: Valoración & Legado")
    
    col_prop_1, col_prop_2 = st.columns(2)
    with col_prop_1:
        es_dueno = st.checkbox("¿Cliente es dueño del local?", value=False)
    
    alquiler_virtual = 0.0
    valor_edificio = 0.0
    
    if es_dueno:
        with col_prop_2:
            alquiler_virtual = st.number_input("Alquiler Virtual de Mercado ($)", value=2000.0)
            valor_edificio = st.number_input("Valor Comercial del Edificio ($)", value=250000.0)
    
    ebitda_ajustado = (ebitda_mes - alquiler_virtual) * 12 
    
    st.markdown("---")
    
    col_val_1, col_val_2 = st.columns(2)
    with col_val_1:
        multiplo = st.selectbox("Calidad del Negocio (Múltiplo)", [2, 3, 4, 5, 6], index=1)
        valor_operativo = ebitda_ajustado * multiplo
    with col_val_2:
        if valor_operativo > 0:
            st.markdown(f"""<div class="metric-card"><h4>Valor Operativo (OpCo)</h4><h2 style="color:green">${valor_operativo:,.2f}</h2></div>""", unsafe_allow_html=True)
        else:
            st.error("🚨 El negocio no vale nada (EBITDA Ajustado Negativo).")
            valor_operativo = 0

    st.markdown("---")
    st.subheader("💎 Tu Patrimonio Real (Net Worth)")
    deuda = st.number_input("Deuda Bancaria Total ($)", value=0.0)
    patrimonio = valor_operativo + valor_edificio - deuda
    
    st.markdown(f"""<div class="valuation-box"><h1 style="color: #0d47a1; text-align: center;">${patrimonio:,.2f}</h1><p style="text-align: center;">(Negocio + Edificio - Deuda)</p></div>""", unsafe_allow_html=True)

# --- TAB 7: LAB DE PRECIOS V2.5 ---
with tabs[6]:
    st.subheader("🧪 Lab de Precios (Bottom-Up)")
    
    c1, c2 = st.columns(2)
    with c1:
        producto = st.text_input("Producto:", "Pastel Boda")
        df_mat = pd.DataFrame([{"Item": "Insumos", "Costo": 10.0}])
        edited_df = st.data_editor(df_mat, num_rows="dynamic", use_container_width=True)
        mat = edited_df["Costo"].sum()
    with c2:
        st.markdown("**Mano de Obra (MOD)**")
        salario = st.number_input("Salario Mes", 600.0)
        mins = st.number_input("Minutos x Unidad", 60.0)
        mod = (salario / (192*60)) * mins
        capacidad = st.number_input("Capacidad Mes (Unds)", 500)
        fijos_u = (gastos_operativos_mes / capacidad) if capacidad > 0 else 0
        
    costo_u = mat + mod + fijos_u
    st.info(f"📊 **Costo Real Unitario: ${costo_u:,.2f}** (MOD: ${mod:,.2f})")
    
    st.markdown("---")
    
    c3, c4 = st.columns(2)
    with c3:
        margen = st.slider("Margen Deseado (%)", 10, 90, 30)
        comision = st.slider("Comisión Plataforma (%)", 0, 50, 0)
    with c4:
        denom = 1 - ((margen + comision) / 100)
        if denom > 0:
            precio = costo_u / denom
            itbms = precio * 0.07
            final = precio + itbms
            st.markdown(f"""<div style="border: 2px solid green; padding: 10px; border-radius: 10px; text-align: center;"><h3>Precio Sugerido: ${precio:,.2f}</h3><p>+ ITBMS: ${itbms:,.2f} | <strong>Ticket: ${final:,.2f}</strong></p></div>""", unsafe_allow_html=True)
            if st.button("➕ Agregar a Tabla"):
                st.session_state.lab_precios.append({
                    "Producto": producto, "Costo": f"${costo_u:,.2f}", "Precio": f"${precio:,.2f}", 
                    "Margen": f"{margen}%", "Ganancia": f"${precio*(margen/100):,.2f}"
                })
        else:
            st.error("🚨 Imposible: Margen + Comisión > 100%")

    if st.session_state.lab_precios:
        st.table(pd.DataFrame(st.session_state.lab_precios))
        if st.button("Limpiar"):
            st.session_state.lab_precios = []
            st.experimental_rerun()

# ==========================================
# PDF GENERATOR
# ==========================================
def create_pdf():
    class PDF(FPDF):
        def header(self):
            self.set_fill_color(21, 101, 192); self.rect(0, 0, 210, 20, 'F')
            self.set_y(5); self.set_font('Arial', 'B', 16); self.set_text_color(255)
            self.cell(0, 10, 'SG CONSULTING | Informe V2.5', 0, 1, 'C'); self.ln(10)
    
    pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f"Veredicto: {veredicto_final}", 0, 1)
    pdf.cell(0, 10, f"EBITDA Mes: ${ebitda_mes:,.2f}", 0, 1)
    pdf.cell(0, 10, f"Patrimonio Neto Est.: ${patrimonio if 'patrimonio' in locals() else 0:,.2f}", 0, 1)
    return pdf.output(dest='S').encode('latin-1', 'replace')

st.sidebar.markdown("---")
if st.sidebar.button("📄 Descargar PDF"):
    st.sidebar.download_button("💾 Guardar Informe", data=create_pdf(), file_name="SG_Informe_V2.5.pdf", mime="application/pdf")






