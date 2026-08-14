import os
import json
import hashlib
from datetime import datetime
from supabase import create_client

SUPABASE_URL = 'https://xcflsfmgtvztykoidegg.supabase.co'
SUPABASE_SERVICE_ROLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjZmxzZm1ndHZ6dHlrb2lkZWdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NjcwNTg0OCwiZXhwIjoyMTAyMjgxODQ4fQ.yA7YnXLiiRjFeNlVRgWBDt5CVfixGJcaAJOA3ZAQZbo'
SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjZmxzZm1ndHZ6dHlrb2lkZWdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3MDU4NDgsImV4cCI6MjEwMjI4MTg0OH0.vgPctgFwgk-9qu3R8kwmEAmvhKWP614LG93iemIUQAo'
SUPABASE_PUBLISHABLE = 'sb_publishable_GXAG6uGIXg-zjYS4kGEwdA_mdimAaqd'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_USUARIOS = os.path.join(BASE_DIR, "simulador_usuarios.json")
FILE_PROGRESSO = os.path.join(BASE_DIR, "simulador_progresso.json")
FILE_QUESTOES = os.path.join(BASE_DIR, "questoes_base.json")

def get_supabase():
    try:
        # Usa a service_role key para acesso administrativo com bypass de RLS
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
        return client
    except Exception:
        return None

def init_local_files():
    if not os.path.exists(FILE_USUARIOS):
        with open(FILE_USUARIOS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
            
    if not os.path.exists(FILE_PROGRESSO):
        with open(FILE_PROGRESSO, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def hash_password(password):
    if not password:
        return ""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_or_create_google_user(email, full_name):
    email_clean = email.strip().lower()
    parts = full_name.strip().split(" ", 1)
    nome = parts[0]
    sobrenome = parts[1] if len(parts) > 1 else ""
    
    user_obj = {
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email_clean,
        "provider": "google",
        "created_at": datetime.now().isoformat()
    }
    
    sb = get_supabase()
    if sb:
        try:
            res = sb.table('usuarios').select('*').eq('email', email_clean).execute()
            if res.data and len(res.data) > 0:
                return res.data[0], True
            else:
                ins = sb.table('usuarios').insert({
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email_clean,
                    "provider": "google"
                }).execute()
                if ins.data and len(ins.data) > 0:
                    return ins.data[0], True
        except Exception:
            pass
            
    init_local_files()
    with open(FILE_USUARIOS, "r", encoding="utf-8") as f:
        users = json.load(f)
        
    for u in users:
        if u["email"].lower() == email_clean:
            return u, True
            
    users.append(user_obj)
    with open(FILE_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return user_obj, True

def registrar_usuario(nome, sobrenome, email, senha):
    email_clean = email.strip().lower()
    sb = get_supabase()
    pwd_h = hash_password(senha)
    
    user_obj = {
        "nome": nome.strip(),
        "sobrenome": sobrenome.strip(),
        "email": email_clean,
        "senha_hash": pwd_h,
        "provider": "email",
        "created_at": datetime.now().isoformat()
    }
    
    if sb:
        try:
            res = sb.table('usuarios').select('*').eq('email', email_clean).execute()
            if res.data and len(res.data) > 0:
                return False, "Este e-mail já está cadastrado no sistema."
            sb.table('usuarios').insert({
                "nome": nome.strip(),
                "sobrenome": sobrenome.strip(),
                "email": email_clean,
                "senha_hash": pwd_h,
                "provider": "email"
            }).execute()
            return True, "Cadastro realizado com sucesso!"
        except Exception:
            pass
            
    init_local_files()
    with open(FILE_USUARIOS, "r", encoding="utf-8") as f:
        users = json.load(f)
        
    for u in users:
        if u["email"].lower() == email_clean:
            return False, "Este e-mail já está cadastrado no sistema."
            
    users.append(user_obj)
    with open(FILE_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return True, "Cadastro realizado com sucesso!"

def autenticar_usuario(email, senha):
    email_clean = email.strip().lower()
    pwd_h = hash_password(senha)
    sb = get_supabase()
    
    if sb:
        try:
            res = sb.table('usuarios').select('*').eq('email', email_clean).execute()
            if res.data and len(res.data) > 0:
                user = res.data[0]
                if user.get("senha_hash") == pwd_h:
                    return user, "Sucesso"
                return None, "Senha incorreta."
        except Exception:
            pass
            
    init_local_files()
    with open(FILE_USUARIOS, "r", encoding="utf-8") as f:
        users = json.load(f)
        
    for u in users:
        if u["email"].lower() == email_clean:
            if u.get("senha_hash") == pwd_h:
                return u, "Sucesso"
            return None, "Senha incorreta."
            
    return None, "Usuário não encontrado."

def load_questoes():
    sb = get_supabase()
    if sb:
        try:
            res = sb.table('questoes').select('*').order('id').execute()
            if res.data and len(res.data) > 0:
                return res.data
        except Exception:
            pass
            
    if os.path.exists(FILE_QUESTOES):
        with open(FILE_QUESTOES, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questoes", [])
    return []

def salvar_tentativa(email, tipo_simulado, secao, acertos, total, aproveitamento, detalhes):
    registro = {
        "usuario_email": email.strip().lower(),
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo_simulado": tipo_simulado,
        "secao": secao,
        "acertos": acertos,
        "total_questoes": total,
        "aproveitamento_pct": round(aproveitamento, 2),
        "detalhes_respostas": detalhes
    }
    
    sb = get_supabase()
    if sb:
        try:
            sb.table('progresso').insert(registro).execute()
            return
        except Exception:
            pass
            
    init_local_files()
    with open(FILE_PROGRESSO, "r", encoding="utf-8") as f:
        history = json.load(f)
        
    history.append(registro)
    with open(FILE_PROGRESSO, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_user_progress(email):
    sb = get_supabase()
    if sb:
        try:
            res = sb.table("progresso").select("*").eq("usuario_email", email).order("data_hora", desc=True).execute()
            if res.data is not None:
                return res.data
        except Exception:
            pass

    if os.path.exists(FILE_PROGRESSO):
        with open(FILE_PROGRESSO, "r", encoding="utf-8") as f:
            try:
                todos = json.load(f)
                return [p for p in todos if p.get("usuario_email") == email]
            except Exception:
                return []
    return []

def get_user_errored_question_ids(email):
    """ Retorna a lista de IDs de questões que o usuário já errou em simulados anteriores. """
    progressos = get_user_progress(email)
    questoes_erradas = set()
    for p in progressos:
        detalhes = p.get("detalhes_respostas", [])
        for item in detalhes:
            if not item.get("acertou", False):
                questoes_erradas.add(item.get("questao_id"))
    return list(questoes_erradas)

def salvar_novas_questoes(questoes_list):
    sb = get_supabase()
    if sb:
        try:
            for q in questoes_list:
                sb.table('questoes').upsert(q).execute()
        except Exception:
            pass
            
    existing = load_questoes()
    existing_ids = {q["id"] for q in existing}
    for q in questoes_list:
        if q["id"] not in existing_ids:
            existing.append(q)
        else:
            existing = [q if item["id"] == q["id"] else item for item in existing]
            
    with open(FILE_QUESTOES, "w", encoding="utf-8") as f:
        json.dump({"questoes": existing}, f, ensure_ascii=False, indent=2)
