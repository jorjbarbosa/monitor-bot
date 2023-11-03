import logging
import os
import globals
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, PicklePersistence
from telegram_utils import start, set_notification, unset_notification
from ptbcontrib.ptb_jobstores.sqlalchemy import PTBSQLAlchemyJobStore

load_dotenv()

possui_agendamentos = False
TIMER = 300

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )



def main():
    persistence = PicklePersistence(filepath='persistence')
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).persistence(persistence).build()
    application.job_queue.scheduler.add_jobstore(
        PTBSQLAlchemyJobStore(
            application=application,
            url="sqlite:///example.sqlite"
        )
    )
    
    application.add_handler(CommandHandler(["start", "ajuda"], start))
    application.add_handler(CommandHandler("notificar", set_notification))
    application.add_handler(CommandHandler("parar", unset_notification))
    
    # application.job_queue.run_repeating(test, interval=60, job_kwargs={"replace_existing": True, "id": 'first_job'})
    
    application.run_polling(allowed_updates=Update.ALL_TYPES,)
    
if __name__ == "__main__":
    main()