odoo.define('pos_multi_session.CrossTab', function (require) {
    "use strict";

    var CrossTabBus = require('bus.CrossTab');


    CrossTabBus.include({
        _heartbeat: function () {
            var now = new Date().getTime();
            var heartbeatValue = parseInt(this._callLocalStorage('getItem', 'heartbeat', 0));
            var peers = this._callLocalStorage('getItem', 'peers', {});

            if ((heartbeatValue + this.HEARTBEAT_OUT_OF_DATE_PERIOD) < now) {
                // Heartbeat is out of date. Electing new master
                this._startElection();
                heartbeatValue = parseInt(this._callLocalStorage('getItem', 'heartbeat', 0));
            }

            if (this._isMasterTab) {
                //walk through all peers and kill old
                var cleanedPeers = {};
                for (var peerName in peers) {
                    if (peers[peerName] + this.HEARTBEAT_KILL_OLD_PERIOD > now) {
                        cleanedPeers[peerName] = peers[peerName];
                    }
                }

                if (heartbeatValue !== this.lastHeartbeat) {
                    // someone else is also master...
                    // it should not happen, except in some race condition situation.
                    console.log("Overwriting: Someone else is also master")
                }
                this.lastHeartbeat = now;
                this._callLocalStorage('setItem', 'heartbeat', now);
                this._callLocalStorage('setItem', 'peers', cleanedPeers);
            } else {
                //update own heartbeat
                peers[this._id] = now;
                this._callLocalStorage('setItem', 'peers', peers);
            }

            // Write lastPresence in local storage if it has been updated since last heartbeat
            var hbPeriod = this._isMasterTab ? this.MASTER_TAB_HEARTBEAT_PERIOD : this.TAB_HEARTBEAT_PERIOD;
            if (this._lastPresenceTime + hbPeriod > now) {
                this._callLocalStorage('setItem', 'lastPresence', this._lastPresenceTime);
            }

            this._heartbeatTimeout = setTimeout(this._heartbeat.bind(this), hbPeriod);
        },
    });
});
