from marshmallow import Schema, fields, validates, ValidationError

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    tags = fields.List(fields.Str(), required=False)

    @validates('price')
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError('Price must be greater than zero.')

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    tags = fields.List(fields.Str())
    
    @validates('price')
    def validate_price(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Price must be greater than zero.')