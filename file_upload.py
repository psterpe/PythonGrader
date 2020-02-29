import requests
import os

class FileUpload:
    def __init__(self, course_id, auth_token):
        self.COURSE_ID = course_id
        self.AUTH_TOKEN = auth_token
        self.COURSE_URL = f'https://bostoncollege.instructure.com/api/v1/courses/{self.COURSE_ID}'
        self.SUBMISSION_URL = self.COURSE_URL + '/assignments/{}/submissions/{}'
        self.UPLOAD_URL = self.SUBMISSION_URL + '/comments/files'


    def upload_file(self, assignment_id, student_id, filename):
        url = self.UPLOAD_URL.format(assignment_id, student_id)
        headers = { 'Authorization': f'Bearer {self.AUTH_TOKEN}' }
        payload = {
            'name': filename,
            'size': os.path.getsize(f'./{filename}'),
            'content_type': 'text'
        }

        # Part 1 of the file upload process
        res1 = requests.post(url, headers=headers, data=payload).json()

        # Part 2 of the file upload process
        res2 = requests.post(
            res1['upload_url'],
            data=res1['upload_params'],
            files={'file': open(filename, 'rb')}
        )

        return res2.json()['id']


    def attach_file_and_post_grade(self, assignment_id, student_id, file_id, grade):
        url = self.SUBMISSION_URL.format(assignment_id, student_id)
        headers = { 'Authorization': f'Bearer {self.AUTH_TOKEN}' }
        params = {
            'comment[file_ids][]': file_id,
            'submission[posted_grade]': grade
        }
        return requests.put(url, headers=headers, params=params).ok
