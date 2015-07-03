import os
import time
import subprocess

from sniffer.api import select_runnable, file_validator, runnable
try:
    from pync import Notifier
except ImportError:
    notify = None
else:
    notify = Notifier.notify


watch_paths = ['mine/', 'tests/']
show_coverage = True


@select_runnable('python_tests')
@file_validator
def py_files(filename):
    return all((filename.endswith('.py'),
               not os.path.basename(filename).startswith('.')))


@runnable
def python_tests(*args):

    group = int(time.time())  # unique per run

    for count, (command, title) in enumerate((
        (('make', 'test-unit'), "Unit Tests"),
        (('make', 'test-int'), "Integration Tests"),
        (('make', 'test-all'), "Combined Tests"),
        (('make', 'check'), "Static Analysis"),
        (('make', 'doc'), None),
    ), start=1):

        print("")
        print("$ %s" % ' '.join(command))
        os.environ['TEST_IDE'] = '1'
        failure = subprocess.call(command, env=os.environ)

        if failure:
            if notify and title:
                mark = "❌" * count
                notify(mark + " [FAIL] " + mark, title=title, group=group)
            return False
        else:
            if notify and title:
                mark = "✅" * count
                notify(mark + " [PASS] " + mark, title=title, group=group)

    global show_coverage
    if show_coverage:
        subprocess.call(['make', 'read-coverage'])
    show_coverage = False

    return True
