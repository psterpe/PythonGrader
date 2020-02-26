import requests
import os
from time import sleep


COURSE_ID = '10190000001607278'
TEST_ASSIGNMENT_ID = '6794941' # First Assignment
STUDENT_ID = '6218019' # Test Student
COURSE_URL = f'https://bostoncollege.instructure.com/api/v1/courses/{COURSE_ID}'
SUBMISSION_URL = COURSE_URL + '/assignments/{}/submissions/{}'
UPLOAD_URL = SUBMISSION_URL + '/comments/files'
AUTH_TOKEN = '1019~hvb525CMuZvZ9rjIouP04Y1MMfBrhdBiRFB29hS0mHckZmvpgkVswWgOSS98Z0gB'
PSET_IDS = {
    'PS1': '6794944',
    'PS2': '6794945',
    'PS3': '6794946',
    'PS4': '6794947',
    'PS5': '6794948',
    'PS6': '6794949'
}


# still need to come up with a way to handle failed requests,
# though I haven't expereinced one so far
def upload_file(assignment_id, student_id, filename):
    url = UPLOAD_URL.format(assignment_id, student_id)
    headers = { 'Authorization': f'Bearer {AUTH_TOKEN}' }
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


def attach_file_and_post_grade(assignment_id, student_id, file_id, grade):
    url = SUBMISSION_URL.format(assignment_id, student_id)
    headers = { 'Authorization': f'Bearer {AUTH_TOKEN}' }
    params = {
        'comment[file_ids][]': file_id,
        'submission[posted_grade]': grade
    }
    return requests.put(url, headers=headers, params=params).ok


# could be useful for uploading batches of comment files
def get_fnames_from_current_dir(file_extension):
    for fname in os.listdir():
        if fname.endswith(file_extension):
            yield fname


# could be useful for uploading batches of comment files / grades
def get_all_submissions(pset_id):
    return requests.get(f'https://canvas.instructure.comapi/v1/courses/{COURSE_ID}/assignments/{pset_id}/submissions').json()


if __name__ == '__main__':
    fname = 'PS1_sterpe_graded.txt'
    file_id = upload_file(PSET_IDS['PS1'], STUDENT_ID, fname)
    success = attach_file_and_post_grade(PSET_IDS['PS1'], STUDENT_ID, file_id, grade=10)
    if not success:
        print(f'\n**ERROR** : {fname} not uploaded\n')

