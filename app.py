from flask import Flask, jsonify, request, session, send_file, send_from_directory
import sqlite3
import os
from werkzeug.security import check_password_hash
import functools

app = Flask(__name__, static_folder='static')
app.secret_key = 'maringa_climatico_lgpd_secret_key_2026'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'maringa_project.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado', 'code': 'UNAUTHORIZED'}), 401
        return f(*args, **kwargs)
    return decorated_function

def log_audit(user_id, username, action, details):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO audit_logs (user_id, username, action, details) VALUES (?, ?, ?, ?)',
            (user_id, username, action, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao gravar log de auditoria: {e}")

# Static Routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Auth Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Informe usuário e senha.'}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['name'] = user['name']
        session['role'] = user['role']
        
        log_audit(user['id'], user['username'], 'LOGIN_SUCESSO', f"Login realizado com papel: {user['role']}")
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'name': user['name'],
                'role': user['role']
            }
        })
    
    return jsonify({'error': 'Usuário ou senha incorretos.'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        log_audit(session.get('user_id'), session.get('username'), 'LOGOUT', 'Sessão encerrada.')
        session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/me', methods=['GET'])
def me():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'name': session['name'],
                'role': session['role']
            }
        })
    return jsonify({'authenticated': False})

# Stats Overview
@app.route('/api/stats/overview', methods=['GET'])
def stats_overview():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM organizations')
    total_orgs = cursor.fetchone()[0]
    
    cursor.execute('SELECT group_type, COUNT(*) as qty FROM organizations GROUP BY group_type')
    orgs_by_group = {row['group_type']: row['qty'] for row in cursor.fetchall()}
    
    cursor.execute('SELECT COUNT(*) FROM people_contacts')
    total_contacts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM people_contacts WHERE contact_status = "CONFIRMADO"')
    confirmed_contacts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM comdema_members')
    comdema_members = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM encoded_interviews')
    total_interviews = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_orgs': total_orgs,
        'orgs_by_group': orgs_by_group,
        'total_contacts': total_contacts,
        'confirmed_contacts': confirmed_contacts,
        'comdema_members': comdema_members,
        'total_interviews': total_interviews,
        'lgpd_status': '100% Codificado & Em Conformidade'
    })

# Organizations Endpoint
@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    conn = get_db()
    cursor = conn.cursor()
    
    group_filter = request.args.get('group', '')
    search = request.args.get('search', '').lower()
    
    query = 'SELECT * FROM organizations WHERE 1=1'
    params = []
    
    if group_filter:
        query += ' AND group_type = ?'
        params.append(group_filter)
        
    if search:
        query += ' AND (LOWER(name) LIKE ? OR LOWER(acronym) LIKE ? OR LOWER(ccfla_main) LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
    query += ' ORDER BY code ASC'
    cursor.execute(query, params)
    orgs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'organizations': orgs, 'count': len(orgs)})

# People and Contacts Endpoint (LGPD Masking for Viewers)
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    user_role = session.get('role', 'visualizador')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Priority contacts first
    cursor.execute('SELECT * FROM people_contacts ORDER BY is_top_priority DESC, id ASC')
    raw_contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    processed_contacts = []
    for c in raw_contacts:
        contact_item = dict(c)
        # Apply LGPD Masking if viewer or unauthenticated
        if user_role == 'visualizador':
            # Mask emails and phone numbers for non-admin viewers
            if contact_item['email'] and '@' in contact_item['email']:
                parts = contact_item['email'].split('@')
                contact_item['email'] = parts[0][:2] + '***@' + parts[1]
            if contact_item['phone'] and len(contact_item['phone']) > 4:
                contact_item['phone'] = contact_item['phone'][:6] + '****'
        processed_contacts.append(contact_item)
        
    return jsonify({
        'contacts': processed_contacts,
        'count': len(processed_contacts),
        'user_role': user_role,
        'lgpd_notice': 'Dados de contato protegidos e mascarados para perfil Visualizador conforme LGPD.' if user_role == 'visualizador' else 'Acesso autorizado a contatos institucionais.'
    })

# COMDEMA Endpoint
@app.route('/api/comdema', methods=['GET'])
def get_comdema():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM comdema_yearly_stats ORDER BY year ASC')
    stats = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT * FROM comdema_members ORDER BY is_six_years DESC, name ASC')
    members = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({
        'yearly_stats': stats,
        'members': members,
        'members_count': len(members)
    })

# Encoded Interviews Endpoint (LGPD Compliant)
@app.route('/api/interviews', methods=['GET'])
def get_interviews():
    conn = get_db()
    cursor = conn.cursor()
    
    dimension = request.args.get('dimension', '')
    sector = request.args.get('sector', '')
    
    query = 'SELECT * FROM encoded_interviews WHERE 1=1'
    params = []
    
    if dimension:
        query += ' AND ccfla_dimension LIKE ?'
        params.append(f'%{dimension}%')
    if sector:
        query += ' AND sector_group = ?'
        params.append(sector)
        
    query += ' ORDER BY interview_code ASC'
    cursor.execute(query, params)
    interviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'interviews': interviews,
        'count': len(interviews),
        'lgpd_status': 'Codificação Sistemática Ativa (Sem Exposição de PII)'
    })

# Downloads
@app.route('/download/excel')
def download_excel():
    excel_path = os.path.join(os.path.dirname(__file__), 'P3_Base_Mapeamento_Atores_Maringa.xlsx')
    return send_file(excel_path, as_attachment=True, download_name='P3_Base_Mapeamento_Atores_Maringa.xlsx')

@app.route('/download/word')
def download_word():
    word_path = os.path.join(os.path.dirname(__file__), 'P3_Relatorio_Mapeamento_Atores_Maringa.docx')
    return send_file(word_path, as_attachment=True, download_name='P3_Relatorio_Mapeamento_Atores_Maringa.docx')

if __name__ == '__main__':
    print("Iniciando Dashboard do Projeto Maringá em http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
