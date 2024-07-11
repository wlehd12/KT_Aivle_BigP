from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Program
from .forms import ProgramForm
from django.contrib import messages
from exhibition.models import Booth_Info
from django.http import JsonResponse

@login_required
def program_open(request):
    if not request.user.profile.user_type == '기업회원' and not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            company_name = request.user.profile.name
            selected_times = request.POST.getlist('selected_times')
            selected_times = sorted(set(selected_times))
            
            program = Program.objects.create(
                user=request.user,
                name=name,
                description=description,
                company_name=company_name,
                selected_times=",".join(selected_times)
            )

            return redirect('index')
        else:
            print("형식이 올바르지 않습니다")
            print(form.errors)
    else:
        form = ProgramForm()
    return render(request, 'program_open.html', {'form': form})

@login_required
def program_manage(request):
    program = get_object_or_404(Program, user=request.user)
    time_slots = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    selected_times = program.selected_times.split(',') if program.selected_times else []
    
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = ProgramForm(request.POST, instance=program)
            if form.is_valid():
                program = form.save(commit=False)
                
                new_selected_times = request.POST.getlist('selected_times')
                new_selected_times = sorted(list(set(new_selected_times[1:])))
                
                program.selected_times = ",".join(new_selected_times)
                
                program.save()
                return redirect('program_manage')
        elif 'delete' in request.POST:
            program.delete()
            return redirect('index')
    else:
        form = ProgramForm(instance=program)
    
    return render(request, 'program_manage.html', {'form': form, 'program': program, 'time_slots': time_slots, 'selected_times': selected_times})

@login_required
def reserve_booth(request, booth_id):
    booth = get_object_or_404(Booth_Info, booth_id=booth_id)
    company_name = booth.company_name
    program_exists = Program.objects.filter(company_name=company_name).exists()

    if not program_exists:
        messages.error(request, '기업에서 프로그램을 생성하지 않았습니다.')
        return redirect('layout1')

    # Proceed with reservation logic
    # Assuming you have a reservation model and form
    # reservation = Reservation.objects.create(user=request.user, booth=booth, program=program)
    messages.success(request, '예약이 완료되었습니다.')
    return redirect('reservation', booth_id=booth_id)

def check_program(request, company_name):
    program_exists = Program.objects.filter(company_name=company_name).exists()
    if program_exists:
        booth = get_object_or_404(Booth_Info, company_name=company_name)
        return JsonResponse({'exists': True, 'booth_id': booth.booth_id})
    return JsonResponse({'exists': False})