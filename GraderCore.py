from os import scandir, devnull, listdir, chdir
from importlib import import_module
import json
import re
import sys
from multiprocessing import Pool, TimeoutError
import dill
from file_upload import *
from tkinter import Tk, filedialog

VERSION = '2.0'
GRADED_SYMBOL = 'Y'
GRADER_FILE_PATTERN = re.compile('.*_GRADER.py')
ASSIGNMENT_FILE_PATTERN = re.compile('([a-zA-Z]+)_.*\.py')
ALL_ASSIGNMENTS = []
FNULL = open(devnull, 'w')
IMPORT_AREA_KEY = 'import'
MAX_TOTAL_POINTS = 8
MAX_IMPORT_POINTS = 3
MAX_CORRECTNESS_POINTS = MAX_TOTAL_POINTS - MAX_IMPORT_POINTS
AUTH_TOKEN = None
COURSE_ID = ''
STUDENT_URL = 'https://canvasurl/api/v1/courses/{}/users'
ASSIGNMENT_DIR = '.'
OUTPUT_DIR = '.'

class Area:
    # An Area describes a gradable topic area of an assignment.
    def __init__(self, key, description, possiblePoints):
        self.key = key
        self.area = description
        self.possiblePoints = possiblePoints
        self.actualPoints = 0
        self.reasons = []


class Assignment:
    # An Assignment holds the gradable areas of a single student's assignment.
    def __init__(self, grader, assignment, shortemail):
        self.grader = grader
        self.assignment = assignment
        self.student = shortemail
        self.areas = {}
        self.actualScore = 0
        self.graderScore = 0
        self.possibleScore = 0

    def add_area(self, area):
        self.areas[area.key] = area

    def score_area(self, key, score, reason=''):
        self.areas[key].actualPoints = score
        if reason != '':
            self.areas[key].reasons.append(reason)

    def calc_score(self):
        score = 0
        graderScore = 0

        for item in self.areas.values():
            if item.key == IMPORT_AREA_KEY:
                score += item.actualPoints
            else:
                graderScore += item.actualPoints

        # Calculate % of available points awarded by PSX_GRADER.py, then apply to MAX_CORRECTNESS_POINTS
        score += (graderScore / self.grader.MAX_POINTS) * MAX_CORRECTNESS_POINTS

        self.actualScore = score
        self.graderScore = graderScore
        self.possibleScore = MAX_TOTAL_POINTS


# To make grading somewhat declarative, we use a data structure as described below. The data structure is a list
# of dictionaries. It is defined in a module that we import. The list must be in the imported module's global
# scope, and it must be named GRADING_DATA. The module we import is named for the assignment being graded,
# e.g., PS1_GRADER.py, PS2_GRADER.py, etc.
#
# The GRADING_DATA list describes the tests we want to run. The tests themselves are NOT declarative; they are
# expressed in functions that we must write and that also live in the PSx_GRADER module.
#
# Here is a sample GRADING_DATA list containing just one dictionary:
#
# [
#     {
#         "key": "genpat",
#         "area": "generatePattern function",
#         "testfunc": test_generatePattern,
#         "possiblePoints": 0
#     }
# ]

# Each dictionary in the list describes an area, meaning an aspect of the assignment, that we want to grade.
# The attributes of each dictionary are as follows:
#
#   key              string  Any short string that can be a valid dict key. Must be unique across all areas.
#   area             string  A user-friendly name for the grading area this dictionary represents.
#   testfunc         func    A function, that must exist within the PSx_GRADER.py module, that should be called to
#                            test this particular area.
#   possiblePoints   int     The number of points this area is worth
#
# To test an assignment, we break it up into conceptual areas and write a function to test each one. These functions
# we write become the values of the 'testfunc' keys in the GRADING_DATA dictionaries.
#
# A testfunc...
#   0) is something we have to write
#   1) will usually call functions in the student's code. To do this, the testfunc can be sure it will receive
#      one argument, the student module, so it can do studentmodule.function_it_wants_to_exercise.
#   2) must return a tuple consisting of an integer and a string; the integer is the score the student
#      earned for the area being tested, and the string gives a reason for the score. The string may be '', e.g.,
#      for when the student earned full points and we don't need to supply a reason.
#   3) is assumed to perform all the tests we want for a given area


# Takes in an object of type os.DirEntry
def is_student_submission(entry):
    return entry.is_file() and \
           entry.name.endswith('.py') and not \
           re.match(GRADER_FILE_PATTERN, entry.name) and \
           entry.name != __file__


def list_student_submissions():
    returnlist = []

    with scandir('.') as it:
        for entry in it:
            if is_student_submission(entry):
                returnlist.append(entry.name)

    it.close()
    returnlist.sort()
    return returnlist


def display_file_list(flist):
    GRADED_TEMPLATE = '{:2} {} {:>4.1f} {}'
    UNGRADED_TEMPLATE = '{:2} {} ---- {}'

    for idx, element in enumerate(flist):
        if element[1]:
            print(GRADED_TEMPLATE.format(idx+1, GRADED_SYMBOL, element[2], element[0]))
        else:
            print(UNGRADED_TEMPLATE.format(idx+1, 'n', element[0]))


def run_dill_encoded(payload):
    funcref, args = dill.loads(payload)
    return funcref(*args)


def apply_async(pool, args):
    payload = dill.dumps((test_wrapper, args))
    return pool.apply_async(run_dill_encoded, (payload,))


def test_wrapper(test_func, student_module, idx):
    try:
        area_score, reason = test_func(student_module, idx)
    except SystemExit:
        area_score = 0
        reason = 'Before function could return a value, it called exit() or quit(). Do not call exit() or quit().'
    except Exception as ex:
        area_score = 0
        reason = 'Your code generated an error: {}'.format(ex)

    return area_score, reason


def grade_file(grader, assignment_name, flist, idx):
    student_file = flist[idx][0]

    try:
        short_email = re.match(ASSIGNMENT_FILE_PATTERN, student_file)[1]
    except:
        print('Cannot extract short email from {}; using filename.'.format(student_file))
        short_email = student_file[:-3]   # Drop the .py suffix

    # Create an Assignment for this student, and add an Area for the ability to import the student's code.
    # There is no dictionary in GRADING_DATA for this; we know we have to import the student's code, so we
    # just create an Area for that.
    assignment = Assignment(grader, assignment_name, short_email)
    ALL_ASSIGNMENTS.append(assignment)

    able_to_import = Area(IMPORT_AREA_KEY, 'Code can be imported without error', MAX_IMPORT_POINTS)
    assignment.add_area(able_to_import)

    # Let's try to import the student's code
    try:
        student_module = import_module(student_file[:-3])
        assignment.score_area(IMPORT_AREA_KEY, MAX_IMPORT_POINTS, '')
    except Exception as ex:
        assignment.score_area(IMPORT_AREA_KEY, 0, 'We could not import your code. Here is the error message: {}'.format(ex))
        return assignment

    # We imported OK, now run tests
    for idx, test_area in enumerate(grader.GRADING_DATA):
        key = test_area['key']
        test_func = test_area['testfunc']
        new_area = Area(key, test_area['area'], test_area['possiblePoints'])
        assignment.add_area(new_area)

        try:
            # Suppress output from student code
            stdout = sys.stdout
            sys.stdout = FNULL

            # Invoke testfunc, passing it student module
            pool = Pool(1)
            job = apply_async(pool, (test_func, student_module, idx))

            try:
                area_score, reason = job.get(timeout=4)
            except TimeoutError as ex:
                # Probably infinite loop if process didn't respond in time
                area_score = 0
                reason = 'Function never returned; infinite loop?'

            pool.terminate()

            # Restore stdout
            sys.stdout = stdout

            assignment.score_area(key, area_score, reason)
        except Exception as ex:
            assignment.score_area(key, 0, 'Error in your code when testing {}. The error message was "{}".'
                                  .format(test_area['area'], ex))

    # Total up the points
    assignment.calc_score()
    return assignment


def files_left_to_grade(flist):
    for entry in flist:
        if not entry[1]:
            return True
    return False


def dump_grading_results(assignments):
    HEADER_TEMPLATE = '{:36}{:10}\n'
    AREA_TEMPLATE = '{:35}{:2} of {:2}\n'
    CORRECTNESS_TEMPLATE = '{:20}{:>11} = {:>3.1f} of  {:<4.1f}\n'
    EQUATION_TEMPLATE ='({:1}/{:1}) * {:1}'
    FOOTER_TEMPLATE = '{:33}{:>4.1f} of  {:<4.1f}\n'
    DASHED_LINE = '-'*50 + '\n'

    for a in assignments:
        outfile = open('{}/{}_{}_graded.txt'.format(ASSIGNMENT_DIR, a.assignment, a.student), 'w')
        import_area = a.areas['import']

        with outfile as o:
            o.write('Automated Grading Output for {} (Student: {})\n\n'.format(a.assignment, a.student))
            o.write(HEADER_TEMPLATE.format('Grading Area', 'Points'))
            o.write(DASHED_LINE)
            o.write(AREA_TEMPLATE.format(import_area.area, import_area.actualPoints, import_area.possiblePoints))
            if len(import_area.reasons) > 0:
                o.write('    {}\n'.format(import_area.reasons[0]))
            o.write(DASHED_LINE)
            for area in list(a.areas.values())[1:]:
                o.write(AREA_TEMPLATE.format(area.area, area.actualPoints, area.possiblePoints))
                if len(area.reasons) > 0:
                    for reason in area.reasons:
                        o.write('    {}\n'.format(reason))
            o.write(DASHED_LINE)
            o.write(CORRECTNESS_TEMPLATE.format(
                'Correctness Points',
                EQUATION_TEMPLATE.format(a.graderScore, a.grader.MAX_POINTS, MAX_CORRECTNESS_POINTS),
                a.actualScore - import_area.possiblePoints,
                MAX_CORRECTNESS_POINTS
            ))
            o.write(DASHED_LINE)
            o.write(FOOTER_TEMPLATE.format('Total', a.actualScore, float(a.possibleScore)))
        outfile.close()


# If the provided progress filename exists, load its data and return that list.
# Otherwise, initialize a new list of assignment files and return it.
def load_grading_progress(fname):
    try:
        with open(fname) as grading_progress_file:
            assignment_files = json.load(grading_progress_file)
    except:
        assignment_files = []
        for filename in list_student_submissions():
            assignment_files.append([filename, False, 0])
    return assignment_files


def save_grading_progress(assignments, fname):
    with open(fname, 'w') as grading_progress_file:
        json.dump(assignments, grading_progress_file)


def get_fnames_from_dir(dir, file_extension):
    for fname in listdir(dir):
        if fname.endswith(file_extension):
            yield fname


def fetch_students():
    url = STUDENT_URL.format(COURSE_ID)
    per_page = 10
    payload = {'enrollment_type': 'student', 'per_page': per_page}
    AUTH_HEADER = {'Authorization': 'Bearer {}'.format(AUTH_TOKEN)}


    resp = requests.get(url, headers=AUTH_HEADER, params=payload)
    students = json.loads(resp.text)

    while 'next' in resp.links:
        nexturl = resp.links['next']['url']
        resp = requests.get(nexturl, headers=AUTH_HEADER)
        students += json.loads(resp.text)

    # Go back and fetch test_student; can be handy during development
    payload = {'enrollment_type': 'student_view'}
    resp = requests.get(url, headers=AUTH_HEADER, params=payload)
    test_student = json.loads(resp.text)
    students += test_student

    return students


def run_grader():
    # First read in our assignment grader file, or quit if that fails.
    assignment = input('Enter the name of the assignment to be graded, e.g., PS1: ').upper()
    try:
        grader = import_module('{}_GRADER'.format(assignment))
    except Exception as ex:
        print('Cannot import {}_GRADER module; error={}. Exiting.'.format(assignment, ex))
        exit()

    # Load in our grading progress thus far, which is represented as a list of lists.
    # Each inner list contains 3 elements that describe a given student submission as follows:
    #    string    the filename
    #    boolean   True if we have graded this file, False otherwise
    #    int       total score for the assignment (so user can see scores as files are graded)

    grading_progress_fname = '{}/{}_PROGRESS.txt'.format(ASSIGNMENT_DIR, assignment)
    assignment_files = load_grading_progress(grading_progress_fname)

    show_anyway = False

    while True:
        if files_left_to_grade(assignment_files) or show_anyway:
            display_file_list(assignment_files)
            filenum = input('Enter file number, from-to range, or q to quit & write files: ')
            if filenum in ['q', 'Q']:
                break
            elif '-' in filenum:
                file_from, file_to = [int(x) for x in filenum.replace(' ', '').split('-')]
            else:
                file_from = int(filenum)
                file_to = file_from

            for fnum in range(file_from, file_to + 1):
                assignment_object = grade_file(grader, assignment, assignment_files, fnum-1)
                assignment_files[fnum - 1][1] = True  # Indicate that we have graded this file
                assignment_files[fnum - 1][2] = assignment_object.actualScore
        else:
            response = input('All files graded. Want to revisit any? [y/n/q]')
            if response in ['y', 'Y']:
                show_anyway = True
            else:
                break

    print('Writing output files...', end='')
    dump_grading_results(ALL_ASSIGNMENTS)
    save_grading_progress(assignment_files, grading_progress_fname)
    print('Done.')


def run_upload():
    global AUTH_TOKEN, COURSE_ID

    if not AUTH_TOKEN:
        token_files = []
        for tf in get_fnames_from_dir(os.curdir, '.token'):
            token_files.append(tf)

        if len(token_files) == 0:
            print('Cannot find any auth token files; will not be able to upload.\n')
            return

        for idx, fname in enumerate(token_files):
            print(f'{idx+1:3}  {fname}')
        tfnum = int(input('Select an auth token file: '))
        f = open(token_files[tfnum-1], 'r')
        AUTH_TOKEN = f.readline().rstrip('\n')
        f.close()

    course_id_ok = input(f'Using COURSE_ID {COURSE_ID}, OK? ').lower() or 'y'
    if course_id_ok not in ['y', 'yes']:
        COURSE_ID = input('Enter the COURSE_ID to use: ')

    assignment_id = input('Enter the assignment id: ')

    uploader = FileUpload(COURSE_ID, AUTH_TOKEN)

    # Fetch student names and ids so we can match the grader output files
    # to students. The grader bases its output filenames on the filenames that
    # Canvas assigned when downloading the assignments. Canvas appears to base
    # the downloaded filenames on its sortable_name field, converted to lowercase
    # and stripped of punctuation.

    try:
        print('Fetching students...')
        students = fetch_students()
        print('Done.\n')
    except Exception as ex:
        print(f'Error fetching students: {ex}')

    student_lookup = {}
    for student in students:
        keyname = ''.join([c.lower() for c in student['sortable_name'] if c.isalpha()])
        student_lookup[keyname] = student

    grader_files = []
    for grader_file in get_fnames_from_dir(OUTPUT_DIR, '.txt'):
        grader_files.append(grader_file)

    while True:
        for idx, grader_file in enumerate(grader_files):
            print(f'{idx+1:3}  {grader_file}')

        filenum = input('\nEnter file number, from-to range, or q to stop uploading: ')
        if filenum in ['q', 'Q']:
            break
        elif '-' in filenum:
            file_from, file_to = [int(x) for x in filenum.replace(' ', '').split('-')]
        else:
            file_from = int(filenum)
            file_to = file_from

        for fnum in range(file_from, file_to + 1):
            fname = grader_files[fnum - 1]
            student_name = fname.split('_')[1]
            try:
                student_id = student_lookup[student_name]['id']
            except:
                print(f'\nCannot match this filename to a student: {fname}')
                print('Select the student from the following list:\n')

                for sidx, student in enumerate(students):
                    print(f"{sidx+1: 3}  {student['name']}")

                snum = int(input('Which student? '))
                keyname = ''.join([c.lower() for c in students[snum-1]['sortable_name'] if c.isalpha()])
                student_id = student_lookup[keyname]['id']

            # Try to parse the score from the grader file.
            score = None
            gfilepath = '{}/{}'.format(OUTPUT_DIR, fname)

            with open(gfilepath, 'r') as gfile:
                line = gfile.readline()
                while line:
                    if line.startswith('Total'):
                        score = float(line.split()[1])
                        break
                    else:
                        line = gfile.readline()

            if not score:
                score = float(input(f'Cannot read score from {fname}; enter score: '))

            file_id = uploader.upload_file(assignment_id, student_id, gfilepath)
            success = uploader.attach_file_and_post_grade(assignment_id, student_id, file_id, grade=score)

            if not success:
                print(f'\n**ERROR** : {fname} not uploaded\n')


if __name__ == '__main__':
    print('Core Grader version {}\n'.format(VERSION))

    while True:
        action = input('Do you want to grade [g], upload [u], or quit [q]? ').lower()
        if action == 'q':
            break
        elif action == 'g':
            win = Tk()
            win.withdraw()
            ASSIGNMENT_DIR = filedialog.askdirectory(title="Where are the files?", initialdir=ASSIGNMENT_DIR)
            win.destroy()
            sys.path.append(ASSIGNMENT_DIR)
            run_grader()
        elif action == 'u':
            win = Tk()
            win.withdraw()
            OUTPUT_DIR = filedialog.askdirectory(title="Where are the files?", initialdir=ASSIGNMENT_DIR)
            win.destroy()
            run_upload()
        else:
            print('Enter a valid action letter')
