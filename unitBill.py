import streamlit as st
import pandas as pd
from io import StringIO

# Page setup
st.set_page_config(page_title="Electricity Bill Splitter", layout="centered")

# Custom styles
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 14px;
    }

    input, select, textarea {
        font-size: 13px !important;
        height: 30px !important;
    }

    .stTextInput input, .stNumberInput input {
        font-size: 13px !important;
        height: 30px !important;
    }

    .stButton button {
        font-size: 13px !important;
        padding: 6px 12px !important;
    }

    .stDownloadButton button {
        font-size: 13px !important;
        padding: 6px 12px !important;
    }

    .stForm {
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("💡 Electricity Bill Splitter")
st.markdown("Made by M.Zaid Naeem")

# ---------------- Session State ------------------
if "data" not in st.session_state:
    st.session_state.data = [{"name": "others", "units": 0.0}]
    st.session_state.unit_sum = 0.0
    st.session_state.total_bill = 0.0
    st.session_state.bill_month = ""

if "name_input" not in st.session_state:
    st.session_state.name_input = ""
if "start_input" not in st.session_state:
    st.session_state.start_input = 0.0
if "end_input" not in st.session_state:
    st.session_state.end_input = 0.0
if "other_input" not in st.session_state:
    st.session_state.other_input = 0.0

# ---------------- Input: Total Bill + Month ------------------
st.session_state.bill_month = st.text_input("🗓️ Enter Bill Month (e.g., july_2025)", value=st.session_state.bill_month)
st.session_state.total_bill = st.number_input("💰 Enter Total Bill (Rs.)", min_value=0.0, step=10.0)

# ---------------- Add Entry Form ------------------
with st.form("entry_form"):
    st.subheader("➕ Add User Entry")

    st.session_state.name_input = st.text_input("👤 Name", value=st.session_state.name_input)
    st.session_state.start_input = st.number_input("🔢 Starting Units", min_value=0.0, key="start")
    st.session_state.end_input = st.number_input("🔢 Ending Units", min_value=0.0, key="end")
    st.session_state.other_input = st.number_input("🔄 Other Units (Shared/Unaccounted)", min_value=0.0)

    submitted = st.form_submit_button("✅ Add Entry")

    if submitted:
        name = st.session_state.name_input.strip().lower()
        start = st.session_state.start_input
        end = st.session_state.end_input
        other = st.session_state.other_input

        if not name:
            st.error("Name cannot be empty.")
        elif start > end:
            st.error("❌ Starting units must be smaller than ending units.")
        else:
            total_units = end - start
            st.session_state.unit_sum += total_units + other
            st.session_state.data[0]["units"] += other

            found = False
            for person in st.session_state.data:
                if person["name"] == name:
                    person["units"] += total_units
                    st.success(f"✅ Updated {name} by {total_units} units.")
                    found = True
                    break

            if not found:
                st.session_state.data.append({"name": name, "units": total_units})
                st.success(f"🆕 Created {name} with {total_units} units.")

            # Clear inputs
            st.session_state.name_input = ""
            st.session_state.start_input = 0.0
            st.session_state.end_input = 0.0
            st.session_state.other_input = 0.0

# ---------------- Final Summary ------------------
if st.session_state.unit_sum > 0:
    st.markdown("---")
    st.markdown("### 📊 Final Summary")
    st.write(f"**Total Units ⚡:** {round(st.session_state.unit_sum, 2)}")

    # Calculate per unit cost if bill entered
    per_unit_bill = (
        st.session_state.total_bill / st.session_state.unit_sum
        if st.session_state.total_bill > 0
        else 0.0
    )

    if st.session_state.total_bill > 0:
        st.write(f"**Per Unit Cost 💸:** Rs. {round(per_unit_bill, 2)}")
    else:
        st.warning("⚠️ Enter total bill to calculate individual shares.")

    # Build table
    table_data = [
        {
            "Name": person["name"],
            "Units": round(person["units"], 2),
            "Bill (Rs.)": round(person["units"] * per_unit_bill, 2)
            if st.session_state.total_bill > 0
            else "—",
        }
        for person in st.session_state.data
    ]
    st.table(table_data)

    # ---------------- Export CSV ------------------
    if st.session_state.total_bill > 0:
        df_export = pd.DataFrame(table_data)

        summary_df = pd.DataFrame({
            "Name": ["Total Units", "Total Bill", "Per Unit Cost"],
            "Units": [round(st.session_state.unit_sum, 2), "", ""],
            "Bill (Rs.)": ["", round(st.session_state.total_bill, 2), round(per_unit_bill, 2)]
        })

        df_export = pd.concat([df_export, summary_df], ignore_index=True)

        csv_buffer = StringIO()
        df_export.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        month = st.session_state.bill_month.strip().replace(" ", "_").lower() or "bill"
        file_name = f"{month}_bill_by_m_zaid_naeem.csv"

        st.download_button(
            label=f"⬇️ Download Summary ({file_name})",
            data=csv_data,
            file_name=file_name,
            mime="text/csv"
        )
