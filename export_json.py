import sqlite3
import json
import os

def export_static_json():
    DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'maringa_project.db')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    out_dirs = [
        os.path.join(os.path.dirname(__file__), 'static', 'data'),
        os.path.join(os.path.dirname(__file__), 'docs', 'data'),
        os.path.join(os.path.dirname(__file__), 'data')
    ]
    
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Overview & Project Roadmap Data
    cursor.execute('SELECT COUNT(*) FROM organizations')
    total_orgs = cursor.fetchone()[0]
    cursor.execute('SELECT group_type, COUNT(*) as qty FROM organizations GROUP BY group_type')
    orgs_by_group = {row['group_type']: row['qty'] for row in cursor.fetchall()}
    cursor.execute('SELECT COUNT(*) FROM people_contacts')
    total_contacts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM people_contacts WHERE contact_status = 'CONFIRMADO'")
    confirmed_contacts = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM comdema_members')
    comdema_members = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM encoded_interviews')
    total_interviews = cursor.fetchone()[0]

    project_products = [
        {"id": "P1", "name": "Produto 1 — Plano de Trabalho & Governança", "status": "CONCLUÍDO", "phase": "Etapa 1", "desc": "Estrutura metodológica CCFLA/CEPAL e plano de trabalho aprovados."},
        {"id": "P2", "name": "Produto 2 — Instrumentos de Coleta Roteirizados", "status": "CONCLUÍDO", "phase": "Etapa 1", "desc": "Roteiros de entrevistas e matrizes de evidências padronizadas."},
        {"id": "P3", "name": "Produto 3 — Mapeamento Institucional & Base de Evidências", "status": "EM FINALIZAÇÃO", "phase": "Etapa 2", "desc": "Mapeamento das 34 organizações, 128 registros no COMDEMA, Base Excel e Relatório Word."},
        {"id": "P4", "name": "Produto 4 — Diagnóstico das Condições Habilitantes", "status": "PRÓXIMO PASSO", "phase": "Etapa 3", "desc": "Realização das entrevistas semiestruturadas com atores das 4 dimensões CCFLA."},
        {"id": "P5", "name": "Produto 5 — Validação Participativa (Oficina Multiatores)", "status": "PLANEJADO", "phase": "Etapa 4", "desc": "Oficina com partes interessadas para validação participativa das recomendações."},
        {"id": "P6", "name": "Produto 6 — Roadmap de Fortalecimento & Relatório Final", "status": "PLANEJADO", "phase": "Etapa 5", "desc": "Plano de ação estratégico e consolidação dos caminhos para financiamento."}
    ]

    doc_evidence_matrix = [
        {"code": "DOC-01", "name": "Plano Diretor de Maringá", "category": "D1 - Planejamento", "type": "Lei Municipal", "status": "Coletado & Analisado", "org": "IPPLAM / SEURBH"},
        {"code": "DOC-02", "name": "PPA (Plano Plurianual 2022–2025)", "category": "D2 - Finanças", "type": "Peça Orçamentária", "status": "Coletado & Analisado", "org": "SEFAZ"},
        {"code": "DOC-03", "name": "LDO & LOA Vigentes", "category": "D2 - Finanças", "type": "Peça Orçamentária", "status": "Coletado & Analisado", "org": "SEFAZ"},
        {"code": "DOC-04", "name": "Legislação do FUNDEMA e IPTU Verde", "category": "D2 / D4", "type": "Arcabouço Legal", "status": "Em Análise", "org": "IAM / PROGE"},
        {"code": "DOC-05", "name": "Mapeamento de Áreas de Risco", "category": "D3 - Dados", "type": "Estudo Técnico", "status": "Coletado", "org": "Defesa Civil"},
        {"code": "DOC-06", "name": "Atos de Nomeação COMDEMA (2021–2026)", "category": "D4 - Governança", "type": "Atos Oficiais", "status": "Sistematizado (128 registros)", "org": "COMDEMA / IAM"}
    ]

    overview_data = {
        'total_orgs': total_orgs,
        'orgs_by_group': orgs_by_group,
        'total_contacts': total_contacts,
        'confirmed_contacts': confirmed_contacts,
        'comdema_members': comdema_members,
        'total_interviews': total_interviews,
        'lgpd_status': '100% Protegido & Em Conformidade',
        'project_products': project_products,
        'doc_evidence_matrix': doc_evidence_matrix
    }

    # Organizations
    cursor.execute('SELECT * FROM organizations ORDER BY code ASC')
    orgs = [dict(row) for row in cursor.fetchall()]

    # Contacts
    cursor.execute('SELECT * FROM people_contacts ORDER BY is_top_priority DESC, id ASC')
    raw_contacts = [dict(row) for row in cursor.fetchall()]

    # COMDEMA
    cursor.execute('SELECT * FROM comdema_yearly_stats ORDER BY year ASC')
    stats = [dict(row) for row in cursor.fetchall()]
    cursor.execute('SELECT * FROM comdema_members ORDER BY is_six_years DESC, name ASC')
    members = [dict(row) for row in cursor.fetchall()]

    # Interviews
    cursor.execute('SELECT * FROM encoded_interviews ORDER BY interview_code ASC')
    interviews = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # Write to target directories
    for d in out_dirs:
        with open(os.path.join(d, 'overview.json'), 'w', encoding='utf-8') as f:
            json.dump(overview_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(d, 'organizations.json'), 'w', encoding='utf-8') as f:
            json.dump({'organizations': orgs, 'count': len(orgs)}, f, ensure_ascii=False, indent=2)
        with open(os.path.join(d, 'contacts.json'), 'w', encoding='utf-8') as f:
            json.dump({'contacts': raw_contacts, 'count': len(raw_contacts)}, f, ensure_ascii=False, indent=2)
        with open(os.path.join(d, 'comdema.json'), 'w', encoding='utf-8') as f:
            json.dump({'yearly_stats': stats, 'members': members}, f, ensure_ascii=False, indent=2)
        with open(os.path.join(d, 'interviews.json'), 'w', encoding='utf-8') as f:
            json.dump({'interviews': interviews, 'count': len(interviews)}, f, ensure_ascii=False, indent=2)

    print('Arquivos JSON atualizados com cronograma de produtos e matriz de evidências!')

if __name__ == '__main__':
    export_static_json()
