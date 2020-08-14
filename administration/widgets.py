from django import forms
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe

custom_file_input = '<div class="file-field "> \
			      		<div class="btn blue input-field"> \
			        		<span><i class="material-icons">attach_file</i></span> \
			      		</div> \
			      		<div class="file-path-wrapper">\
			      	 		<input id="id_file" type="file" name="file">     \
			        		<input class="file-path validate" type="text" >\
			      		</div>\
			    	</div>'

class AdminFileWidget(forms.FileInput):
	"""
	Widget za unos datoteka 
	"""
	def __init__(self, attrs={}):
		super(AdminFileWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None, renderer=None):
		output = []
		if value and hasattr(value, "url"):
			output.append('%s  <a target="_blank" href="%s">%s</a> <br />%s ' % \
			(_('Trenutni dokument:'), value.url, value, _('Promijeni:')))
		output.append(custom_file_input)
		return mark_safe(u''.join(output))