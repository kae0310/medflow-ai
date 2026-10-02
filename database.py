import sqlite3

DB_NAME = "clinica.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            especialidade TEXT,
            data_horario TEXT,
            status TEXT DEFAULT 'Pendente'
        )
    """)
    conn.commit()
    conn.close()

def salvar_agendamento(nome: str, telefone: str, especialidade: str, data_horario: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (nome, telefone, especialidade, data_horario)
        VALUES (?, ?, ?, ?)
    """, (nome, telefone, especialidade, data_horario))
    conn.commit()
    conn.close()
    