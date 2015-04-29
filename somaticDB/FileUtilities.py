import os
import sys
from git import Repo

def is_dir_empty(directory):
    return len(os.listdir(directory)) == 0


def safe_mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def spawn_daemon():
    try:
        pid = os.fork()
        if pid > 0:
            return False #first parent
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    return True # spawned process


def get_git_branch(directory):
    try:
        repo = Repo(directory)
        branch = repo.active_branch
        return str(branch.name)
    except:
        return None
