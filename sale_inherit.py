from osv import osv
from osv import fields

class sale_inherit(osv.osv):
 
 
    #_name = 'customer.inherit.'
    _inherit = 'res.partner'
    
    def on_change_wakf_village_to_taluk(self, cr, uid, ids, village_id, context=None):
        values = {}
        if village_id:
            cust = self.pool.get('wakf.village').browse(cr, uid, village_id, context=context).taluk_id.id
            cust1 = self.pool.get('wakf.village').browse(cr, uid, village_id, context=context).district_id.id
            values = {
                'taluk_id': cust,
                'district_id': cust1
            }
        return {'value' : values}
    
 
    _columns = {
            #'name':fields.char('Wakf Name', size=128, required=False),
            'details':fields.char('Details', size=128, required=False),
            'postoffice':fields.char('Rule of Succession', size=128, required=False),
            'rule_succession':fields.char('Post Office', size=128, required=False),
            'phone':fields.char('Phone Number', size=64, required=False),
            'wakf_old_name':fields.char('Wakf old name', size=128, required=False),
            'suomoto':fields.boolean('Suomoto',required=False),        
            'classification':fields.selection((('sunni','Sunni'), ('shia','Shia')),'Classification',required=False),
            'wakf_objectives':fields.text('Remarks',required=False),
            'wakf_reg_no':fields.integer('Registration No',size=8,required=False),
            'wakf_registration_date':fields.date('Registration Date',required=False),
            'creation_date':fields.date('Wakf Creation Date',required=False),
            'gazetted':fields.boolean('Gazetted'),
            'gazetted_date':fields.date('Gazetted Date',required=False),
            'comm_addr':fields.text('Communication address',help='Address for communication of wakf',required=False),
            'waquif_name':fields.char('Waquif Name',size=128,required=False),
            'waquif_uid':fields.char('Waquif UID',size=32,required=False,help='Unique Identification to be assigned from the Aadhar Project'),
            'waquif_father_name':fields.char("Father/Husband's Name",size=128,required=False),
            'waquif_father_uid':fields.char("Father/Husband's UID",size=32,required=False,help='Unique Identification to be assigned from the Aadhar Project'),
            'waquif_address':fields.text('Waquif Address',required=False),
            'type_id':fields.many2one('wakf.type','Wakf Type',ondelete='set null',required=False),
            'district_id':fields.many2one('wakf.district','District',ondelete='set null'),
            'taluk_id':fields.many2one('wakf.taluk','Taluk',ondelete='set null'),
            'village_id':fields.many2one('wakf.village','Village',ondelete='set null'), 
            'wakf_immovable_property_id':fields.one2many('wakf.immovableproperty','wakf_id','Immovable Properties'),
            'wakf_movable_property_id':fields.one2many('wakf.movableproperty','wakf_id','Movable Properties'),
            'wakf_management_id':fields.one2many('wakf.management','wakf_id','Management Details'),
            'company_id': fields.many2one('res.company', 'Company', required=True),
                
        }
    
    _sql_constraints = [
        ('wakf_reg_uniq', 'unique(wakf_reg_no)', 'Register Number already exists !'),
    ]
    
sale_inherit()