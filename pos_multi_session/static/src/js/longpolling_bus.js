odoo.define('pos_multi_session.Longpolling', function (require) {
"use strict";

    var Longpolling = require('bus.Longpolling');


    Longpolling.include({
        stopPolling: function () {
            let self = this;
            this._super();
            console.log(
                "MS",
                self.pos_longpolling.pos.config.name,
                "Bus inactive (_isActive = false)"
            );
        },
    });
});
