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

'use strict';

/**
 * @ngdoc function
 * @name isomerFrontendApp.controller:ChatCtrl
 * @description
 * # ChatCtrl
 * Controller of the isomerFrontendApp
 */

import sidebar from './chatsidebar.tpl.html';
/*
require('jsxc/build/lib/jquery.slimscroll');
require('jsxc/build/lib/jsxc.dep');
import jsxc from 'jsxc/build/jsxc';

require('jsxc/build/css/jsxc.css');

*/
class chatcomponent {
    constructor(user, rootscope, scope, $aside) {

        this.user = user;
        this.rootscope = rootscope;
        this.scope = scope;

        jsxc.init({
            loginForm: {
                form: '#form',
                jid: '#username',
                pass: '#password'
            },
            logoutElement: $('#logout'),
            root: '/jsxc.example/jsxc',
            xmpp: {
                url: 'http://localhost:5280/http-bind/',
                domain: 'localhost',
                resource: 'example'
            }
        });
        $(document).on('ready.roster.jsxc', function () {
            $('#content').css('right', $('#jsxc_roster').outerWidth() + parseFloat($('#jsxc_roster').css('right')));
        });
        $(document).on('toggle.roster.jsxc', function (event, state, duration) {
            $('#content').animate({
                right: ((state === 'shown') ? $('#jsxc_roster').outerWidth() : 0) + 'px'
            }, duration);
        });

        console.log('Chat component started.');
    }

}

chatcomponent.$inject = ['user', '$rootScope', '$scope', '$aside'];

export default chatcomponent;
