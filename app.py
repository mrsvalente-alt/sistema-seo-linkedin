import streamlit as st
import google.generativeai as genai
import pdfplumber

# Configuração da Página
st.set_page_config(page_title="Engenheiro de Perfil LinkedIn SEO", layout="centered")

st.title("🚀 Engenheiro de Perfil LinkedIn SEO 2026")

# Lógica de Autenticação
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Erro: API Key não configurada nos Secrets.")
    st.stop()

# Interface
vaga_alvo = st.text_input("Qual a vaga ou área de interesse?")
arquivo_pdf = st.file_uploader("Suba o currículo (PDF)", type="pdf")

if st.button("Gerar Rebranding Completo"):
    if vaga_alvo and arquivo_pdf:
        with st.spinner('Processando...'):
            try:
                # Extração de Texto
                texto_cv = ""
                with pdfplumber.open(arquivo_pdf) as pdf:
                    for page in pdf.pages:
                        texto_cv += page.extract_text()

                # TENTATIVA COM O MODELO MAIS RECENTE DISPONÍVEL
                # Mudamos a forma de chamar o modelo para evitar o erro 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt_mestre = f"Atue como especialista em LinkedIn. Vaga: {vaga_alvo}. CV: {texto_cv}. Gere: Headline, Sobre e STAR Experiences."
                
                response = model.generate_content(prompt_mestre)
                st.success("✅ Sucesso!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro detalhado: {e}")
                st.info("Tentando listar modelos disponíveis para sua chave...")
                # Isso nos ajudará a ver o nome real do modelo que você pode usar
                modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write("Modelos disponíveis na sua conta:", modelos)
    else:
        st.warning("Preencha os dados.")
