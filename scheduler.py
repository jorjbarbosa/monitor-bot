from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
import globals
teste = False
    
def set_notification_schedule(update: Update, context: CallbackContext) -> None:
    print('')

def notification_callback(context: CallbackContext):
    print(context.job.context)
    context.application.dispatcher.user_data
    # if not globals.possui_agendamentos:
    #     context.user_data['notification_sent'] = False
    # else:
    #     if context.user_data['notification_sent'] == True:
    #         context.user_data['notification_sent'] = True
    #         await context.bot.send_message(context.job.chat_id, text=f"Agendamentos disponíveis, visite o site para mais informações: ")
    #     else:
    #         print('mensagem ja enviada')