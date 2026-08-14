import streamlit as st
import pandas as pd
import json
import db_manager as db

st.set_page_config(
    page_title="Simulador CIA IIA V2025 - Autenticação & Estudos",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.get("user") else "collapsed"
)

# Custom Styling (Dark Glassmorphism & High-Contrast Typography)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Standardize Inputs & Placeholders for Maximum Legibility */
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label, .stRadio > label {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    .stTextInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1.5px solid #475569 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }
    
    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }

    /* Universal Button Styling - High Contrast Visible Text & Background */
    .stButton > button, div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
        border-radius: 8px !important;
    }
    
    .stButton > button *, div.stButton > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stButton > button:hover, div.stButton > button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #075985 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6) !important;
    }

    /* Tabs Styling - High Contrast (Branco e Azul Ciano em Fundo Escuro) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-radius: 10px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button p {
        color: #cbd5e1 !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #ffffff !important;
        background-color: #0284c7 !important;
        border-radius: 8px !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #ffffff !important;
    }

    .stTabs [data-baseweb="tab-border-bar"] {
        background-color: #0284c7 !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #38bdf8 !important;
    }
    
    /* Login Centered Container */
    .login-container {
        max-width: 550px;
        margin: 2rem auto;
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .login-title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    /* Header Card */
    .header-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        margin-top: 0.3rem;
    }
    
    /* Feedback Containers - High Contrast */
    .feedback-correct {
        background-color: #064e3b;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        color: #ecfdf5;
    }
    
    .feedback-incorrect {
        background-color: #7f1d1d;
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        color: #fef2f2;
    }
    
    .explanation-card {
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 0.75rem;
        line-height: 1.6;
    }
    
    .explanation-card.correct-exp {
        border-left: 5px solid #10b981;
        background: #064e3b;
        color: #f0fdf4;
    }

    .explanation-card.correct-exp strong {
        color: #4ade80;
    }
    
    .explanation-card.incorrect-exp {
        border-left: 5px solid #ef4444;
        background: #7f1d1d;
        color: #fff1f2;
    }

    .explanation-card.incorrect-exp strong {
        color: #fca5a5;
    }

    /* Sidebar Readability (Light Sidebar Background) */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
    }
    
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #0f172a !important;
    }

    /* Radio items readability */
    div[role="radiogroup"] label p {
        color: #f8fafc !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "user" not in st.session_state:
    st.session_state["user"] = None
if "simulado_ativo" not in st.session_state:
    st.session_state["simulado_ativo"] = False
if "questoes_simulado" not in st.session_state:
    st.session_state["questoes_simulado"] = []
if "indice_questao" not in st.session_state:
    st.session_state["indice_questao"] = 0
if "respostas_usuario" not in st.session_state:
    st.session_state["respostas_usuario"] = {}
if "modo_finalizado" not in st.session_state:
    st.session_state["modo_finalizado"] = False
if "menu_selecionado" not in st.session_state:
    st.session_state["menu_selecionado"] = "🎯 Ir Direto para o Simulado"

# ----------------------------------------------------
# TELA EXCLUSIVA DE LOGIN (SE NÃO AUTENTICADO)
# ----------------------------------------------------
if not st.session_state["user"]:
    st.markdown("""
    <div class="login-container">
        <div class="login-title">Simulador CIA IIA V2025</div>
        <div class="login-subtitle">Acesse sua conta para ter acesso completo aos simulados e acompanhamento de progresso.</div>
    </div>
    """, unsafe_allow_html=True)

    col_center = st.columns([1, 2, 1])[1]

    with col_center:
        tab_login, tab_tradicional = st.tabs([
            "🔑 Fazer Login", 
            "📝 Criar Conta"
        ])

        # TAB 1: FAZER LOGIN TRADICIONAL
        with tab_login:
            st.write("")
            st.markdown("<p style='color:#f8fafc; font-weight:600;'>Acesse com seu e-mail e senha cadastrados:</p>", unsafe_allow_html=True)
            log_email = st.text_input("E-mail", key="log_email")
            log_senha = st.text_input("Senha", type="password", key="log_senha")

            if st.button("🔑 Entrar", type="primary", use_container_width=True):
                if not log_email or not log_senha:
                    st.error("Preencha o e-mail e a senha.")
                else:
                    user_obj, msg = db.autenticar_usuario(log_email, log_senha)
                    if user_obj:
                        st.session_state["user"] = user_obj
                        st.success(f"Bem-vindo(a) de volta, {user_obj['nome']}!")
                        st.rerun()
                    else:
                        st.error(msg)

        # TAB 2: CRIAR CONTA TRADICIONAL
        with tab_tradicional:
            st.write("")
            st.markdown("<p style='color:#f8fafc; font-weight:600;'>Preencha os campos abaixo para criar sua conta:</p>", unsafe_allow_html=True)
            reg_nome = st.text_input("Nome", key="reg_nome")
            reg_sobrenome = st.text_input("Sobrenome", key="reg_sobrenome")
            reg_email = st.text_input("E-mail", key="reg_email")
            reg_senha = st.text_input("Senha", type="password", key="reg_senha")
            reg_conf_senha = st.text_input("Confirmação de Senha", type="password", key="reg_conf_senha")

            if st.button("✨ Criar Conta", type="primary", use_container_width=True):
                if not (reg_nome and reg_sobrenome and reg_email and reg_senha and reg_conf_senha):
                    st.error("Por favor, preencha todos os campos do formulário.")
                elif reg_senha != reg_conf_senha:
                    st.error("As senhas digitadas não coincidem. Verifique e tente novamente.")
                elif len(reg_senha) < 4:
                    st.error("A senha deve conter no mínimo 4 caracteres.")
                else:
                    ok, msg = db.registrar_usuario(reg_nome, reg_sobrenome, reg_email, reg_senha)
                    if ok:
                        st.success("Conta criada com sucesso! Você já pode fazer login na aba 'Fazer Login'.")
                    else:
                        st.error(msg)

    st.stop()

# ----------------------------------------------------
# ÁREA RESTRITA PÓS-LOGIN (MENU LATERAL + NAVEGAÇÃO)
# ----------------------------------------------------
user_cur = st.session_state["user"]

with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/shield-with-signature.png", width=60)
    st.title("Simulador CIA")
    sobrenome_str = f" {user_cur.get('sobrenome', '')}" if user_cur.get('sobrenome') else ""
    st.success(f"👤 **{user_cur['nome']}{sobrenome_str}**\n\n📧 `{user_cur['email']}`")
    st.divider()

    st.subheader("📌 Navegação")
    opcao_menu = st.radio(
        "Selecione uma opção:",
        [
            "🎯 Ir Direto para o Simulado", 
            "📊 Dashboard de Progresso e Resultados", 
            "🤖 Gerador de Questões JSON", 
            "📜 Instruções do Exame"
        ],
        key="nav_radio"
    )

    st.divider()
    if st.button("🚪 Sair / Logout", use_container_width=True):
        st.session_state["user"] = None
        st.session_state["simulado_ativo"] = False
        st.rerun()

# --- PÁGINA 1: RESOLVER SIMULADO ---
if opcao_menu == "🎯 Ir Direto para o Simulado":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Simulado de Auditoria Interna (CIA Parte 2)</h1>
        <p class="header-subtitle">Responda a questões situacionais com feedback imediato e estudo das 4 alternativas.</p>
    </div>
    """, unsafe_allow_html=True)

    all_questoes = db.load_questoes()

    if not st.session_state["simulado_ativo"]:
        st.subheader("🎯 Configurar Novo Simulado")
        col_sec, col_q = st.columns([2, 1])
        
        with col_sec:
            secao_opt = st.selectbox(
                "Selecione o Conteúdo Programático:",
                [
                    "Todas as Seções (Simulado Completo Parte 2)",
                    "Seção A: Planejamento do Trabalho (50%)",
                    "Seção B: Coleta, Análise e Avaliação de Informações (40%)",
                    "Seção C: Supervisão e Comunicação (10%)"
                ]
            )
            
        with col_q:
            num_q = st.number_input("Número de Questões", min_value=1, max_value=max(1, len(all_questoes)), value=min(10, len(all_questoes)))

        if st.button("🚀 Iniciar Simulado Agora", type="primary", use_container_width=True):
            if "Todas" in secao_opt:
                filtradas = all_questoes
            else:
                filtradas = [q for q in all_questoes if q.get("secao", "").startswith(secao_opt.split(":")[0])]
                if not filtradas:
                    filtradas = all_questoes

            import random
            selecionadas = filtradas.copy()
            random.shuffle(selecionadas)
            selecionadas = selecionadas[:num_q]

            st.session_state["questoes_simulado"] = selecionadas
            st.session_state["indice_questao"] = 0
            st.session_state["respostas_usuario"] = {}
            st.session_state["simulado_ativo"] = True
            st.session_state["modo_finalizado"] = False
            st.session_state["secao_selecionada"] = secao_opt
            st.rerun()

    else:
        questoes = st.session_state["questoes_simulado"]
        idx = st.session_state["indice_questao"]
        total = len(questoes)

        if st.session_state["modo_finalizado"]:
            st.subheader("🎉 Simulado Concluído!")
            
            acertos = 0
            detalhes = []
            for i, q in enumerate(questoes):
                resp = st.session_state["respostas_usuario"].get(i)
                correta = q["correta"]
                is_correct = (resp == correta)
                if is_correct:
                    acertos += 1
                detalhes.append({
                    "questao_id": q["id"],
                    "resposta": resp,
                    "correta": correta,
                    "acertou": is_correct,
                    "secao": q.get("secao", "N/A")
                })
                
            aproveitamento = (acertos / total) * 100
            
            # Salvar no Banco / JSON
            db.salvar_tentativa(
                email=user_cur["email"],
                tipo_simulado=st.session_state.get("secao_selecionada", "Geral"),
                secao=st.session_state.get("secao_selecionada", "Geral"),
                acertos=acertos,
                total=total,
                aproveitamento=aproveitamento,
                detalhes=detalhes
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Questões", total)
            with col2:
                st.metric("Acertos", acertos)
            with col3:
                st.metric("Aproveitamento", f"{aproveitamento:.1f}%")

            if aproveitamento >= 75:
                st.balloons()
                st.success("🌟 Parabéns! Seu aproveitamento atinge o padrão recomendado para aprovação no Exame CIA!")
            else:
                st.warning("📚 Bom esforço! Recomendamos revisar os conceitos com menor desempenho e realizar um novo simulado.")

            st.divider()
            st.subheader("🔍 Revisão das Questões do Simulado")
            for i, q in enumerate(questoes):
                r_usr = st.session_state["respostas_usuario"].get(i, "Não respondida")
                c_ok = q["correta"]
                status_icon = "✅" if r_usr == c_ok else "❌"
                
                with st.expander(f"{status_icon} Questão {i+1}: {q['texto'][:80]}..."):
                    st.write(f"**Enunciado Completo:** {q['texto']}")
                    st.write(f"**Sua Resposta:** {r_usr} | **Gabarito Oficial:** {c_ok}")
                    st.write(f"**Seção:** `{q.get('secao', 'N/A')}`")
                    st.markdown("---")
                    st.write("**Justificativas Técnicas (Normas Globais IIA V2025):**")
                    for let, exp in q["explicacoes"].items():
                        cls = "correct-exp" if let == c_ok else "incorrect-exp"
                        st.markdown(f"<div class='explanation-card {cls}'><b>Opção {let}:</b> {exp}</div>", unsafe_allow_html=True)

            if st.button("🔄 Iniciar Novo Simulado", type="primary"):
                st.session_state["simulado_ativo"] = False
                st.rerun()

        else:
            q_atual = questoes[idx]

            # Header da Questão
            st.progress((idx + 1) / total)
            col_info, col_sec = st.columns([1, 2])
            with col_info:
                st.markdown(f"**Questão {idx+1} de {total}**")
            with col_sec:
                st.markdown(f"<div style='text-align:right;'><span style='background:rgba(56,189,248,0.2); color:#38bdf8; padding:4px 10px; border-radius:12px; font-size:0.85rem; font-weight:600;'>{q_atual.get('secao', 'Seção A')}</span></div>", unsafe_allow_html=True)

            st.markdown(f"### {q_atual['texto']}")
            st.write("")

            opcoes_dict = q_atual["opcoes"]
            opcoes_labels = [f"{k}) {v}" for k, v in opcoes_dict.items()]

            ja_respondeu = idx in st.session_state["respostas_usuario"]
            resposta_previa = st.session_state["respostas_usuario"].get(idx, None)

            default_idx = 0
            if resposta_previa:
                for i_opt, key in enumerate(opcoes_dict.keys()):
                    if key == resposta_previa:
                        default_idx = i_opt

            escolha = st.radio(
                "Selecione a alternativa que melhor responde ao cenário situacional:",
                opcoes_labels,
                index=default_idx,
                key=f"radio_q_{idx}"
            )

            letra_escolhida = escolha[0] if escolha else "A"

            col_sub, col_next = st.columns([1, 1])
            with col_sub:
                if st.button("Confirmar Resposta", type="primary", use_container_width=True):
                    st.session_state["respostas_usuario"][idx] = letra_escolhida
                    st.rerun()

            if ja_respondeu:
                r_usr = st.session_state["respostas_usuario"][idx]
                r_correta = q_atual["correta"]

                if r_usr == r_correta:
                    st.markdown(f"""
                    <div class="feedback-correct">
                        <b style="font-size:1.1rem;">✅ Resposta Correta! (Alternativa {r_correta})</b><br>
                        Sua análise está alinhada com as Normas Globais de Auditoria Interna (IIA V2025).
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="feedback-incorrect">
                        <b style="font-size:1.1rem;">❌ Resposta Incorreta.</b><br>
                        Você marcou <b>{r_usr}</b>, mas a alternativa correta é <b>{r_correta}</b>.
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")
                st.markdown("#### 📘 Justificativas Técnicas Detalhadas (Retenção Ativa)")

                for let, text_opt in opcoes_dict.items():
                    exp = q_atual["explicacoes"].get(let, "")
                    is_this_correct = (let == r_correta)
                    card_cls = "correct-exp" if is_this_correct else "incorrect-exp"
                    tag = "🟢 CORRETA" if is_this_correct else "🔴 INCORRETA"
                    
                    st.markdown(f"""
                    <div class="explanation-card {card_cls}">
                        <strong>Alternativa {let} [{tag}]:</strong> {text_opt}<br>
                        <span style="font-style:italic;">{exp}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")
                if idx + 1 < total:
                    if st.button("Próxima Questão ➡️", use_container_width=True):
                        st.session_state["indice_questao"] += 1
                        st.rerun()
                else:
                    if st.button("🏁 Finalizar e Ver Desempenho", type="primary", use_container_width=True):
                        st.session_state["modo_finalizado"] = True
                        st.rerun()

# --- PÁGINA 2: DASHBOARD DE PROGRESSO E RESULTADOS ---
elif opcao_menu == "📊 Dashboard de Progresso e Resultados":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Dashboard de Progresso e Resultados</h1>
        <p class="header-subtitle">Acompanhe seu desempenho detalhado por Seção do Conteúdo Programático IIA V2025.</p>
    </div>
    """, unsafe_allow_html=True)

    hist = db.carregar_historico_usuario(user_cur["email"])

    if not hist:
        st.info("Nenhum histórico de simulado encontrado para este usuário. Realize seu primeiro simulado na opção 'Ir Direto para o Simulado'!")
    else:
        df = pd.DataFrame(hist)
        
        total_tentativas = len(df)
        total_q_respondidas = df["total_questoes"].sum()
        total_acertos = df["acertos"].sum()
        media_aproveitamento = df["aproveitamento_pct"].mean()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Simulados Concluídos", total_tentativas)
        with col2:
            st.metric("Questões Respondidas", total_q_respondidas)
        with col3:
            st.metric("Total de Acertos", total_acertos)
        with col4:
            st.metric("Média de Aproveitamento", f"{media_aproveitamento:.1f}%")

        st.divider()

        st.subheader("📜 Histórico de Tentativas")
        df_display = df[["data_hora", "tipo_simulado", "acertos", "total_questoes", "aproveitamento_pct"]].copy()
        df_display.columns = ["Data / Hora", "Tipo / Seção", "Acertos", "Total Questões", "Aproveitamento (%)"]
        st.dataframe(df_display, use_container_width=True)

        st.divider()

        st.subheader("📈 Evolução dos Resultados")
        st.line_chart(df.set_index("data_hora")["aproveitamento_pct"])

# --- PÁGINA 3: GERADOR DE QUESTÕES JSON ---
elif opcao_menu == "🤖 Gerador de Questões JSON":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Gerador & Importador de Questões (JSON)</h1>
        <p class="header-subtitle">Expanda o banco de dados infinito mantendo total fidelidade aos padrões oficiais IIA V2025.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_prompt, tab_import, tab_export = st.tabs(["📝 Prompt Mestre Oficial", "📥 Importar JSON", "📤 Exportar Banco Atual"])

    with tab_prompt:
        st.write("Copie o prompt abaixo e envie para o seu LLM preferido (ChatGPT, Claude, Gemini) para gerar novas questões no formato JSON padronizado:")
        
        prompt_text = """Você é um Engenheiro de Software Sênior especialista em EdTech e um autor credenciado de itens de teste para exames de certificação do IIA (Institute of Internal Auditors), com foco na certificação CIA (Certified Internal Auditor).

Sua tarefa é gerar um lote de novas questões no formato estruturado JSON totalmente alinhadas às Normas Globais de Auditoria Interna (IIA V2025) e à Parte 2 do exame CIA.

PADRÕES DE QUALIDADE:
1. Abordagem Prática e Situacional: Cenários reais enfrentados pelo auditor interno ou Executivo Chefe de Auditoria (CAE).
2. Quatro Alternativas: Exatamente 4 opções (A, B, C, D), com apenas uma correta de acordo com as Normas V2025.
3. Distratores Plausíveis: Alternativas incorretas baseadas em equívocos práticos ou papéis de gestão.
4. Explicações Abrangentes: Justificativa técnica detalhada para TODAS as 4 alternativas (por que a correta é verdadeira e por que as outras 3 estão incorretas).

MAPEMENTO DAS SEÇÕES:
- Seção A: Planejamento do Trabalho (50%)
- Seção B: Coleta, Análise e Avaliação de Informações (40%)
- Seção C: Supervisão e Comunicação do Trabalho de Auditoria (10%)

FORMATO DE SAÍDA EXIGIDO (JSON):
```json
{
  "questoes": [
    {
      "id": 11,
      "texto": "[Cenário prático situacional de auditoria]",
      "opcoes": {
        "A": "[Alternativa A]",
        "B": "[Alternativa B]",
        "C": "[Alternativa C]",
        "D": "[Alternativa D]"
      },
      "correta": "[Letra da correta: A, B, C ou D]",
      "explicacoes": {
        "A": "Incorreta/Correta: [Explicação técnica detalhada]",
        "B": "Incorreta/Correta: [Explicação técnica detalhada]",
        "C": "Incorreta/Correta: [Explicação técnica detalhada]",
        "D": "Incorreta/Correta: [Explicação técnica detalhada]"
      },
      "secao": "[Seção A: Planejamento do Trabalho (50%), Seção B... ou Seção C...]"
    }
  ]
}
```"""
        st.code(prompt_text, language="markdown")

    with tab_import:
        st.subheader("Importar Novas Questões JSON")
        json_input = st.text_area("Cole aqui o bloco JSON gerado:", height=250, placeholder='{\n  "questoes": [...]\n}')
        
        if st.button("📥 Processar e Salvar no Banco de Dados", type="primary"):
            try:
                data = json.loads(json_input)
                novas = data.get("questoes", [])
                if not novas:
                    st.error("Nenhuma questão encontrada na chave 'questoes'.")
                else:
                    db.salvar_novas_questoes(novas)
                    st.success(f"✅ {len(novas)} questões processadas e salvas com sucesso no banco de dados!")
            except Exception as e:
                st.error(f"Erro ao validar código JSON: {e}")

    with tab_export:
        st.subheader("Exportar Banco de Dados Atual")
        q_current = db.load_questoes()
        st.write(f"Atualmente o banco possui **{len(q_current)}** questões cadastradas.")
        
        json_str = json.dumps({"questoes": q_current}, ensure_ascii=False, indent=2)
        st.download_button(
            label="💾 Baixar Banco de Questões (questoes.json)",
            data=json_str,
            file_name="questoes_cia_export.json",
            mime="application/json"
        )

# --- PÁGINA 4: INSTRUÇÕES DO EXAME ---
elif opcao_menu == "📜 Instruções do Exame":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Estrutura Programática Exame CIA Parte 2</h1>
        <p class="header-subtitle">Especificações Ampliadas conforme Normas Globais IIA V2025.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 Divisão do Exame Parte 2: Trabalho de Auditoria Interna
    
    #### 🔷 Seção A: Planejamento do Trabalho (50%)
    - Determinar objetivos e escopo do trabalho (Requisitos Temáticos, apetite ao risco, conformidade regulatória).
    - Critérios de avaliação específicos, práticos e relevantes.
    - Avaliação de riscos e controles primários: Cibersegurança, TI, gestão de incidentes, continuidade de negócios e governança.
    - Abordagens metodológicas: Auditoria Ágil vs Tradicional vs Integrada vs Remota.
    
    #### 🔷 Seção B: Coleta, Análise e Avaliação de Informações (40%)
    - Fontes de evidência (entrevistas, observação, autosserviço, amostragem).
    - Qualidade da evidência: **Suficiência, Relevância, Confiabilidade e Utilidade**.
    - Tecnologias aplicadas: Inteligência Artificial (IA), Automação Robótica de Processos (RPA), Dashboards e Auditoria Contínua.
    - Técnicas analíticas (tendências, benchmarking, causa-raiz) e integridade dos Papéis de Trabalho.
    
    #### 🔷 Seção C: Supervisão e Comunicação (10%)
    - Supervisão contínua em campo, revisão de papéis de trabalho e gestão de notas de revisão.
    - Comunicação formal e informal com auditados, conselho e executivos.
    - Protocolo de escalação para riscos inaceitáveis mantidos ou aceitos pela gestão.
    """)
