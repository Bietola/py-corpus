import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
from pathlib import Path
import time
import sys

import utils
from utils import eprint, SRC_PATH, unique_file_path

import register
from register import RegChats

################################
# Get access to bot with token #
################################

utils.wait_until_connected(delay=20, trace=True)
updater = Updater(token='1612200159:AAFxo3qDQG2AWSmP6pvbrlzYw4cUtDrTpCM', use_context=True)
dispatcher = updater.dispatcher

##############
# Parse args #
##############

if len(sys.argv) != 2:
    eprint('Usage: python main.py DL_ROOT_DIR')
    exit(1)

DL_ROOT_DIR = Path(sys.argv[1])
DL_SUBDIR = Path('.')

##################################
# Helper Functions ans Constants #
##################################

def cur_time():
    return time.strftime("%H:%M:%S", time.localtime())

def intro(txt, silent = False):
    regchats = RegChats.get()

    for chat_id in RegChats.get():
        updater.bot.send_message(
            chat_id = chat_id,
            text = txt,
            disable_notification = silent
        )

#############
# Bot Intro #
#############

intro('NotesBoy is awake')

############
# Handlers #
############

dispatcher.add_handler(
    CommandHandler(
        'hello',
        lambda upd, ctx: ctx.bot.send_message(
            chat_id = upd.effective_chat.id,
            text = "Hello there"
        )
    )
)

dispatcher.add_handler(
    CommandHandler(
        'register',
        register.handler
    )
)

dispatcher.add_handler(
    CommandHandler(
        'regcommit',
        register.commit
    )
)

def download_photo(upd, ctx):
    global DL_ROOT_DIR
    global DL_SUBDIR

    dl_path = unique_file_path(
        DL_ROOT_DIR / DL_SUBDIR,
        fstr = '{}.jpg'
    )

    print(f'Downloading to {dl_path}')

    ctx.bot.get_file(
        upd.message.photo[-1].file_id
    ).download(dl_path)

dispatcher.add_handler(
    MessageHandler(
        Filters.photo,
        download_photo
    )
)

def change_subdir(upd, ctx):
    global DL_ROOT_DIR
    global DL_SUBDIR

    DL_SUBDIR = Path(ctx.args[0])

    ctx.bot.send_message(
        chat_id = upd.effective_chat.id,
        text = f'Updating download dir to {DL_ROOT_DIR / DL_SUBDIR}'
    )
dispatcher.add_handler(
    CommandHandler(
        'sub',
        change_subdir
    )
)

########
# Main #
########

# Start bot
updater.start_polling()
