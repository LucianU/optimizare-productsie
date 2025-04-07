
import streamlit as st
from scipy.optimize import linprog
import numpy as np

st.set_page_config(page_title="Optimizare producție îngrășăminte", page_icon="🧪", layout="centered")
st.title("🧪 Optimizare producție — exemplu Norofert")

st.markdown("Introduceți datele pentru fiecare produs, apoi apăsați **Calculează** pentru a vedea combinația optimă care maximizează profitul.")

with st.form("input_form"):
    st.subheader("🔢 Parametrii de intrare")

    with st.expander("🌾 Starter"):
        cost_starter = st.number_input("Cost de producție (RON/unitate)", value=40.0, key="cost_starter")
        profit_starter = st.number_input("Profit net estimat (RON/unitate)", value=30.0, key="profit_starter")
        min_starter = st.number_input("Cerere minimă estimată (unități)", value=500, key="min_starter")
        max_starter = st.number_input("Capacitate maximă de producție (unități)", value=3000, key="max_starter")

    with st.expander("🌿 Naturamin"):
        cost_naturamin = st.number_input("Cost de producție (RON/unitate)", value=60.0, key="cost_naturamin")
        profit_naturamin = st.number_input("Profit net estimat (RON/unitate)", value=50.0, key="profit_naturamin")
        min_naturamin = st.number_input("Cerere minimă estimată (unități)", value=300, key="min_naturamin")
        max_naturamin = st.number_input("Capacitate maximă de producție (unități)", value=2000, key="max_naturamin")

    with st.expander("🌱 Karbo"):
        cost_karbo = st.number_input("Cost de producție (RON/unitate)", value=30.0, key="cost_karbo")
        profit_karbo = st.number_input("Profit net estimat (RON/unitate)", value=25.0, key="profit_karbo")
        min_karbo = st.number_input("Cerere minimă estimată (unități)", value=400, key="min_karbo")
        max_karbo = st.number_input("Capacitate maximă de producție (unități)", value=2500, key="max_karbo")

    st.markdown("---")
    total_budget = st.number_input("💰 Buget total disponibil (RON)", value=200000.0)

    submitted = st.form_submit_button("Calculează")

if submitted:
    # validări de bază
    warnings = []

    if min_starter > max_starter:
        warnings.append("⚠️ Cererea minimă pentru Starter depășește capacitatea maximă.")
    if min_naturamin > max_naturamin:
        warnings.append("⚠️ Cererea minimă pentru Naturamin depășește capacitatea maximă.")
    if min_karbo > max_karbo:
        warnings.append("⚠️ Cererea minimă pentru Karbo depășește capacitatea maximă.")

    if profit_starter < 0:
        warnings.append("⚠️ Profitul net pentru Starter este negativ.")
    if profit_naturamin < 0:
        warnings.append("⚠️ Profitul net pentru Naturamin este negativ.")
    if profit_karbo < 0:
        warnings.append("⚠️ Profitul net pentru Karbo este negativ.")

    if total_budget <= 0:
        warnings.append("⚠️ Bugetul total trebuie să fie mai mare decât 0.")

    if warnings:
        for w in warnings:
            st.warning(w)
        st.stop()

    # coeficienți funcție obiectiv (profit negativ pt. maximizare)
    c = [-profit_starter, -profit_naturamin, -profit_karbo]

    # matricea A_ub (<=)
    A = [
        [cost_starter, cost_naturamin, cost_karbo],
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    b = [
        total_budget,
        -min_starter,
        -min_naturamin,
        -min_karbo,
        max_starter,
        max_naturamin,
        max_karbo
    ]

    bounds = [(0, None), (0, None), (0, None)]

    result = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if result.success:
        x = np.round(result.x, 2)
        total_profit = -result.fun
        st.success("✅ Soluție optimă găsită!")

        st.markdown(f"""
        - **Starter:** {x[0]} unități  
        - **Naturamin:** {x[1]} unități  
        - **Karbo:** {x[2]} unități  
        - 💸 **Profit total estimat:** `{total_profit:.2f} RON`
        """)
    else:
        st.error("❌ Nu s-a găsit o soluție validă. Verificați dacă cerințele minime sau costurile nu depășesc bugetul.")
