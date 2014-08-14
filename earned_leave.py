from osv import osv
from osv import fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import date
from datetime import datetime
import time
import os
from datetime import timedelta

class earned_leave(osv.osv):
    
    _name = 'earned.leave'
    
    def getdatas(self, cr, uid, ids, context=None):
        def was_on_leave(employee_id, datetime_day, context=None):
            res = False
            day = datetime_day.strftime("%Y-%m-%d")
            holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
            if holiday_ids:
                res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
            return res
        dicto = {}
        list_send = []
        number_list = []
        number = 0
        wasim = 0.0
        jerrymon = 0.0
        worked = 0
        for rec in self.browse(cr, uid, ids, context=context):
            leaves = {}
            emp_id = rec.employee_id.id
            date_from = rec.date_from   
            date_to = rec.date_to
            day_from = datetime.strptime(date_from,"%Y-%m-%d")
            day_to = datetime.strptime(date_to,"%Y-%m-%d")
            nb_of_days = (day_to - day_from).days + 1
            search_condition = [('employee_id', '=', emp_id)]
            search_ids = self.pool.get('hr.contract').search(cr, uid, search_condition, context=context)
            contract = self.pool.get('hr.contract').browse(cr, uid, search_ids, context=context)[0]
            line_ids = [line.id for line in rec.leave_id]
            self.pool.get('earned.leave.line').unlink(cr, uid, line_ids, context=context)
            for day in range(0, nb_of_days):
                working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract.working_hours, day_from + timedelta(days=day), context)
                if working_hours_on_day:
                    #the employee had to work
                    leave_type = was_on_leave(emp_id, day_from + timedelta(days=day), context=context)
                    if leave_type:   # leave detected
                        if leave_type != "Second Saturday":
                            list_send.append((0,0,{'date':day_from + timedelta(days=day),'state':leave_type}))
                            if number >= 11.0:
                                number_list.append(number)
                            number = 0
                    else:
                        list_send.append((0,0,{'date':day_from + timedelta(days=day),'state':"Present"}))
                        number += 1
                        worked += 1
                else:
                    list_send.append((0,0,{'date':day_from + timedelta(days=day),'state':"Sunday"})) 
                    number += 1 
                    worked += 1
            for wasim in number_list:
                if wasim >= 11:
                    jerrymon += wasim / 11.0
            if number >= 11.0:
                jerrymon += number / 11.0    
            self.write(cr, uid, ids, {'leave_id':list_send,'number':jerrymon,'total_days':nb_of_days,'total_worked':worked})
        #return [dicto]
 
    
    _columns = {
                'employee_id':fields.many2one('hr.employee','Employee',ondelete='set null',readonly=False),
                'date_from':fields.date('date_from:',readonly=False),
                'date_to':fields.date('date_to:',readonly=False),
                'leave_id':fields.one2many('earned.leave.line','line_id'),
                'number':fields.float('Leaves Earned',readonly=True),
                'total_days':fields.float('Total Days',readonly=True),
                'total_worked':fields.float('Total Worked Days',readonly=True)
                }
earned_leave()

class earned_leave_line(osv.osv):
    
    _name = 'earned.leave.line'
    _columns = {
                'date':fields.date('Date',readonly=True),
                'state':fields.char('State',readonly=True),
                'line_id':fields.many2one('earned.leave','Line',ondelete='set null',readonly=False),
                
                
                }
earned_leave_line()