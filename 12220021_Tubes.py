import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
import streamlit as st
from PIL import Image

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

#************* sidebar *************#
image = Image.open('oil.png')
st.sidebar.image(image)

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
#************* sidebar *************#

############### Bagian A ###############
left_col.subheader("Data Produksi Minyak Mentah dari Negara Pilihan")

jml_prod=[]
for x in teks[teks['country_name']==negara]['produksi'] :
    jml_prod.append(x)

fig, ax = plt.subplots()
cmap_nama = 'Set3'
cmap = cm.get_cmap(cmap_nama)
wrn = cmap.colors[:len(ngr)]
ax.bar(thn_uniq, jml_prod, color=wrn)

left_col.pyplot(fig)
#*********************************************#
mid_col.subheader("Tabel Data Produksi Minyak Suatu Negara yang telah dipilih")
tabel_1 = pd.DataFrame({
    'Tahun Unik':thn_uniq,
    'Produksi minyak mentah':jml_prod
})
mid_col.dataframe(tabel_1)
#*********************************************#

############### Bagian B ###############
left_col.subheader("Produksi Terbesar dari Sejumlah Negara Pilihan")
file_2 = teks.sort_values(by=['produksi'], ascending=False)
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
left_col.pyplot(fig)
#*********************************************#
mid_col.subheader("Tabel Data Produksi Terbesar dari Sejumlah Negara Pilihan")
tabel_2 = pd.DataFrame({
    'Daftar Negara':dftr_ngr,
    'Jumlah Produksi':jml_production
})
mid_col.dataframe(tabel_2)
#*********************************************#

############### Bagian C ###############
left_col.subheader("Produksi Terbesar Secara Kumulatif dari Keseluruhan Tahun")

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

left_col.pyplot(fig)
#*********************************************#
mid_col.subheader("Tabel Data Produksi Terbesar Secara Kumulatif dari Keseluruhan tahun")
tabel_3 = pd.DataFrame({
    'Daftar Negara':dftr_ngr2,
    'Total Produksi':total_prod
})
mid_col.dataframe(tabel_3)
#*********************************************#

############### Bagian D ###############
left_col.subheader("Summary")
st.write()  
 
T_= tahun
 
tahun = list(dict.fromkeys(teks['tahun'].tolist())) 
 
maks_d = {'negara':[],             
            'kode_negara':[], 
            'region':[], 
            'sub_region':[], 
            'produksi':[jml_prod],             
            'tahun':[tahun]} 
min_d  = {'negara':[],             
            'kode_negara':[], 
            'region':[], 
            'sub_region':[], 
            'produksi':[jml_prod],             
            'tahun':[tahun]}  
zero_d = {'negara':[],             
            'kode_negara':[], 
            'region':[], 
            'sub_region':[], 
            'produksi':[jml_prod],             
            'tahun':[tahun]} 
for l in tahun: 
    df_per_tahun = teks[teks['tahun']==T_] 
    production = np.array(df_per_tahun['produksi'].tolist()) 
    maks_prod = max(production) 
    min_prod = min([p for p in production if p != 0])     
    zero_prod = min([p for p in production if p == 0]) 
    # maksimum 
    kode_negara = df_per_tahun[df_per_tahun['produksi']==maks_prod]['kode_negara'].tolist()[0]     
if kode_negara == 'WLD':         
    kode_negara = 'WLF' 
    maks_d['negara'].append(data_json[data_json['alpha-3']==kode_negara]['name'].tolist()[0]) 
    maks_d['kode_negara'].append(kode_negara) 
    maks_d['region'].append(data_json[data_json['alpha-3']==kode_negara]['region'].tolist()[0])     
    maks_d['sub_region'].append(data_json[data_json['alpha-3']==kode_negara]['sub-region'].tolist()[0]) 
    maks_d['produksi'].append(maks_prod) 
    # minimum != 0 
    kode_negara = df_per_tahun[df_per_tahun['produksi']==min_prod] ['kode_negara'].tolist()[0] 
if kode_negara == 'WLD':         
    kode_negara = 'WLF' 
    min_d['negara'].append(data_json[data_json['alpha-3']==kode_negara]['name'].tolist()[0])     
    min_d['kode_negara'].append(kode_negara) 
    min_d['region'].append(data_json[data_json['alpha-3']==kode_negara]['region'].tolist()[0])     
    min_d['sub_region'].append(data_json[data_json['alpha-3']==kode_negara]['sub-region'].tolist()[0]) 
    min_d['produksi'].append(min_prod) 
    # zero == 0 
    kode_negara = df_per_tahun[df_per_tahun['produksi']==zero_prod]['kode_negara'].tolist()[0]     
if kode_negara == 'WLD':         
    kode_negara = 'WLF' 
    zero_d['negara'].append(data_json[data_json['alpha-3']==kode_negara]['name'].tolist()[0]) 
    zero_d['kode_negara'].append(kode_negara) 
    zero_d['region'].append(data_json[data_json['alpha-3']==kode_negara]['region'].tolist()[0])     
    zero_d['sub_region'].append(data_json[data_json['alpha-3']==kode_negara]['sub-region'].tolist()[0]) 
    zero_d['produksi'].append(zero_prod) 

#**************maksimum*********************#
maksimal = pd.DataFrame({
    'Maksimum': maks_d
})
st.write('Info Produksi Maksimum Tahun ke-{}'.format(T_)) 
st.write(maksimal) 
 
st.write('Tabel Maks per Tahun') 
st.write(maksimal) 

#*************minimum tapi bukan 0**********************#
minimal = pd.DataFrame({
    'Minimum': min_d
})
st.write('Info Produksi Minimum (Not Zero) Tahun ke-{}'.format(T_)) 
st.write(minimal) 
 
st.write('Tabel Min (Not Zero) per Tahun') 
st.write(minimal)

#************sama dengan 0*******************#
nol = pd.DataFrame({
    'Zero': zero_d
})
st.write('Info Produksi Zero Tahun ke-{}'.format(T_)) 
st.write(nol) 
 
st.write('Tabel Zero per Tahun') 
st.write(nol)
#*********************************************#
 