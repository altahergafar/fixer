/** @odoo-module **/
import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.TT = publicWidget.Widget.extend({
    selector: '#request',
    events: {
         'change #group_select': '_onGroupSelectChange',
        'click #search_request': '_onSubmit',
    },
    //        GroupBy filtering the portal requests
        _onGroupSelectChange: function (ev) {
            var self = this;
            var searchValue = this.$el.find('#group_select').val();
            jsonrpc('/requestgroupby', {
                'search_value': searchValue,
            }).then(function (result) {
                  $('.search_request').html(result);
            });
        },
//        Searching the portal requests
    _onSubmit(ev) {
       var search_value = this.$el.find('#search_box').val();
       jsonrpc('/requestsearch', {
                'search_value': search_value,
            }).then(function(result) {
                $('.search_request').html(result);
            });
    }
})
