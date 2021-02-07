import time

from utils import *
import conf

###########
# Globals #
###########

registered_chats = set()

####################
# Server Interface #
####################

def stop_server():
    shell('minecraftd stop')
    shell('systemctl stop logmein-hamachi')

def start_server():
    shell('systemctl start logmein-hamachi')
    shell('minecraftd start')

def get_server_status_desc():
    return shell('minecraftd status').decode('utf-8')

def get_players_num():
    """Get number of playing players, returns None when server is down"""

    list_cmd_stdout = shell('minecraftd command list').decode('utf-8')

    # One line (plus a blank one at the end...) means server is down
    if len(list_cmd_stdout.split('\n')) == 2:
        return None

    # Get num of players in 2nd line, 4th ':' section, 3rd word
    return int(
        list_cmd_stdout
            .split('\n')[1]
            .split(':')[3]
            .split()[2]
    )

################
# Bot Services #
################

def minecraft_handler(upd, ctx):
    # Utilities
    def send_txt(txt, trace=False):
        chat_id = upd.effective_chat.id

        if trace:
            chat_name = conf.get('chat_names').get(chat_id, chat_id)
            print(f'mc_handler(id={chat_name}): {txt}')

        ctx.bot.send_message(
            chat_id = chat_id,
            text = txt
        )

    # Add chat to minecraft chats to that it gets notified of minecraft things
    registered_chats.add(upd.effective_chat)

    # Parse command
    USG_MSG = """
    Usage: minecraft (stop|start)
    Or: minecraft cmd SERVER_CMD [ARGS...]"""

    if len(ctx.args) < 1:
        send_txt(USG_MSG)
        return

    # Parse subcmd
    subcmd = ctx.args[0]

    if subcmd == 'start':
        start_server()
        send_txt('Server started', trace=True)

    elif subcmd == 'stop':
        send_txt('Stopping server...', trace=True)
        stop_server()
        send_txt('Server stopped', trace=True)

    elif subcmd == 'status':
        send_txt(get_server_status_desc())

    elif subcmd == 'cmd':
        minecraft_cmd = ' '.join(ctx.args[1:])

        stdout = shell(f'minecraftd command {minecraft_cmd}').decode('utf-8')

        send_txt(stdout, trace=True)

    else:
        send_txt(USG_MSG)
        return

def server_inactivity_checker(bot):
    def log(txt, silent=False, notify=True):
        print(f'mc_inactivity_checker: {txt}')

        if not silent:
            for chat in registered_chats:
                bot.send_message(
                    chat_id = chat.id,
                    text = txt,
                    disable_notification = not notify
                )

    def service():
        while True:
            # Sleep before check
            time.sleep(60 * 60 * 0.5)

            # Do check
            check_time = time.strftime("%H:%M:%S", time.localtime())

            players_num = get_players_num()

            # Don't do anything if the server is down
            if players_num == None:
                log(f'Skipping inactivity check; server is down', silent=True)
                continue

            log(f'Player inactivity check (time: {check_time}, pls_num: {players_num})', notify=False)

            if players_num == 0:
                log(f'Stopping minecraft server due to inactivity')
                stop_server()
            else:
                log(f'Check passed', silent=True)

    return service
