from io import BytesIO

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Guard, Member, Payslip, CompanyInfo
from users.models import CustomUser, Profile
from users.forms import CustomRegistrationForm
from .forms import GuardForm, MemberForm, PayslipForm, CompanyInfoForm

from django.db.models import Q

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from datetime import date


# Shared context function
def get_dashboard_context():
    number_of_guards = Guard.objects.count()
    number_of_members = Member.objects.count()
    number_of_staffs = CustomUser.objects.count()

    staff_member = Profile.objects.all()
    member_list = Member.objects.all()[:3]
    payslip_list = Payslip.objects.all()[:3]

    male_count = Member.objects.filter(gender='male').count()
    female_count = Member.objects.filter(gender='female').count()

    under_18 = 0
    age_18_35 = 0
    age_36_60 = 0
    over_60 = 0

    for member in Member.objects.all():
        if member.date_of_birth:
            age = date.today().year - member.date_of_birth.year
            if age < 18:
                under_18 += 1
            elif 18 <= age <= 35:
                age_18_35 += 1
            elif 36 <= age <= 60:
                age_36_60 += 1
            else:
                over_60 += 1

    return {
        "number_of_guards": number_of_guards,
        "number_of_members": number_of_members,
        "number_of_staffs": number_of_staffs,
        "staff_member": staff_member,
        "member_list": member_list,
        "payslip_list": payslip_list,
        "male_count": male_count,
        "female_count": female_count,
        "under_18": under_18,
        "age_18_35": age_18_35,
        "age_36_60": age_36_60,
        "over_60": over_60,
    }


# Staff Dashboard
class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_dashboard_context())
        return context


# Admin Dashboard
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_dashboard_context())
        return context

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@login_required
def staff_list(request):
    query = request.GET.get('q', '')
    staff_members = CustomUser.objects.all()
    if query:
        staff_members = staff_members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    paginator = Paginator(staff_members, 13)
    page_number = request.GET.get('page')
    staff_members = paginator.get_page(page_number)
    return render(request, 'portal/admin/staff_list.html', {'staff_members':staff_members, 'query':query})

@login_required
def staff_detail(request, id):
    staff = get_object_or_404(CustomUser, id=id)
    return render(request, 'portal/admin/staff_details.html', {'staff': staff})

@login_required
def staff_update(request, id):
    staff = get_object_or_404(CustomUser, id=id)
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('portal:staff_list')

    else:
        form = CustomRegistrationForm(instance=staff)

    return render(request, 'portal/admin/staff_update.html', {'form': form, 'staff': staff})

@login_required
@user_passes_test(is_admin)
def staff_delete(request, staff_id):
    staff = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        staff.delete()
        messages.success(request, "Staff member deleted successfully.")
        return redirect('portal:staff_list')

    return render(request, 'portal/admin/staff_confirm_delete.html', {'staff': staff})

@login_required
def guard_list(request):
    query = request.GET.get('q', '')  
    guards = Guard.objects.all()

    if query:
        guards = guards.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    paginator = Paginator(guards, 13)
    page_number = request.GET.get('page')
    guards = paginator.get_page(page_number)

    return render(request, 'portal/staff/staff_list_guard.html', {'guards': guards, 'query': query})

@login_required
def guard_detail(request, id):
    guard = get_object_or_404(Guard, id=id)
    return render(request, 'portal/staff/staff_detail_guard.html', {'guard': guard})

@login_required
def add_guard(request):
    if request.method == 'POST':
        form = GuardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal:guard_list')
    else:
        form = GuardForm()
    return render(request, 'portal/staff/staff_create_guard.html', {'form': form})

@login_required
def edit_guard(request, id):
    guard = get_object_or_404(Guard, id=id)
    if request.method == 'POST':
        form = GuardForm(request.POST, instance=guard)
        if form.is_valid():
            form.save()
            return redirect('portal:guard_list')
    else:
        form = GuardForm(instance=guard)
    return render(request, 'portal/staff/staff_update_guard.html', {'form': form, 'guard': guard})

@login_required
def delete_guard(request, id):
    guard = get_object_or_404(Guard, id=id)
    if request.method == 'POST':
        guard.delete()
        return redirect('portal:guard_list')
    return render(request, 'portal/staff/staff_delete_guard.html', {'guard': guard})

@login_required
def member_list(request):
    if request.user.user_type in ["admin", "staff"]:
        members = Member.objects.all()
        query = request.GET.get('q', '')  

        if query:
            members = members.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) 
            )
        paginator = Paginator(members, 13)
        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        return render(request, 'portal/staff/staff_list_member.html', {'members': members, 'query': query})
    else:
        return HttpResponse("You don't permision to access this page")

@login_required
def member_detail(request, id):
    member = get_object_or_404(Member, id=id)
    return render(request, 'portal/staff/staff_detail_member.html', {'member': member})

@login_required
def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal:member_list')
    else:
        form = MemberForm()
    return render(request, 'portal/staff/staff_create_member.html', {'form': form})

@login_required
def edit_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('portal:member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'portal/staff/staff_update_member.html', {'form': form, 'member': member})

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.user.user_type =="admin":
        if request.method == "POST":
            member.delete()
            return redirect('portal:member_list')
        return render(request, 'portal/staff/staff_delete_member.html', {'member': member})

    else:
        return HttpResponse("Only Admins are allowed to delete")

def create_payslip(request):
    if request.method == "POST":
        form = PayslipForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Payslip created successfully!")
    else:
        form = PayslipForm()

    return render(request, 'portal/admin/guard_create_payslip.html', {'form': form})

def payslip_list(request):
    query = request.GET.get('q', '')  
    payslips = Payslip.objects.all()

    if query:
        payslips = payslips.filter(
            Q(guard__first_name__icontains=query) |
            Q(guard__last_name__icontains=query) 
        )
    
    paginator = Paginator(payslips, 13)
    page_number = request.GET.get('page')
    payslips = paginator.get_page(page_number)

    return render(request, 'portal/admin/guard_payslip_list.html', {'payslips': payslips, 'query': query})

def payslip_detail(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)
    return render(request, 'portal/admin/guard_payslip_detail.html', {'payslip': payslip})

def payslip_update(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    
    if request.method == "POST":
        form = PayslipForm(request.POST, instance=payslip)
        if form.is_valid():
            form.save()
            return redirect('portal:payslip_list')
    else:
        form = PayslipForm(instance=payslip)
    
    return render(request, 'portal/admin/guard_payslip_update.html', {'form': form, 'payslip': payslip})

def payslip_delete(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    
    if request.method == "POST":
        payslip.delete()
        return redirect('portal:payslip_list')
    
    return render(request, 'portal/admin/guard_payslip_confirm_delete.html', {'payslip': payslip})

def add_watermark(canvas, doc):
    canvas.saveState()
    watermark_text = "OFFICIAL PAYSLIP" 
    canvas.setFont("Helvetica", 50)
    canvas.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.1))
    canvas.rotate(45)
    canvas.drawCentredString(500, 50, watermark_text)
    canvas.restoreState()

@login_required
def payslip_download_pdf(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    bold_style = styles['Title']
    normal_style.fontSize = 8
    bold_style.fontSize = 10

    # Company Details Table
    if payslip.company and payslip.company.logo:
        logo_path = payslip.company.logo.path
        logo_img = Image(logo_path, width=100, height=100)
        logo_img.hAlign = 'CENTER'
        elements.append(logo_img)

    company_details = [
        ["Company Name", "Contact Info"],
        [f"{payslip.company.company_name}", f"Phone: {payslip.company.phone}"],
        [f"Address: {payslip.company.postal_address}", f"Email: {payslip.company.email}"],
        [f"Website: {payslip.company.website}", f"VAT Number: {payslip.company.vat_number}"],
    ]
    company_table = Table(company_details, colWidths=[doc.width / 2 - 10, doc.width / 2 - 10])
    company_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), 
        ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(company_table)

    # Payslip Header Info
    header_data = [
        [Paragraph(f"Payslip for: {payslip.guard.first_name} {payslip.guard.last_name}", bold_style)],
        [Paragraph(f"Payment Date: {payslip.date_issued.strftime('%B %d, %Y')}", normal_style)],
        [Paragraph(f"Gender: {payslip.guard.get_gender_display()}", normal_style)],
        [Paragraph(f"Identification Number: {payslip.guard.identification_document}", normal_style)],
        [Paragraph(f"Date Employed: {payslip.guard.date_employed.strftime('%B %d, %Y')}", normal_style)],
    ]
    header_table = Table(header_data, colWidths=[doc.width])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(header_table)

    # Salary Breakdown Table
    salary_header = [["Basic Salary", "Allowances", "Tax", "Deductions", "Net Salary"]]
    salary_data = [
        [f"N${payslip.basic_salary:.2f}", 
        f"N${payslip.allowances:.2f}", 
        f"N${payslip.tax:.2f}", 
        f"N${payslip.deductions:.2f}", 
        f"N${payslip.net_pay:.2f}"]
    ]

    salary_table = Table(salary_header + salary_data, colWidths=[doc.width / 5] * 5)  

    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.brown), 
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), 
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 8), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), 
        ('TOPPADDING', (0, 0), (-1, -1), 5), 
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    elements.append(salary_table)

    footer_data = [
        [Paragraph("Thank you for your valued contribution to the company. Your dedication and hard work are greatly appreciated!", normal_style)],
        [Paragraph(f"For any inquiries, please contact: {payslip.company.email}", normal_style)],
    ]
    footer_table = Table(footer_data, colWidths=[doc.width])
    footer_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Oblique', 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(footer_table)

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{payslip.guard.first_name}_{payslip.guard.last_name}_payslip.pdf')


@login_required
def download_members_list_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']
    title_style.fontSize = 14
    normal_style.fontSize = 8

    company = CompanyInfo.objects.first()

    if company and company.logo:
        logo_path = company.logo.path
        logo_img = Image(logo_path, width=100, height=100)
        logo_img.hAlign = 'CENTER'
        elements.append(logo_img)

        centered_style = ParagraphStyle('centered', parent=normal_style, alignment=1)  
        elements.append(Spacer(1, 12)) 
        elements.append(Paragraph(f"{company.company_name}", centered_style))
        elements.append(Paragraph(f"{company.phone} | {company.email}", centered_style))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("Member List", title_style))
    elements.append(Spacer(1, 12))

    member_header = [
        ["First Name", "Last Name", "Gender", "ID", "DOB", "Phone", "Village", "Date Joined", "Status", "Date Deceased", "Age", "Years Active"]
    ]

    member_data = []
    for member in Member.objects.all():
        member_data.append([
            member.first_name,
            member.last_name,
            member.get_gender_display(),
            member.identification_document,
            member.date_of_birth.strftime('%Y-%m-%d'),
            member.cellphone_number,
            member.get_village_display(),
            member.date_join.strftime('%Y-%m-%d'),
            member.get_status_display(),
            member.date_deceased.strftime('%Y-%m-%d') if member.date_deceased else "-",
            member.age(),
            member.membership_period(),
        ])

    table_data = member_header + member_data

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='members_list.pdf')

@login_required
def download_guards_list_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']
    title_style.fontSize = 14
    normal_style.fontSize = 8

    company = CompanyInfo.objects.first()

    if company and company.logo:
        logo_path = company.logo.path
        logo_img = Image(logo_path, width=100, height=100)
        logo_img.hAlign = 'CENTER'
        elements.append(logo_img)

        centered_style = ParagraphStyle('centered', parent=normal_style, alignment=1)  
        elements.append(Spacer(1, 12)) 
        elements.append(Paragraph(f"{company.company_name}", centered_style))
        elements.append(Paragraph(f"{company.phone} | {company.email}", centered_style))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("Guard List", title_style))
    elements.append(Spacer(1, 12))

    guard_header = [
        ["First Name", "Last Name", "Gender", "ID", "DOB", "Phone", "Village Assigned", "Date Employed", "Status", "Age"]
    ]

    guard_data = []
    for guard in Guard.objects.all():
        guard_data.append([
            guard.first_name,
            guard.last_name,
            guard.get_gender_display(),
            guard.identification_document,
            guard.date_of_birth.strftime('%Y-%m-%d'),
            guard.cellphone_number,
            guard.get_village_assigned_display(), 
            guard.date_employed.strftime('%Y-%m-%d') if guard.date_employed else "-",
            guard.get_status_display(),
            guard.age() if guard.date_of_birth else "-"
        ])

    table_data = guard_header + guard_data

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='guards_list.pdf')


# def add_company_info(request):
#     if request.method == 'POST':
#         form = CompanyInfoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('portal:company_info_list')
#     else:
#         form = CompanyInfoForm()
#     return render(request, 'portal/admin/add_company_info.html', {'form': form})

def company_info_list(request):
    company_info = CompanyInfo.objects.all() 
    return render(request, 'portal/admin/company_info_list.html', {'company_info': company_info})

def company_info_detail(request, company_id):
    company_info = get_object_or_404(CompanyInfo, id=company_id)
    return render(request, 'portal/admin/company_info_detail.html', {'company_info': company_info})

def edit_company_info(request, pk):
    company_info = CompanyInfo.get_instance()
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=company_info)
        if form.is_valid():
            form.save()
            return redirect('portal:company_info_list')
    else:
        form = CompanyInfoForm(instance=company_info)
    return render(request, 'portal/admin/edit_company_info.html', {'form': form})

def delete_company_info(request, pk):
    company_info = CompanyInfo.get_instance()
    if request.method == 'POST':
        company_info.delete()
        return redirect('portal:add_company_info')
    return render(request, 'portal/admin/confirm_delete.html', {'company_info': company_info})
