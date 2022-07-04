odoo.define('pos_multi_session.CrossTab', function (require) {
"use strict";

    var CrossTabBus = require('bus.CrossTab');


    CrossTabBus.include({
        _heartbeat: function () {
            let self = this;
            let heartbeatValue = parseInt(this._callLocalStorage('getItem', 'heartbeat', 0));

            if (this._isMasterTab) {
                if (heartbeatValue !== this.lastHeartbeat) {
                    console.log(
                        "MS",
                        self.pos_longpolling.pos.config.name,
                        "heartbeatValue (" + heartbeatValue + ") != this.lastHeartbeat (" + this.lastHeartbeat + ")"
                    );
                }
            }
            this._super();
        },
    });
});
