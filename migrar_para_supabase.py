import json
import os
import db_manager as db

def migrar():
    sb = db.get_supabase()
    if not sb:
        print("Erro: Não foi possível conectar ao Supabase.")
        return

    print("--- INICIANDO MIGRAÇÃO PARA O SUPABASE ---")

    # 1. Migrar Questões
    if os.path.exists(db.FILE_QUESTOES):
        with open(db.FILE_QUESTOES, "r", encoding="utf-8") as f:
            questoes = json.load(f).get("questoes", [])
            print(f"Encontradas {len(questoes)} questões locais.")
            for q in questoes:
                try:
                    sb.table("questoes").upsert(q).execute()
                    print(f"✅ Questão {q['id']} migrada com sucesso.")
                except Exception as e:
                    print(f"❌ Erro ao migrar questão {q['id']}: {e}")

    # 2. Migrar Usuários
    if os.path.exists(db.FILE_USUARIOS):
        with open(db.FILE_USUARIOS, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
            print(f"\nEncontrados {len(usuarios)} usuários locais.")
            for u in usuarios:
                try:
                    sb.table("usuarios").upsert(u).execute()
                    print(f"✅ Usuário {u['email']} migrado com sucesso.")
                except Exception as e:
                    print(f"❌ Erro ao migrar usuário {u.get('email')}: {e}")

    # 3. Migrar Progresso
    if os.path.exists(db.FILE_PROGRESSO):
        with open(db.FILE_PROGRESSO, "r", encoding="utf-8") as f:
            progresso = json.load(f)
            print(f"\nEncontrados {len(progresso)} registros de progresso locais.")
            for p in progresso:
                try:
                    sb.table("progresso").insert(p).execute()
                    print(f"✅ Progresso do usuário {p['usuario_email']} migrado com sucesso.")
                except Exception as e:
                    print(f"❌ Erro ao migrar progresso: {e}")

    print("\n--- MIGRAÇÃO CONCLUÍDA ---")

if __name__ == "__main__":
    migrar()
