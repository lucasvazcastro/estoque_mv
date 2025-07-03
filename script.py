import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

df_total = pd.DataFrame({'ID': [
    "344", "95", "166", "2444", "169", "174", "77", "2653", "81", "2974",
    "75", "206", "217", "80", "220", "225", "224", "232", "86", "23",
    "2445", "919", "27", "2798", "3", "41", "2465", "216", "173", "2470",
    "1946", "2162", "144", "1777", "2981", "119", "120", "193", "22",
    "2476", "147", "145", "184", "5", "116", "2454", "2455", "46", "710",
    "164", "196", "149", "2466", "14", "213", "913", "30", "218", "72",
    "199", "53", "106", "107", "163", "4", "16", "2450", "141", "228",
    "63", "2920", "245", "247", "700", "699", "2447", "236", "701", "207",
    "135", "698", "222", "242", "167", "170", "336", "714", "180", "79",
    "94", "2256", "88", "211", "2449", "235", "87", "65", "42", "55", "21",
    "59", "35", "2827", "122", "121", "61", "cód não padrão (adesão)",
    "158", "123", "189", "204", "38", "712", "230", "6", "212", "215", "36",
    "2475", "71", "140", "195", "243", "244", "176", "239", "124", "238",
    "708", "725", "709", "223", "2453", "343", "129", "83", "154", "2461",
    "711", "2923", "24", "2376", "142", "201", "1333", "3086", "51", "150",
    "2302", "234", "146", "2463", "2918", "713", "2460", "2467", "751",
    "1305", "2464", "132", "153", "2", "161", "128", "2973", "125", "133",
    "134", "156", "2462", "135", "126", "127", "737", "136", "2960", "138",
    "767", "25", "2086", "2303", "151", "2919", "90", "697", "54", "2978",
    "202", "1284", "58", "49", "1270", "102", "15", "2473", "47", "76",
    "157", "19", "177", "2477", "20", "165", "715", "923", "168", "227",
    "2274", "131", "1371", "113", "171", "91", "2294", "2921", "226",
    "1487", "2312", "56", "68", "2457", "17", "52", "9", "18", "70", "240",
    "34", "115", "2163", "2925", "139", "155", "148", "108", "89", "2448",
    "182", "187", "28", "190", "191", "192", "205", "101", "103", "1689",
    "109", "2442", "2301", "2458", "197", "10", "2471", "12", "67", "342",
    "175", "717", "2922", "2843", "110", "2924", "2440"
]})

# Função que trata os valores de quantidade
def tratar_coluna(numero):
    try:
        num = str(numero).replace('.', '').replace(',', '.')
        return float(num)
    except:
        return np.nan

st.title("💊 Tratamento posição de estoque - Sistema MV")

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader("Envie um ou mais arquivos CSV", type="csv", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"### 📄 Arquivo: `{uploaded_file.name}`")
        
        try:
            # --- TRATAMENTO COM SEU CÓDIGO ORIGINAL ---
            df = pd.read_csv(uploaded_file, encoding='latin-1')
            df.columns = df.iloc[0]
            df = df.iloc[1:, :]
            df = df[['Produto', 'Quantidade']]
            df['Quantidade'] = df['Quantidade'].astype(str)
            df['Quantidade_corrigido'] = df['Quantidade'].apply(tratar_coluna)
            df = df.dropna()
            df['ID'], df['Nome_Produto'] = df['Produto'].str.extract(r'^(\d+)\s+(.*)', expand=True).T.values
            df_final = df[['ID', 'Quantidade_corrigido']]
            df_merge = pd.merge(df_total, df_final, on='ID', how='left')
            df_merge = df_merge.fillna(0)
            # --------------------------------------------

            st.success("Arquivo processado com sucesso ✅")
            st.dataframe(df_merge)
            st.text("teste")

            # --- CSV ---
            csv = df_merge.to_csv(index=False).encode('utf-8')
            nome_base = uploaded_file.name.replace(".csv", "")
            nome_csv = f"{nome_base}_tratado.csv"

            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=nome_csv,
                mime='text/csv',
                key=f"{uploaded_file.name}_csv"
            )

            # --- EXCEL ---
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Tratado')
            output.seek(0)

            nome_excel = f"{nome_base}_tratado.xlsx"
            st.download_button(
                label="📥 Baixar Excel",
                data=output,
                file_name=nome_excel,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key=f"{uploaded_file.name}_excel"
            )

        except Exception as e:
            st.error(f"❌ Erro ao processar `{uploaded_file.name}`: {e}")
