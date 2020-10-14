from django import template

register = template.Library()

# @register.inclusion_tag('view.html')
@register.simple_tag
def replaceval(content,oldv, newv):
	""" The function implement the replace func of python """
	return content.replace(oldv, newv)
	