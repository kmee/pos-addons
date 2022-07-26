odoo.define('pos_multi_session.gui', function (require) {
    "use strict";

    var gui = require('point_of_sale.gui');

    gui.Gui.include({
        show_saved_screen:  function(order,options) {
            if (!this.current_popup || !this.current_popup.product) {
                this._super.apply(this, arguments);
            }
        },
    });
});
