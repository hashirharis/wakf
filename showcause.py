from osv import osv
from osv import fields

class Show_Cause(osv.osv):
 
    _name = 'show.cause'
    _description = 'show.cause'
 
    _columns = {
            'reg_no':fields.integer('Registration Number:', size=64, required=False),
            'partner_id':fields.many2one('res.partner','Wakf Name',ondelete='set null'),
            'notice_no':fields.char('Notice Number',size=32),
            'notice_date':fields.date('Notice Date'),
            'assessment_year':fields.many2one('account.fiscalyear','Assessment Year',ondelete='set null'),
            'acc_year_from':fields.many2one('account.fiscalyear','Account Year From',ondelete='set null'),
            'acc_year_to':fields.many2one('account.fiscalyear','Account Year To',ondelete='set null'),
            'user_id':fields.char('user id',size=16),
            'amount':fields.float('Amount')
                    }
    _defaults={
        'user_id': lambda obj, cr, uid, context: uid,
     }
Show_Cause()