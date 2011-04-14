from django import template
register = template.Library()

import markdown

def markdownify(text):
    return markdown.markdown(text)

register.simple_tag(markdownify)