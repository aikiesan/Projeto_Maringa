import unittest
import sqlite3
import os
import json
from werkzeug.security import check_password_hash
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestBackendAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'maringa_project.db')

    def test_01_database_exists_and_populated(self):
        """Verifica se o banco de dados SQLite existe e contém registros."""
        self.assertTrue(os.path.exists(self.db_path), "O banco maringa_project.db não foi encontrado.")
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM users')
        self.assertEqual(c.fetchone()[0], 3, "Devem existir 3 usuários de teste cadastrados.")
        
        c.execute('SELECT COUNT(*) FROM organizations')
        self.assertEqual(c.fetchone()[0], 34, "Devem existir exatamente 34 organizações mapeadas.")
        
        c.execute('SELECT COUNT(*) FROM encoded_interviews')
        self.assertEqual(c.fetchone()[0], 12, "Devem existir 12 entrevistas codificadas.")
        conn.close()

    def test_02_authentication_login_success_and_failure(self):
        """Testa o endpoint de login com credenciais válidas e inválidas."""
        # Login Válido Admin
        res_admin = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'Maringa2026!Admin'
        })
        self.assertEqual(res_admin.status_code, 200)
        data_admin = res_admin.get_json()
        self.assertTrue(data_admin['success'])
        self.assertEqual(data_admin['user']['role'], 'admin')

        # Logout
        self.client.post('/api/auth/logout')

        # Login Inválido
        res_fail = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'SenhaErrada123'
        })
        self.assertEqual(res_fail.status_code, 401)

    def test_03_lgpd_contact_masking(self):
        """Verifica se os dados de contato PII são mascarados para visitantes e liberados para admin."""
        # Acesso deslogado / Visitante
        res_unauth = self.client.get('/api/contacts')
        self.assertEqual(res_unauth.status_code, 200)
        contacts_unauth = res_unauth.get_json()['contacts']
        
        # Testar se o email contém máscara (***)
        first_contact = contacts_unauth[0]
        if first_contact['email'] and '@' in first_contact['email']:
            self.assertIn('***', first_contact['email'], "O email deve conter caracteres de máscara para visitantes.")

        # Login como Admin
        self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'Maringa2026!Admin'
        })

        # Acesso como Admin
        res_admin = self.client.get('/api/contacts')
        contacts_admin = res_admin.get_json()['contacts']
        first_contact_admin = contacts_admin[0]
        self.assertNotIn('***', first_contact_admin['email'], "O email de contato não deve ter máscara para Administrador.")

    def test_04_stats_overview_and_downloads(self):
        """Verifica os endpoints de estatísticas e downloads de arquivos."""
        res_stats = self.client.get('/api/stats/overview')
        self.assertEqual(res_stats.status_code, 200)
        data_stats = res_stats.get_json()
        self.assertEqual(data_stats['total_orgs'], 34)

        # Download Excel
        res_excel = self.client.get('/download/excel')
        self.assertEqual(res_excel.status_code, 200)

        # Download Word
        res_word = self.client.get('/download/word')
        self.assertEqual(res_word.status_code, 200)

if __name__ == '__main__':
    unittest.main()
