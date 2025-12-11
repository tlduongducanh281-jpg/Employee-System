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
