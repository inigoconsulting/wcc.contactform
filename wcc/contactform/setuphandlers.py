from collective.grok import gs
from wcc.contactform import MessageFactory as _

@gs.importstep(
    name=u'wcc.contactform', 
    title=_('wcc.contactform import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.contactform.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
