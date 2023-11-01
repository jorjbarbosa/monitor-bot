import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv();

possui_agendamentos = False
TIMER = 300

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Olá, este bot tem a função de verificar quando o agendamento da nova Carteira de Identidade Nacional está disponível em Manaus")

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    global possui_agendamentos
    job = context.job
    if get_agendamentos(os.getenv('URL')):
        if not possui_agendamentos:
            possui_agendamentos = True
            await context.bot.send_message(job.chat_id, text=f"Agendamentos disponíveis, visite o site para mais informações: { os.getenv('URL') }")
    else: 
        possui_agendamentos = False
        
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True
    

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(alarm, TIMER, first=0, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = "Você receberá um alerta quando o agendamento estiver disponível! Caso não queira mais receber notificações, digite \parar"
    
    await update.effective_message.reply_text(text)

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    remove_job_if_exists(str(chat_id), context)
    text = "Você não receberá mais alertas sobre o agendamento"
    await update.message.reply_text(text)

def get_agendamentos(url) -> bool:
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        rows = soup.find('tr', attrs = { 'class' : 'table-row' })
        if len(rows) > 0:
            return True
        return False

# TO-DO
async def check_protocol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    protocol = context.args[0]
    url_protocolo = os.getenv('URL_PROTOCOLO')
    response = requests.get(f"{ url_protocolo }/get?id={ protocol }")
    if response.status_code == 200:
        response = response.json();
        print(response['Status'])
        text = f"<b>Protocolo:</b> {response['Protocolo']}\
        <b>CPF:</b> {response['Cpf']}\
        <b>Local:</b> {response['Localizacao']}\
        <b>Status:</b> {response['Status'][0]['Descricao']} {response['Status'][0]['Data']}"

        await update.message.reply_text(text=text, parse_mode='HTML')

def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    application.add_handler(CommandHandler(["start", "ajuda"], start))
    application.add_handler(CommandHandler("notificar", set_timer))
    application.add_handler(CommandHandler("parar", unset))
    application.add_handler(CommandHandler("verificar_protocolo", check_protocol))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
        
if __name__ == "__main__":
    main()