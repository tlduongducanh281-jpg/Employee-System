import streamlit as st
import pandas as pd
from app.db.connection import get_db_connection
import services.queries as qsvc
import matplotlib.pyplot as plt

# ============================================================
# APP CONFIG
# ============================================================
st.set_page_config(page_title="EMPLOYEE INFORMATION MANAGEMENT", layout="wide")
custom_css = """
<style>

    /* ---------------------------------------------------
       GLOBAL FONT + DEFAULT TEXT COLOR
    --------------------------------------------------- * 
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif !important;
        color: white !important;
    }

    /* ---------------------------------------------------
       1. TITLES — CENTER + BLUE
    --------------------------------------------------- */
    h1 {
        text-align: center !important;
        color: #1f4bb8 !important;
        font-weight: 800 !important;
        margin-bottom: 25px !important;
    }

    h2, h3, h4, h5 {
        color: #1f4bb8 !important;
        font-weight: 700 !important;
    }

    /* ---------------------------------------------------
       2. SIDEBAR
       - Nền tối
       - Label xanh
       - Radio tùy chỉnh
    --------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #11121a !important;
    }

    section[data-testid="stSidebar"] label {
        color: #1f4bb8 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* Radio items */
    .stRadio [role="radio"] {
        padding: 6px 0 !important;
    }

    /* Vòng tròn radio custom */
    .stRadio [role="radio"]::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        border-radius: 50%;
        background-color: #000 !important;
        border: 2px solid #1f4bb8 !important;
    }

    /* Khi được chọn */
    .stRadio [aria-checked="true"]::before {
        background-color: #1f4bb8 !important;
    }

    /* ---------------------------------------------------
       3. INPUT FIELDS — DARK MODE
       (text_input, number_input, date_input, textarea…)
    --------------------------------------------------- */
    input, textarea, select {
        background-color: #1f1f2b !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #3b3b4d !important;
    }

    ::placeholder {
        color: #bbbbbb !important;
    }

    /* BaseWeb Input wrapper */
    div[data-baseweb="input"] {
        background-color: #1f1f2b !important;
        border-radius: 8px !important;
    }

    /* Text inside input */
    div[data-baseweb="input"] input {
        color: white !important;
    }

    /* ---------------------------------------------------
       4. SELECTBOX / MULTISELECT — DARK MODE
    --------------------------------------------------- */
    div[data-baseweb="select"] {
        background-color: #1f1f2b !important;
        color: white !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: white !important;
    }

    /* Option dropdown */
    ul[role="listbox"] li {
        background-color: #1f1f2b !important;
        color: white !important;
    }

    /* Hover option */
    ul[role="listbox"] li:hover {
        background-color: #2b2b3d !important;
    }

    /* ---------------------------------------------------
       5. TABLE / DATAFRAME — WHITE TEXT
    --------------------------------------------------- */
    .stDataFrame table td, 
    .stDataFrame table th {
        color: white !important;
        font-size: 15px !important;
    }

    /* ---------------------------------------------------
       6. METRICS — BLUE HIGHLIGHT
    --------------------------------------------------- */
    .stMetricValue, .stMetricLabel {
        color: #1f4bb8 !important;
        font-weight: 800 !important;
    }

    /* ---------------------------------------------------
       7. BUTTONS — MODERN BLUE BUTTON
    --------------------------------------------------- */
    button[kind="secondary"], .stButton button {
        background-color: #1f4bb8 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 20px !important;
        font-size: 17px !important;
        font-weight: 600 !important;
    }

    .stButton button:hover {
        background-color: #173a8c !important;
        scale: 1.02;
    }

    /* ---------------------------------------------------
       8. EXPANDER — DARK + BLUE LABEL
    --------------------------------------------------- */
    details {
        background-color: #14141d !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    summary {
        color: #1f4bb8 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.title("Employee Information Manager")

pages = ["Employees", "Departments", "Projects", "Assignments", "Queries", "Dashboard", "Settings"]
page = st.sidebar.radio("Go to", pages)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_id_col(df):
    for col in df.columns:
        if "id" in col.lower():
            return col
    return df.columns[0]


def export_df_csv(df, filename="export.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Export CSV", data=csv, file_name=filename, mime='text/csv')


def db_execute(sql, params=None):
    """Execute SQL safely using MySQL."""
    conn = get_db_connection()
    if not conn:
        return False, "Cannot connect to MySQL"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def get_fk_map(df, label_col, key_col):
    if df.empty:
        return {}
    return {row[label_col]: row[key_col] for _, row in df.iterrows()}


# ============================================================
# PAGE: EMPLOYEES
# ============================================================
if page == "Employees":
    st.header("Employees")

    # ---------------------- CREATE ----------------------
    with st.form("create_employee"):
        st.subheader("Create new employee")
        eid = st.number_input("EmployeeID", min_value=1, step=1)
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")

        deps = qsvc.get_departments()
        dep_idcol = safe_id_col(deps) if not deps.empty else "DepartmentID"
        dep_map = get_fk_map(deps, "DepartmentName", dep_idcol)
        dep_choice = st.selectbox("Department", [""] + list(dep_map.keys()))

        if st.form_submit_button("Create"):
            if not name:
                st.error("Name required")
            else:
                dep_id = dep_map.get(dep_choice)
                sql = "INSERT INTO Employees (EmployeeID, Name, DateOfBirth, DepartmentID) VALUES (%s, %s, %s, %s)"
                ok, err = db_execute(sql, (eid, name, dob.isoformat(), dep_id))
                st.success("Employee created") if ok else st.error(err)

    # ---------------------- VIEW ----------------------
    st.subheader("All Employees")
    df = qsvc.get_employees()
    st.dataframe(df)
    export_df_csv(df, "employees.csv")

    # ---------------------- EDIT + DELETE ----------------------
    if not df.empty:
        idcol = safe_id_col(df)
        sel = st.selectbox("Select employee to Edit/Delete", df[idcol].tolist())
        row = df[df[idcol] == sel].iloc[0]

        with st.form("edit_employee"):
            new_name = st.text_input("Name", value=row["Name"])
            new_dob = st.date_input("DateOfBirth", value=pd.to_datetime(row["DateOfBirth"]).date())

            dep_df = qsvc.get_departments()
            dep_idcol = safe_id_col(dep_df)
            dep_map = get_fk_map(dep_df, "DepartmentName", dep_idcol)

            current_dep_name = ""
            if "DepartmentID" in row:
                match = dep_df[dep_df[dep_idcol] == row["DepartmentID"]]
                if not match.empty:
                    current_dep_name = match.iloc[0]["DepartmentName"]

            new_dep = st.selectbox(
                "Department",
                [""] + list(dep_map.keys()),
                index=(list(dep_map.keys()).index(current_dep_name) if current_dep_name in dep_map else 0)
            )

            if st.form_submit_button("Save"):
                depid = dep_map.get(new_dep)
                sql = "UPDATE Employees SET Name=%s, DateOfBirth=%s, DepartmentID=%s WHERE EmployeeID=%s"
                ok, err = db_execute(sql, (new_name, new_dob.isoformat(), depid, sel))
                st.success("Updated") if ok else st.error(err)

        if st.button("Delete selected employee"):
            sql = "DELETE FROM Employees WHERE EmployeeID=%s"
            ok, err = db_execute(sql, (sel,))
            st.success("Deleted") if ok else st.error(err)


# ============================================================
# PAGE: DEPARTMENTS
# ============================================================
elif page == "Departments":
    st.header("Departments")

    with st.form("create_dept"):
        name = st.text_input("Department Name")
        if st.form_submit_button("Create Department"):
            if not name:
                st.error("Name required")
            else:
                sql = "INSERT INTO Departments (DepartmentName) VALUES (%s)"
                ok, err = db_execute(sql, (name,))
                st.success("Created") if ok else st.error(err)

    df = qsvc.get_departments()
    st.dataframe(df)
    export_df_csv(df, "departments.csv")

    if not df.empty:
        idcol = safe_id_col(df)
        sel = st.selectbox("Select DepartmentID to Edit/Delete", df[idcol].tolist())
        row = df[df[idcol] == sel].iloc[0]

        with st.form("edit_dep"):
            new_name = st.text_input("Name", value=row["DepartmentName"])
            if st.form_submit_button("Save"):
                sql = "UPDATE Departments SET DepartmentName=%s WHERE DepartmentID=%s"
                ok, err = db_execute(sql, (new_name, sel))
                st.success("Saved") if ok else st.error(err)

        if st.button("Delete department"):
            sql = "DELETE FROM Departments WHERE DepartmentID=%s"
            ok, err = db_execute(sql, (sel,))
            st.success("Deleted") if ok else st.error(err)

# ============================================================
# PAGE: PROJECTS
# ============================================================
elif page == "Projects":
    st.header("Projects")

    employees = qsvc.get_employees()
    emp_idcol = safe_id_col(employees) if not employees.empty else "EmployeeID"
    emp_map = get_fk_map(employees, "Name", emp_idcol)

    # ----------------------- CREATE PROJECT -----------------------
    with st.form("create_project"):
        pname = st.text_input("Project Name")
        manager = st.selectbox("Manager", [""] + list(emp_map.keys()))

        if st.form_submit_button("Create Project"):
            if not pname:
                st.error("Project name required")
            else:
                mid = emp_map.get(manager)

                conn = get_db_connection()
                try:
                    cursor = conn.cursor()
                    sql = """
                        INSERT INTO Projects (ProjectName, ManagerEmployeeID)
                        VALUES (%s, %s)
                    """
                    cursor.execute(sql, (pname, mid))
                    conn.commit()
                    st.success("Created")

                except Exception as e:
                    st.error(f"❌ {e}")

                finally:
                    cursor.close()
                    conn.close()

    # ----------------------- VIEW PROJECTS -----------------------
    df = qsvc.get_projects()
    st.dataframe(df)
    export_df_csv(df, "projects.csv")

    # ----------------------- EDIT + DELETE -----------------------
    if not df.empty:
        idcol = safe_id_col(df)
        sel = st.selectbox("Select ProjectID to Edit/Delete", df[idcol].tolist())
        row = df[df[idcol] == sel].iloc[0]

        # Current manager name
        current_mgr_id = row.get("ManagerEmployeeID")
        current_mgr_name = ""
        if current_mgr_id in employees[emp_idcol].values:
            current_mgr_name = employees[employees[emp_idcol] == current_mgr_id].iloc[0]["Name"]

        # --------- EDIT FORM ---------
        with st.form("edit_proj"):
            new_name = st.text_input("Name", value=row["ProjectName"])
            new_mgr = st.selectbox(
                "Manager",
                [""] + list(emp_map.keys()),
                index=(list(emp_map.keys()).index(current_mgr_name) if current_mgr_name in emp_map else 0)
            )

            if st.form_submit_button("Save"):
                mid = emp_map.get(new_mgr)

                conn = get_db_connection()
                try:
                    cursor = conn.cursor()
                    sql = """
                        UPDATE Projects
                        SET ProjectName=%s, ManagerEmployeeID=%s
                        WHERE ProjectID=%s
                    """
                    cursor.execute(sql, (new_name, mid, sel))
                    conn.commit()
                    st.success("Saved")

                except Exception as e:
                    st.error(f"❌ {e}")

                finally:
                    cursor.close()
                    conn.close()

        # --------- DELETE PROJECT ---------
        if st.button("Delete project"):
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                sql = "DELETE FROM Projects WHERE ProjectID=%s"
                cursor.execute(sql, (sel,))
                conn.commit()
                st.success("Deleted")

            except Exception as e:
                st.error(f"❌ {e}")

            finally:
                cursor.close()
                conn.close()

# ============================================================
# PAGE: ASSIGNMENTS
# ============================================================
elif page == "Assignments":
    st.header("Assignments")

    # Load data safely
    employees = qsvc.get_employees()
    projects = qsvc.get_projects()

    if employees.empty or projects.empty:
        st.warning("Employees or Projects table is empty. Please add data first.")
        st.stop()

    emp_idcol = safe_id_col(employees)
    proj_idcol = safe_id_col(projects)

    emp_map = get_fk_map(employees, "Name", emp_idcol)
    proj_map = get_fk_map(projects, "ProjectName", proj_idcol)

    # ----------------------- CREATE ASSIGNMENT -----------------------
    with st.form("create_assign"):
        st.subheader("Create assignment")

        emp_choice = st.selectbox("Employee", [""] + list(emp_map.keys()))
        proj_choice = st.selectbox("Project", [""] + list(proj_map.keys()))
        role = st.text_input("Role")
        salary = st.number_input("Salary", min_value=0.0)

        submit_create = st.form_submit_button("Create Assignment")

        if submit_create:
            if not emp_choice or not proj_choice or not role:
                st.error("Employee, Project and Role are required")
            else:
                empid = emp_map[emp_choice]
                projid = proj_map[proj_choice]

                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    sql = """
                        INSERT INTO employee_manager_db.Assignments 
                        (EmployeeID, ProjectID, Role, Salary)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            Role = VALUES(Role),
                            Salary = VALUES(Salary);
                    """
                    cursor.execute(sql, (empid, projid, role, float(salary)))
                    conn.commit()

                    st.success("Assignment created or updated successfully!")

                except Exception as e:
                    st.error(f"❌ {e}")

                finally:
                    cursor.close()
                    conn.close()

    # ----------------------- VIEW ASSIGNMENTS -----------------------
    df = qsvc.get_assignments()
    st.dataframe(df)
    export_df_csv(df, "assignments.csv")

    st.subheader("Edit or Delete Assignment")

    # ----------------------- ALWAYS SHOW UI EVEN IF EMPTY -----------------------
    if df.empty:
        st.info("No assignments found.")
        st.selectbox("Select Assignment", ["(empty)"], disabled=True)
        st.text_input("Role", value="", disabled=True)
        st.number_input("Salary", value=0.0, disabled=True)
        st.button("Save", disabled=True)
        st.button("Delete Assignment", disabled=True)
        st.stop()

    # ----------------------- EDIT + DELETE UI -----------------------
    df["pair"] = df.apply(
        lambda r: f"{r['EmployeeID']} — {r['EmployeeName']} — Project {r['ProjectID']} — {r['ProjectName']}",
        axis=1
    )

    sel = st.selectbox("Select Assignment", df["pair"].tolist())

    row = df[df["pair"] == sel].iloc[0]
    empid = int(row["EmployeeID"])
    projid = int(row["ProjectID"])

    # --------- EDIT ---------
    with st.form("edit_assign"):
        new_role = st.text_input("Role", value=row["Role"])
        new_salary = st.number_input("Salary", min_value=0.0, value=float(row["Salary"]))

        submit_edit = st.form_submit_button("Save")

        if submit_edit:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                sql = """
                    UPDATE employee_manager_db.Assignments
                    SET Role=%s, Salary=%s
                    WHERE EmployeeID=%s AND ProjectID=%s
                """
                cursor.execute(sql, (new_role, new_salary, empid, projid))
                conn.commit()

                st.success("Assignment updated successfully!")

            except Exception as e:
                st.error(f"❌ {e}")

            finally:
                cursor.close()
                conn.close()

    # --------- DELETE ---------
    if st.button("Delete Assignment"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """
                DELETE FROM employee_manager_db.Assignments
                WHERE EmployeeID=%s AND ProjectID=%s
            """
            cursor.execute(sql, (empid, projid))
            conn.commit()

            st.success("Assignment deleted!")

        except Exception as e:
            st.error(f"❌ {e}")

        finally:
            cursor.close()
            conn.close()


# ============================================================
# PAGE: QUERIES
# ============================================================
elif page == "Queries":
    st.header("Queries / Analysis")

    qtab = st.selectbox("Choose query",
                        ["INNER JOIN (employee per project)",
                         "LEFT JOIN (all employees)",
                         "Multi-table JOIN (with manager)",
                         "Above global average"])

    if qtab == "INNER JOIN (employee per project)":
        df = qsvc.inner_join_per_project()
        st.dataframe(df)
        export_df_csv(df, "inner_join.csv")

    elif qtab == "LEFT JOIN (all employees)":
        df = qsvc.left_join_all_employees()
        st.dataframe(df)
        export_df_csv(df, "left_join.csv")

    elif qtab == "Multi-table JOIN (with manager)":
        df = qsvc.multi_table_join_with_manager()
        st.dataframe(df)
        export_df_csv(df, "multi_join.csv")

    elif qtab == "Above global average":
        df = qsvc.above_global_average()
        st.dataframe(df)
        export_df_csv(df, "above_avg.csv")


# ============================================================
# PAGE: DASHBOARD
# ============================================================
elif page == "Dashboard":
    st.header("Dashboard")

    emp_df = qsvc.get_employees()
    dept_df = qsvc.get_departments()
    proj_df = qsvc.get_projects()
    assign_df = qsvc.get_assignments()

    cols = st.columns(4)
    cols[0].metric("Total Employees", len(emp_df))
    cols[1].metric("Departments", len(dept_df))
    cols[2].metric("Projects", len(proj_df))
    cols[3].metric("Assignments", len(assign_df))

    if not assign_df.empty and "Salary" in assign_df:
        st.write(f"Average salary: {assign_df['Salary'].mean():.2f}")

    # Histogram
    if not assign_df.empty and "Salary" in assign_df:
        fig, ax = plt.subplots()
        ax.hist(assign_df["Salary"], bins=10)
        st.pyplot(fig)

    # Top employees by salary
    st.subheader("Top employees by average assignment salary")
    if not assign_df.empty:
        group_cols = [col for col in ["EmployeeID", "EmployeeName"] if col in assign_df]
        if group_cols:
            avg_by_emp = assign_df.groupby(group_cols)["Salary"].mean().reset_index().sort_values("Salary", ascending=False)
            st.dataframe(avg_by_emp)
            export_df_csv(avg_by_emp, "top_employees_avg_salary.csv")
        else:
            st.warning("No employee identifiers found in assignment data")

# ============================================================
# PAGE: SETTINGS
# ============================================================
elif page == "Settings":
    st.header("Settings / DB info")

    st.subheader("Database Information")
    st.write("Database Type: MySQL")

    # Thử kết nối để hiển thị info
    conn = get_db_connection()
    if conn:
        st.write("Status: Connected ✔")
        try:
            st.write("Server Host:", conn.server_host)
            st.write("Server Version:", conn.get_server_info())
        except:
            pass
        conn.close()
    else:
        st.error("Status: Cannot connect ❌")

    st.info("Using MySQL connection settings from connection.py")
