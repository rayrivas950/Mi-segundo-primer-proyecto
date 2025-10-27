from extensions import ma
from models import Contacto, Telefono, Email
from marshmallow import fields

class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email
        load_instance = True
        # Excluir 'id' y 'contacto_id' de la entrada, ya que son gestionados por la BD.
        exclude = ("id", "contacto_id")

class TelefonoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Telefono
        load_instance = True
        exclude = ("id", "contacto_id")

class ContactoSchema(ma.SQLAlchemyAutoSchema):
    # Anidar los esquemas para la serializaciÃ³n y deserializaciÃ³n automÃ¡tica.
    emails = fields.Nested(EmailSchema, many=True)
    telefonos = fields.Nested(TelefonoSchema, many=True)

    class Meta:
        model = Contacto
        load_instance = True
        # include_relationships = True # Eliminado
        # Campos que son solo de salida (read-only).
        # No se esperarÃ¡n en el JSON de entrada al crear/actualizar.
        dump_only = ("id", "user_id", "created_at")

# Instancias para un solo objeto y para una lista de objetos.
contacto_schema = ContactoSchema()
contactos_schema = ContactoSchema(many=True)
