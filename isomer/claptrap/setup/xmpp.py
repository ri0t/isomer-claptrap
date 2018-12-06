"""
Sets up an ejabberd server for isomer chat operation
"""

import click
from click_didyoumean import DYMGroup
from warmongo import model_factory

from isomer.logger import isolog, debug, error
from isomer.misc import std_uuid
from isomer.tool import check_root
from isomer.tool.misc import run_process


def log(*args, **kwargs):
    kwargs.update({'emitter': 'XMPPSetup', 'frame_ref': 2})
    isolog(*args, **kwargs)


@click.group(cls=DYMGroup)
@click.pass_context
def xmpp(ctx):
    """Hello world"""

    check_root()

    from isomer import database
    database.initialize(ctx.obj['dbhost'], ctx.obj['dbname'])

    from isomer.schemata.component import ComponentConfigSchemaTemplate
    factory = model_factory(ComponentConfigSchemaTemplate)
    bot_config = factory.find_one({'name': 'XMPPBOT'})

    if bot_config is None:
        password = std_uuid()

        bot_config = factory({
            'nick': 'claptrap',
            'name': 'XMPPBOT',
            'componentclass': 'XMPPBot',
            'jid': 'claptrap@localhost/node',
            'password': password,
            'uuid': std_uuid()
        })
        bot_config.save()

    # log(bot_config.serializablefields(), pretty=True)
    ctx.obj['bot_config'] = bot_config


@xmpp.command()
@click.pass_context
def add_system_user(ctx):
    bot_config = ctx.obj['bot_config']

    add_user = [
        'ejabberdctl',
        'register',
        bot_config.get('nick'),
        'localhost',
        bot_config.get('password')
    ]

    success, result = run_process('.', add_user)
    if b'conflict' in result:
        log('User already existing, updating password')
        update_password = [
            'ejabberdctl',
            'change_password',
            bot_config.get('nick'),
            'localhost',
            bot_config.get('password')
        ]
        success, result = run_process('.', update_password)
        if result != b'':
            log('Something problematic happened:', result)
    log('Done')


@xmpp.command()
def install(ctx):
    install_server = [
        'sudo',
        'apt-get',
        'install',
        'ejabberd'
    ]

    success, result = run_process('.', install_server)
    log('Done')
