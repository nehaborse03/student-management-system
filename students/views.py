from django.http import JsonResponse
from django.shortcuts import render
from .models import Student
from .forms import StudentForm
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

import json

@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})

@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.save()
        return redirect('student_list')

    return render(request, 'update_student.html', {'student': student})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect('student_list')

@login_required
def student_list(request):
    query = request.GET.get('q')

    if query:
        student_list = Student.objects.filter(
            Q(name__icontains=query) |
            Q(course__icontains=query)
        )
    else:
        student_list = Student.objects.all()

    paginator = Paginator(student_list, 5)   # 5 students per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    total_students = Student.objects.count()
    total_courses = Student.objects.values('course').distinct().count()

    return render(request, 'students/student_list.html', {
    'students': students,
    'total_students': total_students,
    'total_courses': total_courses,
})


def student_detail(request, id):

    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student Not Found"}, status=404)

    # PUT - Update
    if request.method == "PUT":
        body = json.loads(request.body)

        student.name = body.get("name", student.name)
        student.email = body.get("email", student.email)
        student.age = body.get("age", student.age)
        student.save()

        return JsonResponse({"message": "Student Updated Successfully"})

    # DELETE - Delete
    elif request.method == "DELETE":
        student.delete()
        return JsonResponse({"message": "Student Deleted Successfully"})