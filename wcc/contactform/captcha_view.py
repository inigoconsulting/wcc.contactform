from collective.recaptcha.view import RecaptchaView

class CustomRecaptchaView(RecaptchaView):
    
    def custom_image_tag(self):
        if not self.settings.public_key:
            raise ValueError, 'No recaptcha public key configured. \
                Go to path/to/site/@@recaptcha-settings to configure.'
        options = """<script src='https://www.google.com/recaptcha/api.js'></script>"""
        html = """<div class="g-recaptcha" data-sitekey="%s"></div>""" % self.settings.public_key
        return options+html