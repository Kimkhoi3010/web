odoo.define('web_notify.WebClient', function (require) {
"use strict";

var core = require('web.core'),
    WebClient = require('web.WebClient'),
    base_bus = require('bus.bus'),
    Widget = require('web.Widget');


Widget.include({
    do_notify: function(title, message, sticky, options) {
        this.trigger_up('notification', {title: title, message: message, sticky: sticky, options: options});
    },
    do_warn: function(title, message, sticky, options) {
        this.trigger_up('warning', {title: title, message: message, sticky: sticky, options: options});
    },
});


WebClient.include({
    custom_events: _.extend(
        {},
        WebClient.prototype.custom_events,
        {reload_active_view: 'reload_active_view',
         notification: function (e) {
             if(this.notification_manager) {
                 this.notification_manager.notify(e.data.title, e.data.message, e.data.sticky, e.data.options);
             }
         },
         warning: function (e) {
             if(this.notification_manager) {
                 this.notification_manager.warn(e.data.title, e.data.message, e.data.sticky, e.data.options);
             }
         }
        }
    ),
    init: function(parent, client_options){
        this._super(parent, client_options);
    },
    reload_active_view: function(){
        var action_manager = this.action_manager;
        if(!action_manager){
            return;
        }
        var active_view = action_manager.inner_widget.active_view;
        if(active_view) {
            active_view.controller.reload();
        }
    },
    show_application: function() {
        var res = this._super();
        this.start_polling();
        return res
    },
    on_logout: function() {
        var self = this;
        base_bus.bus.off('notification', this, this.bus_notification);
        this._super();
    },
    start_polling: function() {
        this.channel_warning = 'notify_warning_' + this.session.uid;
        this.channel_info = 'notify_info_' + this.session.uid;
        base_bus.bus.add_channel(this.channel_warning);
        base_bus.bus.add_channel(this.channel_info);
        base_bus.bus.on('notification', this, this.bus_notification);
        base_bus.bus.start_polling();
    },
    bus_notification: function(notifications) {
        var self = this;
        _.each(notifications, function (notification) { 
            var channel = notification[0];
            var message = notification[1];
            if (channel === self.channel_warning) {
                self.on_message_warning(message);
            } else if (channel == self.channel_info) {
                self.on_message_info(message);
            }
        });
    },
    on_message_warning: function(message){
        if(this.notification_manager) {
            this.notification_manager.do_warn(message.title, message.message, message.sticky, message);
        }
    },
    on_message_info: function(message){
        if(this.notification_manager) {
            this.notification_manager.do_notify(message.title, message.message, message.sticky, message);
        }
    }
});

});
