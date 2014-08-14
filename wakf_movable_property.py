from openerp.osv import osv
from openerp.osv import fields

class wakf_movableproperty(osv.osv):
    """
         Open ERP Model
    """
    _name = 'wakf.movableproperty'
    _description = 'wakf.movableproperty'
 
    _columns = {
            'wakf_id':fields.many2one('res.partner','Wakf Name',ondelete='set null'),                      
            'name':fields.char('Name', size=128, required=True),
            'property_nature_id':fields.many2one('wakf.property_nature','Property Nature',ondelete='set null'),
            'expiry_date':fields.date('Expiry Date',required=False),
            'property_assessment':fields.selection((('income','Assessable Property (Income generating)'), ('non-income','Not Assessable Property (Non-Income generating)')),'Property Assessment',required=True),
            'reference_no':fields.char('Reference No',size=8,required=False),
            'value':fields.float('Estimated Value',required=False),
            'valuation_date':fields.date('Valuation Date',required=False),
            'location_property':fields.text('Location',required=True),
            'property_additional_details':fields.text('Additional Info',required=False),
            'property_remarks':fields.text('Remarks',required=False),
            
            
        }
wakf_movableproperty()


class wakf_property_nature(osv.osv):
    
    _name='wakf.property_nature'
    _description='wakf.property_nature'
    
    _columns = {
                'name':fields.char('Name', size=64, required=True),
                'description':fields.text('Description',required=False),
                
                }

wakf_property_nature()
    
    