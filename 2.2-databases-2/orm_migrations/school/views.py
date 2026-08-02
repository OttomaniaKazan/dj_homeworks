from django.shortcuts import render
from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    
    # Добавляем prefetch_related для оптимизации загрузки учителей
    students = Student.objects.order_by('group').prefetch_related('teachers')
    
    context = {'object_list': students}
    return render(request, template, context)
