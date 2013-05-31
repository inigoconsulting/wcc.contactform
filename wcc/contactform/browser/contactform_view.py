from five import grok
from plone.directives import dexterity, form
from wcc.contactform.content.contactform import IContactForm

from z3c.schema.email import RFC822MailAddress
from wcc.contactform import MessageFactory as _
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from email import message_from_string
import z3c.form.button
from zope.globalrequest import getRequest
from zope.component.hooks import getSite
from zope.component import getMultiAdapter
from email.Header import Header
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class IFormSchema(form.Schema):

    form.fieldset(
        'details',
        label=_('About You'),
        fields=['from_email','from_name','city','country','phone']
    )
    
    from_email = RFC822MailAddress(
        title=_(u'Your email')
    )

    from_name = schema.TextLine(
        title=_(u'Your name')
    )

    city = schema.TextLine(
        title=_(u'Your city')
    )

    country = schema.TextLine(
        title=_(u'Your country')
    )

    phone = schema.TextLine(
        title=_(u'Your phone'),
        required=False
    )

    form.fieldset(
        'message',
        label=_('Your message'),
        fields=['subject','message']
    )

    subject = schema.TextLine(
        title=_(u'Subject')
    )

    message = schema.Text(
        title=_(u'Message'),
    )

    form.fieldset(
        'captcha',
        label=_('Verification'),
        fields=['captcha']
    )


class Index(form.SchemaForm):
    grok.context(IContactForm)
    grok.require('zope2.View')
    grok.name('view')
    enable_form_tabbing = False
    css_class = 'wcc-contact-form'
    ignoreContext = True
    schema = IFormSchema

    template = ViewPageTemplateFile('templates/contactform_view.pt')

    mail_template = u'''%(message)s

---

From: %(from_name)s <%(from_email)s>
Country: %(country)s
City: %(city)s
Phone: %(phone)s

You are receiving this mail because %(from_name)s is sending feedback 
on the contact form at %(url)s
    '''
    @z3c.form.button.buttonAndHandler(_(u'Submit'), name='submit')
    def submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if not self.context.restrictedTraverse('@@captcha').verify():
            IStatusMessage(self.request).add(u'Invalid Captcha', type='error')
            return
        
        mailhost = self.context.MailHost

        data['url'] = self.context.absolute_url()
        message = self.mail_template % data
        msg = message_from_string(message.encode(self.context.email_charset))
        msg.set_charset(self.context.email_charset)

        msg['TO'] = u', '.join(self.context.emails_to)
        msg['FROM'] = u'"%s" <%s>' % (data['from_name'],data['from_email'])
        if self.context.emails_bcc:
            msg['BCC'] = u', '.join(self.context.emails_bcc)

        if self.context.emails_cc:
            msg['CC'] = u', '.join(self.context.emails_cc)

        mailhost.send(msg, msg['TO'], msg['FROM'],
                subject=data['subject'], charset=self.context.email_charset)

        IStatusMessage(self.request).add(u'Thank you. ')
