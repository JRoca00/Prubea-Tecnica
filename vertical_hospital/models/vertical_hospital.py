from odoo import models, fields, api
from odoo.exceptions import ValidationError

#Modelo base pacientes
class VerticalHospital(models.Model):
    _name = 'vertical.hospital'
    _description = 'Modelo de pacientes'
 

    #Datos para funcionamiento del formulario
    #Estados del formulario de pacientes
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('high', 'Alta'),
            ('low', 'Baja'),
        ], string='Estado', default='draft')
    name = fields.Char(string="Name", store=True)


    #Informacion del paciente
    patient_name = fields.Char(string='Nombre')
    patient_last_name = fields.Char(string='Apellido')
    dni = fields.Char(string='DNI')
    treatment_id = fields.Many2one('vertical.hostpital.treatment', string="Tratamiento")
    cod_treatment = fields.Char(string='Codigo de Tratamiento')
    create_date = fields.Datetime(string='Fecha de Alta', default=lambda self: fields.Datetime.now())
    process_date = fields.Datetime(string='Fecha de actualizacion')

    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if record.dni and not record.dni.isdigit():
                raise ValidationError("El campo DNI debe contener solo números.")


    #Secuencia de control PA-0001...
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('vertical.hospital')
        return super(VerticalHospital, self).create(vals)

    #Fecha segun actualice la etapa
    @api.onchange('state')
    def _onchange_state(self):
        self.process_date = fields.Datetime.now()

    #Funcion para validar que no acepte caracteres
    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if record.dni and not record.dni.isdigit():
                raise ValidationError("El campo DNI no debe llevar letras")


    #Funcion que me agrega el codigo del tratamiento al campo cod_treatment
    @api.onchange('treatment_id')
    def _onchange_treatment_id(self):
        if self.treatment_id:
            self.cod_treatment = self.treatment_id.cod
        else:
            self.cod_treatment = False

    #Funcion para dejar bitacora de cambios en dni
    """@api.onchange('dni')
    def _onchange_dni(self):
        if self.dni:
            self.message_post(body="Se actualizó el DNI a: %s" % self.dni)"""



#Modelo de tratamientos
class VerticalHospitalTreatment(models.Model):
    _name = 'vertical.hostpital.treatment'
    _description = 'Modelo de tratamientos'

    cod = fields.Char(string='Codigo de Tratamiento', required=True)
    name = fields.Char(string='Nombre del Tratamiento', required=True)
    doctor_name = fields.Char(string='Médico tratante', required=True)

    @api.constrains('cod')
    def _check_cod(self):
        for record in self:
            if record.cod == '026':
                raise ValidationError("El código del tratamiento no puede contener la secuencia '026'.")

