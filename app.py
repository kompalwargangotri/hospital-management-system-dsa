import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
        font-size: 1.1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA STRUCTURES (Ported from C++) ---

class PatientNode:
    def __init__(self, id_val, name, age, disease):
        self.id = id_val
        self.name = name
        self.age = age
        self.disease = disease
        self.next = None

class PatientLinkedList:
    def __init__(self):
        self.head = None

    def add_patient(self, id_val, name, age, disease):
        new_node = PatientNode(id_val, name, age, disease)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def delete_patient(self, id_val):
        if not self.head:
            return False, "No records to delete."

        temp = self.head
        prev = None

        # If head node holds the key
        if temp.id == id_val:
            self.head = temp.next
            return True, f"Patient with ID {id_val} deleted successfully."

        # Search for key
        while temp and temp.id != id_val:
            prev = temp
            temp = temp.next

        # Key not present
        if not temp:
            return False, f"Patient with ID {id_val} not found."

        # Unlink the node
        prev.next = temp.next
        return True, f"Patient with ID {id_val} deleted successfully."

    def get_all_patients(self):
        patients = []
        temp = self.head
        while temp:
            patients.append({
                "ID": temp.id,
                "Name": temp.name,
                "Age": temp.age,
                "Disease": temp.disease
            })
            temp = temp.next
        return patients

    def contains_id(self, id_val):
        temp = self.head
        while temp:
            if temp.id == id_val:
                return True
            temp = temp.next
        return False


class DoctorNode:
    def __init__(self, id_val, name, specialization, available):
        self.id = id_val
        self.name = name
        self.specialization = specialization
        self.available = available
        self.next = None

class DoctorList:
    def __init__(self):
        self.head = None

    def add_doctor(self, id_val, name, specialization, available):
        new_node = DoctorNode(id_val, name, specialization, available)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def get_all_doctors(self):
        doctors = []
        temp = self.head
        while temp:
            doctors.append({
                "ID": temp.id,
                "Name": temp.name,
                "Specialization": temp.specialization,
                "Available": "Yes" if temp.available else "No"
            })
            temp = temp.next
        return doctors

    def contains_id(self, id_val):
        temp = self.head
        while temp:
            if temp.id == id_val:
                return True
            temp = temp.next
        return False


class BedManager:
    def __init__(self, total=10):
        self.total_beds = total
        self.beds = [{"bed_number": i + 1, "patient_name": "", "disease": "", "is_occupied": False} for i in range(total)]

    @property
    def occupied_beds(self):
        return sum(1 for bed in self.beds if bed["is_occupied"])

    def admit_patient(self, patient_name, disease):
        for bed in self.beds:
            if not bed["is_occupied"]:
                bed["is_occupied"] = True
                bed["patient_name"] = patient_name
                bed["disease"] = disease
                return True, f"Patient {patient_name} admitted to Bed {bed['bed_number']}."
        return False, "No beds available!"

    def discharge_patient(self, bed_number):
        if 1 <= bed_number <= self.total_beds:
            bed = self.beds[bed_number - 1]
            if bed["is_occupied"]:
                name = bed["patient_name"]
                bed["is_occupied"] = False
                bed["patient_name"] = ""
                bed["disease"] = ""
                return True, f"Patient {name} discharged from Bed {bed_number}."
            return False, f"Bed {bed_number} is already empty."
        return False, "Invalid bed number."


# --- STATE INITIALIZATION ---

if "patients" not in st.session_state:
    st.session_state.patients = PatientLinkedList()
    # Populate default demo records
    st.session_state.patients.add_patient(1, "Sneha Patil", 30, "Arrhythmia")
    st.session_state.patients.add_patient(2, "Sahil Sharma", 45, "Osteoarthritis")
    st.session_state.patients.add_patient(3, "Priya Patel", 29, "Migraine")
    st.session_state.patients.add_patient(4, "Nikhil Deshmukh", 55, "Eczema")
    st.session_state.patients.add_patient(5, "Riya Verma", 52, "Lung Cancer")

if "doctors" not in st.session_state:
    st.session_state.doctors = DoctorList()
    # Populate default demo records
    st.session_state.doctors.add_doctor(1, "Dr. Rajesh Kumar", "Cardiologist", True)
    st.session_state.doctors.add_doctor(2, "Dr. Sunita Rao", "Neurology", True)
    st.session_state.doctors.add_doctor(3, "Dr. Vikas Mehta", "Dermatology", True)
    st.session_state.doctors.add_doctor(4, "Dr. Nikita Sen", "General Medicine", True)
    st.session_state.doctors.add_doctor(5, "Dr. Amit Verma", "Oncology", False)

if "beds" not in st.session_state or not hasattr(st.session_state.beds, "beds"):
    st.session_state.beds = BedManager(total=10)


# --- SIDEBAR NAVIGATION ---

st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="color: #0284c7; margin-bottom: 0;">🏥 Hospital Panel</h2>
    <span style="color: #64748b; font-size: 0.9rem;">Data Structures Project</span>
</div>
""", unsafe_allow_html=True)

menu_choice = st.sidebar.radio(
    "Navigate System",
    [
        "📊 Dashboard Overview",
        "📋 Patient Records",
        "🩺 Doctor Registry",
        "🛏️ Bed Management"
    ]
)

# Header Section
st.markdown(f"""
<div class="main-header">
    <h1>Hospital Management System</h1>
    <p>Interactive Python Web UI mirroring C++ Linked List Data Structures</p>
</div>
""", unsafe_allow_html=True)


# --- DASHBOARD PAGE ---
if menu_choice == "📊 Dashboard Overview":
    st.subheader("System Performance & Metrics")
    
    # Calculate values
    patient_list = st.session_state.patients.get_all_patients()
    doctor_list = st.session_state.doctors.get_all_doctors()
    
    total_patients = len(patient_list)
    total_doctors = len(doctor_list)
    available_beds = st.session_state.beds.total_beds - st.session_state.beds.occupied_beds
    occupancy_rate = (st.session_state.beds.occupied_beds / st.session_state.beds.total_beds) * 100

    # Grid columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Patients", value=total_patients, help="Total patient records stored")
    with col2:
        st.metric(label="Total Registered Doctors", value=total_doctors, help="Total registered doctors")
    with col3:
        st.metric(label="Available Beds", value=available_beds, delta=f"{st.session_state.beds.occupied_beds} Occupied")
    with col4:
        st.metric(label="Bed Occupancy Rate", value=f"{occupancy_rate:.1f}%")

    st.markdown("---")

    # Quick Summary Cards
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("#### Recent Patients")
        if patient_list:
            df_patients = pd.DataFrame(patient_list).tail(5)
            st.dataframe(df_patients, use_container_width=True, hide_index=True)
        else:
            st.info("No patient records registered yet.")
            
    with right_col:
        st.markdown("#### Doctor Availability Status")
        if doctor_list:
            df_doctors = pd.DataFrame(doctor_list)
            st.dataframe(df_doctors, use_container_width=True, hide_index=True)
        else:
            st.info("No doctors registered yet.")


# --- PATIENT RECORDS PAGE ---
elif menu_choice == "📋 Patient Records":
    st.subheader("Patient Database")
    
    tab1, tab2, tab3 = st.tabs(["View Records", "Add Patient", "Delete Patient"])
    
    with tab1:
        patient_list = st.session_state.patients.get_all_patients()
        if patient_list:
            df_patients = pd.DataFrame(patient_list)
            
            # Simple search filter
            search_query = st.text_input("🔍 Search patients by name or disease:", "")
            if search_query:
                filtered_df = df_patients[
                    df_patients["Name"].str.contains(search_query, case=False, na=False) |
                    df_patients["Disease"].str.contains(search_query, case=False, na=False)
                ]
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                st.caption(f"Showing {len(filtered_df)} of {len(df_patients)} patient records.")
            else:
                st.dataframe(df_patients, use_container_width=True, hide_index=True)
                st.caption(f"Showing all {len(df_patients)} patients.")
        else:
            st.info("No patient records available.")

    with tab2:
        st.write("### Add Patient Record")
        with st.form("add_patient_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                p_id = st.number_input("Patient ID", min_value=1, step=1, value=1)
                p_name = st.text_input("Patient Name", placeholder="Enter name")
            with col2:
                p_age = st.number_input("Age", min_value=0, max_value=120, value=30)
                p_disease = st.text_input("Disease/Department", placeholder="e.g. Cardiology, Orthopedics")
                
            submitted = st.form_submit_button("Add Patient Record")
            if submitted:
                if not p_name or not p_disease:
                    st.error("Name and Disease fields cannot be empty!")
                elif st.session_state.patients.contains_id(p_id):
                    st.error(f"Patient ID {p_id} already exists. Please choose a unique ID.")
                else:
                    st.session_state.patients.add_patient(p_id, p_name, p_age, p_disease)
                    st.success(f"Patient '{p_name}' added successfully!")
                    
    with tab3:
        st.write("### Delete Patient Record")
        patient_list = st.session_state.patients.get_all_patients()
        if patient_list:
            df_patients = pd.DataFrame(patient_list)
            # Create a dropdown mapping ID - Name for easy deletion
            delete_option = st.selectbox(
                "Select Patient to Delete",
                options=df_patients["ID"].tolist(),
                format_func=lambda x: f"ID {x} - {df_patients[df_patients['ID']==x]['Name'].values[0]}"
            )
            
            if st.button("Delete Patient", type="primary"):
                success, msg = st.session_state.patients.delete_patient(delete_option)
                if success:
                    st.success(msg)
                    # Automatically adjust beds if relevant
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("No records to delete.")


# --- DOCTOR REGISTRY PAGE ---
elif menu_choice == "🩺 Doctor Registry":
    st.subheader("Doctors Directory")
    
    tab1, tab2 = st.tabs(["Active Doctors", "Add Doctor"])
    
    with tab1:
        doctor_list = st.session_state.doctors.get_all_doctors()
        if doctor_list:
            df_doctors = pd.DataFrame(doctor_list)
            st.dataframe(df_doctors, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(df_doctors)} registered doctors.")
        else:
            st.info("No doctors registered in the system.")
            
    with tab2:
        st.write("### Add Doctor Profile")
        with st.form("add_doctor_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                d_id = st.number_input("Doctor ID", min_value=1, step=1, value=1)
                d_name = st.text_input("Doctor Name", placeholder="e.g. Dr. Jane Smith")
            with col2:
                d_spec = st.text_input("Specialization", placeholder="e.g. Neurology, Oncology")
                d_avail = st.selectbox("Availability", ["Yes", "No"])
                
            submitted = st.form_submit_button("Register Doctor")
            if submitted:
                if not d_name or not d_spec:
                    st.error("Doctor Name and Specialization fields cannot be empty!")
                elif st.session_state.doctors.contains_id(d_id):
                    st.error(f"Doctor ID {d_id} already exists. Please choose a unique ID.")
                else:
                    is_avail = (d_avail == "Yes")
                    st.session_state.doctors.add_doctor(d_id, d_name, d_spec, is_avail)
                    st.success(f"Doctor '{d_name}' registered successfully!")
                    st.rerun()


# --- BED MANAGEMENT PAGE ---
elif menu_choice == "🛏️ Bed Management":
    st.subheader("Hospital Bed Status & Allocation")
    
    # Bed metrics
    total = st.session_state.beds.total_beds
    occupied = st.session_state.beds.occupied_beds
    free = total - occupied

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Beds Capacity", total)
    with col2:
        st.metric("Occupied Beds", occupied, delta=f"{(occupied/total)*100:.1f}% Occupancy")
    with col3:
        st.metric("Available Beds", free)

    st.markdown("---")
    st.write("#### Admit Patient to Bed")

    # Fetch patients in the database
    patient_list = st.session_state.patients.get_all_patients()
    # Find names of patients already in a bed
    admitted_names = {bed["patient_name"] for bed in st.session_state.beds.beds if bed["is_occupied"]}
    # Get patients who are not already admitted
    eligible_patients = [p for p in patient_list if p["Name"] not in admitted_names]

    if eligible_patients:
        # Create option format: Name (ID) - Disease
        patient_options = {f"{p['Name']} (ID: {p['ID']}) - {p['Disease']}": p for p in eligible_patients}
        selected_option = st.selectbox(
            "Select Patient to Admit",
            options=list(patient_options.keys())
        )
        
        if st.button("🚪 Admit Selected Patient", type="primary", use_container_width=True):
            patient_data = patient_options[selected_option]
            success, msg = st.session_state.beds.admit_patient(patient_data["Name"], patient_data["Disease"])
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    else:
        if not patient_list:
            st.info("No patient records registered yet. Please add a patient first.")
        else:
            st.info("All registered patients are currently admitted to beds.")

    st.markdown("---")
    st.write("#### Bed Layout View")

    # Display bed layout visually
    cols = st.columns(5)
    for i in range(total):
        bed = st.session_state.beds.beds[i]
        is_occupied = bed["is_occupied"]
        color = "#ef4444" if is_occupied else "#22c55e"
        
        if is_occupied:
            status = f"Occupied by:<br><b>{bed['patient_name']}</b><br><span style='font-size:0.8em;opacity:0.9;'>Disease: {bed['disease']}</span>"
            icon = "🛌"
        else:
            status = "Available"
            icon = "🟢"
        
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style="background-color: {color}; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 5px; font-weight: bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); min-height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center; justify-items: center;">
                    <div style="font-size: 1.1rem;">{icon} Bed {bed['bed_number']}</div>
                    <div style="font-size: 0.75rem; font-weight: normal; margin-top: 5px; line-height: 1.3;">{status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Add a small discharge button underneath occupied beds
            if is_occupied:
                if st.button(f"Discharge Bed {bed['bed_number']}", key=f"disc_{bed['bed_number']}", use_container_width=True):
                    success, msg = st.session_state.beds.discharge_patient(bed['bed_number'])
                    if success:
                        st.success(msg)
                        st.rerun()


st.markdown("""
<div class="footer">
    <p>Hospital Management System</p>
</div>
""", unsafe_allow_html=True)
