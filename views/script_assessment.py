import streamlit as st
import pandas as pd
from common import common_patterns
from common.app_utils import AppUtils

# Setting the Page Title

st.set_page_config(page_title="Qlik Script Assessment Tool", layout="wide")

utils = AppUtils()

# ================ SCRIPT ANALYSIS LOGIC =================

# Define common patterns

default_patterns = common_patterns.data

# ================ STREAMLIT UI =================
st.title("📊 Qlik Script Assessment Tool")

st.markdown("Upload Qlik `.qvs` or `.txt` or `.log`  files for analysis.")

uploaded_files = st.file_uploader("Upload one or more Qlik scripts", accept_multiple_files=True, type=['qvs', 'txt', 'log'])

if uploaded_files:
    results, dataConnectResults, join_append_sections = [], [], []

    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode('utf-8')
        issues, pq_scores, ps_scores, pattern_match_counts, regex_patterns, weightages = utils.analyze_script(content,default_patterns)

        # Extract Data Connection Used (Work In Progress)

        dataConnectResp = utils.extract_data_connections(content)
        for issue, pq, ps, pmc, rp, ws in zip(issues, pq_scores, ps_scores, pattern_match_counts, regex_patterns,
                                              weightages):
            results.append({
                "File": uploaded_file.name,
                "Function": issue,
                # "Regex Pattern": 'r"'+rp+'"',
                "Total Occurrence": pmc,
                "Scores": pmc * ws,
                "Power Query": pq,
                "PySpark": ps
            })

        for dc in dataConnectResp:
            dataConnectResults.append({
                "File": uploaded_file.name,
                "Type": dc[0],
                "Data Connection": dc[1]
            })

        # Check For Join & Append Function & extract the details
        join_details, resident_details = utils.extract_join_append(content)

        if resident_details:
            total_residents, total_joins = utils.calculate_total_resident_and_joins(resident_details, join_details)

            if total_residents > 0 and total_joins > 0:
                join_append_sections.append({
                    "file_name": uploaded_file.name,
                    "join_details": join_details,
                    "resident_details": resident_details,
                    "total_residents": total_residents,  # sum(resident_details.values()),
                    "total_joins": total_joins,
                })

    if results:
        st.subheader("🧾 Analysis Results")
        df = pd.DataFrame(results)
        df['Total Occurrence'] = df['Total Occurrence'].astype(str)
        if join_append_sections:
            join_append_df = pd.DataFrame(join_append_sections)
            join_append_df['Function'] = "Joins & Append (Multiple Concat)"
            join_append_df['Power Query'] = 0
            join_append_df['PySpark'] = 1
            # join_append_df['Total Occurrence'] = join_append_df['total_residents']
            join_append_df['Total Occurrence'] = join_append_df['total_residents'].astype(str) + " (Concat), " + \
                                                 join_append_df['total_joins'].astype(str) + " (Joins)"

            join_append_df['Scores'] = 0
            join_append_df = join_append_df.rename(columns={'file_name': 'File'})

            join_append_df = join_append_df.drop(['join_details', 'resident_details', 'total_residents', 'total_joins'],
                                                 axis=1)

            df = pd.concat([df, join_append_df], ignore_index=True)
            df = df.sort_values(by='File')

        # Calculate the total for Score columns i.e Power Query & PySpark
        total_row = df[['Power Query', 'PySpark', 'Total Occurrence']].sum()

        total_row['File'] = 'Total'
        total_row['Function'] = ''

        with st.container():
            col1, col2, col3 = st.columns([2, 3, 2])

            # Centre column: Filter
            with col2:
                # Text input for filtering by function name
                func_filter = st.text_input(label="Search by Function", label_visibility="collapsed",
                                            placeholder="Search by Function...")

                # Apply filter (case-insensitive)
                if func_filter:
                    df = df[df['Function'].str.contains(func_filter, case=False, na=False)]

                    # Calculate the total for Score columns i.e Power Query & PySpark
                    total_row = df[['Power Query', 'PySpark']].sum()

            # Left column: Text
            with col1:
                st.markdown(f"**Total Power Query Score** : `{total_row['Power Query']}`<br>"
                            f"**Total PySpark Score** : `{total_row['PySpark']}`"
                            , unsafe_allow_html=True)

            # Assign Row Values 1 to Yes & 0 to No
            df['Power Query'] = df['Power Query'].map({1: 'Yes', 0: 'No'})
            df['PySpark'] = df['PySpark'].map({1: 'Yes', 0: 'No'})

            # Rename the Column
            df = df.rename(columns={"Power Query": "Can Be Done in Power Query",
                                    "PySpark": "Can Be Done in PySpark"})

            # Right column:  Button
            with col3:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results as CSV", data=csv, file_name="qlik_script_analysis_result.csv",
                                   mime="text/csv")

            # Apply the style to the 'Power Query' and 'PySpark'  column
            df = df.style.map(utils.color_yes_no, subset=['Can Be Done in Power Query', 'Can Be Done in PySpark'])

        # Display the dataframe results
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Display the list of Data Connection Used
        if dataConnectResults:
            df1 = pd.DataFrame(dataConnectResults)

            st.write("List of Data Connections")
            st.dataframe(df1, use_container_width=True, hide_index=True)

        # else:

        #     st.error(" No Data Connection found in uploaded files.")

        # Join & Append Function Details

        for section in join_append_sections:
            with st.expander(f"📌 Detected Join & Append (Multiple Concatenations) in the file  {section['file_name']}"):
                join_details = section["join_details"]
                resident_details = section["resident_details"]

                # Print the summary
                if resident_details:
                    for table, count in resident_details.items():
                        if table in join_details:
                            for join_type, join_count in join_details[table].items():
                                st.write(
                                    f" ◾ {table} is involved in  {join_count} {join_type} and appears in {count} resident loads with concatenation.")
                        # else:
                        #     st.write(
                        #         f" ◾ {table} has no JOIN operations and appears in {count} resident loads with concatenation.")
    else:
        st.success("✅ No issues found in uploaded files.")