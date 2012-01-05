from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from zope.schema import _bootstrapfields as zfields2
from zope.schema import _field as zfields
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabulary
import colander
import deform
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from translationstring import TranslationString
from zope.i18nmessageid.message import Message


def extractFieldsFromDexterityObj(obj):
    fti = getUtility(IDexterityFTI, name=obj.portal_type)

    def extractFields(schema):
        retval = []
        for baseschema in schema.__bases__:
            retval.extend(extractFields(baseschema))
        for fieldname in schema.names():
            retval.append(schema[fieldname])
        return retval
    retval = []
    for schema in [fti.lookupSchema()] + \
            [x for x in getAdditionalSchemata(context=obj)]:
        retval.extend(extractFields(schema))
    retval.sort(key=lambda x:x.order)
    return retval

@colander.deferred
def deferredVocabularyValidator(node, kw):
    def validate(value):
        if node.field.vocabulary:
            factory = node.field.vocabulary
        else:
            factory = getUtility(IVocabularyFactory,
                                 name=node.field.vocabularyName)
        if IVocabulary.providedBy(factory):
            vocabulary = factory
        else:
            vocabulary = factory(kw['context'])
        try:
            vocabulary.getTerm(value)
            return True
        except LookupError:
            raise colander.Invalid()
    return colander.Function(validate)

@colander.deferred
def deferredVocularyWidget(node, kw):
    if node.field.vocabulary:
        factory = node.field.vocabulary
    else:
        factory = getUtility(IVocabularyFactory, name=node.field.vocabularyName)
    if IVocabulary.providedBy(factory):
        vocabulary = factory
    else:
        vocabulary = factory(kw['context'])
    choices = [('', '- Select -')]
    for term in vocabulary.by_token.values():
        choices.append((term.value, term.title))
    return deform.widget.SelectWidget(values=choices)


def mapZopeFieldsToColanderFields(fields):
    def convertI18n(obj):
        if obj.__class__ == Message:
            return TranslationString(unicode(obj),
                                     domain=obj.domain,
                                     default=obj.default,
                                     mapping=obj.mapping)
        else:
            return obj
    retval = {}
    adder = lambda typ, name, field, widget=None, validator=None:\
        retval.update({field: colander.SchemaNode(\
                typ(),
                name=convertI18n(name),
                title=convertI18n(field.title),
                description=convertI18n(field.description),
                widget=widget,
                validator=validator,
                default=field.default or colander.null)})
    for field in fields:
        name = field.__name__
        if field.__class__ in [
            RichText,
            zfields.URI,
            zfields.ASCIILine,
            zfields.ASCII,
            zfields2.Password,
            zfields2.TextLine,
            zfields2.Text,
            zfields.Bytes,
            zfields.BytesLine,
            zfields.Choice,
            ]:
            widget = None
            validator = None
            if field.__class__ in [zfields2.Text]:
                widget = deform.widget.TextAreaWidget(rows=10, cols=60)
            if field.__class__ in [zfields.Choice]:
                widget = deferredVocularyWidget
                validator = deferredVocabularyValidator
            if field.__class__ in [RichText]:
                widget = deform.widget.RichTextWidget()
                widget.skin = 'plone'
                widget.theme = 'advanced'
            adder(colander.String, name, field, widget, validator)
            retval[field].field = field
        elif field.__class__ in [zfields2.Bool]:
            adder(colander.Boolean, name, field)
        elif field.__class__ in [zfields.Float]:
            adder(colander.Float, name, field)
        elif field.__class__ in [zfields.Date]:
            adder(colander.Date, name, field)
        elif field.__class__ in [zfields.Datetime]:
            adder(colander.DateTime, name, field)
        elif field.__class__ in [zfields2.Int]:
            adder(colander.Integer, name, field)
        elif field.__class__ in [NamedBlobImage]:
            # XXX Use session
            class MemoryTmpStore(dict):
                def preview_url(self, name):
                    return None
            adder(deform.FileData, name, field, deform.widget.FileUploadWidget(MemoryTmpStore()))
        elif field.__class__ == zfields.Tuple\
                and field.value_type.__class__ in [zfields2.TextLine]:
            if field.value_type.__class__ == zfields2.TextLine:
                list_field = colander.SchemaNode(colander.Sequence(),
                                                 colander.SchemaNode(colander.String()),
                                                 name=convertI18n(name),
                                                 title=convertI18n(field.title),
                                                 description=convertI18n(field.description),
                                                 default=field.default or colander.null)
                retval[field] = list_field
        elif field.__class__ == zfields.List \
                and field.value_type.__class__ in [zfields.Choice]:
            if field.value_type.__class__ == zfields.Choice:
                list_field = colander.SchemaNode(colander.Sequence(),
                                                 colander.SchemaNode(colander.String(),
                                                                     widget=deferredVocularyWidget,
                                                                     validator=deferredVocabularyValidator,
                                                                     field=field.value_type),
                                                 name=convertI18n(name),
                                                 title=convertI18n(field.title),
                                                 description=convertI18n(field.description),
                                                 default=field.default or colander.null)
                retval[field] = list_field
        else:
            retval[field] = None
        if not field.required and retval[field]:
            retval[field].missing = field.default or ''
    return retval


def convertToColander(fields):
    retval = colander.SchemaNode(colander.Mapping())
    mapping = mapZopeFieldsToColanderFields(fields)
    for field in fields:
        if not mapping[field]:
            raise TypeError("Oh, the mapping for %s has not been defined yet" \
                                % field.__class__)
        retval.add(mapping[field])
    return retval
