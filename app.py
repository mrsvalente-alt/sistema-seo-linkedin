import streamlit as st
import google.generativeai as genai
import pdfplumber

# Configuração da Página
st.set_page_config(page_title="Engenheiro de Perfil LinkedIn SEO", layout="centered")

# Título da Aplicação
st.title("🚀 Engenheiro de Perfil LinkedIn SEO 2026")
st.markdown("Transforme currículos em perfis de alto impacto otimizados para recrutadores e algoritmos.")

# Lógica de Autenticação via Secrets do Servidor
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Erro: API Key não configurada nos Secrets do servidor.")
    st.stop()

# Interface do Usuário
vaga_alvo = st.text_input("Qual a vaga ou área de interesse? (Ex: Gerente de Projetos TI)")
arquivo_pdf = st.file_uploader("Suba o currículo atual (PDF)", type="pdf")

if st.button("Gerar Rebranding Completo"):
    if vaga_alvo and arquivo_pdf:
        with st.spinner('Processando dados e consultando tendências de 2026...'):
            try:
                # 1. Extração de Texto do PDF
                texto_cv = ""
                with pdfplumber.open(arquivo_pdf) as pdf:
                    for page in pdf.pages:
                        texto_cv += page.extract_text()

                # 2. Configuração do Modelo de IA
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")

                # 3. Prompt Mestre Estruturado
                prompt_mestre = f"""
                OBJETIVO: Você é um Engenheiro de Perfil LinkedIn e Especialista em SEO Estratégico.
                Sua missão é realizar o "Rebranding" total de um profissional.

                DADOS BASE:
                Vaga Alvo: {vaga_alvo}
                Texto do Currículo: {texto_cv}

                DIRETRIZES DE EXECUÇÃO:
                1. MAPA DE KEYWORDS: Identifique as 30 palavras-chave mais buscadas para {vaga_alvo}.
                2. HEADLINE: Gere 3 opções de títulos magnéticos (separados por |).
                3. RESUMO (SOBRE): Escreva uma narrativa em 3-4 parágrafos (Método Storytelling: Passado, Presente e Futuro).
                4. EXPERIÊNCIAS: Re-escreva as experiências do currículo usando o MÉTODO STAR (Situação, Tarefa, Ação, Resultado) e linguagem técnica densa.
                5. SKILLS: Liste 40 competências (Hard e Soft Skills).
                6. PROMPT DE IMAGEM: Gere um comando detalhado para uma IA de imagem (DALL-E/Midjourney) criar uma capa de LinkedIn 4:1 única e minimalista para a profissão {vaga_alvo}.
                """

                # 4. Chamada da API
                response = model.generate_content(prompt_mestre)

                # 5. Exibição
                st.success("✅ Rebranding concluído!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Por favor, informe a vaga e faça o upload do PDF.")
