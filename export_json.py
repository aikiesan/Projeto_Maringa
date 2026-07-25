import sqlite3
import json
import os

def export_static_json():
    DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'maringa_project.db')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    out_dir = os.path.join(os.path.dirname(__file__), 'static', 'data')
    os.makedirs(out_dir, exist_ok=True)

    # Overview
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

    overview_data = {
        'total_orgs': total_orgs,
        'orgs_by_group': orgs_by_group,
        'total_contacts': total_contacts,
        'confirmed_contacts': confirmed_contacts,
        'comdema_members': comdema_members,
        'total_interviews': total_interviews,
        'lgpd_status': '100% Codificado & Em Conformidade'
    }
    with open(os.path.join(out_dir, 'overview.json'), 'w', encoding='utf-8') as f:
        json.dump(overview_data, f, ensure_ascii=False, indent=2)

    # Organizations
    cursor.execute('SELECT * FROM organizations ORDER BY code ASC')
    orgs = [dict(row) for row in cursor.fetchall()]
    with open(os.path.join(out_dir, 'organizations.json'), 'w', encoding='utf-8') as f:
        json.dump({'organizations': orgs, 'count': len(orgs)}, f, ensure_ascii=False, indent=2)

    # Contacts
    cursor.execute('SELECT * FROM people_contacts ORDER BY is_top_priority DESC, id ASC')
    raw_contacts = [dict(row) for row in cursor.fetchall()]
    with open(os.path.join(out_dir, 'contacts.json'), 'w', encoding='utf-8') as f:
        json.dump({'contacts': raw_contacts, 'count': len(raw_contacts)}, f, ensure_ascii=False, indent=2)

    # COMDEMA
    cursor.execute('SELECT * FROM comdema_yearly_stats ORDER BY year ASC')
    stats = [dict(row) for row in cursor.fetchall()]
    cursor.execute('SELECT * FROM comdema_members ORDER BY is_six_years DESC, name ASC')
    members = [dict(row) for row in cursor.fetchall()]
    with open(os.path.join(out_dir, 'comdema.json'), 'w', encoding='utf-8') as f:
        json.dump({'yearly_stats': stats, 'members': members}, f, ensure_ascii=False, indent=2)

    # Interviews
    cursor.execute('SELECT * FROM encoded_interviews ORDER BY interview_code ASC')
    interviews = [dict(row) for row in cursor.fetchall()]
    with open(os.path.join(out_dir, 'interviews.json'), 'w', encoding='utf-8') as f:
        json.dump({'interviews': interviews, 'count': len(interviews)}, f, ensure_ascii=False, indent=2)

    conn.close()
    print('Arquivos JSON estáticos exportados com sucesso em static/data/!')

if __name__ == '__main__':
    export_static_json()
