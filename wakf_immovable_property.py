from openerp.osv import osv
from openerp.osv import fields

class wakf_immovableproperty(osv.osv):
    """
         Open ERP Model
    """
    _name = 'wakf.immovableproperty'
    _description = 'wakf.immovableproperty'
 
    _columns = {
            'wakf_id':fields.many2one('res.partner','Wakf Name',ondelete='set null'), 
            'type_id':fields.many2one('wakf.type','Wakf Type',ondelete='set null',required=True),
                        
            'name':fields.char('Name', size=128, required=True),
            'landtype_id':fields.many2one('wakf.landtype','Land Type',ondelete='set null'),
            'location_boundaries':fields.text('Location / Boundaries',required=False),
            'propery_specifications':fields.text('Wakf Objectives',required=False),
            'area':fields.float('Area',required=False),
            'units_id':fields.many2one('wakf.units','Units',ondelete='set null'),
            'propery_classification':fields.selection((('rural','Rural'), ('urban','Urban')),'Rural/Urban',required=True),
            'wakf_objectives':fields.text('Wakf Objectives',required=False),
            'value':fields.float('Estimated Value',required=False),
            'valuation_date':fields.date('Valuation Date',required=False),
            'property_curr_status':fields.many2one('wakf.properystatus','Property Status',ondelete='set null'),
            'survey_no':fields.char('Survey Number',size=64,required=True),
            'survey_details':fields.text('survey Details',required=False),
            'survey_date':fields.date('Survey Date',required=False),
            'census_code':fields.char('Censud Code',size=8,required=False),
            'khata_no':fields.char('Khata No',size=8,required=False),
            'khewat_no':fields.char('Khasra / Khewat No',size=8,required=False),
            'amsom':fields.char('Amsom',size=8,required=False),
            'plot_no':fields.char('Plot no',size=8,required=False),
            'door_no':fields.char('Door No',size=8,required=False),
            'patta_no':fields.char('Patta No',size=8,required=False),
            'district_id':fields.many2one('wakf.district','District',ondelete='set null'),
            'taluk_id':fields.many2one('wakf.taluk','Taluk',ondelete='set null'),
            'village_id':fields.many2one('wakf.village','Village',ondelete='set null'),           
            
        }
wakf_immovableproperty()

class wakf_landtype(osv.osv):
    
    _name='wakf.landtype'
    _description='wakf.description'
    
    _columns= {
               'name':fields.char('Name',size=32,required=True),
               'description':fields.text('Description',required=True)
               
               }
wakf_landtype()

class wakf_units(osv.osv):
    
    _name='wakf.units'
    _description='wakf.description'
    
    _columns= {
               'code':fields.char('Code',size=32,required=True),
               'name':fields.char('Name',size=32,required=True),
               'description':fields.text('Description',required=True)           
              
              }
wakf_units()

class wakf_properystatus(osv.osv):
    
    _name ='wakf.properystatus'
    _description='wakf.properystatus'
    
    _columns = {
            'name':fields.char('Name',size=32,required=True),
            'description':fields.text('Description',required=True) 
                
     }
wakf_properystatus()

