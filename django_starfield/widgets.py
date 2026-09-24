from django.conf import settings
from django.forms.widgets import Widget
import random
import string

STARFIELD_COLOUR = '#f5b301'
STARFIELD_CONTENT = "'\\2605'"
STARFIELD_STARS = 5
STARFIELD_TEMPLATE = 'django_starfield/stars.html'
STARFIELD_CSS = "django_starfield.css"

class Stars(Widget):
    template_name = getattr(settings, 'STARFIELD_TEMPLATE', STARFIELD_TEMPLATE)

    def __init__(self, attrs=None, stars=None, content=None, colour=None, unique_id=None, css_file=None):
        super(Stars, self).__init__(attrs)

        self.stars = stars if stars else getattr(settings, 'STARFIELD_STARS', STARFIELD_STARS)
        self.content = content if content else getattr(settings, 'STARFIELD_CONTENT', STARFIELD_CONTENT)
        self.colour = colour if colour else getattr(settings, 'STARFIELD_COLOUR', STARFIELD_COLOUR)
        self.css_file = css_file if css_file else getattr(settings, 'STARFIELD_CSS', STARFIELD_CSS)
        self.unique_id = unique_id

    def get_context(self, name, value, attrs):
        context = super(Stars, self).get_context(name, value, attrs)
        context['stars'] = range(self.stars, 0, -1)
        # A fresh id per render keeps several copies of the same form on one page apart
        context['unique_id'] = self.unique_id or ''.join([random.choice(string.ascii_lowercase) for i in range(8)])
        context['css_file'] = self.css_file
        if not self.content == STARFIELD_CONTENT:
            context['content'] = self.content
        if not self.colour == STARFIELD_COLOUR:
            context['colour'] = self.colour
        return context
