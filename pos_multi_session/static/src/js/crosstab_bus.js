odoo.define('pos_multi_session.CrossTab', function (require) {
"use strict";

    var CrossTabBus = require('bus.CrossTab');


    CrossTabBus.include({
        _heartbeat: function () {
            return;
        },
    });
});
