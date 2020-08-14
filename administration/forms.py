from django import forms
from .models import Study, Thesis, Employee
from .widgets import AdminFileWidget
import os

class ThesisForm(forms.ModelForm):
	"""
	Obrazac za predaju i ažuriranje radova
	"""
	def __init__(self, *args, **kwargs):
		self._newly_created = kwargs.get('instance') is not None
		student = kwargs.pop('student',None)
		super(ThesisForm, self).__init__(*args, **kwargs)
		
		studies = Study.objects.all()
		for i in studies:
			if student.area_of_study in i.__str__().lower() and student.category.split(":",1)[1] in i.__str__().lower():
				self.fields['study'].queryset = Study.objects.filter(id=i.id)
				break;	
		
		self.fields['mentor'].queryset = Employee.objects.all()

		self.fields['study'].label='Smjer'
		self.fields['title'].label='Naslov rada'
		self.fields['title_english'].label='Naslov rada(engleski)'
		self.fields['summary'].label='Sažetak rada'
		self.fields['summary_english'].label='Sažetak rada(engleski)'
		self.fields['file'].label='Dokument'
		self.fields['remark'].label='Napomena'

		self.fields['mentor'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['komentor'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['study'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['title'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['summary'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['title_english'].error_messages={'required': 'Ovo polje je obavezno'}
		self.fields['summary_english'].error_messages={'required': 'Ovo polje je obavezno'}

	class Meta:
		model = Thesis
		fields = ['study','mentor','komentor', 'file','title', 'title_english','summary','summary_english', 'remark']
		widgets = {

          'summary': forms.Textarea(),
          'summary_english': forms.Textarea(),
          'remark': forms.Textarea(),
          'file' : AdminFileWidget(),
          
        }
		
	def clean_komentor(self):
		if self.cleaned_data["komentor"] != None and self.cleaned_data["komentor"] == self.cleaned_data["mentor"]:
			raise forms.ValidationError("Komentor mora biti različit od mentora!")
		return self.cleaned_data["komentor"]
	
	def clean_file(self):
		if self.cleaned_data["file"] == None and self._newly_created == False:
			raise forms.ValidationError("Morate unijeti dokument!")
		else:
			name, ext = os.path.splitext("{}".format(self.cleaned_data["file"]))
			if ext not in ['.pdf', '.PDF']:
				raise forms.ValidationError("Dozvoljen je samo pdf format!")
		return self.cleaned_data["file"]

class VerificationForm(forms.Form):
	"""
	Obrazac za generiranje obrasca o provjeri izvornosti
	"""
	work_match = forms.CharField(label='Podudarnost rada:',error_messages={'required': 'Ovo polje je obavezno'})
	explanation = forms.CharField(label='Obrazloženje mentora:',widget=forms.Textarea,error_messages={'required': 'Ovo polje je obavezno'})
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 't_id1'}))

class PresidentChangeStatusForm(forms.Form):
	"""
	Obrazac kojim predsjednk povjerenstva mjenja status rada
	"""
	PRIHVACEN = 5
	ODBIJEN = 6
	U_DORADI = 7


	CHOICES = {
		(PRIHVACEN, 'PRIHVAĆEN'),
		(ODBIJEN, 'ODBIJEN'),
		(U_DORADI, 'U DORADI'),

	}
	status = forms.ChoiceField(label='Status: ', widget=forms.Select(attrs={'id': 'status_select'}), choices=CHOICES)
	explanation = forms.CharField(label='Obrazloženje: ',widget=forms.Textarea)
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 't_id'}))

class AddComitee(forms.Form):
	"""
	Obrazac kojim djelovođa povjerenstva dodaje članove povjerenstva za obranu diplomskog rada
	"""
	CHOICES = Employee.objects.all()
	member1 = forms.ChoiceField(label='Član 1: ', widget=forms.Select(attrs={'class': 'comitee_select'}), choices=((x.id, x.user.username) for x in CHOICES ))
	member2 = forms.ChoiceField(label='Član 2: ', widget=forms.Select(attrs={'class': 'comitee_select'}), choices=((x.id, x.user.username) for x in CHOICES ))
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'td_id'}))

	def clean_member2(self):
		if self.cleaned_data["member2"] == self.cleaned_data["member1"]:
			raise forms.ValidationError("Članovi povjerenstva moraju biti dvije različite osobe")
		return self.cleaned_data["member2"]

class ChangeDocument(forms.Form):
	"""
	Obrazac kojim student mjenja dokument rada u slučaju da je predsjednik stavio status rada u U_DORADI
	"""
	file = forms.FileField(widget=AdminFileWidget(),label='Dokument ',error_messages={'required': 'Obavezno je unijeti datoteku'})
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'thesis_id'}))

	def clean_file(self):
		if self.cleaned_data["file"] == None and self._newly_created == False:
			raise forms.ValidationError("Morate unijeti dokument!")
		else:
			name, ext = os.path.splitext("{}".format(self.cleaned_data["file"]))
			if ext not in ['.pdf', '.PDF']:
				raise forms.ValidationError("Dozvoljen je samo pdf format!")
		return self.cleaned_data["file"]

class GradeForm(forms.Form):
	"""
	Obrazac kojim članovi povjerenstva unose ocjenu rada i obrane za diplomske radove
	"""
	CHOICES = {
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),

	}
	grade = forms.ChoiceField(label='Ocjena rada: ', widget=forms.Select(attrs={'class': 'grade_select'}), choices=CHOICES)
	defense_grade = forms.ChoiceField(label='Ocjena obrane rada: ', widget=forms.Select(attrs={'class': 'grade_select'}), choices=CHOICES)
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'tg_id'}))

class FinalGradeForm(forms.Form):
	"""
	Obrazac kojim mentor unosi konačnu ocjenu za završni rad
	"""
	CHOICES = {
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),

	}
	grade = forms.ChoiceField(label='Konačna ocjena rada: ', widget=forms.Select(attrs={'id': 'final_grade_select'}), choices=CHOICES)
	thesis_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'tfg_id'}))