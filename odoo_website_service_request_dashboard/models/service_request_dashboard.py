# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import calendar
from odoo import api, models


class requestHelpdesk(models.Model):
    """ Inherited class to get help desk request details...."""
    _inherit = 'service.request'

    @api.model
    def check_user_group(self):
        """Checking user group"""
        user = self.env.user
        if user.has_group('base.group_user'):
            return True
        return False

    @api.model
    def get_requests_count(self):
        """ Function To Get The request Count"""
        request_details = self.env['service.request'].search([])
        request_data = []
        for request in request_details:
            request_data.append({
                'request_name': request.name,
                'customer_name': request.customer_id.name,
                'subject': request.subject,
                'priority': request.priority,
                'assigned_to': request.assigned_user_id.name,
                'assigned_image': request.assigned_user_id.image_1920,
            })
        requests_new_count = self.env['service.request'].search_count(
            [('stage_id.name', 'in', ['Inbox', 'Draft'])])
        requests_in_progress_count = self.env['service.request'].search_count(
            [('stage_id.name', '=', 'In Progress')])
        requests_closed_count = self.env['service.request'].search_count(
            [('stage_id.name', '=', 'Done')])
        very_low_count = self.env['service.request'].search_count([
            ('priority', '=', '0')])
        very_low_count1 = very_low_count * 10
        low_count = self.env['service.request'].search_count([
            ('priority', '=', '1')])
        low_count1 = low_count * 10
        normal_count = self.env['service.request'].search_count([
            ('priority', '=', '2')])
        normal_count1 = normal_count * 10
        high_count = self.env['service.request'].search_count([
            ('priority', '=', '3')])
        high_count1 = high_count * 10
        very_high_count = self.env['service.request'].search_count([
            ('priority', '=', '4')])
        very_high_count1 = very_high_count * 10
        response = self.env['service.request'].search_count([
            ('review', '!=', None)])
        teams_count = self.env['team.servicerequest'].search_count([])
        requests = self.env['service.request'].search(
            [('stage_id.name', 'in', ['Inbox', 'Draft'])])
        p_requests = []
        for request in requests:
            p_requests.append(request.name)
        values = {
            'inbox_count': requests_new_count,
            'progress_count': requests_in_progress_count,
            'done_count': requests_closed_count,
            'team_count': teams_count,
            'p_requests': p_requests,
            'very_low_count1': very_low_count1,
            'low_count1': low_count1,
            'normal_count1': normal_count1,
            'high_count1': high_count1,
            'very_high_count1': very_high_count1,
            'response': response,
            'request_details': request_data,
        }
        return values

    @api.model
    def get_requests_view(self):
        """ Function To Get The request View"""
        requests_new_count = self.env['service.request'].search_count(
            [('stage_id.name', 'in', ['Inbox', 'Draft'])])
        requests_in_progress_count = self.env['service.request'].search_count(
            [('stage_id.name', '=', 'In Progress')])
        requests_closed_count = self.env['service.request'].search_count(
            [('stage_id.name', '=', 'Done')])
        teams_count = self.env['team.servicerequest'].search_count([])
        requests_new = self.env['service.request'].search(
            [('stage_id.name', 'in', ['Inbox', 'Draft'])])
        requests_in_progress = self.env['service.request'].search(
            [('stage_id.name', '=', 'In Progress')])
        requests_closed = self.env['service.request'].search(
            [('stage_id.name', '=', 'Done')])
        teams = self.env['team.servicerequest'].search([])
        new_list = []
        progress_list = []
        done_list = []
        teams_list = []
        for new in requests_new:
            new_list.append(str(new.name) + ' : ' + str(new.subject))
        for progress in requests_in_progress:
            progress_list.append(
                str(progress.name) + ' : ' + str(progress.subject))
        for done in requests_closed:
            done_list.append(str(done.name) + ' : ' + str(done.subject))
        for team in teams:
            teams_list.append(team.name)
        requests = self.env['service.request'].search(
            [('stage_id.name', 'in', ['Inbox', 'Draft'])])
        p_requests = []
        for request in requests:
            p_requests.append(request.name)
        values = {
            'inbox_count': requests_new_count,
            'progress_count': requests_in_progress_count,
            'done_count': requests_closed_count,
            'team_count': teams_count,
            'new_tkts': new_list,
            'progress': progress_list,
            'done': done_list,
            'teams': teams_list,
            'p_requests': p_requests
        }
        return values

    @api.model
    def get_request_month_pie(self):
        """For pie chart"""
        month_count = []
        month_value = []
        requests = self.env['service.request'].search([])
        for rec in requests:
            month = rec.create_date.month
            if month not in month_value:
                month_value.append(month)
            month_count.append(month)
        month_val = []
        for index in range(len(month_value)):
            value = month_count.count(month_value[index])
            month_name = calendar.month_name[month_value[index]]
            month_val.append({'label': month_name, 'value': value})
        name = []
        for record in month_val:
            name.append(record.get('label'))
        count = []
        for record in month_val:
            count.append(record.get('value'))
        month = [count, name]
        return month

    @api.model
    def get_team_request_count_pie(self):
        """For bar chart"""
        request_count = []
        team_list = []
        requests = self.env['service.request'].search([])
        for rec in requests:
            if rec.team_id:
                team = rec.team_id.name
                if team not in team_list:
                    team_list.append(team)
                request_count.append(team)
        team_val = []
        for index in range(len(team_list)):
            value = request_count.count(team_list[index])
            team_name = team_list[index]
            team_val.append({'label': team_name, 'value': value})
        name = []
        for record in team_val:
            name.append(record.get('label'))
        count = []
        for record in team_val:
            count.append(record.get('value'))
        team = [count, name]
        return team
