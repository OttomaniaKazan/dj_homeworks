import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return course

@pytest.fixture
def student_factory():
    def student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return student


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    
    # Используем reverse для генерации URL
    url = reverse('courses-detail', kwargs={'pk': course.id})
    
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    
    # Используем reverse для генерации URL
    url = reverse('courses-list')
    
    response = api_client.get(url)
    
    assert response.status_code == 200
    assert len(response.data) == len(courses)

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=5)
    target_course = courses[2]

    # Используем reverse для генерации URL
    url = reverse('courses-list')

    response = api_client.get(url, data={'id': target_course.id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    courses = course_factory(_quantity=5, _fill_optional=['name'])
    target_course = courses[2]

    # Используем reverse для генерации URL
    url = reverse('courses-list')

    response = api_client.get(url, data={'name': target_course.name})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == target_course.name

@pytest.mark.django_db
def test_create_course(api_client):

    data = {
        'name': 'Python developer',
    }
    
    url = reverse('courses-list')
    response = api_client.post(url, data=data, format='json')
    
    assert response.status_code == 201
    
    assert Course.objects.count() == 1
    created_course = Course.objects.first()
    assert created_course is not None
    assert created_course.name == 'Python developer'

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    
    course = course_factory()
    
    url = reverse('courses-detail', kwargs={'pk': course.id})
    
    # Данные для обновления
    update_data = {
        'name': 'Python developer',
    }
    
    response = api_client.patch(url, data=update_data, format='json')
    
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Python developer'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):

    course = course_factory()
    course_id = course.id
    
    url = reverse('courses-detail', kwargs={'pk': course_id})
    
    response = api_client.delete(url)
    
    assert response.status_code == 204
    assert not Course.objects.filter(id=course_id).exists()