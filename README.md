# Python Assignment Grader (with Canvas LMS integration)

This is work in progress to make some code that I wrote for personal use a bit more generally useful
to others.

Do you teach programming with the Python language? This code will help you grade coding assignments.
It will grade for correctness, that is, whether a student's code does what you asked for. It
won't grade for elegance or efficiency (no AI here!), but if you're willing to write some tests
(also in Python), this code will:
* retrieve your roster from Canvas LMS
* run your tests against each student's assignment
* total the points for the tests that passed
* create a small report detailing the tests that were run and the points earned
* upload each report file to Canvas LMS, attached to the appropriate student and the appropriate assignment
* set the grade (the points earned) on the assignment in Canvas

Of course, the Canvas parts expect that your institution uses Canvas and that you have a token
that permits you to use the API. (Where I teach, I was able to create my own token right in Canvas.
It isn't a big deal -- your Canvas token only lets you modify your own courses.)

## Overview of How This Works

Suppose you want to grade a coding assignment for your first problem set, call it _PS1_.
You have to perform these steps:
* Write an "assignment grader" file that contains Python code to test your students' work. Exactly
what goes in this file is detailed below. This will be easy to write for someone who teaches programming.
* Determine the Canvas Course ID for your course (instructions below)
* Determine the Canvas Assignment ID for the assignment you are grading (instructions below)
* Download student submissions for the assignment and place the files in a folder anywhere on your computer
* Run the GraderCore.py program

### What goes in the _assignment grader_ file

A sample assignment grader file is included here in Github -- it's named _PS1_GRADER.py_. Any
assignment grader you create must be named _zzz_GRADER.py_, where _zzz_ is a prefix that you invent; the
__GRADER.py_ part of the filename is required. The sample is named _PS1_GRADER.py_ to stand for "Problem Set 1."
Let's look at the contents of the assignment grader file, starting at the bottom of the file.

1. Your file must define a list of dictionaries named _GRADING_DATA_ (in uppercase). This must be defined
in the global scope because the grading "engine" will import your assignment grader and expect to
find this symbol.

2. Before the GRADING_DATA list, define functions that, if called, would test some aspect of the assignment.

3. At the top of the assignment grader file, set MAX_POINTS to the maximum number of points a student
can earn for this assignment _based on what you are testing with this grading engine_. Remember that
the grading engine is only assessing correctness based on tests you write. If _all_ the points for
the assignment will be determined by this grading engine, set MAX_POINTS to a perfect score on the
assignment. However, if you will read student code for structure and overall quality, you might
only have the grading engine assess _some_ of the points for the assignment; maybe a 10-point
assignment can get up to 8 points from the grading engine for correctness, and you will give up
to 2 points for code quality. In that scenario, set MAX_POINTS to 8.

### Exactly what goes in the GRADING_DATA list?

Each dictionary in the GRADING_DATA list describes one test that you
want to run on your students' code. Here's a sample of one of these dictionaries:

```
{
    "key": "loan_pmt",
    "area": "Loan payment calculation",
    "testfunc": test_payment_calculator,
    "possiblePoints": 3
}
```

The attributes of each dictionary are as follows:

|Dictionary Key|Value|
|---|-----|
|key| A short string that identifies this test. It must be unique across all the dictionaries in your GRADING_DATA list. Also, this value must meet Python's rules for being a valid dictionary key (because the grading engine will use it that way internally).|
|area| A user-friendly name (string) for the aspect of the assignment that this test focuses on. For example, if an assignment requires students to calculate a loan payment, you might set _area_ to "Loan payment calculation."| 
|testfunc|A function that, when called, tests something particular about the assignment. This function must be defined earlier in the assignment grader module. There are no rules for the name of a _testfunc_. See below for details on what one of these functions receives as arguments and what it must return.|
|possiblePoints|The number of points this test is worth.|

Each dictionary describes one test to run. What a test actually exercises in student code is up to you.
Each dictionary specifies a _testfunc_, that is, a function you write. For every dictionary in the
GRADING_DATA list, the grading engine calls that dictionary's _testfunc_.

Typically, my assignments require students to write functions, and I write one _testfunc_
per function in the assignment. You are free to write as many _testfuncs_ as you want, though.
Just create a dictionary for each one.

A _testfunc_ function...
* will receive two arguments: the student module that is being tested, and the integer index of this test in the GRADING_DATA list.
* must return a tuple consisting of an integer and a string; the integer is the number of points earned from the test (0 or greater), and the string gives a reason for the score. The string may be empty ('') for the case when the student earned full points and you don't need to supply a reason.
* will usually call a function in the student's code, passing some arguments and expecting to receive a certain returned value. A testfunc doesn't _have to_ call functions in your students' code, however -- it can exercise their code however you choose to.

### Determining the Canvas IDs you need

This is easy -- navigate to your course in Canvas, and then navigate to a particular assignment
you want to grade. Look at your browser's address line. You will see something like this:
```
https://yourschool.instructure.com/courses/9876543/assignments/1234567
```

The number after `courses/` is your Course ID, and the number after `assignments/` is your Assignment ID.

## Running the Grading Engine

### Before you run it

1. Get a Canvas API token and put it in a file whose name ends in _.token_. Put this file in the same folder with the GraderCore.py file.
1. Write a _zzz_GRADER.py_ assignment grader file (described above). Put it in the same folder with the GraderCore.py file.
1. Download student assignments into a folder. This can be anywhere you want; student files do not need to be in the same folder as the GraderCore.py. If Canvas gives you a .zip file, you have to unzip it.

### To run it

To run the grading engine:
1. Open a Terminal (Mac) or Command Prompt (Windows).
1. Navigate to the folder where your GraderCore.py file is located
1. Run this command: `python GraderCore.py`

The grader will issue this prompt: `Do you want to grade [g], upload [u], or quit [q]?` Enter a `g`.
The grader will then prompt you for some values:
* **Location of student files** The grader will open a file selection dialog (based on the Python _tkinter_ module). Navigate to the folder where you have put the student code files and click OK in the dialog.
* **Assignment name** When you are asked to enter the name of the assignment, enter only the prefix part of the assignment grader's filename. For example, for the sample _PS1_GRADER.py_, you would enter _PS1_. If there is more than one file in the folder starting with the prefix you entered, the grader will print a list of them and ask you to pick one by number.
* 

# Work in progress ... more to come ...
