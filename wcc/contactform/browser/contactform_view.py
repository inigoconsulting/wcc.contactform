from five import grok
from plone.directives import dexterity, form
from wcc.contactform.content.contactform import IContactForm
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator

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

    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(
        title=u"Captcha",
        required=True
    )

@form.validator(field=IFormSchema['captcha'])
def validateCaptcha(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IFormSchema['captcha'], None)
    captcha.validate(value)

class Index(form.SchemaForm):
    grok.context(IContactForm)
    grok.require('zope2.View')
    grok.name('view')
    enable_form_tabbing = False
    css_class = 'wcc-contact-form'
    ignoreContext = True
    schema = IFormSchema

    template = ViewPageTemplateFile('templates/contactform_view.pt')

    mail_template = '''
From: %(from_name)s <%(from_email)s>
Country: %(country)s
City: %(city)s
Phone: %(phone)s

Message
--------

%(message)s


    '''
    @z3c.form.button.buttonAndHandler(_(u'Submit'), name='submit')
    def submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        mailhost = self.context.MailHost

        msg = message_from_string(self.mail_template % data)
        msg.set_charset('utf-8')

        msg['TO'] = ', '.join(self.context.emails_to)
        msg['FROM'] = '"%s" <%s>' % (data['from_name'],data['from_email'])
        if self.context.emails_bcc:
            msg['BCC'] = ', '.join(self.context.emails_bcc)

        if self.context.emails_cc:
            msg['CC'] = ', '.join(self.context.emails_cc)

        mailhost.send(msg, subject=data['subject'])
