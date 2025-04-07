from django.urls import reverse
from rest_framework import status

# اختبار أن الطالب يمكنه رؤية الدورات غير المسجل بها:
def test_student_can_view_unenrolled_courses(self):
    self.client.force_authenticate(user=self.student_user)
    response = self.client.get(reverse('course:courseList'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['code'], 'C2')

# اختبار أن الطالب يمكنه رؤية الدورات المسجل بها:
def test_student_can_view_enrolled_courses(self):
    self.client.force_authenticate(user=self.student_user)
    response = self.client.get(reverse('course:mycourseList'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['code'], 'C1')

# اختبار أن المدرس يمكنه رؤية جميع الدورات التي يدرسها:
def test_instructor_can_view_all_courses(self):
    self.client.force_authenticate(user=self.instructor_user)
    response = self.client.get(reverse('course:courseList'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)
    self.assertIn('C1', [course['code'] for course in response.data])
    self.assertIn('C2', [course['code'] for course in response.data])
