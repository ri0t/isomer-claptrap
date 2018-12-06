#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Isomer Application Framework
# ============================
# Copyright (C) 2011-2018 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Heiko 'riot' Weinen"
__license__ = "AGPLv3"

"""

Module: XMPP
============

XMPP Bot


"""

from circuits.core.events import Event
from sleekxmpp.clientxmpp import ClientXMPP
from sleekxmpp import Message

from isomer.debugger import cli_register_event
from isomer.misc import std_hash, std_uuid

from isomer.component import ConfigurableComponent, handler
from isomer.logger import error, warn, hilight, debug, verbose
from isomer.events.client import broadcast, send


class cli_test_xmpp_send(Event):
    """Test xmpp message transmission"""
    pass


class send_xmpp_message(Event):
    """Transmit a xmpp message to a user"""

    def __init__(self, username, subject, body, msg_type='chat', *args, **kwargs):
        super(send_xmpp_message, self).__init__(*args, **kwargs)
        self.msg_type = msg_type
        self.body = body
        self.subject = subject
        self.username = username


class XMPPGate(ConfigurableComponent, ClientXMPP):
    """
    Chat bot with NLP interface

    Handles
    * incoming chat messages
    * responding to various requests
    """

    configprops = {
        'nick': {
            'type': 'string',
            'title': 'Nick',
            'description': 'Name of this chat bot',
            'default': 'claptrap'
        },
        'jid': {
            'type': 'string',
            'title': 'JID',
            'description': 'Jabber ID of this chat bot',
            'default': 'claptrap@localhost/node'
        },
        'password': {
            'type': 'string',
            'title': 'Password',
            'description': 'Jabber Password for this chat bot',
        }
    }
    channel = 'isomer-web'

    def __init__(self, *args):
        ConfigurableComponent.__init__(self, "XMPPBOT", *args)
        if self.config.get('password', None) is None:
            self.config.password = std_uuid()
            self.config.save()

        ClientXMPP.__init__(self, self.config.jid, self.config.password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        # Discard SSL Error
        self.add_event_handler("ssl_invalid_cert", self.discard)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

        import ssl
        self.ssl_version = ssl.PROTOCOL_SSLv23

        self.log('Connecting bot to ejabberd')
        self.connect(use_tls=True)
        self.log('Processing ejabberd connection')
        self.process(block=False)

        self.auto_authorize = True
        self.auto_subscribe = True
        self.send_presence(
            pfrom='claptrap@localhost',
            pstatus='Curiouser and curiouser!',
            pshow='xa')

        self.fireEvent(cli_register_event('test_xmpp_send', cli_test_xmpp_send))
        self.log("Started")

    @handler('cli_test_xmpp_send')
    def cli_test_xmpp_send(self, *args):
        """Tests XMPP message sending"""

        self.log('Testing XMPP message sending')
        self.fireEvent(send_xmpp_message('riot', 'Testing', 'This is a test message'))

    def discard(self, event):
        """Ignore SSL errors on localhost"""
        return

    def session_start(self, event):
        """XMPP has been connected, get things rolling"""

        self.log('Jabber session started')
        self.send_presence()
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def message(self, msg):
        """The bot received a direct message"""

        self.log('Message received:', msg['body'], pretty=True)

        if msg['type'] in ('chat', 'normal'):
            body = str(msg['body'])
            if body.startswith('/'):
                cmd, arg_string = body.split(' ', maxsplit=1)
                cmd = cmd.lstrip('/')

                if arg_string:
                    args = arg_string.split(' ')
                else:
                    args = None

                self.log('XMPP remote command received:', cmd, args)
                return
            else:
                if True:
                    msg.reply("Sorry, I did not understand that:\n%s" % body).send()

    def send_xmpp_message(self, event):
        """Transmit a message to a user"""

        self.log('Transmitting XMPP message', lvl=debug)
        msg = Message()
        msg['type'] = event.msg_type
        msg['to'] = '%s@localhost' % event.username
        msg['from'] = self.config.jid
        msg['body'] = event.body
        msg['subject'] = event.subject
        self.send(msg)

    def stopped(self, event, source):
        """Stop the XMPP connection"""

        self.log('Disconnecting XMPP bot')
        self.disconnect()
