/** @odoo-module **/
import { registry } from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { onMounted, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
/** Initializes the ServicerequestDashboard component**/
class ServicerequestDashboard extends Component{
    /**Set up function**/
    setup() {
        super.setup();
        var self = this;
        this.ref = useRef("ServicerequestDashboard")
        this.rpc = useService("rpc");
        this.actionService = useService("action");
        onMounted(this.onMounted);
    }
    /**Function for onMounted**/
    onMounted(){
        this.render_dashboards();
        this.render_graphs();
    }
    /**To render the charts**/
    render_graphs() {
        var self = this;
        self.render_requests_month_graph();
        self.render_team_request_count_graph();
    }
    /**Doughnut chart: request STATUS**/
    render_requests_month_graph() {
        var self = this;
        var ctx = this.ref.el.querySelector('#request_month')
        jsonrpc('/web/dataset/call_kw/service.request/get_requests_count', {
            model: "service.request",
            method: "get_requests_view",
             args: [],
            kwargs: {},
        }).then(function (values) {
            var data = {
                labels: ['New', 'In Progress', 'Solved'],
                datasets: [{
                    data: [values.inbox_count, values.progress_count, values.done_count],
                    backgroundColor: [
                        "#665191",
                        "#ff7c43",
                        "#ffa600"
                    ],
                    borderColor: [
                        "#003f5c",
                        "#2f4b7c",
                        "#f95d6a"
                    ],
                    borderWidth: 1
                }]
            };
            /** Options **/
            var options = {
                responsive: true,
                title: false,
                legend: {
                    display: true,
                    position: "right",
                    labels: {
                        fontColor: "#333",
                        fontSize: 16
                    }
                },
                scales: {
                    yAxes: [{
                        gridLines: {
                            color: "rgba(0, 0, 0, 0)",
                            display: false,
                        },
                        ticks: {
                            min: 0,
                            display: false,
                        }
                    }]
                }
            };
            /** Create Chart class object **/
            var chart = new Chart(ctx, {
                type: "doughnut",
                data: data,
                options: options
            });
        });
    }
    /** Bar chart: Team - requests Count Ratio **/
    render_team_request_count_graph() {
        var self = this
        var ctx = this.ref.el.querySelector('.team_request_count');
        jsonrpc('/web/dataset/call_kw/service.request/get_requests_count', {
            model: "service.request",
            method: "get_team_request_count_pie",
             args: [],
            kwargs: {},
        }).then(function (arrays) {
            var data = {
                labels: arrays[1],
                datasets: [{
                    label: "",
                    data: arrays[0],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, rpc102, 255, 0.2)',
                        'rgba(201, 203, 207, 0.2)'
                    ],
                    borderColor: ['rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'
                    ],
                    borderWidth: 1
                },]
            };
            /** Options **/
            var options = {
                responsive: true,
                title: false,
                maintainAspectRatio: true,
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        display: true,
                        ticks: {
                            beginAtZero: true,
                            steps: 10,
                            stepValue: 5,
                            // max: 100
                        }
                    }]
                }
            };
            /** Create Chart class object **/
            var chart = new Chart(ctx, {
                type: "bar",
                data: data,
                options: options
            });
        });
    }
    /** List view of requests in dashboard **/
    render_dashboards() {
        var self = this;
        jsonrpc('/web/dataset/call_kw/service.request/get_requests_count', {
            model: 'service.request',
            method: 'get_requests_count',
            args: [],
            kwargs: {},
        }).then(function(result) {
            var inbox_count_span = document.createElement("span");
            inbox_count_span.textContent = result.inbox_count
            self.ref.el.querySelector('#inbox_count').appendChild(inbox_count_span);
            var progress_count_span = document.createElement("span");
            progress_count_span.textContent = result.progress_count
            self.ref.el.querySelector('#inprogress_count').appendChild(progress_count_span);
            var done_count_span = document.createElement("span");
            done_count_span.textContent = result.done_count
            self.ref.el.querySelector('#done_count').appendChild(done_count_span);
            var team_count_span = document.createElement("span");
            team_count_span.textContent = result.team_count
            self.ref.el.querySelector('#team_count').appendChild(team_count_span);
            var priorityCounts = {
                very_low: result.very_low_count1,
                low: result.low_count1,
                normal: result.normal_count1,
                high: result.high_count1,
                very_high : result.very_high_count1
            };
            /**Loop through the priorities and create progress bars**/
            for (var priority in priorityCounts) {
                var progressBarWidth = priorityCounts[priority] + "%";
                var progressBar = $("<div class='progress-bar'></div>").css("width", progressBarWidth);
                var progressBarContainer = $("<div class='progress'></div>").append(progressBar);
                var progressValue = $("<div class='progress-value'></div>").text(priorityCounts[priority] + "%");
                // Append the progress bar container to elements with class corresponding to the priority
                $("." + priority + "_count").append(progressBarContainer);
                $("." + priority + "_count .progress-value").append(progressValue);
            }
            var tbody = $(".request-details");
            var request_details = result.request_details;
            for (var i = 0; i < request_details.length; i++) {
                 /** Get the current request object **/
                var request = request_details[i];
                var row = $("<tr></tr>");
                /** Assuming you have the Base64-encoded image data in a
                variable called request.assigned_image **/
                var base64Image = request.assigned_image;
                var assignedUserCell = $("<td class='td'></td>");
                var imgElement = $("<img>");
                /** Set the image source **/
                imgElement.attr("src", "data:image/png;base64," + base64Image);
                /** Set an alt attribute for accessibility **/
                imgElement.attr("alt", "User Image");
                /** Add the 'oe-avatar' class to the <img> element **/
                imgElement.addClass("user-image");
                /** Append the img element to the assignedUserCell **/
                assignedUserCell.append(imgElement);
                /** Append the assignedUserCell to the row **/
                row.append(assignedUserCell);
                row.append("<td class='td'>" + request.customer_name + "</td>");
                row.append("<td class='td'>" + request.request_name + "</td>");
                row.append(assignedUserCell);
                row.append("<td>" + request.assigned_to + "</td>");
                row.append("<td>" + request.subject + "</td>");
                row.append("<td>" + request.priority + "</td>");
                tbody.append(row);
            }
            $(".response").append(result.response);
            self.rpc('/help/requests', {}).then((values) => {
                $('.pending_requests').append(values);
            });
        });
    }
    /** To show new requests **/
    requests_inbox(ev) {
        var self = this;
        ev.stopPropagation();
        ev.preventDefault();
        self.actionService.doAction({
            name: _t("Inbox"),
            type: 'ir.actions.act_window',
            res_model: 'service.request',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['stage_id.name', 'in', ['Inbox', 'Draft']]],
            context: {default_stage_id_name: 'Draft'},
            target: 'current'
        });
    }
    /** To show in progress requests **/
    requests_inprogress(ev) {
        var self = this;
        ev.stopPropagation();
        ev.preventDefault();
        self.actionService.doAction({
            name: _t("In Progress"),
            type: 'ir.actions.act_window',
            res_model: 'service.request',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['stage_id.name', '=', 'In Progress']],
            context: {create: false},
            target: 'current'
        });
    }
    /** To show done requests **/
    requests_done(ev) {
        var self = this;
        ev.stopPropagation();
        ev.preventDefault();
        self.actionService.doAction({
            name: _t("Done"),
            type: 'ir.actions.act_window',
            res_model: 'service.request',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            domain: [['stage_id.name', '=', 'Done']],
            context: {create: false},
            target: 'current'
        });
    }
    /** To show the helpdesk teams**/
    helpdesk_teams(ev) {
        var self = this;
        ev.stopPropagation();
        ev.preventDefault();
        self.actionService.doAction({
            name: _t("Teams"),
            type: 'ir.actions.act_window',
            res_model: 'team.servicerequest',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current'
        });
    }
}
ServicerequestDashboard.template = 'ServicerequestDashboard'
registry.category("actions").add("service_request_dashboard", ServicerequestDashboard)
