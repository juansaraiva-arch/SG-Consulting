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


# --- TAB 3: SEMÁFORO DE RIESGOS & PLAN DE CHOQUE ---
with tabs[2]:
    st.subheader("🚦 Panel de Control de Riesgos (KPIs Críticos)")
    
    # 1. CÁLCULO DE RATIOS
    # A. Alquiler (Sobre Ventas)
    ratio_alquiler = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
    
    # B. Planilla (Sobre Utilidad Bruta - Ojo: Usuario pidió sobre UB, no Ventas)
    ratio_planilla_ub = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0
    
    # C. Cobertura Bancaria (EBITDA / Intereses)
    if intereses_mes > 0:
        cobertura_bancaria = ebitda_mes / intereses_mes
    else:
        cobertura_bancaria = 10.0 # Valor seguro si no hay deuda
        
    # D. Prueba Ácida ( (Caja + CxC) / CxP ) -> Usamos Pasivo Circulante estimado como CxP
    pasivo_circulante = cuentas_pagar 
    prueba_acida = (caja + cuentas_cobrar) / pasivo_circulante if pasivo_circulante > 0 else 0

    # 2. LÓGICA DE SEMÁFOROS (VERDE / NARANJA / ROJO)
    def obtener_estado(valor, umbral_rojo, tipo='mayor_es_malo'):
        # Retorna: (Color Hex, Icono, Estado)
        if tipo == 'mayor_es_malo':
            if valor > umbral_rojo: return ("#ffebee", "🔴", "CRÍTICO") # Fondo Rojo suave
            elif valor > (umbral_rojo * 0.8): return ("#fff3e0", "🟠", "ALERTA") # Fondo Naranja
            else: return ("#e8f5e9", "🟢", "ÓPTIMO") # Fondo Verde
        else: # menor_es_malo (Cobertura y Ácida)
            if valor < umbral_rojo: return ("#ffebee", "🔴", "CRÍTICO")
            elif valor < (umbral_rojo * 1.2): return ("#fff3e0", "🟠", "ALERTA")
            else: return ("#e8f5e9", "🟢", "ÓPTIMO")

    # Evaluamos los 4 KPIs
    est_alquiler = obtener_estado(ratio_alquiler, 15.0, 'mayor_es_malo')
    est_planilla = obtener_estado(ratio_planilla_ub, 45.0, 'mayor_es_malo')
    est_bancos = obtener_estado(cobertura_bancaria, 1.5, 'menor_es_malo')
    est_acida = obtener_estado(prueba_acida, 0.8, 'menor_es_malo')

    # 3. VISUALIZACIÓN EN GRID
    c1, c2, c3, c4 = st.columns(4)
    
    def tarjeta_kpi(columna, titulo, valor, sufijo, estado_tuple, explicacion):
        color_bg, icono, texto_estado = estado_tuple
        columna.markdown(f"""
        <div style="background-color: {color_bg}; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 200px;">
            <h4 style="margin:0; font-size: 14px; color: #555;">{titulo}</h4>
            <h2 style="margin:10px 0; font-size: 28px; color: #333;">{valor:.1f}{sufijo}</h2>
            <p style="font-weight: bold; font-size: 18px; margin: 0;">{icono} {texto_estado}</p>
            <hr style="margin: 5px 0;">
            <p style="font-size: 11px; color: #666;">{explicacion}</p>
        </div>
        """, unsafe_allow_html=True)

    tarjeta_kpi(c1, "Eficiencia Inmobiliaria", ratio_alquiler, "%", est_alquiler, "Meta: <15% de Ventas. Si es alto, trabajas para el arrendador.")
    tarjeta_kpi(c2, "Peso de Nómina", ratio_planilla_ub, "%", est_planilla, "Meta: <45% de Ut. Bruta. Mide productividad del equipo.")
    tarjeta_kpi(c3, "Cobertura Intereses", cobertura_bancaria, "x", est_bancos, "Meta: >1.5x. Capacidad de pagar al banco con tu EBITDA.")
    tarjeta_kpi(c4, "Prueba Ácida", prueba_acida, "x", est_acida, "Meta: >0.8x. Capacidad de pagar hoy sin vender inventario.")

    # 4. GENERADOR DE "PLAN DE CHOQUE" (Lógica para PDF y Pantalla)
    acciones_choque = []
    
    if est_alquiler[2] == "CRÍTICO":
        acciones_choque.append("🏢 **INMOBILIARIO:** Renegociar contrato de alquiler inmediatamente, subarrendar espacios ociosos o evaluar mudanza a 'Dark Kitchen/Office'.")
    if est_planilla[2] == "CRÍTICO":
        acciones_choque.append("👥 **NÓMINA:** La estructura es obesa. Implementar esquema de comisiones variables, reducir turnos improductivos o ajustar plantilla base.")
    if est_bancos[2] == "CRÍTICO":
        acciones_choque.append("🏦 **DEUDA:** Riesgo de Default. No tomes más deuda. Acude al banco para pedir meses de gracia (período de carencia) o reestructurar plazo.")
    if est_acida[2] == "CRÍTICO":
        acciones_choque.append("🩸 **LIQUIDEZ:** Sangrado activo. Detener pagos a proveedores no críticos. Lanzar promoción de efectivo inmediato (descuento por pronto pago) para recuperar cartera.")

    if not acciones_choque:
        acciones_choque.append("✨ **MANTENIMIENTO:** Tu estructura es sólida. Enfócate en estrategias de crecimiento (Marketing) en lugar de supervivencia.")

    # Guardar en Session State para el PDF
    st.session_state['plan_choque'] = acciones_choque
    
    st.markdown("---")
    st.subheader("🛡️ Plan de Choque Sugerido")
    
    if not acciones_choque:
        st.success("✨ **MANTENIMIENTO:** Tu estructura es sólida. Enfócate en estrategias de crecimiento.")
    else:
        for accion in acciones_choque:
            # CORRECCIÓN: Usamos un bloque if/else estándar para evitar el error 'DeltaGenerator'
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
# 📊 GENERADOR DE REPORTE PROFESIONAL (PDF V5.0)
# ==========================================
# Nota: Colocar este bloque al final del script para asegurar que tiene todos los datos.

from datetime import datetime

def create_professional_pdf():
    class PDF(FPDF):
        def header(self):
            # Logo / Banner Corporativo
            self.set_fill_color(21, 101, 192) # Azul Corporativo
            self.rect(0, 0, 210, 40, 'F')
            
            self.set_y(10)
            self.set_font('Arial', 'B', 24)
            self.set_text_color(255)
            self.cell(0, 10, 'SG CONSULTING', 0, 1, 'C')
            
            self.set_font('Arial', 'I', 12)
            self.cell(0, 10, 'La Máquina de Verdad Financiera', 0, 1, 'C')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.cell(0, 10, f'Generado el {fecha} | Página {self.page_no()}', 0, 0, 'C')

        def section_title(self, title):
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(240, 240, 240)
            self.set_text_color(33)
            self.cell(0, 10, f"  {title}", 0, 1, 'L', 1)
            self.ln(5)

        def kpi_card(self, label, value, color_status):
            # Dibuja una tarjeta de KPI con semáforo visual
            self.set_font('Arial', '', 10)
            self.set_text_color(50)
            self.cell(90, 8, label, 0, 0)
            
            self.set_font('Arial', 'B', 10)
            if color_status == 'ROJO': self.set_text_color(198, 40, 40)
            elif color_status == 'AMARILLO': self.set_text_color(255, 160, 0)
            else: self.set_text_color(46, 125, 50)
            
            self.cell(40, 8, value, 0, 1, 'R')
            self.set_text_color(0) # Reset

    pdf = PDF()
    pdf.add_page()
    
    # --- 1. RESUMEN EJECUTIVO (FOTO) ---
    pdf.section_title("1. RADIOGRAFÍA FINANCIERA (P&L)")
    
    # Tabla Principal
    pdf.set_font('Arial', '', 11)
    
    # Datos recuperados de las variables globales del script
    data_pl = [
        ("Ventas Totales", ventas_mes, ""),
        ("(-) Costo de Ventas", costo_ventas_mes, ""),
        ("(=) Utilidad Bruta", utilidad_bruta_mes, ""),
        ("(-) Gastos Operativos (OPEX)", gastos_operativos_mes, ""),
        ("(=) EBITDA (Motor del Negocio)", ebitda_mes, "KEY"), # Marcado como clave
        ("(-) Intereses e Impuestos", intereses_mes + impuestos_mes + depreciacion_mes, ""),
        ("(=) Utilidad Neta", utilidad_neta_mes, "KEY")
    ]

    for label, val, tag in data_pl:
        pdf.set_font('Arial', 'B' if tag=="KEY" else '', 11)
        pdf.cell(100, 8, label, 1)
        pdf.cell(50, 8, f"${val:,.2f}", 1, 1, 'R')

    pdf.ln(5)
    
    # --- 2. DIAGNÓSTICO DEL CONSULTOR ---
    pdf.section_title("2. DIAGNÓSTICO DE INTELIGENCIA (Veredictos)")
    
    # Recuperar textos del session_state (generados en los Tabs)
    motor_txt = st.session_state.get('reporte_motor', "Sin diagnóstico.")
    mandibula_txt = st.session_state.get('reporte_mandibula', "Sin diagnóstico.")
    legado_txt = st.session_state.get('reporte_legado', "Sin diagnóstico.")
    
    pdf.set_font('Arial', 'B', 10); pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 8, "Estado del Motor (EBITDA):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.set_text_color(50)
    pdf.multi_cell(0, 6, motor_txt.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(3)

    pdf.set_font('Arial', 'B', 10); pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 8, "Riesgo de Mandíbulas (Costos vs Ventas):", 0, 1)
    pdf.set_font('Arial', '', 10); pdf.set_text_color(50)
    pdf.multi_cell(0, 6, mandibula_txt.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(3)

    # --- 3. SEMÁFOROS Y SOLVENCIA (VISUAL) ---
    pdf.ln(5)
    pdf.section_title("3. TABLERO DE CONTROL (SEMÁFOROS)")
    
    # Recálculo rápido de estados para el reporte
    ratio_alq = (gasto_alquiler_mes / ventas_mes) * 100 if ventas_mes > 0 else 0
    ratio_nom = (gasto_planilla_mes / utilidad_bruta_mes) * 100 if utilidad_bruta_mes > 0 else 0
    pasivo = cuentas_pagar if 'cuentas_pagar' in locals() else 1
    acida = (caja + cuentas_cobrar) / pasivo if pasivo > 0 else 0
    
    # Renderizado de KPIs con lógica de color
    pdf.kpi_card("Eficiencia Alquiler (<15%)", f"{ratio_alq:.1f}%", 'ROJO' if ratio_alq > 15 else 'VERDE')
    pdf.kpi_card("Peso Nómina vs Ut. Bruta (<45%)", f"{ratio_nom:.1f}%", 'ROJO' if ratio_nom > 45 else 'VERDE')
    pdf.kpi_card("Prueba Ácida (Liquidez > 0.8)", f"{acida:.2f}x", 'ROJO' if acida < 0.8 else 'VERDE')
    
    # Barra visual simulada para EBITDA
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10); pdf.set_text_color(0)
    pdf.cell(0, 8, "Visualización de Márgenes (Ventas vs EBITDA vs Neta):", 0, 1)
    
    # Dibujar barras proporcionales
    w_max = 150 # Ancho máximo en mm
    if ventas_mes > 0:
        w_ventas = w_max
        w_ebitda = (ebitda_mes / ventas_mes) * w_max
        w_neta = (utilidad_neta_mes / ventas_mes) * w_max
    else:
        w_ventas = w_ebitda = w_neta = 0

    # Barra Ventas (Azul)
    pdf.set_fill_color(33, 150, 243)
    pdf.cell(30, 6, "Ventas", 0, 0)
    pdf.rect(pdf.get_x(), pdf.get_y(), w_ventas, 6, 'F')
    pdf.ln(8)
    
    # Barra EBITDA (Verde o Naranja)
    pdf.set_fill_color(76, 175, 80) if ebitda_mes > 0 else pdf.set_fill_color(255, 152, 0)
    pdf.cell(30, 6, "EBITDA", 0, 0)
    if w_ebitda > 0: pdf.rect(pdf.get_x(), pdf.get_y(), w_ebitda, 6, 'F')
    pdf.ln(8)

    # Barra Neta (Gris Oscuro)
    pdf.set_fill_color(66, 66, 66)
    pdf.cell(30, 6, "Neta", 0, 0)
    if w_neta > 0: pdf.rect(pdf.get_x(), pdf.get_y(), w_neta, 6, 'F')
    pdf.ln(10)

    # --- 4. PLAN DE CHOQUE (NUEVA PÁGINA) ---
    pdf.add_page()
    pdf.set_fill_color(183, 28, 28) # Rojo Intenso
    pdf.rect(0, 0, 210, 30, 'F')
    pdf.set_y(10)
    pdf.set_font('Arial', 'B', 16); pdf.set_text_color(255)
    pdf.cell(0, 10, "PLAN DE CHOQUE INMEDIATO", 0, 1, 'C')
    pdf.ln(25)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', '', 12)
    
    acciones = st.session_state.get('plan_choque', ["Ejecuta el análisis primero para ver acciones."])
    
    for i, accion in enumerate(acciones, 1):
        # Limpieza de caracteres markdown para PDF
        txt = accion.replace("**", "").replace("🔴", "").replace("⚠️", "[ALERTA]").replace("🏢", "").replace("👥", "").replace("✨", "")
        txt = txt.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.set_fill_color(255, 235, 238) # Fondo rosado suave
        pdf.rect(10, pdf.get_y(), 190, 20, 'F')
        
        pdf.set_x(15)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(10, 10, f"{i}.", 0, 0)
        
        pdf.set_font('Arial', '', 11)
        pdf.set_y(pdf.get_y() + 2) # Ajuste vertical
        pdf.set_x(25)
        pdf.multi_cell(170, 6, txt)
        pdf.ln(10)

    return pdf.output(dest='S').encode('latin-1', 'replace')

# ==========================================
# 🔘 BOTÓN DE DESCARGA (VISIBLE SIEMPRE)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.header("📥 Descargar Reporte")

# Generamos el PDF solo cuando el script llega aquí (ya tiene todos los datos)
try:
    pdf_bytes = create_professional_pdf()
    
    st.sidebar.download_button(
        label="📄 Generar Informe PDF Completo",
        data=pdf_bytes,
        file_name="SG_Reporte_Financiero.pdf",
        mime="application/pdf",
        help="Descarga un reporte ejecutivo con todos los diagnósticos y gráficas."
    )
except Exception as e:
    st.sidebar.error(f"Error generando PDF: {e}")
