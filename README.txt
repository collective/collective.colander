Introduction
============

This package provides a method to transform a zope schema to a colander schema.
Colander is a library for defining schemas, it was created by the people behind
repoze. Deform is a form library to create forms based on colander schemas.

Putting it all together, it means that you can create forms with the
repoze form library based on your zope schemas.
Deform does a bit less than z3c.form and its plone helper libraries.
There are no CRUD Form generators there is no ready to use code that
automatically creates edit views that take care of storing changes.

Here is an example, how you can use deform:

    >>> from zope import schema
    >>> from zope import interface
    >>> class IParticipant(interface.Interface):
    ...     firstname = schema.TextLine(title=u"First name")
    ...     lastname  = schema.TextLine(title=u"Family name")
    ...     email = schema.TextLine(title=u"E-Mail")
    ...
    >>> from collective.colander.converter import convertToColander
    >>> import colander
    >>> colander_schema = convertToColander(IParticipant)
    >>> class Users(colander.SequenceSchema):
    ...     user = colander_schema
    ...
    >>> class Schema(colander.MappingSchema):
    ...     users = Users()
    ...
    >>> many_users_schema = Schema()
    >>> import deform
    >>> file('example.html').read().endswith(deform.Form(many_users_schema).render())
    True
