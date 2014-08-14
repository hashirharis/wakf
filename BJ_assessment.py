from osv import osv
from osv import fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import datetime
from datetime import date
import time


class bj_assessment(osv.osv):
    _name = 'bj.assessment'
       
    def open_popup(self, cr, uid, ids, context=None):
        """Method is used to show form view in new windows"""
        this = self.browse(cr, uid, ids, context=None)
        return this
    
    def on_change_confirm_bj(self, cr, uid, ids, context=None):
        invoice_ids = []
        for key in self.browse(cr,uid,ids,context=context):
            reg_no = key.reg_no
            output = key.wakf_id.id
            bj_line_id = key.bj_line_id
            for bj_line in key.bj_line_id:
                product_id = 3
                name = "BJ"
                quantity = 1
                price_subtotal = bj_line.net_income1
                price_unit = bj_line.net_income1
                new_amount = bj_line.net_income1
                acc_year = bj_line.account_year_line.id
                invoice_ids.append((0,0,{'product_id':product_id,'name':name,'quantity':quantity,'price_subtotal':price_subtotal,'price_unit':price_unit,'new_amount':new_amount}))
                self.pool.get('account.invoice').create(cr,uid,{'registration_no':reg_no,'account_id':1,'journal_id':'1','partner_id':output,'invoice_line':invoice_ids,'assess_year_saleorder':acc_year,'assessment_type':'bj'})
                invoice_ids = []
            self.write(cr, uid, ids, {'state':'approved'})
        return False
    
    def on_change_wakf_regno_to_name_new_assess(self, cr, uid, ids, reg_no, context=None):
        values = {}
        invoice_lines1 = []
        id_res_partner = self.pool.get('res.partner')
        output = False
        if reg_no:
            search_condition = [('wakf_reg_no', '=', reg_no)]
            search_ids = id_res_partner.search(cr, uid, search_condition, context=context)
            similar_objs = id_res_partner.browse(cr, uid, search_ids, context=context)
            if similar_objs:
                output = id_res_partner.browse(cr, uid, search_ids, context=context)[0].id
                values = {'wakf_id': output,}
            else:
                invoice_lines1.append((2,0))
                values ={'wakf_id': False,
                         'bj_line_id':invoice_lines1
                         } 
                return {'warning': {
                    'title': _('Warning!'),
                    'message':  _('No Wakf registered with specified Register No'),},'value':values,
                }
        bj_slab_id = self.pool.get('bj.slab')
        search_condition=[('approved','=',True)]
        key_search = bj_slab_id.search(cr,uid,search_condition)
        key_browse = bj_slab_id.browse(cr,uid,key_search)[0]
        total_lines = []
        for lock in key_browse.slab_id:
            total_lines.append(lock.sl_no)
        lines = total_lines[-1]
        #for lock1 in key_browse.slab_id:
            #to_net_amnt[0] = lock1.bj_amount_end
            #count = count-1
        invoice_id = self.pool.get('account.invoice')
        registration_id = self.pool.get('res.partner')
        search_condition = [('wakf_reg_no', '=', reg_no)]
        search_ids1 = registration_id.search(cr, uid, search_condition)
        date_year = False
        acc_year_today = False
        balance_year =False
        last_net_amount = 0
        today = date.today()
        month_today = today.month
        if month_today <= 3:
            acc_year_today = '%d-%d'%(today.year-1,today.year)   ##   finding acc year from today
            year_today = today.year                              ##
        if month_today >= 4:
            acc_year_today = '%d-%d'%(today.year,today.year+1)   ##   finding acc year from today
            year_today = today.year +1                           ##
        if search_ids1:                    
            date_registration = registration_id.browse(cr,uid,search_ids1)[0].wakf_registration_date
            if date_registration:                              # checking registration date of wakf
                date_year = (datetime.strptime(date_registration, '%Y-%m-%d')).year
                date_month = (datetime.strptime(date_registration, '%Y-%m-%d')).month
                if date_month <= 3:
                    date_year = '%d-%d'%(date_year-1,date_year)
                    year_registration = (datetime.strptime(date_registration, '%Y-%m-%d')).year-1
                if date_month >= 4:
                    date_year = '%d-%d'%(date_year,date_year+1)
                    year_registration = (datetime.strptime(date_registration, '%Y-%m-%d')).year
            else:                                            # No last paid, ie first Assessment
                invoice_lines1.append((2,0))
                values = {'bj_line_id':invoice_lines1,
                      'wakf_id': False,
                      'year_pending':0,
                      'year_registration':False,
                      'last_paid':False,
                      'last_paid_amount':False,
                      'for_year': False,
                      'net_income':0, 
                      'net_income_assess':0,
                      'contri_amount':0,
                      }
                warning_of = {
                    'title': _('Warning!'),
                    'message':  _('First Set Registration Date for Wakf'),}
                return {'value' : values,'warning':warning_of}
            
        if date_year:
            search_condition = [('name', '=', date_year)]
            search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition, context=context)
            acc_year_to_compare = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids, context=context)[0].id
            search_condition = [('registration_no', '=', reg_no) , ('state','=',"paid"),]
            search_ids3 = self.pool.get('account.invoice').search(cr, uid, search_condition)
            if search_ids3:
                dummy = 0
                net = 0
                for loop in invoice_id.browse(cr,uid,search_ids3):    
                    search_condition = [('id', '=', loop.assess_year_saleorder.id)]
                    search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition, context=context)
                    acc_year_last1 = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids, context=context)[0].name
                    vals = int(acc_year_last1[5:9])
                    if dummy <= vals:
                        dummy = vals
                        net =loop.net_amount
                        last_payment_date=loop.date_invoice
                        last_payment = loop.amount_total
                        for_year = loop.assess_year_saleorder.id
                year_change1 = '%d-%d'%(dummy-1,dummy)
                year_last = dummy
                year_last_copy = year_last              
                #year_last = int(year_last)                  ### We got Last paid Account Year !!  
                last_net_amount = net
                last_net_amount_copy = net
                if year_last >=1:
                    balance_year = int(year_today)-year_last                

            else:
                year_last = year_registration
                balance_year = int(year_today)-year_registration
                last_net_amount = 5000
                last_payment_date=0
                last_payment=0
                for_year=0
            if balance_year != 0:                          # last paid is detected
                for repeat in range(balance_year):
                    for harry in key_browse.slab_id:
                        if harry.bj_amount_start<last_net_amount<harry.bj_amount_end:  #### checking BJ slab ###
                            percentage = harry.percentage
                            bj_amount = last_net_amount + last_net_amount * percentage / 100  ### Returning BJ amount with increment
                            year_change = '%s-%s'%(year_last,year_last+1)
                            search_condition = [('name', '=', year_change)]
                            search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition, context=context)
                            acc_year = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids, context=context)[0].id
                            invoice_lines1.append((0,0,{'reg_no':reg_no,'account_year_line':acc_year,'assessment_year_line':acc_year,'assess_amount':last_net_amount,'net_income1':bj_amount,'contri_amount1':bj_amount*7/100}))
                            year_last = year_last+1 
                            last_net_amount = last_net_amount + bj_amount*7/100                  
                    values = {'bj_line_id':invoice_lines1,
                              'year_pending':balance_year,
                              'year_registration':date_registration,
                              'last_paid':last_payment_date,
                              'last_paid_amount':last_payment,
                              'for_year': for_year,
                              'wakf_id': output,
                              'net_income':0, 
                              'net_income_assess':0,
                              'contri_amount':0,
                                      }
                    
            else:                                            # No last paid, ie first Assessment
                invoice_lines1.append((2,0))
                values = {'bj_line_id':invoice_lines1,
                      'wakf_id': False,
                      'year_pending':0,
                      'year_registration':False,
                      'last_paid':False,
                      'last_paid_amount':False,
                      'for_year': False,
                      'net_income':0, 
                      'net_income_assess':0,
                      'contri_amount':0,
                      }
                warning_of = {
                    'title': _('Warning!'),
                    'message':  _('Assessments are upto-date for this wakf'),}
                return {'value' : values,'warning':warning_of}
                    
        else:
            invoice_lines1.append((2,0))
            values = {'bj_line_id':invoice_lines1,
                      'wakf_id': False,
                      'year_pending':0,
                      'year_registration':False,
                      'last_paid':False,
                      'last_paid_amount':False,
                      'for_year': False,
                      'net_income':0, 
                      'net_income_assess':0,
                      'contri_amount':0,
                      }
            
            return {'value' : values}
        return {'value' : values}
    def on_change_all_wakf_bj(self, cr, uid, ids,all_wakf):
        invoice_lines1 = []
        values = {}
        date_year = False
        acc_year_today = False
        balance_year =False
        last_payment_date = False
        date_registration = False
        for_year = False
        output = False
        last_payment = False
        last_net_amount = 0
        id_res_partner = self.pool.get('res.partner')
        search_ids = id_res_partner.search(cr,uid,[])
        if all_wakf:
            for loop in id_res_partner.browse(cr,uid,search_ids):
                reg_no = loop.wakf_reg_no
                if reg_no:
                    search_condition = [('wakf_reg_no', '=', reg_no)]
                    search_ids = id_res_partner.search(cr, uid, search_condition)
                    similar_objs = id_res_partner.browse(cr, uid, search_ids)
                    if similar_objs:
                        output = id_res_partner.browse(cr, uid, search_ids)[0].id
                        values = {'wakf_id': output,}
                    
                    bj_slab_id = self.pool.get('bj.slab')
                    search_condition=[('approved','=',True)]
                    key_search = bj_slab_id.search(cr,uid,search_condition)
                    key_browse = bj_slab_id.browse(cr,uid,key_search)[0]
                    total_lines = []
                    for lock in key_browse.slab_id:
                        total_lines.append(lock.sl_no)
                        lines = total_lines[-1]
                    #for lock1 in key_browse.slab_id:
                        #to_net_amnt[0] = lock1.bj_amount_end
                        #count = count-1
                    invoice_id = self.pool.get('account.invoice')
                    registration_id = self.pool.get('res.partner')
                    search_condition = [('wakf_reg_no', '=', reg_no)]
                    search_ids1 = registration_id.search(cr, uid, search_condition)
                    today = date.today()
                    month_today = today.month
                    if month_today <= 3:
                        acc_year_today = '%d-%d'%(today.year-1,today.year)   ##   finding acc year from today
                        year_today = today.year                              ##
                    if month_today >= 4:
                        acc_year_today = '%d-%d'%(today.year,today.year+1)   ##   finding acc year from today
                        year_today = today.year +1                           ##
                    if search_ids1:                    
                        date_registration = registration_id.browse(cr,uid,search_ids1)[0].wakf_registration_date
                        if date_registration:                              # checking registration date of wakf
                            date_year = (datetime.strptime(date_registration, '%Y-%m-%d')).year
                            date_month = (datetime.strptime(date_registration, '%Y-%m-%d')).month
                            if date_month <= 3:
                                date_year = '%d-%d'%(date_year-1,date_year)
                                year_registration = (datetime.strptime(date_registration, '%Y-%m-%d')).year-1
                            if date_month >= 4:
                                date_year = '%d-%d'%(date_year,date_year+1)
                                year_registration = (datetime.strptime(date_registration, '%Y-%m-%d')).year
                        
                        if date_year and date_registration:
                            search_condition = [('name', '=', date_year)]
                            search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition)
                            acc_year_to_compare = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids)[0].id
                            search_condition = [('registration_no', '=', reg_no) , ('state','=',"paid")]
                            search_ids3 = self.pool.get('account.invoice').search(cr, uid, search_condition)
                            if search_ids3:
                                dummy = 0
                                net = 0
                                for loop in invoice_id.browse(cr,uid,search_ids3):
                                    if dummy <= loop.assess_year_saleorder.id:
                                        dummy = loop.assess_year_saleorder.id
                                        net =loop.net_amount
                                        last_payment_date=loop.date_invoice
                                        last_payment = loop.amount_total
                                        for_year = loop.assess_year_saleorder.id
                                search_condition = [('id', '=', dummy)]
                                search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition)
                                acc_year_last = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids)[0].name
                                year_last = acc_year_last[5:9]
                                year_last_copy = year_last              
                                year_last = int(year_last)                  ### We got Last paid Account Year !!  
                                last_net_amount = net
                                last_net_amount_copy = net
                                if year_last >=1:
                                    balance_year = int(year_today)-year_last                
                
                            else:
                                year_last = year_registration
                                balance_year = int(year_today)-year_registration
                                last_net_amount = 5000
                            if balance_year != 0 and year_last:                          # last paid is detected
                                for repeat in range(balance_year):
                                    for harry in key_browse.slab_id:
                                        if harry.bj_amount_start<last_net_amount<harry.bj_amount_end:  #### checking BJ slab ###
                                            percentage = harry.percentage
                                            bj_amount = last_net_amount + last_net_amount * percentage / 100  ### Returning BJ amount with increment
                                            year_change = '%s-%s'%(year_last,year_last+1)
                                            search_condition = [('name', '=', year_change)]
                                            search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition)
                                            acc_year = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids)[0].id
                                            invoice_lines1.append((0,0,{'reg_no':reg_no,'account_year_line':acc_year,'assessment_year_line':acc_year,'assess_amount':last_net_amount,'net_income1':bj_amount,'contri_amount1':bj_amount*7/100}))
                                            year_last = year_last+1 
                                            last_net_amount = last_net_amount + bj_amount*7/100                                      
                                last_net_amount = 0
                                year_change = False
                                year_last = False
                        
            return {'value' : {'bj_line_id':invoice_lines1,
                                              'year_pending':False,
                                              'year_registration':False,
                                              'last_paid':False,
                                              'last_paid_amount':False,
                                              'for_year': False,
                                              'wakf_id': False,
                                              'net_income':False, 
                                              'net_income_assess':False,
                                              'contri_amount':False,
                                                      }}
        else:
            return {'value' : {'bj_line_id':False,
                                              'year_pending':False,
                                              'year_registration':False,
                                              'last_paid':False,
                                              'last_paid_amount':False,
                                              'for_year': False,
                                              'wakf_id': False,
                                              'net_income':False, 
                                              'net_income_assess':False,
                                              'contri_amount':False,
                                                      }}
    def _total_amount_net_bj(self, cr, uid, ids, field_name, arg, context=None):
        val1 = 0
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
            'total_income' : 0,
            }
            for line in order.bj_line_id:
                val1 += line.net_income1
            res[order.id]['net_income']=val1          
        return res
    def _total_amount_net_Assess(self, cr, uid, ids, field_name, arg, context=None):
        val1 = 0
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
            'total_income' : 0,
            }
            for line in order.bj_line_id:
                val1 += line.assess_amount
            res[order.id]['net_income_assess']=val1          
        return res
    def _total_amount_contribution_bj(self, cr, uid, ids, field_name, arg, context=None):
        val1 = 0
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
            'total_income' : 0,
            }
            for line in order.bj_line_id:
                val1 += line.contri_amount1
            res[order.id]['contri_amount']=val1          
        return res
    def _deflt_ass_year(self, cr, uid, ids, context=None):
        res ={}
        today = date.today()
        month_of = today.month
        if month_of <= 3:
            date_of = '%d-%d'%(today.year-1,today.year)
        if month_of >= 4:
            date_of = '%d-%d'%(today.year,today.year+1)
        search_condition = [('name', '=', date_of)]
        search_ids = self.pool.get('account.fiscalyear').search(cr, uid, search_condition, context=context)
        similar_objs = self.pool.get('account.fiscalyear').browse(cr, uid, search_ids, context=context)
        return similar_objs[0].id
   
    def action_approve(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {'state':'created'})
        return True
    
    def showcause(self, cr, uid, ids, context=None):
        acc_year_1 = False
        acc_year = False
        for key in self.browse(cr,uid,ids,context=context):
            reg_no = key.reg_no
            output = key.wakf_id.id
            amount = key.contri_amount
            assessment_year=key.assessment_year.id
            count = 0
            for bj_line in key.bj_line_id:
                if count == 0:
                    acc_year_1 = bj_line.account_year_line.id
                acc_year = bj_line.account_year_line.id
                count += 1          
            self.pool.get('show.cause').create(cr,uid,{'reg_no':reg_no,'assessment_year':assessment_year,'acc_year_from':acc_year_1,'partner_id':output,'acc_year_to':acc_year,'amount':amount})
            self.write(cr, uid, ids, {'state':'showcause'})
        return False

    
    _columns = {
         'reg_no':fields.integer('Registration No:',size=16),
         'wakf_id':fields.many2one('res.partner','Wakf Name'),                 
         'assess_year':fields.char('Assessment Year:',size=16),
         'account_year':fields.date('Account Year'),
         'assessment_year':fields.many2one('account.fiscalyear','Assessment Year',ondelete='set null',readonly=True),
         'year_pending':fields.char('Year Pending:',size=16,readonly=False),
         'year_registration':fields.date('Year of Registration:',readonly=True),
         'last_paid':fields.date('Last Paid on:',readonly=True),
         'last_paid_amount':fields.float('Last Paid Amount:',size=16,readonly=True),
         'for_year':fields.many2one('account.fiscalyear','For account Year',ondelete='set null',readonly=True),
         'net_income_assess':fields.function(_total_amount_net_Assess,multi='sums2',string='Net Income(Assessment)',store=True),
         'net_income':fields.function(_total_amount_net_bj,multi='sums',string='Net Income(BJ)',store=True), 
         'contri_amount':fields.function(_total_amount_contribution_bj,multi='sums1',string='Total Contribution',store=True),
         'bj_line_id':fields.one2many('bj.assessment.line','bj_line'),
         'all_wakf':fields.boolean('Want to see all wakf ?'),
         'user_id':fields.char('user id',size=16),
         'state':fields.selection((('draft','Draft'),('created','BJ Created'), ('approved','BJ Confirmed'),('showcause','ShowCause')),'BJ State',required=False), 
                                          
                }
    _defaults ={
                'assessment_year':_deflt_ass_year,
                'state':'draft',
                'user_id': lambda obj, cr, uid, context: uid,
                }
bj_assessment()

class bj_assessment_line(osv.osv):
    _name = 'bj.assessment.line'
    _columns = {
         'reg_no':fields.char('Register No',size=8),
         'bj_line':fields.many2one('bj.assessment','BJ Line',ondelete='set null',required=False),
         'account_year_line':fields.many2one('account.fiscalyear','Account Year',ondelete='set null'),
         'assessment_year_line':fields.many2one('account.fiscalyear','Assessment Year',ondelete='set null'),
         'assess_amount':fields.float('Assessment Amount',size=16),
         'net_income1':fields.float('BJ Amount',size=16), 
         'contri_amount1':fields.float('Contribution',size=16),
          
                                        
                }
bj_assessment_line()