from osv import osv
from osv import fields
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import pooler
from tools.translate import _
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import decimal_precision as dp
import netsvc

class Revenue_Recovery(osv.osv):
    
    _name = 'revenue.recovery'
    _columns = {
                'reg_no':fields.integer('Register No:', size=16, required=False),
                'assess_year':fields.many2one('account.fiscalyear','Assessment Year',ondelete='set null',readonly=False),
                'wakf_district':fields.many2one('wakf.district','District',ondelete='set null',readonly=False),
                'recover_amount':fields.float('Recover Amount', size=16, required=False),
                'collection_charge':fields.float('Collection Charge', size=16, required=False),
                'grand_total':fields.float('Grand Total', size=16, required=False),
                'certified_date':fields.date('Certified Date', required=False),
                'approve':fields.boolean('Approve', required=False),
                'certified_date':fields.date('Certified Date', required=False),
                'file_no':fields.char('File No:', size=16, required=False),
                'requisiton_no':fields.char('Requisition No:', size=16, required=False),
                'certificate_no':fields.char('Certificate No:', size=16, required=False),
                'send':fields.boolean('Send', required=False),
                'rr_execute':fields.boolean('RR Execute', required=False),
                'cancel':fields.boolean('Cancel', required=False),
                'cancel_date':fields.date('Cancel Date', required=False),
                'partner_id':fields.many2one('res.partner','Wakf Name',ondelete='set null',readonly=False),
                'company_id': fields.many2one('res.company', 'Company',size=64, required=False, readonly=False),
                'user_id':fields.char('user id',size=16),
                }
    _defaults={
        'user_id': lambda obj, cr, uid, context: uid,
     }
Revenue_Recovery()
