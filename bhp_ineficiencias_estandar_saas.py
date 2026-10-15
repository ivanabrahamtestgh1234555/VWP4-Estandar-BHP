import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BHP ENC-3430 | Evaluación de Ineficiencias de Rendimiento",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .stMetric label {
        font-weight: 600 !important;
        color: #374151 !important;
    }
    .metric-box {
        background-color: #F3F4F6;
        border-left: 5px solid #2563EB;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATASET INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_data
def load_base_mto_data():
    raw_mto = [
        # --- S/E EGP 220/33 kV (GIS) ---
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Civil", "Item": "Excavación Suelo Tipo 2 (Roca Agrietada/H-3)", "Cantidad": 2673.5, "Unidad": "m³", "Rend_Base": 0.92, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Civil", "Item": "Excavación Suelo Tipo 3 (Grava Densa/H-1)", "Cantidad": 2673.5, "Unidad": "m³", "Rend_Base": 0.41, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Civil", "Item": "Excavación Suelo Tipo 4 (Suelo Fino/H-2)", "Cantidad": 1145.8, "Unidad": "m³", "Rend_Base": 0.41, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Civil", "Item": "Rellenos Compactados Estructurales", "Cantidad": 3190.2, "Unidad": "m³", "Rend_Base": 0.91, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Hormigones", "Item": "Hormigón Estructural G35 Pedestales", "Cantidad": 286.0, "Unidad": "m³", "Rend_Base": 4.40, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Hormigones", "Item": "Hormigón Estructural G35 Muros Cortafuego", "Cantidad": 512.8, "Unidad": "m³", "Rend_Base": 5.28, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Hormigones", "Item": "Hormigón Estructural G35 Zapatas / Losas / Edificios", "Cantidad": 2453.9, "Unidad": "m³", "Rend_Base": 3.80, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Hormigones", "Item": "Hormigón Emplantillado G10", "Cantidad": 292.0, "Unidad": "m³", "Rend_Base": 4.69, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Estructuras/Enfierradura", "Item": "Armadura Acero de Refuerzo A630-420H", "Cantidad": 252183.0, "Unidad": "kg", "Rend_Base": 0.060, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Estructuras/Enfierradura", "Item": "Malla Electrosoldada ACMA C-188", "Cantidad": 11539.0, "Unidad": "kg", "Rend_Base": 0.060, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Estructuras/Enfierradura", "Item": "Estructuras de Acero Soporte y Galpón GIS", "Cantidad": 139500.0, "Unidad": "kg", "Rend_Base": 0.0389, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Electromecánica", "Item": "Transformadores de Poder 125 MVA (220/33 kV)", "Cantidad": 3.0, "Unidad": "c/u", "Rend_Base": 1200.0, "Aplica_Clima": False, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Disciplina": "Electromecánica", "Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Cantidad": 1.0, "Unidad": "Gl", "Rend_Base": 15000.0, "Aplica_Clima": False, "Aplica_SIMOPS": True, "Aplica_ROT": True},

        # --- S/E Monte Mina 220 kV (AIS) ---
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Civil", "Item": "Excavación Patio AIS y Patios Mufas", "Cantidad": 2100.0, "Unidad": "m³", "Rend_Base": 0.41, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Hormigones", "Item": "Hormigón Estructural Fundaciones AIS", "Cantidad": 450.0, "Unidad": "m³", "Rend_Base": 4.40, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": False},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Electromecánica", "Item": "Interruptores Tanque Muerto SF6 220 kV 3150A", "Cantidad": 3.0, "Unidad": "c/u", "Rend_Base": 136.62, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Electromecánica", "Item": "Transformadores de Potencial TPC 220 kV", "Cantidad": 10.0, "Unidad": "c/u", "Rend_Base": 111.34, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Electromecánica", "Item": "Desconectadores Tripolares SPT/CPT 220 kV", "Cantidad": 10.0, "Unidad": "c/u", "Rend_Base": 342.75, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Electromecánica", "Item": "Pararrayos 220 kV y Aisladores Pedestal", "Cantidad": 12.0, "Unidad": "c/u", "Rend_Base": 107.55, "Aplica_Clima": True, "Aplica_SIMOPS": True, "Aplica_ROT": True},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Disciplina": "Electromecánica", "Item": "Cable XLPE 220 kV 3000 mm² (Cruce Subterráneo)", "Cantidad": 1800.0, "Unidad": "m", "Rend_Base": 1.25, "Aplica_Clima": False, "Aplica_SIMOPS": True, "Aplica_ROT": True},

        # --- Línea Transmisión 2x220 kV ---
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Civil", "Item": "Excavación Estructural Suelo 1 (Roca Sana)", "Cantidad": 53.5, "Unidad": "m³", "Rend_Base": 0.92, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Civil", "Item": "Excavación Estructural Suelo 2 (Unidad H-3)", "Cantidad": 645.6, "Unidad": "m³", "Rend_Base": 0.92, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Civil", "Item": "Excavación Estructural Suelo 3 (Unidad H-1)", "Cantidad": 3402.7, "Unidad": "m³", "Rend_Base": 0.41, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Civil", "Item": "Excavación Estructural Suelo 4 (Unidad H-2)", "Cantidad": 2358.8, "Unidad": "m³", "Rend_Base": 0.41, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Civil", "Item": "Relleno Compactado Fundaciones Torres", "Cantidad": 5271.0, "Unidad": "m³", "Rend_Base": 0.91, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Hormigones", "Item": "Hormigón Estructural G35 Fundaciones LAT", "Cantidad": 1210.8, "Unidad": "m³", "Rend_Base": 4.40, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Hormigones", "Item": "Hormigón Emplantillado G10 Fundaciones", "Cantidad": 98.7, "Unidad": "m³", "Rend_Base": 4.69, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Estructuras/Enfierradura", "Item": "Armadura Acero A630-420H Fundaciones LAT", "Cantidad": 126737.0, "Unidad": "kg", "Rend_Base": 0.060, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": False},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Estructuras/Enfierradura", "Item": "Montaje Torres Reticuladas A36/A572 (84 Torres)", "Cantidad": 1229600.0, "Unidad": "kg", "Rend_Base": 0.045, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": True},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Electromecánica", "Item": "Tendido Conductor AAAC Flint (312 km cto equiv)", "Cantidad": 312.0, "Unidad": "km", "Rend_Base": 140.0, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": True},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Electromecánica", "Item": "Tendido Cable OPGW / Guardia (54.7 km equiv)", "Cantidad": 54.7, "Unidad": "km", "Rend_Base": 110.0, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": True},
        {"Area": "Línea Transmisión 2x220 kV", "Disciplina": "Electromecánica", "Item": "Montaje Cadenas Aisladores y Herrajes", "Cantidad": 504.0, "Unidad": "Juego", "Rend_Base": 8.50, "Aplica_Clima": True, "Aplica_SIMOPS": False, "Aplica_ROT": True}
    ]
    return pd.DataFrame(raw_mto)

base_mto_df = load_base_mto_data()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & PARAMETERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## BHP ENC-3430")
st.sidebar.markdown("**Modelo de Ineficiencias Estándar BHP**")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Módulos de la Aplicación:",
    [
        "📊 Dashboard General de Ineficiencias",
        "⚙️ Matriz de Factores (Simulador Live)",
        "📋 Detalle de Ineficiencias por Partida",
        "👷 Planificación de Dotación & Curva S",
        "📤 Exportación de Resultados"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Ajuste Global de Factores (%)")

f_alt = st.sidebar.slider("F-ALT (Altura Geográfica 3.200 msnm):", 0.0, 30.0, 18.0, step=0.5) / 100.0
f_hsec = st.sidebar.slider("F-HSEC (Protocolos HSEC / Permisos):", 0.0, 25.0, 12.0, step=0.5) / 100.0
f_clima = st.sidebar.slider("F-CLIMA (Clima Atacama / Viento):", 0.0, 20.0, 8.0, step=0.5) / 100.0
f_turno = st.sidebar.slider("F-TURNO (Turnos 7x7 / Traslados):", 0.0, 15.0, 7.0, step=0.5) / 100.0
f_simops = st.sidebar.slider("F-SIMOPS (Interferencia SIMOPS):", 0.0, 20.0, 8.0, step=0.5) / 100.0
f_rot = st.sidebar.slider("F-ROT (Rotación / Curva Aprendizaje):", 0.0, 15.0, 5.0, step=0.5) / 100.0

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Parámetros Económicos")
blended_rate = st.sidebar.number_input("Tarifa Blended Rate (USD/HH):", value=38.5, step=0.5)
contract_months = st.sidebar.number_input("Plazo de Contrato (Meses):", value=12, step=1)
monthly_hours = st.sidebar.number_input("Jornada Mensual (HH/mes):", value=180, step=10)

# -----------------------------------------------------------------------------
# DYNAMIC CALCULATION ENGINE
# -----------------------------------------------------------------------------
def calculate_mto_inefficiencies(df, f_alt, f_hsec, f_clima, f_turno, f_simops, f_rot, rate):
    calc_df = df.copy()
    
    # Calculate base HH
    calc_df["HH_Base"] = calc_df["Cantidad"] * calc_df["Rend_Base"]
    
    # Calculate individual factors per item
    calc_df["P_ALT"] = f_alt
    calc_df["P_HSEC"] = f_hsec
    calc_df["P_CLIMA"] = np.where(calc_df["Aplica_Clima"], f_clima, 0.0)
    calc_df["P_TURNO"] = f_turno
    calc_df["P_SIMOPS"] = np.where(calc_df["Aplica_SIMOPS"], f_simops, 0.0)
    calc_df["P_ROT"] = np.where(calc_df["Aplica_ROT"], f_rot, 0.0)
    
    # Total inefficiency factor sum
    calc_df["Factor_Ineficiencia_Total"] = (
        calc_df["P_ALT"] + calc_df["P_HSEC"] + calc_df["P_CLIMA"] +
        calc_df["P_TURNO"] + calc_df["P_SIMOPS"] + calc_df["P_ROT"]
    )
    
    # Adjusted unit rate and real HH
    calc_df["Rend_Ajustado_BHP"] = calc_df["Rend_Base"] * (1.0 + calc_df["Factor_Ineficiencia_Total"])
    calc_df["HH_Reales_BHP"] = calc_df["Cantidad"] * calc_df["Rend_Ajustado_BHP"]
    calc_df["Incremento_HH"] = calc_df["HH_Reales_BHP"] - calc_df["HH_Base"]
    
    # Costs
    calc_df["Tarifa_USD_HH"] = rate
    calc_df["Costo_MO_Base_USD"] = calc_df["HH_Base"] * rate
    calc_df["Costo_MO_Real_USD"] = calc_df["HH_Reales_BHP"] * rate
    calc_df["Impacto_Ineficiencia_USD"] = calc_df["Incremento_HH"] * rate
    
    return calc_df

mto_calc = calculate_mto_inefficiencies(base_mto_df, f_alt, f_hsec, f_clima, f_turno, f_simops, f_rot, blended_rate)

# Summary metrics
total_hh_base = mto_calc["HH_Base"].sum()
total_hh_real = mto_calc["HH_Reales_BHP"].sum()
total_hh_increment = mto_calc["Incremento_HH"].sum()
pct_global_inefficiency = (total_hh_increment / total_hh_base) * 100.0 if total_hh_base > 0 else 0.0

total_cost_base = mto_calc["Costo_MO_Base_USD"].sum()
total_cost_real = mto_calc["Costo_MO_Real_USD"].sum()
total_cost_impact = mto_calc["Impacto_Ineficiencia_USD"].sum()

base_staffing = total_hh_base / (contract_months * monthly_hours)
real_staffing = total_hh_real / (contract_months * monthly_hours)
peak_staffing = real_staffing * 1.30

# -----------------------------------------------------------------------------
# MODULE 1: DASHBOARD GENERAL DE INEFICIENCIAS
# -----------------------------------------------------------------------------
if module == "📊 Dashboard General de Ineficiencias":
    st.markdown('<div class="main-header">Evaluación de Ineficiencias de Rendimiento (Estándar BHP)</div>', unsafe_allow_html=True)
    st.markdown("""<div class="sub-header">Análisis de Pérdida de Productividad por Altura Geográfica, Protocolos HSEC y Condiciones de Campo</div>""", unsafe_allow_html=True)

    # Top KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("HH Base (Saravia)", f"{total_hh_base:,.0f} HH", "Sin Ineficiencias")
    with k2:
        st.metric("HH Reales Ajustadas BHP", f"{total_hh_real:,.0f} HH", f"+{pct_global_inefficiency:.1f}% Pérdida")
    with k3:
        st.metric("Incremento Neto HH", f"{total_hh_increment:,.0f} HH", "Horas Adicionales")
    with k4:
        st.metric("Sobrecosto Directo MO", f"${total_cost_impact:,.0f} USD", f"@ ${blended_rate:.1f}/HH")
    with k5:
        st.metric("Dotación Real Requerida", f"{real_staffing:,.0f} Pers.", f"+{real_staffing - base_staffing:,.0f} vs Base")

    st.markdown("---")

    # Waterfall Chart: Transmission from Base HH to BHP Real HH
    col_w1, col_w2 = st.columns([6, 4])

    with col_w1:
        st.subheader("Desglose Waterfall del Incremento de HH por Factor")
        
        # Calculate individual factor contributions
        hh_alt = (mto_calc["HH_Base"] * mto_calc["P_ALT"]).sum()
        hh_hsec = (mto_calc["HH_Base"] * mto_calc["P_HSEC"]).sum()
        hh_clima = (mto_calc["HH_Base"] * mto_calc["P_CLIMA"]).sum()
        hh_turno = (mto_calc["HH_Base"] * mto_calc["P_TURNO"]).sum()
        hh_simops = (mto_calc["HH_Base"] * mto_calc["P_SIMOPS"]).sum()
        hh_rot = (mto_calc["HH_Base"] * mto_calc["P_ROT"]).sum()

        fig_waterfall = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x=["HH Base Saravia", "F-ALT (Altura)", "F-HSEC (Seguridad)", "F-CLIMA (Viento/Polvo)", "F-TURNO (7x7)", "F-SIMOPS (Interf.)", "F-ROT (Rotación)", "HH REALES BHP"],
            text=[f"{total_hh_base/1e3:.1f}k", f"+{hh_alt/1e3:.1f}k", f"+{hh_hsec/1e3:.1f}k", f"+{hh_clima/1e3:.1f}k", f"+{hh_turno/1e3:.1f}k", f"+{hh_simops/1e3:.1f}k", f"+{hh_rot/1e3:.1f}k", f"{total_hh_real/1e3:.1f}k"],
            y=[total_hh_base, hh_alt, hh_hsec, hh_clima, hh_turno, hh_simops, hh_rot, total_hh_real],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#EF4444"}},
            totals={"marker": {"color": "#1E3A8A"}}
        ))
        fig_waterfall.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_w2:
        st.subheader("Comparativa de HH Base vs. Real BHP por Área")
        area_group = mto_calc.groupby("Area")[["HH_Base", "HH_Reales_BHP"]].sum().reset_index()
        fig_area_comp = px.bar(
            area_group,
            x="Area",
            y=["HH_Base", "HH_Reales_BHP"],
            barmode="group",
            text_auto=".2s",
            color_discrete_sequence=["#93C5FD", "#1E3A8A"],
            labels={"value": "Horas Hombre", "variable": "Cómputo", "Area": "Instalación"}
        )
        fig_area_comp.update_layout(height=400, showlegend=True, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_area_comp, use_container_width=True)

    # Impact by Discipline
    st.subheader("Impacto Financiero de Ineficiencias por Disciplina Técnica (USD)")
    disc_summary = mto_calc.groupby("Disciplina")[["Costo_MO_Base_USD", "Impacto_Ineficiencia_USD", "Costo_MO_Real_USD"]].sum().reset_index()
    fig_disc = px.bar(
        disc_summary,
        x="Disciplina",
        y=["Costo_MO_Base_USD", "Impacto_Ineficiencia_USD"],
        text_auto=".2s",
        color_discrete_sequence=["#2563EB", "#EF4444"],
        labels={"value": "Costo Mano de Obra (USD)", "variable": "Componente"}
    )
    fig_disc.update_layout(height=380, barmode="stack")
    st.plotly_chart(fig_disc, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 2: MATRIZ DE FACTORES (SIMULADOR LIVE)
# -----------------------------------------------------------------------------
elif module == "⚙️ Matriz de Factores (Simulador Live)":
    st.markdown('<div class="main-header">Matriz de Factores de Ineficiencia de Campo</div>', unsafe_allow_html=True)
    st.markdown("""<div class="sub-header">Parametrización y Justificación Técnica según Estándares BHP HSEC y Geotecnia de Faena</div>""", unsafe_allow_html=True)

    factors_table = pd.DataFrame([
        {"Código": "F-ALT", "Factor de Ineficiencia": "Efecto Altura Geográfica (3.200 msnm)", "Valor Aplicado": f"{f_alt*100:.1f}%", "Rango Estándar": "15% - 25%", "Disciplinas Afectadas": "Todas las disciplinas en terreno", "Justificación Técnica": "Disminución de capacidad aeróbica por menor presión parcial de O2."},
        {"Código": "F-HSEC", "Factor de Ineficiencia": "Protocolos de Seguridad BHP HSEC", "Valor Aplicado": f"{f_hsec*100:.1f}%", "Rango Estándar": "10% - 15%", "Disciplinas Afectadas": "Todas las disciplinas en terreno", "Justificación Técnica": "Permisos Work Permit, análisis de riesgo FWRM, bloqueos LOTO y charlas."},
        {"Código": "F-CLIMA", "Factor de Ineficiencia": "Condiciones Climáticas Atacama", "Valor Aplicado": f"{f_clima*100:.1f}%", "Rango Estándar": "5% - 12%", "Disciplinas Afectadas": "Obras Civiles, Estructuras y Montaje LAT", "Justificación Técnica": "Vientos > 50 km/h que detienen izajes, polvo en suspensión y congelamiento."},
        {"Código": "F-TURNO", "Factor de Ineficiencia": "Sistema de Turnos Mineros 7x7 / 4x3", "Valor Aplicado": f"{f_turno*100:.1f}%", "Rango Estándar": "5% - 10%", "Disciplinas Afectadas": "Todas las disciplinas", "Justificación Técnica": "Fatiga en últimos días de turno, tiempos de traslado campamento-frente."},
        {"Código": "F-SIMOPS", "Factor de Ineficiencia": "Operaciones Simultáneas (SIMOPS)", "Valor Aplicado": f"{f_simops*100:.1f}%", "Rango Estándar": "5% - 12%", "Disciplinas Afectadas": "Subestaciones EGP y Monte Mina", "Justificación Técnica": "Interferencia con operadoras de la Planta Concentradora y líneas energizadas."},
        {"Código": "F-ROT", "Factor de Ineficiencia": "Curva de Aprendizaje y Rotación", "Valor Aplicado": f"{f_rot*100:.1f}%", "Rango Estándar": "3% - 8%", "Disciplinas Afectadas": "Montajes Electromecánicos", "Justificación Técnica": "Rotación de linieros y especialistas; curva de Inducción BHP."}
    ])

    st.dataframe(factors_table, use_container_width=True, height=280)

    st.markdown("---")
    st.subheader("💡 Resumen del Modelo de Pérdida de Productividad")
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.info(f"**Factor Acumulado Promedio:** +{pct_global_inefficiency:.1f}%\n\nCada 1,00 HH teórica requiere **{1.0 + (pct_global_inefficiency/100.0):.2f} HH reales** en terreno.")
    with c_m2:
        st.warning(f"**Horas Adicionales Requeridas:** {total_hh_increment:,.0f} HH\n\nDebido a restricciones operativas y de seguridad.")
    with c_m3:
        st.error(f"**Sobrecosto Total Directo:** ${total_cost_impact:,.0f} USD\n\nImpacto financiero directo en la partida de Mano de Obra.")

# -----------------------------------------------------------------------------
# MODULE 3: DETALLE DE INEFICIENCIAS POR PARTIDA
# -----------------------------------------------------------------------------
elif module == "📋 Detalle de Ineficiencias por Partida":
    st.markdown('<div class="main-header">Detalle MTO de Ineficiencias por Partida</div>', unsafe_allow_html=True)
    st.markdown("""<div class="sub-header">Cómputo Detallado del Rendimiento Ajustado Estándar BHP para cada Ítem de Cubicación</div>""", unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        sel_area = st.multiselect("Filtrar Área:", options=mto_calc["Area"].unique(), default=mto_calc["Area"].unique())
    with f_col2:
        sel_disc = st.multiselect("Filtrar Disciplina:", options=mto_calc["Disciplina"].unique(), default=mto_calc["Disciplina"].unique())
    with f_col3:
        search_item = st.text_input("🔍 Buscar Partida / Actividad:", "")

    mto_view = mto_calc[
        (mto_calc["Area"].isin(sel_area)) &
        (mto_calc["Disciplina"].isin(sel_disc))
    ]
    if search_item:
        mto_view = mto_view[mto_view["Item"].str.contains(search_item, case=False, na=False)]

    st.markdown(f"**Partidas encontradas:** {len(mto_view)}")

    st.dataframe(
        mto_view[[
            "Area", "Disciplina", "Item", "Cantidad", "Unidad",
            "Rend_Base", "HH_Base", "Factor_Ineficiencia_Total",
            "Rend_Ajustado_BHP", "HH_Reales_BHP", "Incremento_HH",
            "Costo_MO_Base_USD", "Impacto_Ineficiencia_USD", "Costo_MO_Real_USD"
        ]].rename(columns={
            "Rend_Base": "Rend. Saravia",
            "Factor_Ineficiencia_Total": "% Ineff Total",
            "Rend_Ajustado_BHP": "Rend. Ajust. BHP",
            "HH_Reales_BHP": "HH Reales BHP",
            "Incremento_HH": "Incremento HH",
            "Costo_MO_Base_USD": "Costo MO Base ($)",
            "Impacto_Ineficiencia_USD": "Impacto Ineff ($)",
            "Costo_MO_Real_USD": "Costo MO Real ($)"
        }).style.format({
            "Cantidad": "{:,.1f}",
            "Rend. Saravia": "{:,.3f}",
            "HH_Base": "{:,.1f}",
            "% Ineff Total": "{:.1%}",
            "Rend. Ajust. BHP": "{:,.3f}",
            "HH Reales BHP": "{:,.1f}",
            "Incremento HH": "{:,.1f}",
            "Costo MO Base ($)": "${:,.2f}",
            "Impacto Ineff ($)": "${:,.2f}",
            "Costo MO Real ($)": "${:,.2f}"
        }),
        use_container_width=True,
        height=450
    )

    sub_impact = mto_view["Impacto_Ineficiencia_USD"].sum()
    sub_hh_inc = mto_view["Incremento_HH"].sum()
    st.info(f"💡 **Subtotal Selección:** +{sub_hh_inc:,.1f} HH Adicionales | Impacto Financiero: **${sub_impact:,.2f} USD**")

# -----------------------------------------------------------------------------
# MODULE 4: PLANIFICACIÓN DE DOTACIÓN & CURVA S
# -----------------------------------------------------------------------------
elif module == "👷 Planificación de Dotación & Curva S":
    st.markdown('<div class="main-header">Planificación de Mano de Obra y Dotación de Campo</div>', unsafe_allow_html=True)
    st.markdown("""<div class="sub-header">Estimación de Personal Directo Necesario (Mes a Mes) e Histograma de Carga de Trabajo</div>""", unsafe_allow_html=True)

    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.metric("Dotación Teórica BASE", f"{base_staffing:,.0f} Personas", "Sin Ineficiencias")
    with d_col2:
        st.metric("Dotación REAL BHP", f"{real_staffing:,.0f} Personas", f"+{real_staffing-base_staffing:,.0f} por Ineficiencia")
    with d_col3:
        st.metric("Dotación Peak en Terreno", f"{peak_staffing:,.0f} Personas", "+30% Factor Peak Mes 6-7")

    st.markdown("---")
    st.subheader("Curva S Teórica vs. Real de Personal Directo (Meses 1 a 12)")

    # Monthly bell curve distribution factors for 12 months
    monthly_weights = np.array([0.03, 0.05, 0.08, 0.11, 0.13, 0.14, 0.14, 0.12, 0.09, 0.06, 0.03, 0.02])
    monthly_weights = monthly_weights / monthly_weights.sum()

    months = [f"Mes {i}" for i in range(1, 13)]
    hh_base_monthly = total_hh_base * monthly_weights
    hh_real_monthly = total_hh_real * monthly_weights

    staff_base_monthly = hh_base_monthly / monthly_hours
    staff_real_monthly = hh_real_monthly / monthly_hours

    curve_df = pd.DataFrame({
        "Mes": months,
        "Staff_Base": staff_base_monthly,
        "Staff_Real_BHP": staff_real_monthly,
        "HH_Real_Acumulada": np.cumsum(hh_real_monthly)
    })

    fig_staff = go.Figure()
    fig_staff.add_trace(go.Bar(x=curve_df["Mes"], y=curve_df["Staff_Base"], name="Dotación Base Teórica", marker_color="#93C5FD"))
    fig_staff.add_trace(go.Bar(x=curve_df["Mes"], y=curve_df["Staff_Real_BHP"], name="Dotación Real Ajustada BHP", marker_color="#1E3A8A"))
    
    fig_staff.update_layout(
        title="Histograma Mensual de Personal Directo en Faena (Personas/Mes)",
        barmode="group",
        height=420,
        xaxis_title="Mes de Ejecución",
        yaxis_title="Cantidad de Personas Directas",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_staff, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 5: EXPORTACIÓN DE RESULTADOS
# -----------------------------------------------------------------------------
elif module == "📤 Exportación de Resultados":
    st.markdown('<div class="main-header">Centro de Exportación de Resultados</div>', unsafe_allow_html=True)
    st.markdown("""<div class="sub-header">Descargar Tablas de Cálculo de Ineficiencias para Integración Presupuestaria</div>""", unsafe_allow_html=True)

    e1, e2 = st.columns(2)

    with e1:
        st.subheader("📥 Exportar Matriz MTO de Ineficiencias (CSV)")
        csv_mto = mto_calc.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Matriz MTO Ineficiencias (CSV)",
            data=csv_mto,
            file_name="BHP_ENC3430_Ineficiencias_MTO.csv",
            mime="text/csv"
        )

    with e2:
        st.subheader("📊 Exportar Consolidado por Área (CSV)")
        summary_export = mto_calc.groupby("Area")[["HH_Base", "HH_Reales_BHP", "Incremento_HH", "Costo_MO_Base_USD", "Impacto_Ineficiencia_USD", "Costo_MO_Real_USD"]].sum().reset_index()
        csv_summary = summary_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Consolidado Ineficiencias Áreas (CSV)",
            data=csv_summary,
            file_name="BHP_ENC3430_Consolidado_Ineficiencias.csv",
            mime="text/csv"
        )

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 BHP | Modelo de Ineficiencias HSEC & Altura - ENC-3430")
