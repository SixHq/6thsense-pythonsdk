import os
import fcntl
import pickledb

class PickleDBWithLock(pickledb.PickleDB):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)
        self.lockfile = os.path.abspath(filename) + ".lock"

    def acquire_lock(self):
        self.lock = open(self.lockfile, "w")
        try:
            fcntl.lockf(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            self.lock.close()
            raise

    def release_lock(self):
        self.lock.close()