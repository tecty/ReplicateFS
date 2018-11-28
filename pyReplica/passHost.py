#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno


from fuse import FUSE, FuseOSError, Operations
from Journal import Journal
import Constants

from Callbacks import Callbacks as cb 
import base64


"""
Rewrite the write callback, to gain little performance 
"""
def do_write_local(data):
    # seek and write the data use local fd 
    # this will boost the performance, because we don't have onetime 
    # fd to modify the file 
    os.lseek(data['fh'], data['offset'], data['SEEK_SET'])
    return os.write(
        data['fh'], 
        base64.standard_b64decode(data['buf'])
    )
    
cb[Constants.J_WRITE] = do_write_local




class Passthrough(Operations):
    def __init__(self, root):
        # setup as a path constant in constant 
        Constants.PATH = root

        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        print("Chmod at ", path, "to mode ", mode)
        full_path = self._full_path(path)
        print("full path is ", full_path)
        
        # return os.chmod(full_path, mode)
        return cb[Constants.J_CHMOD]({
            'path': str(path), 
            'mode': mode
        })

    def chown(self, path, uid, gid):
        print("Chown at", path, "uid:", uid, "gid", gid)
        # full_path = self._full_path(path)
        # return os.chown(full_path, uid, gid)
        return cb[Constants.J_CHOWN]({
            'path': str(path),
            'uid': uid,
            'gid': gid
        })


    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

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

    def mknod(self, path, mode, dev):
        # path = self._full_path(path)
        print("Mknod at ",path)
        # return os.mknod(path, mode, dev)
        return cb[Constants.J_MKNOD]({
            'path': path,
            'mode': mode,
            'dev': dev 
        })

    def rmdir(self, path):
        path = self._full_path(path)
        print("Rmdir at ",path)
        # return os.rmdir(path)
        return cb[Constants.J_RMDIR]({
            'path': str(path)
        })

    def mkdir(self, path, mode):
        print("Mkdir at ",path)
        # return os.mkdir(self._full_path(path), mode)
        return cb[Constants.J_MKDIR]({
            'path': path,
            'mode': mode
        })

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("Unlink from",path)
        # return os.unlink(self._full_path(path))
        return cb[Constants.J_UNLINK]({
            'path':path
        })

    def symlink(self, name, target):
        """
        This method should be deprecate ? 
        """
        print("Symlink from", name, " to ", target)
        # return os.symlink(name, self._full_path(target))
        return cb[Constants.J_SYMLINK]({
            'src': str(name),
            'dest': str(target)
        })

    def rename(self, old, new):
        print("Rename from", old, " to ", new)
        # return os.rename(self._full_path(old), self._full_path(new))
        return cb[Constants.J_RENAME]({
            'old': str(old),
            'new': str(new)
        })

    def link(self, target, name):
        print("Link to", target)
        # return os.link(self._full_path(target), self._full_path(name))
        return cb[Constants.J_LINK]({
            'name': name, 
            'target': target
        })

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        # this should be more careful 
        print("Write to", path)
        # return os.write(fh, buf)
        return cb[Constants.J_WRITE]({
            'fh': fh, 
            'offset': offset,
            'path': path,
            'SEEK_SET':os.SEEK_SET,
            'buf': base64.standard_b64encode(buf),
        })

    def truncate(self, path, length, fh=None):
        print("Truncate to", path)
        # full_path = self._full_path(path)
        # with open(full_path, 'r+') as f:
        #     f.truncate(length)
        return cb[Constants.J_TRUNCATE]({
            'path': path,
            'length': length
        })


    def flush(self, path, fh):
        # use local call, because remote doesn't 
        # have same fd
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    parser.add_argument('root')
    args = parser.parse_args()
    main(args.mount, args.root)