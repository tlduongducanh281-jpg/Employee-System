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