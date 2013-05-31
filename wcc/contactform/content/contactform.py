from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from z3c.schema.email import RFC822MailAddress
from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.contactform import MessageFactory as _


# Interface class; used to define content-type schema.

class IContactForm(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
    emails_to = schema.List(
        title=_(u'TO addresses'),
        description=_(u'One address per line'),
        required=False,
        value_type=RFC822MailAddress()
    )

    emails_cc = schema.List(
        title=_(u'CC addresses'),
        description=_(u'One address per line'),
        required=False,
        value_type=RFC822MailAddress()
    )

    emails_bcc = schema.List(
        title=_(u'BCC addresses'),
        description=_(u'One address per line'),
        required=False,
        value_type=RFC822MailAddress()
    )

    mail_sent_message = schema.TextLine(
        title=_(u'Message to display after a successful mail send'),
        default=u'Mail sent',
    )
