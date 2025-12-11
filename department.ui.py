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