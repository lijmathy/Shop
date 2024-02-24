from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Shop Distribution", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Shop Distribution EDA")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\Dese\Desktop\van")
    df = pd.read_csv("New_final2.csv", encoding = "ISO-8859-1")


st.sidebar.header("Choose your filter: ")
# Create for City/Town
region = st.sidebar.multiselect("Pick your City/Town", df["City/Town"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["City/Town"].isin(region)]

# Create for Sub City
state = st.sidebar.multiselect("Pick the Sub city", df2["Subcity/Kebele"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["Subcity/Kebele"].isin(state)]

col1, col2 = st.columns((2))
# Create for Locality
city = st.sidebar.multiselect("Pick the Locality",df3["Locality"].unique())

# Filter the data based on City/Town, Sub_City and Locality
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["City/Town"].isin(region)]
elif not region and not city:
    filtered_df = df[df["Subcity/Kebele"].isin(state)]
elif state and city:
    filtered_df = df3[df["Subcity/Kebele"].isin(state) & df3["Locality"].isin(city)]
elif region and city:
    filtered_df = df3[df["City/Town"].isin(region) & df3["Locality"].isin(city)]
elif region and state:
    filtered_df = df3[df["City/Town"].isin(region) & df3["Subcity/Kebele"].isin(state)]
elif city:
    filtered_df = df3[df3["Locality"].isin(city)]
else:
    filtered_df = df3[df3["City/Town"].isin(region) & df3["Subcity/Kebele"].isin(state) & df3["Locality"].isin(city)]

category_df = filtered_df.groupby(by = ["Channel Type "], as_index = False)['Num'].sum()
with col1:
    st.subheader("Shops with Subcities")
    #fig = px.bar(category_df, x = "Channel Types", y = "Num ", text=['{:d}'.format(x) for x in category_df["Num"]], template = "seaborn")
    #st.plotly_chart(fig,use_container_width=True, height = 200)
    subcities = df['Subcity/Kebele'].unique()
    plt.figure()
    subcity_counts = df['Subcity/Kebele'].value_counts()
    subcity_counts.plot(kind='bar')
    plt.xlabel('Subcity')
    plt.ylabel('Count')
    plt.title('Subcity Distribution')
    st.pyplot(plt)
     # Display count values on the bars
    for i, count in enumerate(subcity_counts):
        plt.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')
    # Display the list of subcities
#st.write('List of Subcities:', subcities)

with col2:
    st.subheader("Number of Shops with SubCity")
    fig = px.pie(filtered_df, values = "Num", names = "Subcity/Kebele", hole = 0.5)
    fig.update_traces(text = filtered_df["Subcity/Kebele"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Channel Type Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
        
with cl2:
    with st.expander("Subcity/Kebele_ViewData"):
        region = filtered_df.groupby(by = "Subcity/Kebele", as_index = False)["Num"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


