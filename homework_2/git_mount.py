import os
import sys
import re

from fuse import FUSE, Operations


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    @staticmethod
    def _update_repo(full_path):
        if not os.path.isdir(full_path):
            full_path = os.path.dirname(full_path)
        os.system(f'git -C "{full_path}" reset --hard origin')
        os.system(f'git -C "{full_path}" pull')

    # Filesystem methods
    # ==================

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        self._update_repo(full_path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        self._update_repo(full_path)
        return os.open(full_path, flags)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)


def main(root, mountpoint):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    mo = re.search(r"/([a-zA-Z0-9_-]*)\.git", sys.argv[1])
    rep_dir = mo.group(1)
    rep_dir = os.path.join('repos', rep_dir)

    if not os.path.exists('repos'):
        os.mkdir('repos')
        if not os.path.exists(rep_dir):
            os.mkdir(rep_dir)
            os.system(f'git clone {sys.argv[1]} {rep_dir}')

    main(rep_dir, sys.argv[2])
