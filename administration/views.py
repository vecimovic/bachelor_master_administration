from django.shortcuts import render,redirect
from django.conf import settings
from django.db.models import Exists
from .models import Student, Study, Thesis, Notification, Role, Employee,MemberOfThesisComitee,User
from .forms import ThesisForm, VerificationForm,PresidentChangeStatusForm,AddComitee,ChangeDocument,GradeForm,FinalGradeForm
from .utils import render_to_pdf
from io import BytesIO
from django.core.files import File
from django.http import HttpResponseRedirect, HttpResponse
import time
from PyPDF2 import PdfFileReader
from django.core.mail import send_mail
# Create your views here.

#naslovi i sadržaji svih obavijesti
SUBMISSION_TITLE = 'PREDAN {} RAD, ULOGA: {}'
SUBMISSION_CONTENT = 'Korisnik/ca <a href="/profil/{}/">{}</a> predao/la vam je rad kojemu \
možete pristupiti na sljedećoj poveznici <a href="/prikaz/{}/">{}</a> <br> <br> '

STUDENT_TO_MENTOR_SUBMISSION_TITLE = 'PREDALI STE {} RAD MENTORU'
STUDENT_TO_MENTOR_SUBMISSION_CONTENT = 'Uspješno ste predali svoj rad mentoru. Status rada možete pratiti ovdje \
 <a href="/prikaz/{}/">{}</a>'

STUDENT_TO_PRESIDENT_SUBMISSION_TITLE = 'PREDALI STE {} RAD PREDSJEDNIKU POVJERENSTVA'
STUDENT_TO_PRESIDENT_SUBMISSION_CONTENT = 'Uspješno ste predali svoj rad predjedniku povjerenstva. Status rada možete pratiti ovdje \
 <a href="/prikaz/{}/">{}</a>'

VERIFICATION_TITLE = 'IZVRŠENA PROVJERA IZVORNOSTI'
MENTOR_VERIFICATION_CONTENT = 'Uspješno ste izvršili provjeru izvornosti za rad: <a href="/prikaz/{}/">{}</a>. \
Generirani obrazac o provjeri izvornosti možete preuzeti <a href="/media/{}">ovdje</a>'
STUDENT_VERIFICATION_CONTENT = 'Mentor/ica je izvršio/la provjeru izvornosti za vaš rad: <a href="/prikaz/{}/">{}</a>. \
Generirani obrazac o provjeri izvornosti možete preuzeti <a href="/media/{}">ovdje</a>'

STATUS_CHANGE_TITLE = 'PROMJENA STATUSA RADA'
STATUS_CHANGER_CONTENT = 'Uspješno ste promijenili status rada u <b>{}</b> za rad: <a href="/prikaz/{}/">{}</a>.'
STATUS_CHANGED_CONTENT = 'Status vašeg rada: <a href="/prikaz/{}/">{}</a> promijenjen je u <b>{}</b>. <br> <br>'

BACHELOR_GRADE_TITLE = 'UNESENA KONAČNA OCJENA ZAVRŠNOG RADA'
MENTOR_GRADE_CONTENT = 'Uspješno ste unijeli konačnu ocjenu za rad: <a href="/prikaz/{}/">{}</a> \
<br> <br> Ocjena: <b>{}</b> <br> Status rada: <b>{}</b>'
STUDENT_BACHELOR_GRADE_CONTENT = 'Mentor/ica je unio/jela konačnu ocjenu za vaš rad: <a href="/prikaz/{}/">{}</a> \
<br> <br>Konačna ocjena: <b>{}</b> <br> Status rada: <b>{}</b>'

ADDED_TO_COMITEE_TITLE = 'DODANI STE KAO ČLAN POVJERENSTVA DIPLOMSKOG RADA'
ADDED_TO_COMITEE_CONTENT = 'Dodani ste kao član povjerenstva za diplomski rad: <a href="/prikaz/{}/">{}</a>. <br> \
Nakon obrane rada na ovoj <a class="modal-trigger" data-target="grade" href="#grade" data-tg_id="{}" >poveznici</a> možete \
unesti ocjenu rada i obrane.'

ADDED_COMITEE_TITLE = 'DODANI ČLANOVI POVJERENSTVA ZA DIPLOMSKI RAD'
ADDED_COMITEE_CONTENT = 'Uspješno ste dodali članove povjerenstva za diplomski rad: <a href="/prikaz/{}/">{}</a>'
STUDENT_ADDED_COMITEE_TITLE = 'DODANI ČLANOVI POVJERENSTVA ZA DIPLOMSKI RAD'
STUDENT_ADDED_COMITEE_CONTENT = 'Dodani su članovi povjerenstva za vaš diplomski rad: <a href="/prikaz/{}/">{}</a> <br> <br> \
Članovi: <br>'

COMITEE_MEMBER_ADDED_GRADE_TITLE = 'UNESENE OCJENA RADA I OCJENA OBRANE'
COMITEE_MEMBER_ADDED_GRADE_CONTENT = 'Uspješno ste unijeli ocjenu rada i ocjenu obrane za rad: <a href="/prikaz/{}/">{}</a><br> <br> \
Ocjena rada: <b>{}</b> <br> Ocjena obrane: <b>{}</b>'

MASTER_GRADE_TITLE = 'UNESENA KONAČNA OCJENA DIPLOMSKOG RADA'
STUDENT_MASTER_GRADE_CONTENT = 'Članovi povjerenstva unijeli su ocjene za vaš rad :<a href="/prikaz/{}/">{}</a> \
<br> <br>Konačna ocjena: <b>{}</b> <br> Status rada: <b>{}</b> <br> <br> Ocjene članova: <br>'

CHANGED_DOCUMENT_TITLE = 'PROMJENA DOKUMENTA RADA'
STUDENT_CHANGED_DOCUMENT_CONTENT = 'Uspješno ste promijenili datoteku rada za <a href="/prikaz/{}/">{}</a>'
PRESIDENT_CHANGED_DOCUMENT_CONTENT = 'Izvršena je promjena datoteke za rad <a href="/prikaz/{}/">{}</a> u ispravljenu verziju'

def login(request):
	"""
	Prikazuje početnu stranicu za prijavu u sustav koja preusmjerava korisnika 
	na stranicu za prijavu sa AAI@EduHr elektroničkim identitetom .

    **Template:**

	Ako je neki korisnik ulogiran :template:`error.html`,
	Ako nitko nije ulogiran :template:`login.html`,
    
	"""
	if request.user.is_authenticated:
		return render(request, 'error.html')
	else:
		return render(request, 'login.html')


def index(request):
	"""
    Prikazuje početnu stranicu ovisno o tome je li se prijavio djelatnik ili student. 
    U slučaju da je prijavljen student ako on nema spremljen završni/diplomski rad prikazuje mu se
    mogućnost da ga doda, a ako ima spremljen rad pokazuje se kartica sa određenim podacima o završnom radu.
    U slučaju da je prijavljen djelatnik na navigacijskoj traci prikazuju mu se sve uloge te ovisno o
    ulozi prikazuju se tablice sa svim radovima kojima djelatnik može pristupiti u toj ulozi.

    **Context**

    ``student``
        Instanca :model:`administration.Student`.
    ``employee``
        Instanca :model:`administration.Thesis`.
    ``thesis``
        Instanca :model:`administration.Employee`.
    ``roles``
       Lista instanci :model:`administration.Roles`.
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``change_document_form``
		Instanca obrasca administration.forms.ChangeDocument.
	``mentor_form``
		Instanca obrasca administration.forms.VerificationForm.
	``president_form``
		Instanca obrasca administration.forms.PresidentChangeStatusForm.
	``writer_form``
		Instanca obrasca administration.forms.AddComitee.

    **Template:**

    Ako je prijavljen student: :template:`student/student_index.html`,
    ako je prijavljen djelatnik :template:`employee/employee_index.html`,
    ako je došlo do pogreške  :template:`error.html`

    """
	if request.user.is_authenticated:

		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		notifications_unread = Notification.objects.filter(user=request.user, status=1)

		try:
			student = request.user.student
		except Student.DoesNotExist:
			student = None

		try:
			employee = request.user.employee
		except Employee.DoesNotExist:
			employee = None
		
		if student:
			thesis = Thesis.objects.filter(author=student)
			change_document_form = ChangeDocument()
			context = {
				
				'student': student,
				'thesis' : thesis,
				'notifications': notifications,
				'notifications_unread': notifications_unread,
				'change_document_form': change_document_form,
			}
			
			return render(request, 'student/student_index.html', context)
		elif employee:
			roles = employee.roles.all()
			mentor_form = VerificationForm()
			president_form = PresidentChangeStatusForm()
			writer_form = AddComitee()
			context = {
				'employee': employee,
				'roles': roles,
				'notifications': notifications,
				'notifications_unread': notifications_unread,
				'mentor_form':mentor_form,
				'president_form':president_form,
				'writer_form':writer_form,
			}



			return render(request, 'employee/employee_index.html', context)
		else: 
			return render(request, 'error.html')
	else:
		return render(request, 'error.html')

def insert_thesis_into_db(request, form,student, thesis_id=None):
	"""
	Funkcija koja se koristi za unos rada u bazu tijekom predaje i ažuriranja rada
	"""
	if thesis_id == None:
		thesis = Thesis()
	else:
		thesis = Thesis.objects.get(id=thesis_id)

	thesis.mentor = form.cleaned_data.get("mentor")
	thesis.komentor = form.cleaned_data.get("komentor")
	thesis.study = form.cleaned_data.get("study")
	thesis.title = form.cleaned_data.get("title")
	thesis.title_english = form.cleaned_data.get("title_english")
	thesis.summary = form.cleaned_data.get("summary")
	thesis.summary_english = form.cleaned_data.get("summary_english")
	if form.cleaned_data.get("file") != None: 
		thesis.file = form.cleaned_data.get("file")
	thesis.remark = form.cleaned_data.get("remark")
	thesis.author = student

	if 'Diplomski' in thesis.study.__str__():
		rad = "DIPLOMSKI"
		thesis.type = 2
	else:
		thesis.type = 1
		rad = "ZAVRŠNI"
	
	if request.POST['action'] == 'Predaj':				
		thesis.status = 2
		thesis.mentor.roles.add(Role.objects.get(id=34))
		if thesis.komentor != None:
			thesis.komentor.roles.add(Role.objects.get(id=35))
	

	thesis.save()
	
	if thesis.status == 2:
		mentor_notification = Notification(user=thesis.mentor.user)
		mentor_notification.title = SUBMISSION_TITLE.format(rad,"mentor")
		mentor_notification.content = SUBMISSION_CONTENT.format(request.user.id, thesis.author,thesis.id,thesis.title)
		mentor_notification.save()	

		student_notification = Notification(user=thesis.author.user)
		student_notification.title = STUDENT_TO_MENTOR_SUBMISSION_TITLE.format(rad)
		student_notification.content = STUDENT_TO_MENTOR_SUBMISSION_CONTENT.format(thesis.id,thesis.title)
		student_notification.save()

		if thesis.komentor != None:
			thesis.komentor.roles.add(Role.objects.get(id=35))
			komentor_notification = Notification(user=thesis.komentor.user)
			komentor_notification.title = SUBMISSION_TITLE.format(rad,"komentor")
			komentor_notification.content = SUBMISSION_CONTENT.format(request.user.id, thesis.author,thesis.id,thesis.title)
			komentor_notification.save()

def thesis_submission(request):
	"""
    GET : Prikazuje obrazac za predaju/spremanje rada ako je u sustav prijavljen student i nema predan završni rad,
    inače prikazuje grešku.
    POST: Sprema instancu rada u bazu ako je validacija obrasca uspjela.
    Šalje obavijest mentoru i studentu ako je rad uspješno pohranjen u bazu sa statusom PREDAN_MENTORU.

    **Context**
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``form``
		Instanca obrasca administration.forms.ThesisForm.
	
    **Template:**

    Ako je prijavljen student: :template:`student/student_thesis_submission.html`,
    ako je prijavljen djelatnik ili je došlo do pogreške :template:`error.html`,
    
    """
	if request.user.is_authenticated:
		notifications_unread = Notification.objects.filter(user=request.user, status=1)
		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		try:
			student = Student.objects.get(user=request.user)
		except Student.DoesNotExist:
			student = None

		if(student):
			if request.method == 'POST':
				form = ThesisForm(request.POST,request.FILES,student=student)

				if form.is_valid():
					insert_thesis_into_db(request,form,student)	
					return redirect('index')
				else:
					context = {
						'form' : form,
						'notifications_unread': notifications_unread,
						'notifications': notifications,
					}
				
					return render(request, 'student/student_thesis_submission.html', context)
			else:
				if Thesis.objects.filter(author=student):
					return render(request, 'error.html')
				else:
					form = ThesisForm(student=student)
					context = {
						'form' : form,
						'notifications_unread': notifications_unread,
						'notifications': notifications,
					}
				
					return render(request, 'student/student_thesis_submission.html', context)
		else:
			return render(request, 'error.html')	



def thesis_update(request, thesis_id=None):
	"""
    GET : Prikazuje obrazac za ažuriranje rada ako je u sustav prijavljen student i ako je status rada koji se 
    ažurira SPREMLJEN,inače prikazuje grešku.
    POST: Sprema instancu rada u bazu ako je validacija obrasca uspjela.
    Šalje obavijest mentoru i studentu ako je rad uspješno pohranjen u bazu sa statusom PREDAN_MENTORU.

    **Context**
	``thesis_id``
		Id instance :model:`administration.Thesis` koja se ažurira.
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``form``
		Instanca obrasca administration.forms.ThesisForm.
	
    **Template:**

    Ako je prijavljen student: :template:`student/student_thesis_submission.html`,
    ako je prijavljen djelatnik ili je došlo do pogreške :template:`error.html`,
    
    """
	if request.user.is_authenticated:
		notifications_unread = Notification.objects.filter(user=request.user, status=1)
		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		try:
			student = Student.objects.get(user=request.user)
		except Student.DoesNotExist:
			student = None

		if(student):
			if request.method == 'POST':
				form = ThesisForm(request.POST,request.FILES,student=student,instance=Thesis.objects.get(id=thesis_id))

				if form.is_valid():
					insert_thesis_into_db(request,form,student,thesis_id)		
					return redirect('index')
				else:
					context = {
						'thesis_id' : thesis_id,
						'form' : form,
						'notifications_unread': notifications_unread,
						'notifications': notifications,
					}
				
					return render(request, 'student/student_update_thesis.html', context)
			else:
				thesis = Thesis.objects.get(id=thesis_id)
				if thesis.status > 1:
					return render(request, 'error.html')
				else:
					form = ThesisForm(student=student, instance=thesis)
					context = {
						'thesis_id' : thesis_id,
						'form' : form,
						'notifications_unread': notifications_unread,
						'notifications': notifications,
					}
				
				return render(request, 'student/student_update_thesis.html', context)
		else:
			return render(request, 'error.html')


def thesis_display(request, thesis_id):
	"""
    Prikazuje karticu sa svim podacima o završnom radu te ovisno o ulozi prikazuje i mogućnosti unosa nekih podataka.

    **Context**
	``student``
		Instanca :model:`administration.Student`.
	``employee``
		Instanca :model:`administration.Thesis`.
	``thesis``
		Instanca :model:`administration.Employee`.
	``nav``
		ovisno o vrsti korisnika koji je prijavljen bira se html sa određenom navigacijskom trakom
		(:template:`student/student_index.html` ili :template:`employee/employee_index.html`).
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``change_document_form``
		Instanca obrasca administration.forms.ChangeDocument.
	``mentor_form``
		Instanca obrasca administration.forms.VerificationForm.
	``president_form``
		Instanca obrasca administration.forms.PresidentChangeStatusForm.
	``writer_form``
		Instanca obrasca administration.forms.AddComitee.
	``grade_form``
		Instanca obrasca administration.forms.GradeForm.
	``final_grade_form``
		Instanca obrasca administration.forms.FinalGradeForm.

	
    **Template:**

    Ako je sve uredu: :template:`student/thesis_display.html`,
    ako je došlo do pogreške :template:`error.html`,
    
    """
	try:
		thesis = Thesis.objects.get(id=thesis_id)
	except Thesis.DoesNotExist:
		thesis = None

	if request.user.is_authenticated:
		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		notifications_unread = Notification.objects.filter(user=request.user, status=1)
		try:
			student = request.user.student
		except Student.DoesNotExist:
			student = None
		
		try:
			employee = request.user.employee
		except Employee.DoesNotExist:
			employee = None
		
		if(student): nav = "student/student_index.html"
		else: nav = "employee/employee_index.html" 

		change_document_form = ChangeDocument()
		mentor_form = VerificationForm()
		president_form = PresidentChangeStatusForm()
		writer_form = AddComitee()
		grade_form = GradeForm()
		final_grade_form = FinalGradeForm()
		
		context = {
			'student':student,
			'employee':employee,
			'nav': nav,
			'thesis' : thesis,
			'mentor_form' : mentor_form,
			'president_form':president_form,
			'writer_form':writer_form,
			'change_document_form': change_document_form,
			'grade_form':grade_form,
			'final_grade_form':final_grade_form,
			'notifications_unread': notifications_unread,
			'notifications': notifications,
		}

		return render(request, 'thesis_display.html', context)
	else:
		return render(request, 'error.html')


def notifications(request):
	"""
	Prikazuje obavijesti korisnika

    **Context**
	``nav``
		ovisno o vrsti korisnika koji je prijavljen bira se html sa određenom navigacijskom trakom
		(:template:`student/student_index.html` ili :template:`employee/employee_index.html`).
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``notification``
		Instanca :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.
	``grade_form``
		Instanca obrasca administration.forms.GradeForm.

	
    **Template:**

    Ako je sve uredu: :template:`notifications.html`,
    ako je došlo do pogreške :template:`error.html`,
	"""
	if request.user.is_authenticated:
		try:
			user_obj = Student.objects.get(user=request.user)
		except Student.DoesNotExist:
			user_obj = None

		if(user_obj): nav = "student/student_index.html"
		else: nav = "employee/employee_index.html" 
		
		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		notifications_unread = Notification.objects.filter(user=request.user, status=1)
		grade_form = GradeForm()
		context = {
			'nav' : nav,
			'notifications': notifications,
			'notifications_unread': notifications_unread,
			'grade_form': grade_form,
		}
		if 'id' in request.GET:		
			notification = Notification.objects.get(id=request.GET['id'])
			notification.status = 2
			notification.save()
			context['notification'] = notification
		return render(request, 'notifications.html', context)
	else:
		return render(request, 'error.html')

def notifications_mark_read(request):
	"""
	Označuje sve obavijesti kao pročitane

    **Template:**

    ako je došlo do pogreške :template:`error.html`
	"""
	if request.user.is_authenticated:
	   for i in Notification.objects.filter(user=request.user.id):
	   	   i.status = 2
	   	   i.save()
	   return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return render(request, 'error.html')

def profile(request, user_id):
	"""
    Prikazuje profil korisnika.

    **Context**
	``student``
		Instanca :model:`administration.Student`.
	``employee``
		Instanca :model:`administration.Thesis`.
	``nav``
		ovisno o vrsti korisnika koji je prijavljen bira se html sa određenom navigacijskom trakom
		(:template:`student/student_index.html` ili :template:`employee/employee_index.html`).
	``notifications``
		Lista svih instanci :model:`administration.Notifications` prijavljenog korisnika.	
	``notifications_unread``
		Lista svih nepročitanih instanci :model:`administration.Notifications` prijavljenog korisnika.

    **Template:**

    Ako je sve uredu: :template:`profile.html`,
    ako je došlo do pogreške :template:`error.html`
    
    """
	if request.user.is_authenticated:
		notifications = Notification.objects.filter(user=request.user).order_by('-date')
		notifications_unread = Notification.objects.filter(user=request.user, status=1)

		#checking if student with such profile exists		
		try:
			student = Student.objects.get(user=User.objects.get(id=user_id))
		except Student.DoesNotExist:
			student = None		
		try:
			employee = Employee.objects.get(user=User.objects.get(id=user_id))
		except Employee.DoesNotExist:
			employee = None
			

		#checking if a student is logged in to know which navbar to show
		try:
			user_obj = request.user.student
		except Student.DoesNotExist:
			user_obj = None

		if(user_obj): nav = "student/student_index.html"
		else: nav = "employee/employee_index.html"
		

		context = {
			'student': student,
			'employee': employee,
			'nav' : nav,
			'notifications': notifications,
			'notifications_unread': notifications_unread,
		}

		return render(request, 'profile.html', context)
	else:
		return render(request, 'error.html')

def generate_verification(request):
	"""
	Generira obrazac o provjeri izvornosti u obliku pdf datoteke.
	Šalje obavijest mentoru i studentu ako je provjera izvornosti uspješno izvršena.

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""

	if request.method == "POST":
		form = VerificationForm(request.POST)

		if form.is_valid():
			thesis = Thesis.objects.get(id=form.cleaned_data.get('thesis_id'))
			path_to_pdf = "{}{}".format(settings.MEDIA_ROOT, thesis.file)
			pdf = PdfFileReader(open(path_to_pdf,'rb'))

			data = {
				'name': thesis.author.user.first_name,
				'surname': thesis.author.user.last_name,
				'jmbag': thesis.author.jmbag,
				'study': thesis.study,
				'type': thesis.get_type_display,
				'title': thesis.title,
				'date': time.strftime(r"%d.%m.%Y", time.localtime()),
				'num_of_pages': pdf.getNumPages(), 
				'work_match': form.cleaned_data.get('work_match'),
				'explanation': form.cleaned_data.get('explanation'),
				'mentor' : thesis.mentor.user,

			}
			filename = "Provjera_izvornosti_{}".format(thesis.id)
			pdf = render_to_pdf('verification_of_work_authenticity/verification_document.html', data)
			thesis.verification_of_authenticity.save(filename, File(BytesIO(pdf.content)))

			student_notification = Notification(user=thesis.author.user)
			student_notification.title = VERIFICATION_TITLE
			student_notification.content = STUDENT_VERIFICATION_CONTENT.format(thesis.id, thesis.title,thesis.verification_of_authenticity)
			student_notification.save()	

			mentor_notification = Notification(user=thesis.mentor.user)
			mentor_notification.title = VERIFICATION_TITLE
			mentor_notification.content = MENTOR_VERIFICATION_CONTENT.format(thesis.id, thesis.title, thesis.verification_of_authenticity)
			mentor_notification.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return render(request, 'error.html')

def mentor_status_change(request):
	"""
	Mijenja status rada u provjeren te šalje obavijest mentoru i studentu ako je promjena statusa uspješno obavljena.

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == "POST":
		thesis = Thesis.objects.get(id=request.POST['id'])
		thesis.status = 3
		thesis.save()
		student_notification = Notification(user=thesis.author.user)
		student_notification.title = STATUS_CHANGE_TITLE
		student_notification.content = STATUS_CHANGED_CONTENT.format(thesis.id, thesis.title, thesis.get_status_display())
		student_notification.save()	

		mentor_notification = Notification(user=thesis.mentor.user)
		mentor_notification.title = STATUS_CHANGE_TITLE
		mentor_notification.content = STATUS_CHANGER_CONTENT.format(thesis.get_status_display(),thesis.id, thesis.title)
		mentor_notification.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return render(request, 'error.html')

def president_status_change(request):
	"""
	Mjenja status rada u ODBIJEN,U DORADI ili u PRIHVAĆEN te šalje obavijest predsjedniku povjerenstva
	i studentu ako je promjena statusa uspješno obavljena.

	**Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == "POST":
		form = PresidentChangeStatusForm(request.POST)
		if form.is_valid():
			thesis = Thesis.objects.get(id=form.cleaned_data.get('thesis_id'))
			
			thesis.status = int(form.cleaned_data.get('status'))
			thesis.save() 
			student_notification = Notification(user=thesis.author.user)
			student_notification.title = STATUS_CHANGE_TITLE
			student_notification.content = STATUS_CHANGED_CONTENT.format(thesis.id, thesis.title, thesis.get_status_display())
			student_notification.content += "Objašnjenje: <br> {}".format(form.cleaned_data.get('explanation'))
			student_notification.save()	

			president_notification = Notification(user=thesis.study.studycomitee.president.user)
			president_notification.title = STATUS_CHANGE_TITLE
			president_notification.content = STATUS_CHANGER_CONTENT.format(thesis.get_status_display(),thesis.id, thesis.title)
			president_notification.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return render(request, 'error.html')


def student_status_change(request):
	"""
	Mjenja status rada u PREDAN_POVJERENSTVU te šalje obavijesti predsjedniku, zamjeniku i djelovođi povjerenstva i studentu
	ako je promjena statusa uspješno obavljena

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == "POST":
		thesis = Thesis.objects.get(id=request.POST['id'])
		thesis.status = 4
		thesis.save()
		if(thesis.type == 1): rad = "ZAVRŠNI"
		else: rad = "DIPLOMSKI"
		student_notification = Notification(user=thesis.author.user)
		student_notification.title = STUDENT_TO_PRESIDENT_SUBMISSION_TITLE.format(rad)
		student_notification.content = STUDENT_TO_PRESIDENT_SUBMISSION_CONTENT.format(thesis.id, thesis.title)
		student_notification.save()	

		president_notification = Notification(user=thesis.study.studycomitee.president.user)
		president_notification.title = SUBMISSION_TITLE.format(rad,"predsjednik povjerenstva")
		president_notification.content = SUBMISSION_CONTENT.format(thesis.author.user.id,thesis.author.user,thesis.id, thesis.title)
		president_notification.save()

		deputy_notification = Notification(user=thesis.study.studycomitee.deputy.user)
		deputy_notification.title = SUBMISSION_TITLE.format(rad,"zamjenik povjerenstva")
		deputy_notification.content = SUBMISSION_CONTENT.format(thesis.author.user.id,thesis.author.user,thesis.id, thesis.title)
		deputy_notification.save()

		writer_notification = Notification(user=thesis.study.studycomitee.writer.user)
		writer_notification.title = SUBMISSION_TITLE.format(rad,"djelovođa povjerenstva")
		writer_notification.content = SUBMISSION_CONTENT.format(thesis.author.user.id,thesis.author.user,thesis.id, thesis.title)
		writer_notification.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return render(request, 'error.html')


def student_document_change(request):
	"""
	Mjenja datoteku rada u slučaju da je status rada U_DORADI te šalje obavijest predsjedniku povjerenstva i studentu ako
	je promjena datoteke uspješno izvršena.

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == "POST":
		form = ChangeDocument(request.POST,request.FILES)
		if form.is_valid():
			thesis_id = form.cleaned_data.get('thesis_id')
			thesis = Thesis.objects.get(id=thesis_id)
			thesis.file = form.cleaned_data.get('file')
			thesis.save() 

			student_notification = Notification(user=thesis.author.user)
			student_notification.title = CHANGED_DOCUMENT_TITLE
			student_notification.content = STUDENT_CHANGED_DOCUMENT_CONTENT.format(thesis.id, thesis.title)
			student_notification.save()	

			president_notification = Notification(user=thesis.study.studycomitee.president.user)
			president_notification.title = CHANGED_DOCUMENT_TITLE
			president_notification.content = PRESIDENT_CHANGED_DOCUMENT_CONTENT.format(thesis.id, thesis.title)
			president_notification.save()

			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			return render(request, 'error.html', {'document_form': form})
	else:
		return render(request, 'error.html')

def add_comitee(request):
	"""
	U slučaju diplomskog rada dodaje članove povjerenstva za rad te ako je to uspješno šalje im obavijest. Također se šalju obavijest 
	studentu i djelovođi povjerenstva

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == "POST":
		form = AddComitee(request.POST)
		if form.is_valid():
			employee1 = Employee.objects.get(id=form.cleaned_data.get('member1'))
			employee2 = Employee.objects.get(id=form.cleaned_data.get('member2'))
			thesis = Thesis.objects.get(id=form.cleaned_data.get('thesis_id'))

			member1 = MemberOfThesisComitee(thesis=thesis, employee=employee1)
			member1.save()


			member2 = MemberOfThesisComitee(thesis=thesis, employee=employee2)
			member2.save()
			
			mentor = MemberOfThesisComitee(thesis=thesis, employee=thesis.mentor)
			mentor.save()
			
			if thesis.komentor != None:
				komentor = MemberOfThesisComitee(thesis=thesis,employee=thesis.komentor)
				komentor.save()
			
			
			writer_notification = Notification(user=thesis.study.studycomitee.writer.user)
			writer_notification.title = ADDED_COMITEE_TITLE
			writer_notification.content = ADDED_COMITEE_CONTENT.format(thesis.id, thesis.title)	
			writer_notification.save()
			
			student_notification = Notification(user=thesis.author.user)
			student_notification.title = STUDENT_ADDED_COMITEE_TITLE
			student_notification.content = STUDENT_ADDED_COMITEE_CONTENT.format(thesis.id, thesis.title)
			for i in MemberOfThesisComitee.objects.filter(thesis=thesis):
				member_notification = Notification(user=i.employee.user)
				member_notification.title = ADDED_TO_COMITEE_TITLE
				member_notification.content = ADDED_TO_COMITEE_CONTENT.format(thesis.id, thesis.title, thesis.id)
				member_notification.save()
				student_notification.content += '<a href="/profil/{}/">{}</a> <br>'.format(i.employee.user.id, i.employee)
			student_notification.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			return render(request, 'error.html', {'comitee_form':form})
	else:
		return render(request, 'error.html')

def proper_round(num, dec=0):
	"""
	Funkcija za zaokruživanje brojeva. Koristi se tijekom izračuna ocijene.
	"""
	num = str(num)[:str(num).index('.')+dec+2]
	if num[-1]>='5':
		return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
	return float(num[:-1])

def add_grade(request):
	"""
	U slučaju diplomskog rada dodaje ocjene rada i obrane za pojedinog člana povjerenstva te kada svi članovi unesu ocjene 
	izračunava se konačna ocjena i mjenja se status rada u OBRANJEN ili NIJE POLOŽEN ovisno o ocjeni.
	Šalje obavijesti svakom članu da je unio ocjenu te studentu kada se izračuna konačna ocjena

    **Template:**

    Ako je došlo do pogreške :template:`error.html`
	"""
	if request.method == 'POST':
		form = GradeForm(request.POST)
		if form.is_valid():
			try:
				employee = Employee.objects.get(user=request.user)
			except Employee.DoesNotExist:
				employee = None

			thesis_id = form.cleaned_data.get('thesis_id')
			thesis = Thesis.objects.get(id=thesis_id)
			member= MemberOfThesisComitee.objects.get(thesis=thesis, employee=employee)
			member.grade = form.cleaned_data.get('grade')
			member.defense_grade = form.cleaned_data.get('defense_grade')
			member.save()
			member_notification = Notification(user=member.employee.user)
			member_notification.title = COMITEE_MEMBER_ADDED_GRADE_TITLE
			member_notification.content = COMITEE_MEMBER_ADDED_GRADE_CONTENT.format(thesis.id, thesis.title, member.grade, member.defense_grade)
			member_notification.save()
			grade = 0
			defense_grade = 0
			final_grade = 0
			if not MemberOfThesisComitee.objects.filter(grade=None, defense_grade=None, thesis=thesis):
				members = MemberOfThesisComitee.objects.filter(thesis=thesis)
				for i in members:
					grade += i.grade
					defense_grade += i.defense_grade
				grade = grade / len(members)
				defense_grade = defense_grade / len(members)
				final_grade = 0.7 * grade + 0.3 * defense_grade
				thesis.final_grade = int(proper_round(final_grade))
				if(final_grade < 2): 
					thesis.status = 9
				else:
					thesis.status = 8
				thesis.save()

				student_notification = Notification(user=thesis.author.user)
				student_notification.title = MASTER_GRADE_TITLE
				student_notification.content = STUDENT_MASTER_GRADE_CONTENT.format(thesis.id, thesis.title,thesis.final_grade,thesis.get_status_display())
				for i in MemberOfThesisComitee.objects.filter(thesis=thesis):
					student_notification.content += '<a href="/profil/{}/">{}</a> : Ocjena rada: {}, Ocjena obrane: {} <br>'.format(i.employee.user.id, i.employee,i.grade,i.defense_grade)
				student_notification.save()
				
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			return render(request, 'error.html')
	else:
		return render(request, 'error.html')

def add_final_grade(request):
	"""
	U slučaju završnog rada dodaje konačnu ocjenu za rad te mjenja status rada u OBRANJEN ili NIJE POLOŽEN ovisno o ocjeni.
	Nakon što su ocjena i status uneseni šalje se obavijest studentu i mentoru koji je upisao ocjenu.

    **Template:**

    Ako je došlo do pogreške :template:`error.html`,
	"""
	if request.method == 'POST':
		form = FinalGradeForm(request.POST)
		if form.is_valid():
			thesis_id = form.cleaned_data.get('thesis_id')
			thesis = Thesis.objects.get(id=thesis_id)
			thesis.final_grade = form.cleaned_data.get('grade')
			print(thesis.final_grade)
			if(thesis.final_grade != '1'): 
				thesis.status = 8
			else:
				thesis.status = 9  
			thesis.save()
			student_notification = Notification(user=thesis.author.user)
			student_notification.title = BACHELOR_GRADE_TITLE
			student_notification.content = STUDENT_BACHELOR_GRADE_CONTENT.format(thesis.id, thesis.title, thesis.final_grade,thesis.get_status_display())
			student_notification.save()	

			mentor_notification = Notification(user=thesis.mentor.user)
			mentor_notification.title = BACHELOR_GRADE_TITLE
			mentor_notification.content = MENTOR_GRADE_CONTENT.format(thesis.id, thesis.title, thesis.final_grade,thesis.get_status_display())
			mentor_notification.save()

			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			return render(request, 'error.html')
	else:
		return render(request, 'error.html')