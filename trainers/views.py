from django.shortcuts import render, redirect
from django.utils import timezone
from members.models import Member
from trainers.models import Trainer
from attendance.models import Attendance
from courses.models import Course, CourseContent


# TRAINER CHECK

def trainer_check(request):
    if not request.user.is_authenticated:
        return False
    return request.user.role == 'trainer'

# TRAINER VIEWS

def trainer_dashboard(request):
    if not trainer_check(request):
        return redirect('login')

    from django.utils import timezone
    from attendance.models import Attendance

    trainer    = request.user.trainer
    my_members = Member.objects.filter(
        assigned_trainer=trainer
    ).select_related('user')

    today = timezone.now().date()
    present_today = Attendance.objects.filter(
        member__assigned_trainer=trainer,
        date=today,
        status='present'
    ).count()
    
    today_records = Attendance.objects.filter(
        member__assigned_trainer=trainer,
        date=today
    ).select_related('member__user')

    return render(request, 'trainer/dashboard.html', {
        'trainer':       trainer,
        'my_members':    my_members,
        'total_members': my_members.count(),
        'present_today': present_today,
        'today_records': today_records,
        'today':         today,
    })


def trainer_members(request):
    if not trainer_check(request):
        return redirect('login')
    trainer    = request.user.trainer
    my_members = Member.objects.filter(
        assigned_trainer=trainer
    ).select_related('user')
    return render(request, 'trainer/members.html', {
        'my_members': my_members
    })


def mark_attendance(request):
    if not trainer_check(request):
        return redirect('login')
    trainer    = request.user.trainer
    my_members = Member.objects.filter(
        assigned_trainer=trainer
    ).select_related('user')

    if request.method == 'POST':
        member_id    = request.POST.get('att-member')
        status       = request.POST.get('att-status')
        date         = request.POST.get('date') or \
                       timezone.now().date()
        checkin_time = request.POST.get(
                           'checkin_time') or None
        member = Member.objects.get(id=member_id)
        Attendance.objects.update_or_create(
            member=member,
            date=date,
            defaults={
                'status':       status,
                'checkin_time': checkin_time,
                'marked_by':    trainer
            }
        )
        return redirect('mark_attendance')

    selected_date = request.GET.get(
    'date', str(timezone.now().date())
       )

    today_records = Attendance.objects.filter(
    member__assigned_trainer=trainer,
    date=selected_date
          ).select_related('member__user')

    return render(request, 'trainer/attendance.html', {
    'my_members':    my_members,
    'today_records': today_records,
    'today':         timezone.now().date(),
    'selected_date': selected_date,
     })


def trainer_workout(request):
    if not trainer_check(request):
        return redirect('login')
    trainer    = request.user.trainer
    my_courses = Course.objects.filter(
        trainer=trainer
    ).select_related('trainer__user')
    return render(request, 'trainer/workout.html', {
        'my_courses': my_courses
    })


def upload_content(request):
    if not trainer_check(request):
        return redirect('login')
    trainer    = request.user.trainer
    my_courses = Course.objects.filter(trainer=trainer)

    if request.method == 'POST':
        title         = request.POST.get('title')
        content_type  = request.POST.get(
                            'content_type', 'pdf')
        course_id     = request.POST.get('course_id')
        uploaded_file = request.FILES.get('file')
        course = Course.objects.get(id=course_id)
        CourseContent.objects.create(
            course=course,
            title=title,
            content_type=content_type,
            file=uploaded_file
        )
        return redirect('upload_content')

    all_content = CourseContent.objects.filter(
        course__trainer=trainer
    ).order_by('-uploaded_at')

    return render(request, 'trainer/upload.html', {
        'my_courses':  my_courses,
        'all_content': all_content,
    })


def trainer_progress(request):
    if not trainer_check(request):
        return redirect('login')
    trainer    = request.user.trainer
    my_members = Member.objects.filter(
        assigned_trainer=trainer
    ).select_related('user')
    this_month   = timezone.now().month
    members_data = []

    for member in my_members:
        monthly = Attendance.objects.filter(
            member=member,
            date__month=this_month
        )
        present = monthly.filter(status='present').count()
        total   = monthly.count()
        percent = int((present / total * 100)) \
                  if total > 0 else 0
        members_data.append({
            'member':  member,
            'present': present,
            'total':   total,
            'percent': percent,
        })

    return render(request, 'trainer/progress.html', {
        'members_data': members_data
    })