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

# --- TAB 1: CASCADA MAESTRA & DIAGNÓSTICO (ACTUALIZADO) ---
with tabs[0]:
    st.subheader("💎 Cascada de Rentabilidad: La Ruta del Dinero")
    
    # 1. PREPARACIÓN DE DATOS PARA CASCADA
    # Calculamos valores absolutos para graficar
    val_ventas = ventas_mes
    val_cogs = -costo_ventas_mes
    val_bruta = utilidades_bruta_mes = val_ventas + val_cogs
    val_opex = -(gasto_alquiler_mes + gasto_planilla_mes + gasto_otros_mes)
    val_ebitda = val_bruta + val_opex
    val_fin_tax = -(intereses_mes + impuestos_mes + depreciacion_mes) # Agrupamos para simplificar gráfico
    val_neta = val_ebitda + val_fin_tax
    
    # Lógica de colores dinámica
    color_ebitda = "#2e7d32" if val_ebitda > 0 else "#ef6c00" # Verde o Naranja
    color_neta = "#1565c0" if val_neta > 0 else "#c62828"    # Azul o Rojo

    col_chart, col_text = st.columns([2, 1])

    with col_chart:
        # 2. GRÁFICO CASCADA (WATERFALL) - CORREGIDO
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Flujo de Caja", 
            orientation = "v",
            measure = ["relative", "relative", "total", "relative", "total", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Ut. Bruta", "Gastos Op. (OPEX)", "EBITDA (Motor)", "Intereses/Imp", "Ut. Neta"],
            textposition = "outside",
            text = [f"${val_ventas/1000:.1f}k", f"${val_cogs/1000:.1f}k", f"${val_bruta/1000:.1f}k", 
                    f"${val_opex/1000:.1f}k", f"${val_ebitda/1000:.1f}k", f"${val_fin_tax/1000:.1f}k", f"${val_neta/1000:.1f}k"],
            y = [val_ventas, val_cogs, 0, val_opex, 0, val_fin_tax, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            
            # --- CORRECCIÓN DE COLORES ---
            decreasing = {"marker":{"color":"#ef5350"}}, # Rojo suave para salidas de dinero
            increasing = {"marker":{"color":"#1565c0"}}, # Azul para entradas
            totals = {"marker":{"color":"#37474f"}}      # Gris Oscuro (Charcoal) para todos los Totales
        ))
        
        fig_waterfall.update_layout(
            title="De la Venta a la Bolsa (P&L)",
            showlegend=False,
            height=550,
            waterfallgap=0.1
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_text:
        st.markdown("### 🩺 Diagnóstico Automático")
        
        # --- LÓGICA DE DIAGNÓSTICO (CORREGIDA) ---
        mensaje_motor = ""
        margen_ebitda_actual = (val_ebitda / val_ventas) * 100 if val_ventas > 0 else 0
        
        # A. Análisis del Motor (EBITDA)
        if df_historico is not None:
            # CORRECCIÓN: Calculamos EBITDA usando las columnas que SÍ existen
            # EBITDA = Ventas - Costos Variables - Gastos Fijos (Sin contar impuestos/intereses)
            
            # 1. EBITDA del Último Mes (Final)
            ebitda_ultimo = df_historico['Ventas'].iloc[-1] - (
                df_historico['Costo_Ventas'].iloc[-1] + 
                df_historico['Alquiler'].iloc[-1] + 
                df_historico['Planilla'].iloc[-1] + 
                df_historico['Otros_Gastos'].iloc[-1]
            )
            
            # 2. EBITDA del Primer Mes (Inicio)
            ebitda_primero = df_historico['Ventas'].iloc[0] - (
                df_historico['Costo_Ventas'].iloc[0] + 
                df_historico['Alquiler'].iloc[0] + 
                df_historico['Planilla'].iloc[0] + 
                df_historico['Otros_Gastos'].iloc[0]
            )

            crecimiento_ventas = (df_historico['Ventas'].iloc[-1] - df_historico['Ventas'].iloc[0])
            crecimiento_ebitda = ebitda_ultimo - ebitda_primero
            
            # Lógica de comparación
            if crecimiento_ventas > 0 and crecimiento_ebitda <= 0:
                 mensaje_motor = "⚠️ **Tu motor pierde potencia.** Estás vendiendo más, pero ganas menos (EBITDA decreciente). Revisa fugas en costos variables."
            elif crecimiento_ebitda > 0:
                 mensaje_motor = f"🚀 **Motor Acelerando.** Tu EBITDA creció en ${crecimiento_ebitda:,.0f} respecto al inicio del año."
            else:
                 mensaje_motor = f"ℹ️ **Estado del Motor:** Tu margen EBITDA actual es del {margen_ebitda_actual:.1f}%."
        else:
            # Lógica Flash (Estática - Sin cambios)
            if margen_ebitda_actual < 10:
                mensaje_motor = "⚠️ **Motor débil.** Tu margen operativo es muy bajo (<10%). Cualquier error te lleva a pérdidas."
            else:
                mensaje_motor = "✅ **Motor estable.** La operación genera flujo positivo por sí misma."

        # B. Alerta de la Mandíbula (Sin cambios)
        costos_totales_reales = abs(val_cogs) + abs(val_opex)
        mensaje_mandibula = ""
        if costos_totales_reales > val_ventas:
            mensaje_mandibula = "🚨 **ALERTA DE LA MORDIDA:** Estás en la 'Zona de Mordida'. Cada dólar que vendes te cuesta más de un dólar producirlo. **ACCIÓN:** Ve al Lab de Precios YA."
            style_m = "background-color: #ffebee; color: #b71c1c; border-left: 5px solid red;"
        else:
            mensaje_mandibula = "🛡️ **Zona Segura:** Tus ventas cubren tus costos operativos. Mantén la vigilancia en el OPEX."
            style_m = "background-color: #e8f5e9; color: #1b5e20; border-left: 5px solid green;"

        # C. Recomendación de Legado (Sin cambios)
        mensaje_legado = ""
        if margen_ebitda_actual > 15:
            mensaje_legado = "🚀 **EMPRESA ESCALABLE:** Tu negocio es saludable (>15% EBITDA). Tienes capacidad para reinvertir sin desangrar la caja."
        elif val_neta > 0:
            mensaje_legado = "🌱 **EMPRESA EN CRECIMIENTO:** Eres rentable, pero necesitas optimizar antes de escalar agresivamente."
        else:
            mensaje_legado = "🚑 **EMPRESA EN TERAPIA:** Prioridad absoluta: Detener el sangrado de caja. No inviertas en nada nuevo."

        # RENDERIZADO DEL TEXTO
        st.markdown(f"""
        <div style="padding:15px; border-radius:5px; margin-bottom:10px; background-color: #f5f5f5;">
            <strong>1. Análisis del Motor (EBITDA):</strong><br>{mensaje_motor}
        </div>
        
        <div style="padding:15px; border-radius:5px; margin-bottom:10px; {style_m}">
            <strong>2. Alerta de Mandíbula:</strong><br>{mensaje_mandibula}
        </div>
        
        <div style="padding:15px; border-radius:5px; margin-bottom:10px; background-color: #e3f2fd; border-left: 5px solid #1565c0;">
            <strong>3. Veredicto de Legado:</strong><br>{mensaje_legado}
        </div>
        """, unsafe_allow_html=True)
        
        # Guardamos en session state para el PDF
        st.session_state['reporte_motor'] = mensaje_motor
        st.session_state['reporte_mandibula'] = mensaje_mandibula
        st.session_state['reporte_legado'] = mensaje_legado

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


# --- TAB 3: SEMÁFORO DE RIESGOS & PLAN DE CHOQUE (VERSIÓN FINAL INTEGRADA) ---
with tabs[2]:
    st.subheader("🚦 Panel de Control de Riesgos (KPIs Críticos)")
    
    # 1. CÁLCULO DE RATIOS GENERALES
    # A. Alquiler
    ratio_alquiler = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
    # B. Planilla (Sobre Utilidad Bruta)
    ratio_planilla_ub = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0
    # C. Cobertura Bancaria
    if intereses_mes > 0:
        cobertura_bancaria = ebitda_mes / intereses_mes
    else:
        cobertura_bancaria = 10.0
        
    # D. PRUEBA ÁCIDA (MONITOR DE OXÍGENO) - Lógica Nueva
    pasivo_circulante = cuentas_pagar + deuda_bancaria # Asumimos toda la deuda como CP para estrés
    if pasivo_circulante > 0:
        prueba_acida = (caja + cuentas_cobrar) / pasivo_circulante
    else:
        prueba_acida = 0

    # Lógica del Semáforo de Oxígeno
    activar_rescate = False
    if prueba_acida < 1.0:
        color_bg_acida = "#ffebee" # Rojo
        icono_acida = "🔴 Asfixia"
        msj_acida = "¡Alerta Roja! No cubres tus deudas hoy."
        activar_rescate = True
    elif 1.0 <= prueba_acida < 1.5:
        color_bg_acida = "#fff3e0" # Naranja
        icono_acida = "🟡 Vigilancia"
        msj_acida = "Estás al límite. Cuidado con retrasos."
    else:
        color_bg_acida = "#e8f5e9" # Verde
        icono_acida = "🟢 Oxígeno"
        msj_acida = "Tienes liquidez para maniobrar."

    # 2. DEFINICIÓN DE COLUMNAS (Aquí corregimos el NameError)
    c1, c2, c3, c4 = st.columns(4)
    
    # Función auxiliar para tarjetas estándar
    def tarjeta_kpi(col, titulo, valor, sufijo, target, inverso=False):
        # Lógica de color simple
        es_rojo = valor > target if not inverso else valor < target
        color_bg = "#ffebee" if es_rojo else "#e8f5e9"
        icono = "🔴" if es_rojo else "🟢"
        
        col.markdown(f"""
        <div style="background-color: {color_bg}; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 320px;">
            <h4 style="margin:0; font-size: 14px; color: #555;">{titulo}</h4>
            <h2 style="margin:10px 0; font-size: 28px; color: #333;">{valor:.1f}{sufijo}</h2>
            <p style="font-size: 20px; margin: 0;">{icono}</p>
            <hr>
            <small>Meta: {target}{sufijo}</small>
        </div>
        """, unsafe_allow_html=True)

    # 3. RENDERIZADO DE TARJETAS
    tarjeta_kpi(c1, "Eficiencia Alquiler", ratio_alquiler, "%", 15.0)
    tarjeta_kpi(c2, "Peso Nómina (UB)", ratio_planilla_ub, "%", 45.0)
    tarjeta_kpi(c3, "Cobertura Bancos", cobertura_bancaria, "x", 1.5, inverso=True)

    # Tarjeta Especial de Oxígeno (c4)
    with c4:
        st.markdown(f"""
        <div style="background-color: {color_bg_acida}; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="margin:0; font-size: 14px; color: #555;">Capacidad de Pago</h4>
                <h2 style="margin:10px 0; font-size: 28px; color: #333;">{prueba_acida:.2f}x</h2>
                <p style="font-weight: bold; font-size: 16px; margin: 0;">{icono_acida}</p>
            </div>
            <hr style="margin: 5px 0; width: 100%;">
            <p style="font-size: 11px; color: #444; font-style: italic; line-height: 1.2;">"{msj_acida}"</p>
        </div>
        """, unsafe_allow_html=True)

    # 4. BOTÓN DE EMERGENCIA (RESCATE DE CAJA)
    if activar_rescate:
        st.markdown("---")
        st.error("🚨 **SISTEMA ACTIVADO:** Tu nivel de oxígeno es crítico (< 1.0).")
        with st.expander("🚑 PLAN DE RESCATE DE CAJA (Abrir Inmediatamente)", expanded=True):
            st.markdown("""
            **Protocolo de Emergencia:**
            1.  🛑 **Congelar Pagos:** Detener pagos a proveedores no esenciales por 7 días.
            2.  📞 **Cobranza Agresiva:** Llamar a todos los clientes con facturas vencidas hoy. Ofrece un 5% de descuento si pagan en 24h.
            3.  📉 **Liquidar Inventario:** Rematar productos de baja rotación al costo para generar efectivo ya.
            4.  🤝 **Renegociar:** Hablar con el banco para pedir solo pago de intereses este mes.
            """)

    # 5. GENERACIÓN DEL PLAN DE CHOQUE GENERAL
    acciones_choque = []
    if ratio_alquiler > 15: acciones_choque.append("🏢 **ALQUILER:** Renegociar contrato o subarrendar espacios.")
    if ratio_planilla_ub > 45: acciones_choque.append("👥 **NÓMINA:** Revisar turnos improductivos y pasar a esquema variable.")
    if cobertura_bancaria < 1.5: acciones_choque.append("🏦 **DEUDA:** No tomar más deuda. Solicitar periodo de gracia al banco.")
    if activar_rescate: acciones_choque.append("🩸 **LIQUIDEZ:** Ejecutar Plan de Rescate de Caja inmediatamente.")

    # Guardar en Session State para el PDF
    st.session_state['plan_choque'] = acciones_choque
    
    st.markdown("---")
    st.subheader("🛡️ Plan de Choque Sugerido")
    
    if not acciones_choque:
        st.success("✨ **MANTENIMIENTO:** Tu estructura es sólida. Enfócate en crecer.")
    else:
        for accion in acciones_choque:
            if "MANTENIMIENTO" in accion:
                st.success(accion)
            else:
                st.warning(accion)


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

# --- TAB 7: LABORATORIO DE PRECIOS (SIMULADOR ESTRATÉGICO) ---
with tabs[6]:
    st.subheader("🧪 Simulador Estratégico: '¿Qué pasaría si...?'")
    
    # 1. VISUALIZACIÓN DE CONTROLES (SLIDERS)
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #1565c0; margin-bottom: 20px;">
        <small>Mueve las palancas para ver cómo cambia tu futuro financiero en tiempo real.</small>
    </div>
    """, unsafe_allow_html=True)

    col_controls, col_impact = st.columns([1, 1.5])

    with col_controls:
        st.markdown("### 🎛️ Palancas de Mando")
        
        # SLIDER A: PRECIO
        delta_precio = st.slider("💰 A. Subir Precios (%)", 0, 50, 0, step=1, help="Incremento directo al precio de venta.")
        
        # SLIDER B: COSTOS (EFICIENCIA)
        delta_costos = st.slider("✂️ B. Recortar Gastos Fijos (%)", 0, 50, 0, step=1, help="Optimización de Alquiler, Planilla y Otros Gastos.")
        
        # SLIDER C: VOLUMEN
        delta_volumen = st.slider("📦 C. Variación de Volumen (%)", -50, 50, 0, step=1, help="¿Qué pasa si vendes más o menos unidades?")

    # 2. MOTOR DE CÁLCULO (SIMULACIÓN)
    # Definimos Factores
    f_precio = 1 + (delta_precio / 100)
    f_costos_fijos = 1 - (delta_costos / 100)
    f_volumen = 1 + (delta_volumen / 100)

    # Escenario Actual (Base)
    base_ventas = ventas_mes
    base_cv = costo_ventas_mes
    base_fijos = gastos_operativos_mes
    base_ebitda = ebitda_mes

    # Escenario Simulado
    # Ventas: Afectadas por Precio y Volumen
    sim_ventas = base_ventas * f_precio * f_volumen
    
    # Costo Ventas (Variable): Afectado SOLO por Volumen (Si subo precio, mi costo de harina no sube)
    sim_cv = base_cv * f_volumen
    
    # Gastos Fijos (OPEX): Afectados por Eficiencia (Slider B)
    sim_fijos = base_fijos * f_costos_fijos
    
    # Nuevo EBITDA
    sim_ebitda = sim_ventas - sim_cv - sim_fijos
    sim_margen = (sim_ebitda / sim_ventas) * 100 if sim_ventas > 0 else 0

    # 3. VISUALIZACIÓN DE IMPACTO (MANDÍBULA SIMULADA)
    with col_impact:
        st.markdown("### 🦈 Efecto en la Mandíbula")
        
        # Datos para el gráfico comparativo
        x_stages = ["Actual", "Simulado"]
        y_ventas = [base_ventas, sim_ventas]
        y_costos = [base_cv + base_fijos, sim_cv + sim_fijos]
        
        fig_sim = go.Figure()
        
        # Línea Ventas
        fig_sim.add_trace(go.Scatter(
            x=x_stages, y=y_ventas, mode='lines+markers+text', name='Ventas',
            text=[f"${v/1000:.1f}k" for v in y_ventas], textposition="top center",
            line=dict(color='#1565c0', width=4)
        ))
        
        # Línea Costos
        fig_sim.add_trace(go.Scatter(
            x=x_stages, y=y_costos, mode='lines+markers+text', name='Costos Totales',
            text=[f"${v/1000:.1f}k" for v in y_costos], textposition="bottom center",
            line=dict(color='#c62828', width=4)
        ))
        
        # Sombreado de Utilidad (Area entre líneas)
        fig_sim.add_trace(go.Scatter(
            x=x_stages, y=y_ventas,
            fill=None, mode='none', showlegend=False
        ))
        fig_sim.add_trace(go.Scatter(
            x=x_stages, y=y_costos,
            fill='tonexty', mode='none', showlegend=False,
            fillcolor='rgba(76, 175, 80, 0.2)' if sim_ebitda > base_ebitda else 'rgba(239, 83, 80, 0.2)'
        ))

        fig_sim.update_layout(
            title="Apertura de la Mandíbula (Rentabilidad)",
            yaxis_title="Dinero ($)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True
        )
        st.plotly_chart(fig_sim, use_container_width=True)

    # 4. METRICAS DE RESULTADO (VERDE SI LOGRA EL LEGADO)
    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns(3)
    
    delta_dinero = sim_ebitda - base_ebitda
    color_delta = "normal" if delta_dinero >= 0 else "inverse"
    
    col_res1.metric("Nuevo EBITDA (Mensual)", f"${sim_ebitda:,.0f}", f"{delta_dinero:+,.0f} vs Actual", delta_color=color_delta)
    col_res2.metric("Nuevo Margen", f"{sim_margen:.1f}%", f"{sim_margen - margen_ebitda:.1f}% vs Actual")
    
    # Veredicto de Objetivo (15%)
    if sim_margen >= 15:
        col_res3.markdown("""
        <div style="background-color:#e8f5e9; padding:10px; border-radius:5px; border: 2px solid green; text-align:center;">
            <h3 style="color:green; margin:0;">🏆 OBJETIVO LOGRADO</h3>
            <small>Negocio de Legado (>15%)</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_res3.markdown(f"""
        <div style="background-color:#ffebee; padding:10px; border-radius:5px; border: 2px solid red; text-align:center;">
            <h3 style="color:red; margin:0;">FALTA POTENCIA</h3>
            <small>Meta: 15% (Estás en {sim_margen:.1f}%)</small>
        </div>
        """, unsafe_allow_html=True)

    # 5. EL ESCUDO CONTRA EL MIEDO (ANÁLISIS DE DESERCIÓN)
    st.markdown("---")
    st.subheader("🛡️ El Escudo contra el Miedo")
    
    if delta_precio > 0:
        # Cálculo de Volumen de Equilibrio: %Q = - (%P) / (%P + %MargenContribucion)
        # Margen de Contribución Actual %
        mc_pct = ((base_ventas - base_cv) / base_ventas) if base_ventas > 0 else 0
        
        # Fórmula: Cuánto volumen puedo perder antes de ganar MENOS dinero que hoy
        # Threshold = (New Price - Old Price) / New Margin per unit... 
        # Simplificación porcentual:
        try:
            perdida_maxima_clientes_pct = (delta_precio / 100) / ((delta_precio/100) + mc_pct) * 100
        except:
            perdida_maxima_clientes_pct = 0
            
        st.info(f"""
        **🧠 Dato de Paz Mental:**
        Si subes tus precios un **{delta_precio}%**, puedes permitirte perder hasta el **{perdida_maxima_clientes_pct:.1f}%** de tus clientes (o ventas) y seguirás ganando **exactamente el mismo dinero** que hoy.
        
        *Traducción: Trabajarías un {perdida_maxima_clientes_pct:.1f}% menos para ganar lo mismo. ¡Tu tiempo vale!*
        """)
    else:
        st.caption("Mueve el slider de 'Subir Precios' para activar el Escudo contra el Miedo.")

    # 6. CALCULADOR DE LEGADO (PUNTO DE EQUILIBRIO INVERSO)
    st.markdown("---")
    st.subheader("🏛️ Calculador de Precio de Legado")
    
    # Objetivo: Margen EBITDA 15%
    # Formula: Precio = Costos Totales / (1 - MargenDeseado) ... asumiendo volumen constante
    # O mejor: Ventas Necesarias = Costos Totales / (1 - %CV - %MargenDeseado)
    
    target_margin = 0.15
    ratio_cv = base_cv / base_ventas if base_ventas > 0 else 0
    
    # Denominador de seguridad
    denominador = 1 - ratio_cv - target_margin
    
    if denominador > 0:
        ventas_necesarias_legado = base_fijos / denominador
        # Si asumimos mismo volumen, el precio debe subir
        factor_ajuste_precio = ventas_necesarias_legado / base_ventas
        precio_sugerido_pct = (factor_ajuste_precio - 1) * 100
        
        st.markdown(f"""
        <div style="padding: 15px; border-left: 5px solid #fbc02d; background-color: #fffde7;">
            <p style="font-size: 16px; margin: 0;">
                📢 <strong>Veredicto del Consultor:</strong><br>
                "Soraya, para que este negocio sea un <strong>Legado</strong> (y te deje un 15% limpio después de todo), 
                tus ventas mensuales deberían ser de <strong>${ventas_necesarias_legado:,.0f}</strong>."
            </p>
            <p style="margin-top: 10px;">
                Esto significa que, manteniendo tus costos actuales, deberías <strong>subir tus precios un {precio_sugerido_pct:.1f}%</strong> hoy mismo.
                Cualquier número por debajo es un subsidio que sale de tu bolsillo.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Tu estructura de costos variables es demasiado alta. Incluso con precios infinitos, el margen variable no cubre el 15% de rentabilidad. ¡Optimiza costos variables primero!")

# ==========================================
# 📊 GENERADOR DE REPORTE "ULTIMATE CONSULTANT" (V FINAL)
# ==========================================
# Este motor genera un informe de 4-5 páginas con calidad de auditoría.

def create_ultimate_report():
    class PDF(FPDF):
        def header(self):
            # Banner Superior Azul Oscuro
            self.set_fill_color(26, 35, 126) # Azul Navy
            self.rect(0, 0, 210, 35, 'F')
            
            # Títulos
            self.set_y(10)
            self.set_font('Arial', 'B', 20)
            self.set_text_color(255)
            self.cell(0, 10, 'INFORME DE SALUD FINANCIERA', 0, 1, 'R')
            self.set_font('Arial', '', 10)
            self.cell(0, 5, 'SG CONSULTING | DIVISIÓN DE ESTRATEGIA', 0, 1, 'R')
            self.ln(15)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            fecha = datetime.now().strftime("%d/%m/%Y")
            self.cell(0, 10, f'Confidencial - Generado el {fecha} | Página {self.page_no()}', 0, 0, 'C')

        # --- UTILIDADES GRÁFICAS ---
        def chapter_title(self, num, label):
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(230, 230, 230)
            self.set_text_color(0)
            self.ln(5)
            self.cell(0, 10, f"  {num}. {label.upper()}", 0, 1, 'L', 1)
            self.ln(5)

        def draw_kpi_box(self, x, y, title, value, status_color, subtitle):
            self.set_xy(x, y)
            self.set_fill_color(255, 255, 255)
            self.set_draw_color(200, 200, 200)
            self.rect(x, y, 45, 30) # Caja
            
            # Título
            self.set_xy(x, y+2)
            self.set_font('Arial', 'B', 8)
            self.set_text_color(100)
            self.cell(45, 5, title, 0, 1, 'C')
            
            # Valor
            self.set_xy(x, y+8)
            self.set_font('Arial', 'B', 14)
            # Color del Texto según Estado
            if status_color == 'R': self.set_text_color(198, 40, 40)
            elif status_color == 'A': self.set_text_color(255, 143, 0)
            else: self.set_text_color(46, 125, 50)
            self.cell(45, 10, value, 0, 1, 'C')
            
            # Subtítulo (Diagnóstico corto)
            self.set_xy(x, y+20)
            self.set_font('Arial', '', 7)
            self.set_text_color(80)
            self.cell(45, 5, subtitle, 0, 1, 'C')

        def draw_bar_chart_row(self, label, value, max_val, color_rgb):
            # Simula una barra de gráfico horizontal
            self.set_font('Arial', '', 10)
            self.set_text_color(0)
            self.cell(50, 8, label, 0, 0)
            
            # Calcular ancho barra
            if max_val > 0:
                bar_w = (value / max_val) * 100 # 100mm max width
            else:
                bar_w = 1
            
            # Dibujar barra
            self.set_fill_color(color_rgb[0], color_rgb[1], color_rgb[2])
            current_y = self.get_y()
            current_x = self.get_x()
            self.rect(current_x, current_y+1, bar_w, 6, 'F')
            
            # Valor texto al final
            self.set_xy(current_x + bar_w + 2, current_y)
            self.cell(30, 8, f"${value:,.0f}", 0, 1)

    pdf = PDF()
    pdf.add_page()

    # ===================== PÁGINA 1: RESUMEN EJECUTIVO =====================
    
    # 1.1 INTRODUCCIÓN
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "El siguiente informe presenta un diagnóstico profundo de la salud operativa, financiera y de solvencia de la empresa. Los datos han sido sometidos a pruebas de estrés para identificar riesgos ocultos.")
    
    # 1.2 EL VEREDICTO (TEXTO GRANDE)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(255, 235, 238) # Fondo suave alerta
    pdf.cell(0, 10, "  VEREDICTO DEL ANALISTA:", 0, 1, 'L', 1)
    
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(50)
    pdf.multi_cell(0, 8, f"\"{veredicto_final}\"")
    pdf.ln(5)

    # 1.3 TABLERO DE CONTROL (KPIs SEMÁFORO)
    pdf.chapter_title(1, "Signos Vitales (KPIs)")
    
    # Recalculamos estados rápidos para el PDF
    r_alq = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
    r_nom = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0
    pasivo_c = cuentas_pagar if cuentas_pagar > 0 else 1
    r_acid = (caja + cuentas_cobrar) / pasivo_c
    
    # Fila de 4 Cajas
    y_start = pdf.get_y() + 5
    pdf.draw_kpi_box(10, y_start, "Eficiencia Renta", f"{r_alq:.1f}%", 'R' if r_alq > 15 else 'V', "Meta: <15%")
    pdf.draw_kpi_box(60, y_start, "Peso Nómina", f"{r_nom:.1f}%", 'R' if r_nom > 45 else 'V', "Meta: <45% (UB)")
    pdf.draw_kpi_box(110, y_start, "Prueba Ácida", f"{r_acid:.2f}x", 'R' if r_acid < 0.8 else 'V', "Liquidez Real")
    pdf.draw_kpi_box(160, y_start, "Margen EBITDA", f"{margen_ebitda:.1f}%", 'R' if margen_ebitda < 10 else 'V', "Potencia Operativa")
    
    pdf.set_y(y_start + 35)

    # ===================== PÁGINA 1 (Cont): CASCADA =====================
    pdf.chapter_title(2, "Estructura de Resultados (P&L)")
    
    # Dibujamos "Gráfico" de Barras nativo
    pdf.draw_bar_chart_row("Ventas Totales", ventas_mes, ventas_mes, (33, 150, 243)) # Azul
    pdf.draw_bar_chart_row("Utilidad Bruta", utilidad_bruta_mes, ventas_mes, (100, 100, 100)) # Gris
    pdf.draw_bar_chart_row("Gastos Operativos", gastos_operativos_mes, ventas_mes, (239, 83, 80)) # Rojo
    pdf.draw_bar_chart_row("EBITDA (Caja)", ebitda_mes, ventas_mes, (76, 175, 80) if ebitda_mes > 0 else (255, 152, 0)) # Verde/Naranja
    pdf.draw_bar_chart_row("Utilidad Neta", utilidad_neta_mes, ventas_mes, (21, 101, 192)) # Azul Oscuro
    
    pdf.ln(5)
    # Tabla Detallada
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 8, "Concepto", 1); pdf.cell(50, 8, "Monto ($)", 1, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(100, 6, "Ingresos Operativos", 1); pdf.cell(50, 6, f"${ventas_mes:,.2f}", 1, 1, 'R')
    pdf.cell(100, 6, "(-) Costos Variables", 1); pdf.cell(50, 6, f"${costo_ventas_mes:,.2f}", 1, 1, 'R')
    pdf.cell(100, 6, "(-) Gastos Estructurales", 1); pdf.cell(50, 6, f"${gastos_operativos_mes:,.2f}", 1, 1, 'R')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 6, "(=) EBITDA Normalizado", 1); pdf.cell(50, 6, f"${ebitda_mes:,.2f}", 1, 1, 'R')

    # ===================== PÁGINA 2: ANÁLISIS PROFUNDO =====================
    pdf.add_page()
    pdf.chapter_title(3, "Diagnóstico de Solvencia & Caja")
    
    # 3.1 DINERO ATRAPADO
    dinero_atrapado = cuentas_cobrar + inventario
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 10, "Análisis del Ciclo de Conversión de Efectivo (CCC):", 0, 1)
    
    # Caja de Dinero Atrapado
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 25, 'F')
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 12); pdf.set_text_color(198, 40, 40)
    pdf.cell(90, 10, "CAPITAL INMOVILIZADO:", 0, 0)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(50, 10, f"${dinero_atrapado:,.2f}", 0, 1)
    
    pdf.set_x(15); pdf.set_font('Arial', 'I', 10); pdf.set_text_color(80)
    pdf.cell(0, 8, f"Desglose: ${cuentas_cobrar:,.0f} en Clientes + ${inventario:,.0f} en Inventario.", 0, 1)
    pdf.ln(10)
    
    # 3.2 PUNTO DE EQUILIBRIO
    pdf.set_text_color(0)
    pdf.cell(0, 8, f"Punto de Equilibrio Mensual: ${punto_equilibrio_mes:,.2f}", 0, 1)
    pdf.set_font('Arial', '', 10)
    if ventas_mes > punto_equilibrio_mes:
        diff = ventas_mes - punto_equilibrio_mes
        pdf.multi_cell(0, 5, f"STATUS: SUPERAVIT. Usted vende ${diff:,.0f} por encima de su necesidad mínima. La empresa genera valor.")
    else:
        diff = punto_equilibrio_mes - ventas_mes
        pdf.multi_cell(0, 5, f"STATUS: DEFICIT. Usted necesita vender ${diff:,.0f} adicionales solo para no perder dinero.")

    # 3.3 VALORACIÓN
    pdf.ln(5)
    pdf.chapter_title(4, "Valoración Estimada de Mercado")
    
    valor_negocio_est = ebitda_mes * 12 * multiplo_global
    patrimonio_est = valor_negocio_est - deuda_bancaria # Simplificado
    if patrimonio_est < 0: patrimonio_est = 0
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"Basado en un múltiplo de mercado de {multiplo_global}x EBITDA Anualizado:", 0, 1)
    
    # Tabla Valoración
    pdf.set_fill_color(227, 242, 253) # Azul muy claro
    pdf.rect(60, pdf.get_y()+2, 90, 30, 'F')
    pdf.set_y(pdf.get_y()+5)
    
    pdf.set_x(60)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(90, 8, f"VALOR OPERATIVO: ${valor_negocio_est:,.0f}", 0, 1, 'C')
    pdf.set_x(60)
    pdf.set_font('Arial', '', 10)
    pdf.cell(90, 6, f"(-) Deuda Bancaria: ${deuda_bancaria:,.0f}", 0, 1, 'C')
    pdf.set_x(60)
    pdf.set_font('Arial', 'B', 14); pdf.set_text_color(21, 101, 192)
    pdf.cell(90, 10, f"PATRIMONIO NETO: ${patrimonio_est:,.0f}", 0, 1, 'C')
    pdf.set_text_color(0)
    pdf.ln(10)

    # ===================== PÁGINA 3: PLAN DE ACCIÓN =====================
    pdf.add_page()
    pdf.set_fill_color(183, 28, 28) # Rojo
    pdf.rect(0, 0, 210, 30, 'F')
    pdf.set_y(10)
    pdf.set_font('Arial', 'B', 16); pdf.set_text_color(255)
    pdf.cell(0, 10, "PLAN DE CHOQUE ESTRATÉGICO", 0, 1, 'C')
    pdf.ln(25)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'I', 11)
    pdf.multi_cell(0, 8, "Basado en las alertas detectadas, se prescriben las siguientes acciones inmediatas de cumplimiento obligatorio para garantizar la continuidad del negocio.")
    pdf.ln(5)
    
    # Recuperar Plan de Choque
    acciones = st.session_state.get('plan_choque', ["Ejecute el análisis en la app primero."])
    
    for i, accion in enumerate(acciones, 1):
        # Limpieza Markdown
        txt = accion.replace("**", "").replace("🔴", "").replace("⚠️", "[ALERTA]").replace("🏢", "").replace("👥", "").replace("✨", "").replace("🏦", "").replace("🩸", "")
        txt = txt.encode('latin-1', 'replace').decode('latin-1')
        
        # Caja de Acción
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(0)
        pdf.set_line_width(0.5)
        
        current_y = pdf.get_y()
        # Icono numérico
        pdf.set_font('Arial', 'B', 16); pdf.set_text_color(183, 28, 28)
        pdf.text(10, current_y + 8, f"{i}")
        
        # Texto
        pdf.set_x(20)
        pdf.set_font('Arial', '', 11); pdf.set_text_color(0)
        pdf.multi_cell(180, 6, txt)
        pdf.ln(5)
        
        # Línea separadora
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

    # ===================== FIRMA Y DISCLAIMER =====================
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 8); pdf.set_text_color(100)
    pdf.multi_cell(0, 4, "AVISO LEGAL: Este reporte es un diagnóstico automatizado basado en la información provista. SG Consulting no se hace responsable por decisiones tomadas sin la validación de un contador público autorizado.")
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- BOTÓN DE DESCARGA ---
st.sidebar.markdown("---")
if st.sidebar.button("🖨️ Generar Reporte Auditoría (PDF)"):
    try:
        pdf_bytes = create_ultimate_report()
        st.sidebar.download_button(
            label="💾 Descargar Informe Oficial",
            data=pdf_bytes,
            file_name=f"SG_Consulting_Auditoria_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.sidebar.success("✅ Informe generado correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error al generar PDF: {e}")

