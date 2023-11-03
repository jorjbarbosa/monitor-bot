from telegram import Update
from telegram.ext import ContextTypes
from scheduler import set_notification_schedule
import globals

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Olá, este bot tem a função de verificar quando o agendamento da nova Carteira de Identidade Nacional está disponível em Manaus")

async def set_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_notification_schedule(update, context)
    text = "Você receberá um alerta quando o agendamento estiver disponível! Caso não queira mais receber notificações, digite \parar"
    await update.effective_message.reply_text(text)

async def unset_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Você não receberá mais alertas sobre o agendamento"
    await update.message.reply_text(text)
