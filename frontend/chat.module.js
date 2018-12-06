/*
 * #!/usr/bin/env python
 * # -*- coding: UTF-8 -*-
 *
 * __license__ = """
 * Isomer Application Framework
 * ============================
 * Copyright (C) 2011- 2018 riot <riot@c-base.org> and others.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * """
 */

//import './chat/chat.scss';

import angular from 'angular';
import uirouter from 'angular-ui-router';

import { routing } from './chat.config.js';

import './chatxmpp/chat.scss';

import chatserviceclass from './chatxmpp/chatservice.js';
import chatcomponent from './chatxmpp/chatcomponent.js';
import chatbutton from './chatxmpp/chatbutton';

import template from './chatxmpp/chat.tpl.html';

export default angular
    .module('main.app.chatxmpp', [uirouter])
    .config(routing)
//    .service('chatservicexmpp', chatserviceclass)
    .component('chatxmpp', {controller: chatcomponent, template: template})
//    .directive('chatbuttonxmpp', chatbutton)
//    .run(function (chatservicexmpp) {})
    .name;
