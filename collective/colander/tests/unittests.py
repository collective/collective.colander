import datetime
import pkg_resources
import unittest

from zope import interface
from zope import schema
import colander
import deform

from collective.colander.converter import convertToColander

class IAllSchemaFields(interface.Interface):
    ascii_ = schema.ASCII(title=u'title', description=u'description', \
        default='default', required=False)
    ascii_line = schema.ASCIILine(title=u'title', description=u'description', \
        default='default')
    bool_ = schema.Bool(title=u'title', description=u'description', \
        default=True)
    bytes_ = schema.Bytes(title=u'title', description=u'description', \
        default='default')
    bytes_line = schema.BytesLine(title=u'title', description=u'description', \
        default='default')
    choice = schema.Choice(values = [1,2])
    date = schema.Date(title=u'title', description=u'description', \
        default=datetime.date(2010, 10, 10))
    datetime = schema.Datetime(title=u'title', description=u'description', \
        default=datetime.datetime(2010, 10, 10, 10, 10))
    float_ = schema.Float(title=u'title', description=u'description', \
        default=1.5)
    int_ = schema.Int(title=u'title', description=u'description', \
        default=1)
    password = schema.Password(title=u'title', description=u'description')
    text = schema.Text(title=u'title', description=u'description', \
        default=u'default')
    text_line = schema.TextLine(title=u'title', description=u'description', \
        default=u'default')

class Tests(unittest.TestCase):
    def test_all_fields(self):
        colander_schema = convertToColander(IAllSchemaFields)
        class_getter = lambda key: colander_schema[key].typ.__class__
        self.assertEquals(colander.String, class_getter('ascii_'))
        self.assertEquals(colander.String, class_getter('ascii_line'))
        self.assertEquals(colander.Boolean, class_getter('bool_'))
        self.assertEquals(colander.String, class_getter('bytes_'))
        self.assertEquals(colander.String, class_getter('bytes_line'))
        self.assertEquals(colander.String, class_getter('choice'))
        self.assertEquals(colander.Date, class_getter('date'))
        self.assertEquals(colander.DateTime, class_getter('datetime'))
        self.assertEquals(colander.Float, class_getter('float_'))
        self.assertEquals(colander.Integer, class_getter('int_'))
        self.assertEquals(colander.String, class_getter('password'))
        self.assertEquals(colander.String, class_getter('text'))
        self.assertEquals(colander.String, class_getter('text_line'))

    def test_attributes(self):
        colander_schema = convertToColander(IAllSchemaFields)
        self.assertEquals('title', colander_schema['ascii_'].title)
        self.assertEquals('description', colander_schema['ascii_'].description)
        self.assertEquals('default', colander_schema['ascii_'].default)
        self.assertEquals(False, colander_schema['ascii_'].required)
        self.assertEquals(True, colander_schema['ascii_line'].required)

    def test_deform(self):
        colander_schema = convertToColander(IAllSchemaFields)
        form = deform.Form(colander_schema)
        self.assertEquals(pkg_resources.resource_string(__name__, 'testform.txt').strip(), form.render())
