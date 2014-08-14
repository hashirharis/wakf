from openerp.osv import osv
from openerp.osv import fields

class wakf_district(osv.osv):
    """
         Open ERP Model
    """
    _name = 'wakf.district'
    _description = 'wakf.district'
 
    _columns = {
            'name':fields.char('Name', size=64, required=True),
            'taluk_id':fields.one2many('wakf.taluk','district_id','Taluk'),
            'dist_id':fields.one2many('wakf.village','district_id','Taluk'),
        }
wakf_district()


class wakf_taluk(osv.osv):
    
    _name='wakf.taluk'
    _description = 'wakf.taluk'
    
    
    _columns = {
                'name':fields.char('Name', size=64, required=True),
                'district_id':fields.many2one('wakf.district','District',ondelete='set null'),
                'village_id':fields.one2many('wakf.village','taluk_id','Village')             
                
                }
wakf_taluk()


class wakf_village(osv.osv):
    
    _name='wakf.village'
    _description='wakf.village'
    
    
    
    
    _columns = {
                'name':fields.char('Name', size=64, required=True),
                'taluk_id':fields.many2one('wakf.taluk','Taluk',ondelete='set null'),
                'wakf_id':fields.one2many('res.partner','taluk_id','Wakf'),
                'district_id':fields.many2one('wakf.district','District',ondelete='set null'),
                
                
                }  
wakf_village()
    
    
    
