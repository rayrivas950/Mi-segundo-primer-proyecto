from extensions import ma
from models import Contacto, Telefono, Email
from marshmallow import fields, validate

class EmailSchema(ma.SQLAlchemyAutoSchema):
    # Se define explícitamente para añadir validación y manejar 'id'
    email = ma.auto_field(validate=[
        validate.Length(max=50, error="El email no puede tener más de 50 caracteres."),
        validate.Email(error="El formato del email no es válido.")
    ])

    class Meta:
        model = Email
        load_instance = True
        # Excluir 'contacto_id' de la entrada/salida
        exclude = ("contacto_id",)
        # Incluir 'id' solo en la salida (dump)
        dump_only = ("id",)

class TelefonoSchema(ma.SQLAlchemyAutoSchema):
    # Se define explícitamente para manejar 'id'
    class Meta:
        model = Telefono
        load_instance = True
        exclude = ("contacto_id",)
        dump_only = ("id",)

class ContactoSchema(ma.SQLAlchemyAutoSchema):
    nombre = ma.auto_field(
        validate=validate.Length(max=30, error="El nombre no puede tener más de 30 caracteres.")
    )
    notes = ma.auto_field(
        required=False, 
        allow_none=True, 
        validate=validate.Length(max=150, error="Las notas no pueden tener más de 150 caracteres.")
    )
    
    emails = fields.Nested(EmailSchema, many=True)
    telefonos = fields.Nested(TelefonoSchema, many=True)
    image_url = ma.auto_field(
        required=False, 
        allow_none=True, 
        validate=validate.Length(max=2048, error="La URL de la imagen no puede tener más de 2048 caracteres.")
    )

    class Meta:
        model = Contacto
        load_instance = True
        dump_only = ("id", "user_id", "created_at") # Estos ya eran dump_only

# Instancias para un solo objeto y para una lista de objetos.
contacto_schema = ContactoSchema()
contactos_schema = ContactoSchema(many=True)
