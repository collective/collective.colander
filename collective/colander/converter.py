import colander
from zope.schema import _field as zfields
from zope.schema import _bootstrapfields as zfields2

def convertToColander(schema):
    retval = colander.SchemaNode(colander.Mapping())
    adder = lambda typ, name, field, schema: schema.add(colander.SchemaNode(typ(), name=name, title=field.title, description=field.description, default=field.default))
    for name in schema.names():
        if schema[name].__class__ in [\
                zfields.URI\
              , zfields.ASCIILine
              , zfields.ASCII
              , zfields2.Password
              , zfields2.TextLine
              , zfields2.Text
              , zfields.Bytes
              , zfields.BytesLine
              , zfields.Choice
            ]:
            adder(colander.String, name, schema[name], retval)
        elif schema[name].__class__ in [zfields2.Bool]:
            adder(colander.Boolean, name, schema[name], retval)
        elif schema[name].__class__ in [zfields.Float]:
            adder(colander.Float, name, schema[name], retval)
        elif schema[name].__class__ in [zfields.Date]:
            adder(colander.Date, name, schema[name], retval)
        elif schema[name].__class__ in [zfields.Datetime]:
            adder(colander.DateTime, name, schema[name], retval)
        elif schema[name].__class__ in [zfields2.Int]:
            adder(colander.Integer, name, schema[name], retval)
        else:
            raise TypeError("Oh, the mapping for %s has not been defined yet" % schema[name].__class__)
        if not schema[name].required:
            retval[name].missing = schema[name].default or ''
    return retval
