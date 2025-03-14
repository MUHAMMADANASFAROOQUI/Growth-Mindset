import os
import streamlit as st
import pandas as pd
from io import BytesIO


st.set_page_config(page_title="Data Sweeper" , layout="wide")

# #custom CSS
# st.markdown(
#     """
#     <style>
#     .stApp{
#     background-color : black;
#     color: white
#     }
#     """,
#     unsafe_allow_html=True
# )

# Title and Description
st.title("📀 DataSweeper")
st.write("Upload CSV or Excel,clean or visualize data and convert formats!")


# File Uploader
uploaded_Files = st.file_uploader("Upload your file(CSV or Excel):", type=["csv","xlsx"], accept_multiple_files= True)

if uploaded_Files:
    for file in uploaded_Files:
        file_text = os.path.splitext(file.name)[-1].lower() 
        
        if file_text == ".csv":  
            data = pd.read_csv(file)
        elif file_text == ".xlsx":  
            data = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_text}")
            continue

        # File Details
        st.write("🔍 Preview the head of Dataframe")
        st.dataframe(data.head())


        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Removing duplicates from the file: {file.name}"):
                    data.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_col = data.select_dtypes(include=["number"]).columns
                    data[numeric_col] = data[numeric_col].fillna(data[numeric_col].mean())
                    st.write("✅ Missing values have been filled!")


            st.subheader("🎯 Columns to keep")
            columns : list[str] = st.multiselect(f"Choose columns for {file.name}", data.columns, default=data.columns)
            data1 = data[columns]


            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Showing Visualization for {file.name}"):
                 numeric_data = data1.select_dtypes(include='number')
                 if numeric_data.shape[1] >= 2:
                     st.line_chart(numeric_data.iloc[:, :5])
                 else:
                     st.warning("Not enough numeric columns to display the bar chart.")


            # Conversion Options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert{file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    data.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_text, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    data.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_text, ".xlsx")
                    mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                st.download_button(
                    label = f"Download{file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                    )
                    
                st.success("🎉 All files proceed succesfully!!")










    



