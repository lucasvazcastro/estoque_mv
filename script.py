import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Função que trata os valores de quantidade
def tratar_coluna(numero):
    try:
        num = str(numero).replace('.', '').replace(',', '.')
        return float(num)
    except:
        return np.nan

st.title("💊 Tratamento de Arquivos de Produtos")

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
            # --------------------------------------------

            st.success("Arquivo processado com sucesso ✅")
            st.dataframe(df_final)

            # --- CSV ---
            csv = df_final.to_csv(index=False).encode('utf-8')
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
