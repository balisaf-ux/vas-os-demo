import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import random

# --- 1. VISUAL CORE: THE SOFT TRICOLOR PROTOCOL ---
def set_design_system():
    st.set_page_config(page_title="Veridian | Group OS", layout="wide", page_icon="🦅")
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* GLOBAL THEME */
        .stApp { background-color: #F8F9FA; color: #2C3E50; font-family: 'Inter', sans-serif; }
        
        /* TYPOGRAPHY */
        h1, h2, h3 { color: #0056b3 !important; font-weight: 800; letter-spacing: -0.5px; }
        h4, h5, .stMetricLabel { color: #5D6D7E !important; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; }
        
        /* METRIC CARDS */
        div[data-testid="stMetricValue"] { color: #2C3E50 !important; font-weight: 700; }
        
        /* CARDS & CONTAINERS */
        .css-1r6slb0, div.stDataFrame, .stPlotlyChart, div[data-testid="stForm"], div[data-testid="stExpander"] {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #E5E8EB;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        
        /* SIDEBAR */
        section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E8EB; }
        
        /* BUTTONS (Trust Blue) */
        .stButton > button {
            background-color: #0056b3; color: white; border-radius: 8px; border: none; padding: 0.5rem 1rem;
            font-weight: 600; transition: all 0.2s;
        }
        .stButton > button:hover { background-color: #004494; box-shadow: 0 4px 8px rgba(0,86,179,0.2); }
        
        /* ALERTS */
        .alert-box { padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.9rem; border-left: 4px solid; }
        .alert-red { background-color: #FDEDEC; color: #922B21; border-color: #D9534F; }
        .alert-green { background-color: #EAFAF1; color: #186A3B; border-color: #27AE60; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION & STATE MANAGEMENT (THE MEMORY BANK) ---
def check_login():
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

    if st.session_state.user_role is None:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("## 🔒 VAS | OS Secure Login")
            st.markdown("Veridian Autonomous Systems v3.3 (Logic Restored)")
            
            # THE DEMO KEYS
            role = st.selectbox("Select Identity (Simulated)", 
                ["Select Identity...", "ADMIN_VAS (Balisa)", "CLIENT_SR (Sturrock Exec)"])
            
            if st.button("Authenticate"):
                if role == "ADMIN_VAS (Balisa)":
                    st.session_state.user_role = "ADMIN"
                    init_cortex_db() # Load the Logic
                    st.rerun()
                elif role == "CLIENT_SR (Sturrock Exec)":
                    st.session_state.user_role = "CLIENT"
                    st.rerun()
                else:
                    st.error("Identity Required")
        return False
    return True

def init_cortex_db():
    # RESTORING PROJECT CORTEX LOGIC:
    # We initialize session_state with mutable dataframes so edits persist during the session.
    
    if 'deals_db' not in st.session_state:
        # The CRM Database
        data = {
            'Deal Name': ['Sturrock & Robson Pilot', 'JCI Sandton Expansion', 'Bonnyvale Off-Take', 'EnergyShield Seed Round', 'Pineapple Export Logistics'],
            'Entity': ['VAS', 'FAFT', 'Bonnyvale', 'EnergyShield', 'Bonnyvale'],
            'Stage': ['Proposal', 'Lead', 'Negotiation', 'Due Diligence', 'Active'],
            'Value (ZAR)': [35000, 1500000, 450000, 5000000, 120000],
            'Probability': [0.9, 0.4, 0.7, 0.5, 1.0],
            'Next Action': ['Audit Engagement', 'Sister Presentation', 'Contract Review', 'Data Room Prep', 'Route Opt.']
        }
        st.session_state.deals_db = pd.DataFrame(data)

    if 'hunter_db' not in st.session_state:
        # The Prospecting Database (Raw Targets)
        targets = {
            'Company': ['Orion Mining', 'Titan Logistics', 'Apex Retail', 'Delta Energy', 'Echo Farms'],
            'Sector': ['Mining', 'Logistics', 'Retail', 'Energy', 'Agriculture'],
            'Turnover (ZAR)': [85000000, 12000000, 55000000, 120000000, 8000000],
            'Region': ['North West', 'Gauteng', 'KZN', 'Mpumalanga', 'Eastern Cape'],
            'Status': ['Cold', 'Target', 'Target', 'Cold', 'Warm']
        }
        st.session_state.hunter_db = pd.DataFrame(targets)

def logout():
    st.session_state.user_role = None
    st.rerun()

# --- 3. INTERNAL OPS MODULES (RESTORED FUNCTIONALITY) ---
def render_crm_module():
    st.markdown("## 🤝 DealStream (Group CRM)")
    st.caption("Internal Pipeline Management & Execution")

    df = st.session_state.deals_db # Access the mutable DB
    
    # 1. LIVE METRICS (Calculated from real state)
    weighted_val = (df['Value (ZAR)'] * df['Probability']).sum()
    total_val = df['Value (ZAR)'].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Pipeline", f"R {total_val:,.0f}", f"{len(df)} Deals")
    m2.metric("Weighted Forecast", f"R {weighted_val:,.0f}", "Risk Adjusted")
    m3.metric("Win Rate (Est)", "32%", "+4%")
    
    st.divider()

    # 2. THE INTERACTIVE WORKSPACE
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("Active Opportunities")
        # Visual Polish: Color code by Probability
        st.dataframe(
            df.style.background_gradient(subset=['Probability'], cmap="Blues"),
            use_container_width=True,
            hide_index=True
        )
    
    with c2:
        st.subheader("Deal Inspector")
        # FUNCTIONALITY RESTORED: Edit a Deal
        selected_deal = st.selectbox("Select Deal to Edit", df['Deal Name'].unique())
        
        # Get current values
        current_row = df[df['Deal Name'] == selected_deal].iloc[0]
        
        with st.form("edit_deal_form"):
            # Ensure the current stage is in the list
            stages = ["Lead", "Meeting", "Proposal", "Negotiation", "Closed", "Active"]
            current_stage = current_row['Stage']
            default_index = stages.index(current_stage) if current_stage in stages else 0
            
            new_stage = st.selectbox("Update Stage", stages, index=default_index)
            new_prob = st.slider("Update Probability", 0.0, 1.0, float(current_row['Probability']))
            submitted = st.form_submit_button("Update Deal Record")
            
            if submitted:
                # Update the database
                idx = df.index[df['Deal Name'] == selected_deal].tolist()[0]
                st.session_state.deals_db.at[idx, 'Stage'] = new_stage
                st.session_state.deals_db.at[idx, 'Probability'] = new_prob
                st.success(f"Updated {selected_deal}")
                st.rerun()

    # 3. ADD NEW DEAL (RESTORED)
    with st.expander("➕ Add Manual Entry"):
        with st.form("new_deal"):
            c_a, c_b = st.columns(2)
            with c_a:
                d_name = st.text_input("Deal Name")
                d_entity = st.selectbox("Entity", ["VAS", "FAFT", "Bonnyvale", "EnergyShield"])
            with c_b:
                d_val = st.number_input("Value (ZAR)", step=10000)
                d_stage = st.selectbox("Initial Stage", ["Lead", "Meeting", "Proposal"])
            
            if st.form_submit_button("Add to Pipeline"):
                new_row = pd.DataFrame({
                    'Deal Name': [d_name], 'Entity': [d_entity], 'Stage': [d_stage],
                    'Value (ZAR)': [d_val], 'Probability': [0.1], 'Next Action': ['Initial Contact']
                })
                st.session_state.deals_db = pd.concat([st.session_state.deals_db, new_row], ignore_index=True)
                st.success("Deal Added")
                st.rerun()

def render_hunter_module():
    st.markdown("## 🦅 Hunter (Prospecting Engine)")
    st.caption("Market Segmentation & Target Identification")
    
    df_hunt = st.session_state.hunter_db
    
    # 1. FILTERS (RESTORED)
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            sector_filter = st.multiselect("Filter by Sector", df_hunt['Sector'].unique(), default=df_hunt['Sector'].unique())
        with c2:
            region_filter = st.multiselect("Filter by Region", df_hunt['Region'].unique(), default=df_hunt['Region'].unique())
        with c3:
            min_rev = st.number_input("Min Turnover (ZAR)", 0, 100000000, 0)
            
    # Apply Filters
    filtered_df = df_hunt[
        (df_hunt['Sector'].isin(sector_filter)) & 
        (df_hunt['Region'].isin(region_filter)) & 
        (df_hunt['Turnover (ZAR)'] >= min_rev)
    ]
    
    st.divider()
    
    # 2. ACTIONABLE LIST
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # 3. CONVERSION LOGIC
    st.subheader("Convert to Lead")
    c1, c2 = st.columns([2,1])
    with c1:
        target_to_convert = st.selectbox("Select Target to Promote", filtered_df['Company'].unique())
    with c2:
        if st.button("Promote to DealStream"):
            # Logic to move from Hunter DB to Deals DB
            target_row = df_hunt[df_hunt['Company'] == target_to_convert].iloc[0]
            new_deal = pd.DataFrame({
                'Deal Name': [target_row['Company'] + " - Initial Scope"], 
                'Entity': ["VAS"], 
                'Stage': ["Lead"],
                'Value (ZAR)': [target_row['Turnover (ZAR)'] * 0.05], # Assume 5% deal size
                'Probability': [0.1], 
                'Next Action': ['Outreach']
            })
            st.session_state.deals_db = pd.concat([st.session_state.deals_db, new_deal], ignore_index=True)
            st.success(f"Promoted {target_to_convert} to CRM!")

# --- 4. CLIENT / MOCK DATA (UNCHANGED) ---
def get_fuel_data():
    dates = pd.date_range(start='2025-12-01', periods=14, freq='D')
    flow = [12000, 12500, 11900, 12100, 12300, 12050, 11800, 12200, 12400, 12100, 12300, 12000, 11500, 9800] 
    return pd.DataFrame({'Date': dates, 'Flow Rate (L/hr)': flow})

def get_safety_docs():
    return pd.DataFrame({
        'Document': ['Site_Inspection_Secunda.pdf', 'PPE_Audit_JHB.pdf', 'Incident_Report_KZN.pdf', 'Compliance_Cert_04.pdf'],
        'Status': ['Processed', 'Processed', 'FLAGGED', 'Processed'],
        'Risk Score': ['Low', 'Low', 'HIGH', 'Low'],
        'Date': ['Today 09:00', 'Today 08:30', 'Yesterday', 'Yesterday']
    })

# --- 5. RENDER CLIENT MODULES ---
def render_group_dashboard():
    st.markdown("## 🦅 Group Control Tower")
    st.caption("Aggregated oversight across **Liquid Automation**, **Safety**, and **Thermal**.")
    # Executive Smoothing Algorithm (Visuals)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Real-Time Operational Health")
        time_index = pd.date_range("2025-12-01", periods=20, freq="H")
        np.random.seed(42) 
        las_data = 100 + np.random.randn(20).cumsum() 
        safety_data = 95 + (np.random.randn(20) * 0.3).cumsum()
        thermal_data = 88 + np.sin(np.linspace(0, 4, 20)) * 5 + np.random.normal(0, 0.5, 20)
        chart_data = pd.DataFrame({"LAS Efficiency": las_data, "Safety Score": safety_data, "Thermal Output": thermal_data}, index=time_index)
        st.line_chart(chart_data, color=["#0056b3", "#27AE60", "#C0392B"]) 
    with col2:
        st.subheader("Critical Alerts")
        st.markdown("""
        <div class="alert-box alert-red"><b>⚠️ LAS (Jwaneng):</b> Flow rate deviation >15% detected at Pump 4. Potential leak.</div>
        <div class="alert-box alert-red"><b>⚠️ Safety (KZN):</b> Incident Report #902 flagged for immediate review.</div>
        <div class="alert-box alert-green"><b>✅ Thermal:</b> Predictive maintenance check passed on Boiler 3.</div>
        """, unsafe_allow_html=True)

def render_las_module():
    st.markdown("## 💧 Liquid Automation Systems")
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Flow Rate", "9,800 L/hr", "-1,200 L/hr", delta_color="inverse")
    m2.metric("Tank Level", "82%", "Stable")
    m3.metric("Theft Prediction", "HIGH RISK", "AI Confidence: 94%")
    st.divider()
    st.subheader("Anomaly Detection Engine")
    df = get_fuel_data()
    c = alt.Chart(df).mark_area(line={'color':'#0056b3'}, color=alt.Gradient(gradient='linear', stops=[alt.GradientStop(color='#0056b3', offset=0), alt.GradientStop(color='rgba(255,255,255,0)', offset=1)], x1=1, x2=1, y1=1, y2=0)).encode(x='Date', y='Flow Rate (L/hr)', tooltip=['Date', 'Flow Rate (L/hr)']).properties(height=300)
    st.altair_chart(c, use_container_width=True)
    st.error("🚨 ANOMALY DETECTED: Sudden drop in flow rate.")

def render_safety_module():
    st.markdown("## 🦺 Sturrock Safety (HSE)")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("ℹ️ **AI Agent Status:** Watching folder `Input/Scans`")
        uploaded_file = st.file_uploader("Drop Scanned PDF Here", type=['pdf'])
        if uploaded_file:
            with st.spinner("Extracting Data..."): time.sleep(1)
            st.success("File received. Compliance: YES")
    with c2:
        st.subheader("Live Processing Queue")
        st.dataframe(get_safety_docs(), use_container_width=True, hide_index=True)

def render_admin_home():
    st.markdown("## 🌍 Central Command (God View)")
    c1, c2, c3 = st.columns(3)
    
    # Calculate Real Total from the DB
    if 'deals_db' in st.session_state:
        real_pipeline_val = st.session_state.deals_db['Value (ZAR)'].sum()
        c1.metric("Total System Value", f"R {real_pipeline_val:,.0f}", "Live Data")
    else:
        c1.metric("Total System Value", "R 0", "No Data")
        
    c2.metric("Active Nodes", "3", "JHB • EL • MP")
    c3.metric("Global Alert Level", "LOW", "Stable")
    st.divider()
    st.subheader("Sovereign Footprint")
    map_data = pd.DataFrame({'lat': [-26.1076, -25.8728, -32.9833], 'lon': [28.0567, 29.2554, 27.8667], 'Entity': ['Veridian HQ', 'S&R Site', 'Bonnyvale'], 'Status': ['Online', 'Alert', 'Online']})
    st.map(map_data, zoom=5, use_container_width=True)

# --- 6. MAIN CONTROLLER ---
def main():
    set_design_system()
    
    if not check_login():
        return

    with st.sidebar:
        st.title("VAS | OS")
        st.caption("Veridian Autonomous Systems")
        
        if st.session_state.user_role == "ADMIN":
            st.markdown("Identity: **STRATEGIST** (God Mode)")
            menu = st.radio("Navigation", 
                ["Central Command", "DealStream (CRM)", "Hunter (Prospecting)", "S&R Overlay (Sim)"])
        else:
            st.markdown("Identity: **CLIENT** (S&R Exec)")
            menu = st.radio("Navigation", 
                ["Group Cockpit", "Liquid Automation", "Sturrock Safety"])
        
        st.divider()
        if st.button("Log Out"): logout()

    # ROUTING
    if st.session_state.user_role == "ADMIN":
        if menu == "Central Command": render_admin_home()
        elif menu == "DealStream (CRM)": render_crm_module()
        elif menu == "Hunter (Prospecting)": render_hunter_module()
        elif menu == "S&R Overlay (Sim)": render_group_dashboard()
            
    elif st.session_state.user_role == "CLIENT":
        if menu == "Group Cockpit": render_group_dashboard()
        elif menu == "Liquid Automation": render_las_module()
        elif menu == "Sturrock Safety": render_safety_module()

if __name__ == "__main__":
    main()
