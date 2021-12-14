import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
import streamlit as st

teks = pd.read_csv('produksi_minyak_mentah.csv')
teks['produksi'] = pd.to_numeric(teks['produksi'])
json_teks = open("kode_negara_lengkap.json")
data_json = json.loads(json_teks.read())

country_name=[]
for a in range (len(teks.index)):
    d=0
    indx = 0
    for k in data_json:
        if teks['kode_negara'][a] == data_json[d]['alpha-3'] :
            country_name.append(data_json[d]['name'])
            indx +=1
        d+=1
    if indx == 0:
        country_name.append(0)

teks['country_name']=country_name
teks = teks[teks.country_name != 0]


#*************** title ***************#
st.set_page_config(layout="wide")  
st.title("Statistic Production Data of Crude Oil")
#*************** title ***************#

############### sidebar ###############
#gambar = image.open('oil.jpg')
#st.sidebar.image(gambar)

st.sidebar.title("Menu Setting")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Menu Pilihan")
ngr=list(dict.fromkeys(country_name))
ngr.remove(0)
negara = st.sidebar.selectbox("Negara", ngr)
jml_ngr = st.sidebar.number_input("Banyak Negara", min_value=1, max_value=None, value=1)
thn_uniq = list(teks['tahun'].unique())
tahun = st.sidebar.selectbox ("Tahun", thn_uniq)

############### lower left column ###############
left_col.subheader("Data Produksi Minyak Mentah Per Negara")

jml_prod=[]
for x in teks[teks['country_name']==negara]['produksi'] :
    jml_prod.append(x)

fig, ax = plt.subplots()
cmap_nama = 'Set3'
cmap = cm.get_cmap(cmap_nama)
wrn = cmap.colors[:len(ngr)]
ax.bar(thn_uniq, jml_prod, color=wrn)

left_col.pyplot(fig)
############### lower left column ###############

############### lower middle column ###############
mid_col.subheader("Produksi Terbesar")

file_2=teks.sort_values(by=['produksi'], ascending=False)
file_2 = file_2.loc[file_2['tahun']==tahun]
jml_production = []
dftr_ngr=[]
d=0
for x in file_2['produksi']:
    if d < jml_ngr:
        jml_production.append(x)
        d+=1
d=0
for x in file_2['country_name']:
    if d < jml_ngr:
        dftr_ngr.append(x)
        d+=1

fig, ax = plt.subplots()
ax.bar(dftr_ngr, jml_production, color=wrn)

plt.tight_layout()

mid_col.pyplot(fig)

############### lower middle column ###############

############### lower right column ###############
right_col.subheader("Produksi Terbesar Secara Kumulatif dari Keseluruhan Tahun")

file_3 = pd.DataFrame(teks, columns= ['country_name','produksi'])
file_3['total_prod'] = file_3.groupby(['country_name'])['produksi'].transform('sum')
file_3 = file_3.drop_duplicates(subset=['country_name'])
file_3=file_3.sort_values(by=['total_prod'], ascending=False)
dftr_ngr2=[]
total_prod=[]
y=0
for x in file_3['total_prod']:
    if y < jml_ngr:
        total_prod.append(x)
        y+=1
y=0
for x in file_3['country_name']:
    if y < jml_ngr:
        dftr_ngr2.append(x)
        y+=1

fig, ax = plt.subplots()
ax.bar(dftr_ngr2, total_prod, color=wrn)

plt.tight_layout()

right_col.pyplot(fig)
############### lower right column ###############
