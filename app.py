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

# Custom Styling (EdTech 2026 Design Tokens, Modern Glassmorphism & High-Contrast Typography)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        /* Design Tokens - Palette HSL / OKLCH Calibrated WCAG 2.2 AA/AAA */
        --bg-gradient: linear-gradient(135deg, #0b1329 0%, #111c3a 50%, #1e293b 100%);
        --card-bg: rgba(30, 41, 59, 0.75);
        --card-border: rgba(255, 255, 255, 0.12);
        --accent-cyan: #38bdf8;
        --accent-blue: #0284c7;
        --accent-indigo: #6366f1;
        --accent-emerald: #10b981;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-dark: #0f172a;
        
        /* Font Scale Clamp Tokens */
        --font-h1: clamp(1.6rem, 4vw, 2.5rem);
        --font-h2: clamp(1.3rem, 3vw, 1.8rem);
        --font-body: clamp(0.9rem, 1.5vw, 1rem);
    }
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    }
    
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-primary);
    }

    /* Standardize Inputs & Placeholders for Maximum Legibility & Focus States */
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label, .stRadio > label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em;
    }

    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
        outline: none !important;
    }
    
    .stTextInput input::placeholder {
        color: var(--text-secondary) !important;
    }

    /* Universal Button Styling - High Contrast Visible Text & Smooth Microinteractions */
    .stButton > button, div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
        border-radius: 10px !important;
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease !important;
    }
    
    .stButton > button *, div.stButton > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stButton > button:hover, div.stButton > button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #4338ca 100%) !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.5) !important;
    }

    .stButton > button:focus-visible {
        outline: 3px solid var(--accent-cyan) !important;
        outline-offset: 2px !important;
    }

    /* Tabs Styling - Glassmorphism High Contrast */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 10px 18px !important;
        border-radius: 8px !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 180ms ease !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, #0284c7 0%, #3b82f6 100%) !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
    }
    
    /* Modern Split-Screen Login Container */
    .split-login-wrapper {
        display: flex;
        flex-direction: row;
        width: 100%;
        max-width: 1040px;
        margin: 2rem auto;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }

    .split-hero-side {
        flex: 1.1;
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.25) 0%, rgba(99, 102, 241, 0.3) 100%);
        padding: 3rem 2.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .split-hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 30px;
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 700;
        width: fit-content;
        margin-bottom: 1.5rem;
    }

    .split-hero-title {
        font-size: clamp(1.8rem, 3.5vw, 2.4rem);
        font-weight: 800;
        line-height: 1.2;
        background: linear-gradient(90deg, #ffffff, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    .split-hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .split-feature-item {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
        color: #e2e8f0;
        font-weight: 500;
    }

    .split-feature-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(56, 189, 248, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #38bdf8;
        font-weight: 700;
    }

    .split-form-side {
        flex: 1;
        padding: 2.5rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Bento Grid Card Tokens for Dashboard */
    .bento-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .bento-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        transition: transform 200ms ease, border-color 200ms ease;
    }

    .bento-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
    }

    .bento-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .bento-card-title {
        color: var(--text-secondary);
        font-size: 0.88rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .bento-card-value {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
    }

    .bento-card-badge {
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
    }
    
    /* Header Card */
    .header-card {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 1.75rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.75rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: var(--font-h1);
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header-subtitle {
        color: var(--text-secondary);
        font-size: var(--font-body);
        margin-top: 0.4rem;
    }
    
    /* Feedback Containers - High Contrast WCAG AA */
    .feedback-correct {
        background-color: rgba(6, 78, 59, 0.85);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        color: #ecfdf5;
    }
    
    .feedback-incorrect {
        background-color: rgba(127, 29, 29, 0.85);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        color: #fef2f2;
    }
    
    .explanation-card {
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-top: 0.75rem;
        line-height: 1.6;
    }
    
    .explanation-card.correct-exp {
        border-left: 5px solid #10b981;
        background: rgba(6, 78, 59, 0.9);
        color: #f0fdf4;
    }

    .explanation-card.correct-exp strong {
        color: #4ade80;
    }
    
    .explanation-card.incorrect-exp {
        border-left: 5px solid #ef4444;
        background: rgba(127, 29, 29, 0.9);
        color: #fff1f2;
    }

    .explanation-card.incorrect-exp strong {
        color: #fca5a5;
    }

    /* Sidebar Readability (Light Sidebar Background) & SVG Icon Patterns */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }

    /* Estilização para o menu recolhido (Sidebar Retrátil Visível) */
    [data-testid="stSidebar"][aria-expanded="false"],
    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        transform: none !important;
        min-width: 75px !important;
        max-width: 75px !important;
        width: 75px !important;
        visibility: visible !important;
        display: block !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] .user-profile-card,
    [data-testid="stSidebar"][aria-expanded="false"] .sidebar-app-title,
    [data-testid="stSidebar"][aria-expanded="false"] p,
    [data-testid="stSidebar"][aria-expanded="false"] h1,
    [data-testid="stSidebar"][aria-expanded="false"] h2,
    [data-testid="stSidebar"][aria-expanded="false"] h3,
    [data-testid="stSidebar"][aria-expanded="false"] hr,
    [data-testid="stSidebar"][aria-expanded="false"] .stAlert {
        display: none !important;
    }

    /* Exibir os itens do radio group como ícones centralizados quando recolhido */
    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] {
        padding-top: 1rem !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] label {
        justify-content: center !important;
        padding: 10px 0 !important;
        margin: 6px 0 !important;
        border-radius: 10px !important;
        background: rgba(2, 132, 199, 0.08) !important;
    }

    /* Inserir ícones explicativos via CSS nos botões do rádio quando recolhido */
    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] label:nth-child(1)::after {
        content: "🎯" !important;
        font-size: 1.4rem !important;
        display: block !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] label:nth-child(2)::after {
        content: "📊" !important;
        font-size: 1.4rem !important;
        display: block !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] label:nth-child(3)::after {
        content: "📜" !important;
        font-size: 1.4rem !important;
        display: block !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] label > div:nth-child(2) {
        display: none !important;
    }

    /* Respeito às preferências de movimento do usuário (A11y) */
    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    /* Regras Responsivas Mobile (<= 768px) */
    @media screen and (max-width: 768px) {
        .block-container {
            padding: 0.75rem 0.5rem !important;
        }

        .split-login-wrapper {
            flex-direction: column !important;
            margin: 0.5rem auto !important;
            border-radius: 16px !important;
        }

        .split-hero-side {
            padding: 1.75rem 1.25rem !important;
            border-right: none !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        .split-form-side {
            padding: 1.5rem 1.25rem !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            width: 100% !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            flex: 1 1 50% !important;
            padding: 8px 4px !important;
            font-size: 0.85rem !important;
            text-align: center !important;
        }

        .stButton > button, div.stButton > button {
            font-size: 0.95rem !important;
            padding: 0.55rem 0.75rem !important;
            width: 100% !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
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
# TELA EXCLUSIVA DE LOGIN (SE NÃO AUTENTICADO) - SPLIT SCREEN EDTECH
# ----------------------------------------------------
if not st.session_state["user"]:
    col_hero, col_form = st.columns([1.1, 1], gap="large")

    with col_hero:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(2,132,199,0.2) 0%, rgba(99,102,241,0.25) 100%); padding: 2.5rem 2rem; border-radius: 24px; border: 1px solid rgba(255,255,255,0.12); margin-top: 1rem;">
            <div style="display:inline-flex; align-items:center; gap:8px; padding:6px 16px; background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.3); border-radius:30px; color:#38bdf8; font-size:0.85rem; font-weight:700; margin-bottom:1.25rem;">
                🛡️ PLATAFORMA OFICIAL IIA V2025
            </div>
            <h1 style="font-size: clamp(1.8rem, 3.5vw, 2.5rem); font-weight:800; line-height:1.25; background: linear-gradient(90deg, #ffffff, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;">
                Prepare-se com Excelência para a Certificação CIA Parte 2
            </h1>
            <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem;">
                Simulados situacionais inteligentes com gabaritos comentados opção a opção, métricas de desempenho e reforço personalizado de erros.
            </p>
            <div style="display:flex; flex-direction:column; gap:12px;">
                <div style="display:flex; align-items:center; gap:12px; color:#e2e8f0; font-weight:600;">
                    <div style="width:32px; height:32px; border-radius:8px; background:rgba(56,189,248,0.2); display:flex; align-items:center; justify-content:center; color:#38bdf8;">✓</div>
                    100% Alinhado às novas Normas Globais IIA 2025
                </div>
                <div style="display:flex; align-items:center; gap:12px; color:#e2e8f0; font-weight:600;">
                    <div style="width:32px; height:32px; border-radius:8px; background:rgba(99,102,241,0.2); display:flex; align-items:center; justify-content:center; color:#818cf8;">✓</div>
                    Modo Reforço Inteligente para Questões Incorretas
                </div>
                <div style="display:flex; align-items:center; gap:12px; color:#e2e8f0; font-weight:600;">
                    <div style="width:32px; height:32px; border-radius:8px; background:rgba(16,185,129,0.2); display:flex; align-items:center; justify-content:center; color:#10b981;">✓</div>
                    Divisão Ponderada Oficial (50% A / 40% B / 10% C)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("<h2 style='font-size:1.6rem; font-weight:700; color:#ffffff; margin-top:1rem; margin-bottom:0.25rem;'>Bem-vindo(a) de volta! 👋</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.95rem; margin-bottom:1.5rem;'>Acesse com sua conta para continuar seus estudos.</p>", unsafe_allow_html=True)

        tab_login, tab_tradicional = st.tabs([
            "🔑 Fazer Login", 
            "📝 Criar Conta"
        ])

        # TAB 1: FAZER LOGIN TRADICIONAL
        with tab_login:
            log_email = st.text_input("E-mail", key="log_email", placeholder="seu.email@exemplo.com")
            log_senha = st.text_input("Senha", type="password", key="log_senha", placeholder="••••••••")

            if st.button("🔑 Entrar na Plataforma", type="primary", use_container_width=True, key="btn_login_direct"):
                if not log_email.strip() or not log_senha.strip():
                    st.error("Por favor, preencha o e-mail e a senha.")
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
            reg_nome = st.text_input("Nome", key="reg_nome", placeholder="Seu nome")
            reg_sobrenome = st.text_input("Sobrenome", key="reg_sobrenome", placeholder="Seu sobrenome")
            reg_email = st.text_input("E-mail", key="reg_email", placeholder="seu.email@exemplo.com")
            reg_senha = st.text_input("Senha", type="password", key="reg_senha", placeholder="Mínimo 4 caracteres")
            reg_conf_senha = st.text_input("Confirmação de Senha", type="password", key="reg_conf_senha", placeholder="Repita sua senha")

            # Feedback de validação visual de confirmação de senha em tempo real
            if reg_conf_senha:
                if reg_senha == reg_conf_senha:
                    st.markdown("<p style='color:#4ade80; font-size:0.85rem; font-weight:600;'>✅ As senhas coincidem.</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color:#fca5a5; font-size:0.85rem; font-weight:600;'>❌ As senhas não coincidem.</p>", unsafe_allow_html=True)

            if st.button("✨ Criar Minha Conta", type="primary", use_container_width=True, key="btn_reg_direct"):
                if not (reg_nome.strip() and reg_sobrenome.strip() and reg_email.strip() and reg_senha.strip() and reg_conf_senha.strip()):
                    st.error("Por favor, preencha todos os campos do formulário.")
                elif reg_senha != reg_conf_senha:
                    st.error("As senhas digitadas não coincidem. Verifique e tente novamente.")
                elif len(reg_senha) < 4:
                    st.error("A senha deve conter no mínimo 4 caracteres.")
                else:
                    ok, msg = db.registrar_usuario(reg_nome, reg_sobrenome, reg_email, reg_senha)
                    if ok:
                        user_obj, _ = db.autenticar_usuario(reg_email, reg_senha)
                        if user_obj:
                            st.session_state["user"] = user_obj
                            st.success(f"Conta criada com sucesso! Bem-vindo(a), {user_obj['nome']}!")
                            st.rerun()
                        else:
                            st.success("Conta criada com sucesso! Faça login para continuar.")
                    else:
                        st.error(msg)

    st.stop()

# ----------------------------------------------------
# ÁREA RESTRITA PÓS-LOGIN (MENU LATERAL + NAVEGAÇÃO)
# ----------------------------------------------------
user_cur = st.session_state["user"]

with st.sidebar:
    # Header da Sidebar sem imagens quebradas e no padrão visual do sistema
    st.markdown("""
    <div class="sidebar-app-title" style="display:flex; align-items:center; gap:12px; margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid #e2e8f0;">
        <div style="width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg, #0284c7 0%, #4f46e5 100%); display:flex; align-items:center; justify-content:center; color:#ffffff; font-weight:800; font-size:1.2rem;">
            🛡️
        </div>
        <div>
            <div style="font-size:1.1rem; font-weight:800; color:#0f172a; line-height:1.2;">Simulador CIA</div>
            <div style="font-size:0.75rem; color:#64748b; font-weight:600;">Normas IIA V2025</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Perfil do Usuário com avatar vetorial SVG profissional
    sobrenome_str = f" {user_cur.get('sobrenome', '')}" if user_cur.get('sobrenome') else ""
    iniciais = f"{user_cur['nome'][0]}{user_cur.get('sobrenome', ' ')[0]}".upper()
    
    st.markdown(f"""
    <div class="user-profile-card" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:1rem; margin-bottom:1.25rem; display:flex; align-items:center; gap:12px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="width:42px; height:42px; border-radius:50%; background:linear-gradient(135deg, #38bdf8 0%, #0284c7 100%); color:#ffffff; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem;">
            {iniciais}
        </div>
        <div style="overflow:hidden;">
            <div style="font-size:0.95rem; font-weight:700; color:#0f172a; text-overflow:ellipsis; overflow:hidden; whitespace:nowrap;">{user_cur['nome']}{sobrenome_str}</div>
            <div style="font-size:0.75rem; color:#64748b; text-overflow:ellipsis; overflow:hidden; whitespace:nowrap;">{user_cur['email']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem;'>Navegação Principal</p>", unsafe_allow_html=True)
    
    opcao_menu = st.radio(
        "Navegação:",
        [
            "Simulados", 
            "Progresso", 
            "Instruções"
        ],
        key="nav_radio",
        label_visibility="collapsed"
    )

    st.divider()
    if st.button("🚪 Sair / Logout", use_container_width=True):
        st.session_state["user"] = None
        st.session_state["simulado_ativo"] = False
        st.rerun()

# --- PÁGINA 1: SIMULADOS ---
if opcao_menu == "Simulados":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Simulado de Auditoria Interna (CIA Parte 2)</h1>
        <p class="header-subtitle">Responda a questões situacionais com feedback imediato e estudo das 4 alternativas.</p>
    </div>
    """, unsafe_allow_html=True)

    all_questoes = db.load_questoes()
    user_email = st.session_state["user"]["email"] if st.session_state.get("user") else ""
    questoes_erradas_ids = db.get_user_errored_question_ids(user_email) if user_email else []

    if not st.session_state["simulado_ativo"]:
        st.subheader("🎯 Configurar Novo Simulado")

        # Opções de filtro por nível ou modo de reforço
        opcoes_filtro = ["Todas as Dificuldades", "Fáceis", "Intermediárias", "Difíceis"]
        if questoes_erradas_ids:
            opcoes_filtro.append("⚠️ Apenas Questões que Errei (Modo Reforço)")

        col_sec, col_dificuldade, col_q = st.columns([2, 2, 1])

        with col_sec:
            secao_opt = st.selectbox(
                "Selecione o Conteúdo Programático:",
                [
                    "Todas as Seções (Simulado Completo Parte 2 - 100 Qs)",
                    "Seção A: Planejamento do Trabalho (50%)",
                    "Seção B: Coleta, Análise e Avaliação de Informações (40%)",
                    "Seção C: Supervisão e Comunicação (10%)"
                ]
            )

        with col_dificuldade:
            filtro_dificuldade = st.selectbox(
                "Nível de Dificuldade ou Modo:",
                opcoes_filtro
            )

        is_completo = "Todas as Seções" in secao_opt

        with col_q:
            if is_completo and "Errei" not in filtro_dificuldade:
                num_q = st.number_input("Número de Questões", min_value=1, max_value=max(100, len(all_questoes)), value=min(100, max(10, len(all_questoes))), disabled=True, help="O Simulado Completo Oficial possui 100 questões divididas proporcionalmente.")
            else:
                max_val = len(questoes_erradas_ids) if "Errei" in filtro_dificuldade else len(all_questoes)
                num_q = st.number_input("Número de Questões", min_value=1, max_value=max(1, max_val), value=min(10, max(1, max_val)))

        if "Errei" in filtro_dificuldade:
            st.info(f"💡 Você possui **{len(questoes_erradas_ids)}** questão(ões) registradas que errou em simulados anteriores.")

        if st.button("🚀 Iniciar Simulado Agora", type="primary", use_container_width=True):
            import random

            # 1. Aplicar filtro inicial (Dificuldade ou Questões Erradas)
            base_pool = all_questoes.copy()
            if "Errei" in filtro_dificuldade:
                base_pool = [q for q in base_pool if q["id"] in questoes_erradas_ids]
            elif filtro_dificuldade != "Todas as Dificuldades":
                # Normalização de rótulos (Fáceis -> Fácil, Intermediárias -> Intermediário, Difíceis -> Difícil)
                map_nivel = {"Fáceis": "Fácil", "Intermediárias": "Intermediário", "Difíceis": "Difícil"}
                target_nivel = map_nivel.get(filtro_dificuldade, filtro_dificuldade)
                filtradas_nivel = [q for q in base_pool if q.get("nivel", "") == target_nivel]
                if filtradas_nivel:
                    base_pool = filtradas_nivel

            # 2. Lógica para Simulado Completo Oficial (100 questões com proporção 50% A, 40% B, 10% C)
            if is_completo and "Errei" not in filtro_dificuldade:
                pool_a = [q for q in base_pool if q.get("secao", "").startswith("Seção A")]
                pool_b = [q for q in base_pool if q.get("secao", "").startswith("Seção B")]
                pool_c = [q for q in base_pool if q.get("secao", "").startswith("Seção C")]

                random.shuffle(pool_a)
                random.shuffle(pool_b)
                random.shuffle(pool_c)

                # Proporção ideal para 100 questões: 50 de A, 40 de B, 10 de C
                # Caso a base de dados ainda não tenha 100 questões, distribuímos proporcionalmente ao total disponível
                qtd_total = min(100, len(base_pool))
                target_a = int(round(qtd_total * 0.50))
                target_b = int(round(qtd_total * 0.40))
                target_c = qtd_total - target_a - target_b

                sel_a = pool_a[:target_a]
                sel_b = pool_b[:target_b]
                sel_c = pool_c[:target_c]

                selecionadas = sel_a + sel_b + sel_c
                # Preencher com questões restantes da base se alguma seção tiver poucas questões
                if len(selecionadas) < qtd_total:
                    usados_ids = {q["id"] for q in selecionadas}
                    restantes = [q for q in base_pool if q["id"] not in usados_ids]
                    random.shuffle(restantes)
                    selecionadas.extend(restantes[:qtd_total - len(selecionadas)])

                random.shuffle(selecionadas)

            else:
                # Simulado por Seção Específica ou Modo Erros
                if is_completo:
                    filtradas = base_pool
                else:
                    secao_prefix = secao_opt.split(":")[0]
                    filtradas = [q for q in base_pool if q.get("secao", "").startswith(secao_prefix)]
                    if not filtradas:
                        filtradas = base_pool

                selecionadas = filtradas.copy()
                random.shuffle(selecionadas)
                selecionadas = selecionadas[:num_q]

            if not selecionadas:
                st.warning("Nenhuma questão encontrada para os filtros selecionados. Tente ajustar a dificuldade ou seção.")
            else:
                st.session_state["questoes_simulado"] = selecionadas
                st.session_state["indice_questao"] = 0
                st.session_state["respostas_usuario"] = {}
                st.session_state["simulado_ativo"] = True
                st.session_state["modo_finalizado"] = False
                st.session_state["secao_selecionada"] = f"{secao_opt} ({filtro_dificuldade})"
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

# --- PÁGINA 2: PROGRESSO ---
elif opcao_menu == "Progresso":
    st.markdown("""
    <div class="header-card">
        <h1 class="header-title">Dashboard de Progresso e Resultados</h1>
        <p class="header-subtitle">Acompanhe seu desempenho detalhado por Seção do Conteúdo Programático IIA V2025.</p>
    </div>
    """, unsafe_allow_html=True)

    hist = db.get_user_progress(user_cur["email"])

    if not hist:
        total_tentativas = 0
        total_q_respondidas = 0
        total_acertos = 0
        media_aproveitamento = 0.0
    else:
        df = pd.DataFrame(hist)
        total_tentativas = len(df)
        total_q_respondidas = df["total_questoes"].sum() if "total_questoes" in df.columns else 0
        total_acertos = df["acertos"].sum() if "acertos" in df.columns else 0
        media_aproveitamento = df["aproveitamento_pct"].mean() if "aproveitamento_pct" in df.columns else 0.0

    # Exibição do Bento Grid com valores zerados ou calculados sem erro
    st.markdown(f"""
    <div class="bento-grid">
        <div class="bento-card">
            <div class="bento-card-header">
                <span class="bento-card-title">Simulados Concluídos</span>
                <span class="bento-card-badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">🎯 ATIVIDADE</span>
            </div>
            <div class="bento-card-value">{total_tentativas}</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.4rem;">Sessões registradas no banco</div>
        </div>
        <div class="bento-card">
            <div class="bento-card-header">
                <span class="bento-card-title">Questões Respondidas</span>
                <span class="bento-card-badge" style="background:rgba(99,102,241,0.2); color:#818cf8;">📚 VOLUME</span>
            </div>
            <div class="bento-card-value">{total_q_respondidas}</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.4rem;">Itens situacionais processados</div>
        </div>
        <div class="bento-card">
            <div class="bento-card-header">
                <span class="bento-card-title">Total de Acertos</span>
                <span class="bento-card-badge" style="background:rgba(16,185,129,0.2); color:#10b981;">✅ PRECISÃO</span>
            </div>
            <div class="bento-card-value">{total_acertos}</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.4rem;">Respostas corretas confirmadas</div>
        </div>
        <div class="bento-card">
            <div class="bento-card-header">
                <span class="bento-card-title">Média de Aproveitamento</span>
                <span class="bento-card-badge" style="background:rgba(245,158,11,0.2); color:#f59e0b;">📊 DESEMPENHO</span>
            </div>
            <div class="bento-card-value">{media_aproveitamento:.1f}%</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.4rem;">Meta recomendada IIA: ≥ 75%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if not hist:
        st.info("💡 Nenhum histórico de simulado encontrado ainda para este usuário. Ao concluir seu primeiro simulado na aba 'Simulados', suas estatísticas detalhadas e gráficos serão atualizados aqui automaticamente.")
    else:
        st.subheader("📜 Histórico de Tentativas")
        df_display = df[["data_hora", "tipo_simulado", "acertos", "total_questoes", "aproveitamento_pct"]].copy()
        df_display.columns = ["Data / Hora", "Tipo / Seção", "Acertos", "Total Questões", "Aproveitamento (%)"]
        st.dataframe(df_display, use_container_width=True)

        st.divider()

        st.subheader("📈 Evolução dos Resultados")
        st.line_chart(df.set_index("data_hora")["aproveitamento_pct"])

# --- PÁGINA 3: INSTRUÇÕES ---
elif opcao_menu == "Instruções":
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
