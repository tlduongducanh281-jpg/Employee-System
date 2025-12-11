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
