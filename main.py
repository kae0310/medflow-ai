import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import database

load_dotenv()

# Inicializa o banco SQLite
database.init_db()

app = FastAPI(title="MedFlow AI - WhatsApp Agent")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "chave_temporaria"))

class MensagemRecebida(BaseModel):
    telefone: str
    mensagem: str
    nome: str = "Paciente"

class AgendamentoManual(BaseModel):
    nome: str
    telefone: str
    especialidade: str
    data_horario: str

SYSTEM_PROMPT = """
Você é a atendente virtual de uma clínica médica de alto padrão.
Seu objetivo é acolher os pacientes, tirar dúvidas básicas sobre consultas e coletar dados para agendamento.
Diretrizes:
1. Seja educada, acolhedora e direta.
2. Pergunte qual especialidade ou médico o paciente busca.
3. Peça o nome completo e o melhor dia/período para a consulta.
4. NUNCA dê diagnósticos, prescreva medicamentos ou avalie exames médicos. Se o paciente insistir, informe que isso só pode ser feito presencialmente pelo médico.
"""

@app.get("/")
def home():
    return {"status": "MedFlow AI ativo e rodando"}

@app.post("/webhook")
def receber_mensagem(dados: MensagemRecebida):
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Mensagem do paciente ({dados.nome}, tel: {dados.telefone}): {dados.mensagem}"}
            ],
            temperature=0.3
        )
        texto_resposta = resposta.choices[0].message.content
        return {
            "para": dados.telefone,
            "resposta": texto_resposta
        }
    except Exception as e:
        # Se a chave da OpenAI não estiver configurada, responde em modo de simulação
        return {
            "para": dados.telefone,
            "resposta": f"Olá {dados.nome}! Recebemos sua mensagem: '{dados.mensagem}'. Nosso sistema está pronto para conectar à sua agenda.",
            "aviso": "Modo de simulação ativo. Configure sua OPENAI_API_KEY no arquivo .env para respostas reais de IA."
        }

@app.post("/agendar")
def salvar_lead(dados: AgendamentoManual):
    database.salvar_agendamento(
        nome=dados.nome,
        telefone=dados.telefone,
        especialidade=dados.especialidade,
        data_horario=dados.data_horario
    )
    return {"status": "sucesso", "mensagem": "Agendamento salvo no banco de dados com sucesso!"}