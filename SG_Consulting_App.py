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

# ESTILOS CSS (DISEÑO VISUAL)
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
    # Valores por defecto para evitar errores si no se cargan datos
    ventas_mes = 0.0
    costo_ventas_mes = 0.0
    gasto_alquiler_mes = 0.0
    gasto_planilla_mes = 0.0
    gasto_otros_mes = 0.0
    depreciacion_mes = 0.0
    intereses_mes = 0.0
    impuestos_mes = 0.0
    
    df_historico = None # Variable para guardar la "Película"

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
        
        # 1. Generador de Plantilla
        data_plantilla = {
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            'Ventas': [50000]*12, 'Costo_Ventas': [30000]*12,
            'Alquiler': [5000]*12, 'Planilla': [8000]*12, 'Otros_Gastos': [2000]*12,
            'Depreciacion': [2000]*12, 'Intereses': [1000]*12, 'Impuestos': [1500]*12
        }
        df_plantilla = pd.DataFrame(data_plantilla)
        csv = df_plantilla.to_csv(index=False).encode('utf-8')
        
        st.download_button("⬇️ Descargar Plantilla Excel (CSV)", data=csv, file_name="plantilla_sg_consulting.csv", mime="text/csv")
        
        # 2. Subidor de Archivo
        archivo_subido = st.file_uploader("Sube tu archivo (CSV) con 12 meses", type=['csv'])
        
        if archivo_subido is not None:
            try:
                df_historico = pd.read_csv(archivo_subido)
                st.success("✅ Datos cargados exitosamente")
                
                # CÁLCULO DE PROMEDIOS PARA ALIMENTAR LA CASCADA (MÓDULOS ESTÁTICOS)
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
            st.warning("⚠️ Esperando archivo... (Se usarán datos demo mientras tanto)")
            # Datos Demo para que no se vea vacío antes de cargar
            ventas_mes = 50000.0
            costo_ventas_mes = 30000.0
            gasto_alquiler_mes = 5000.0
            gasto_planilla_mes = 8000.0
            gasto_otros_mes = 2000.0
            depreciacion_mes = 2000.0
            intereses_mes = 1000.0
            impuestos_mes = 1500.0

    # --- BALANCE GENERAL (SIEMPRE VISIBLE) ---
    with st.expander("Balance General (Saldos)", expanded=True):
        st.caption("FOTO ACTUAL (No se divide ni promedia)")
        inventario = st.number_input("Inventario ($)", value=20000.0)
        cuentas_cobrar = st.number_input("Cuentas por Cobrar ($)", value=15000.0)
        cuentas_pagar = st.number_input("Cuentas por Pagar ($)", value=10000.0)

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

# 5. Juez Digital
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

# Veredicto Global
st.markdown(f"""<div class="verdict-box"><h3>{icono_veredicto} Veredicto de la Estratega:</h3><p style="font-size: 18px;">"{veredicto_final}"</p></div>""", unsafe_allow_html=True)

# DEFINICIÓN DE PESTAÑAS (AHORA SON 7 SI CONTAMOS MANDÍBULAS)
tabs = st.tabs(["💎 Cascada", "🦈 Mandíbulas (Tendencia)", "🚦 Semáforo", "⚖️ Supervivencia", "🫁 Oxígeno", "🏆 Valoración V2.5", "🧪 Lab Precios"])

# --- TAB 1: CASCADA (DIAGNÓSTICO FOTO) ---
with tabs[0]:
    col_main, col_chart = st.columns([1.2, 1])
    with col_main:
        st.subheader("Diagnóstico de Potencia (Foto Promedio)")
        st.caption("Análisis capa por capa.")
        
        # Nivel 1
        st.markdown('<div class="power-level-title">Nivel 1: Potencia Comercial (Bruta)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${utilidad_bruta_mes:,.2f} (Margen: {margen_bruto:.1f}%)</div>', unsafe_allow_html=True)
        if margen_bruto > 30: st.markdown('<div class="check-box-success">✅ Modelo Saludable.</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="check-box-warning">⚠️ Margen Bajo.</div>', unsafe_allow_html=True)

        # Nivel 2
        st.markdown('<div class="power-level-title">Nivel 2: Potencia Operativa (EBITDA)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="power-value">${ebitda_mes:,.2f} (Margen: {margen_ebitda:.1f}%)</div>', unsafe_allow_html=True)
        if ebitda_mes > 0 and margen_ebitda > 10: st.markdown('<div class="check-box-success">✅ Corazón Fuerte.</div>', unsafe_allow_html=True)
        elif ebitda_mes > 0: st.markdown('<div class="check-box-warning">⚠️ Vulnerable.</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="check-box-danger">🚨 Quema Efectivo.</div>', unsafe_allow_html=True)

        # Nivel 3 y 4
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

# --- TAB 2: LAS MANDÍBULAS (TENDENCIAS) ---
with tabs[1]:
    st.subheader("🦈 Las Mandíbulas de la Muerte (Tendencias)")
    
    if modo_operacion == "Modo A: Diagnóstico Flash (Foto)":
        st.warning("⚠️ Esta función solo está disponible en 'Modo B: Estratega' cargando un Excel de 12 meses.")
        st.image("https://via.placeholder.com/800x400.png?text=Gráfico+de+Tendencias+Solo+Disponible+en+Modo+Estratega", use_container_width=True)
    
    elif df_historico is not None:
        # Preparar datos para el gráfico
        df_historico['Costos_Totales'] = df_historico['Costo_Ventas'] + df_historico['Alquiler'] + df_historico['Planilla'] + df_historico['Otros_Gastos']
        
        # Gráfico de Líneas (Jaws)
        fig_jaws = go.Figure()
        fig_jaws.add_trace(go.Scatter(x=df_historico['Mes'], y=df_historico['Ventas'], mode='lines+markers', name='Ventas (Azul)', line=dict(color='blue', width=3)))
        fig_jaws.add_trace(go.Scatter(x=df_historico['Mes'], y=df_historico['Costos_Totales'], mode='lines+markers', name='Costos Totales (Rojo)', line=dict(color='red', width=3)))
        
        fig_jaws.update_layout(title="Análisis de Tendencia: ¿Las líneas se abren o se cruzan?", xaxis_title="Mes", yaxis_title="Dinero ($)", height=500)
        st.plotly_chart(fig_jaws, use_container_width=True)
        
        # Diagnóstico Automático de Tendencia
        tendencia_ventas = df_historico['Ventas'].iloc[-1] - df_historico['Ventas'].iloc[0]
        tendencia_utilidad = (df_historico['Ventas'].iloc[-1] - df_historico['Costos_Totales'].iloc[-1]) - (df_historico['Ventas'].iloc[0] - df_historico['Costos_Totales'].iloc[0])
        
        c1, c2 = st.columns(2)
        with c1:
            if tendencia_ventas > 0: st.success("📈 Tus ventas están creciendo.")
            else: st.error("📉 Tus ventas están cayendo.")
        with c2:
            if tendencia_utilidad < 0 and tendencia_ventas > 0:
                st.error("🚨 ALERTA DE MANDÍBULA: Vendes más pero ganas menos. Ineficiencia Operativa (Desconomía de Escala).")
            elif tendencia_utilidad > 0:
                st.success("✅ Crecimiento Sano: Ganas más a medida que vendes más.")
    else:
        st.info("Carga un archivo en la barra lateral para ver el gráfico.")

# --- TAB 3: SEMÁFORO ---
with tabs[2]:
    col_renta, col_nomina = st.columns(2)
    with col_renta:
        st.metric("Ratio Alquiler", f"{ratio_alquiler:.1f}%")
        st.progress(min(ratio_alquiler/30, 1.0))
        if ratio_alquiler > 15: st.error("🚨 Local: Ancla Financiera")
        else: st.success("✅ Local: Estructura OK")
    with col_nomina:
        st.metric("Ratio Planilla", f"{ratio_planilla:.1f}%")
        st.progress(min(ratio_planilla/60, 1.0))
        if ratio_planilla > 40: st.error("🚨 Planilla: Estructura Obesa")
        else: st.success("✅ Planilla: Productiva")

# --- TAB 4: SUPERVIVENCIA ---
with tabs[3]:
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Punto Equilibrio Mensual", f"${punto_equilibrio_mes:,.2f}")
        if margen_seguridad_mes > 0: st.success(f"✅ Margen Seguridad: ${margen_seguridad_mes:,.2f}")
        else: st.error(f"🚨 Faltan Ventas: ${abs(margen_seguridad_mes):,.2f}")
    with c2:
        # Gráfico de P.E. Visual (Simplificado)
        pct_meta = (ventas_mes / punto_equilibrio_mes) * 100 if punto_equilibrio_mes > 0 else 0
        st.markdown(f"**Estás al {pct_meta:.0f}% de tu meta de supervivencia.**")
        st.progress(min(pct_meta/200, 1.0))

# --- TAB 5: OXÍGENO ---
with tabs[4]:
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Ciclo de Caja (CCC)", f"{ccc:.0f} días")
        if ccc > 0: st.warning("Tardas en recuperar tu dinero.")
        else: st.success("Te financias con proveedores.")
    with c2:
        st.markdown(f"""<div class="money-trap"><h4>💸 Efectivo Atrapado</h4><p>Total: <strong>${dinero_atrapado_total:,.2f}</strong></p></div>""", unsafe_allow_html=True)

# --- TAB 6: VALORACIÓN V2.5 (PATRIMONIO NETO) ---
with tabs[5]:
    st.subheader("🏆 Motor de Riqueza: Valoración & Legado")
    st.caption("Separamos el negocio del ladrillo para ver tu Patrimonio Real.")

    # 1. Normalización (OpCo vs PropCo)
    col_prop_1, col_prop_2 = st.columns(2)
    with col_prop_1:
        es_dueno = st.checkbox("¿Cliente es dueño del local?", value=False)
    
    alquiler_virtual = 0.0
    valor_edificio = 0.0
    
    if es_dueno:
        with col_prop_2:
            alquiler_virtual = st.number_input("Alquiler Virtual de Mercado ($)", value=2000.0)
            valor_edificio = st.number_input("Valor Comercial del Edificio ($)", value=250000.0)
    
    # Cálculo EBITDA Ajustado
    ebitda_ajustado = (ebitda_mes - alquiler_virtual) * 12 # Anualizado
    
    st.markdown("---")
    
    # 2. El Múltiplo
    col_val_1, col_val_2 = st.columns(2)
    with col_val_1:
        multiplo = st.selectbox("Calidad del Negocio (Múltiplo)", [2, 3, 4, 5, 6], index=1, help="2x: Autoempleo, 5x: Gerencia Pro.")
        valor_operativo = ebitda_ajustado * multiplo
    with col_val_2:
        if valor_operativo > 0:
            st.markdown(f"""<div class="metric-card"><h4>Valor Operativo (OpCo)</h4><h2 style="color:green">${valor_operativo:,.2f}</h2></div>""", unsafe_allow_html=True)
        else:
            st.error("🚨 El negocio no vale nada (EBITDA Ajustado Negativo).")
            valor_operativo = 0

    st.markdown("---")

    # 3. Patrimonio Neto
    st.subheader("💎 Tu Patrimonio Real (Net Worth)")
    deuda = st.number_input("Deuda Bancaria Total ($)", value=0.0)
    patrimonio = valor_operativo + valor_edificio - deuda
    
    st.markdown(f"""
    <div class="valuation-box">
        <h1 style="color: #0d47a1; text-align: center;">${patrimonio:,.2f}</h1>
        <p style="text-align: center;">(Negocio + Edificio - Deuda)</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 7: LAB DE PRECIOS V2.5 ---
with tabs[6]:
    st.subheader("🧪 Lab de Precios (Bottom-Up)")
    
    # 1. Costos Unitarios
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
    
    # 2. Estrategia (Fórmula Inversa)
    c3, c4 = st.columns(2)
    with c3:
        margen = st.slider("Margen Deseado (%)", 10, 90, 30)
        comision = st.slider("Comisión Plataforma (%)", 0, 50, 0)
    with c4:
        # FÓRMULA V2.5: Precio = Costo / (1 - (Margen + Comision))
        denom = 1 - ((margen + comision) / 100)
        if denom > 0:
            precio = costo_u / denom
            itbms = precio * 0.07
            final = precio + itbms
            st.markdown(f"""
            <div style="border: 2px solid green; padding: 10px; border-radius: 10px; text-align: center;">
                <h3>Precio Sugerido: ${precio:,.2f}</h3>
                <p>+ ITBMS: ${itbms:,.2f} | <strong>Ticket: ${final:,.2f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón Guardar
            if st.button("➕ Agregar a Tabla"):
                st.session_state.lab_precios.append({
                    "Producto": producto, "Costo": f"${costo_u:,.2f}", "Precio": f"${precio:,.2f}", 
                    "Margen": f"{margen}%", "Ganancia": f"${precio*(margen/100):,.2f}"
                })
        else:
            st.error("🚨 Imposible: Margen + Comisión > 100%")

    # 3. Tabla
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
