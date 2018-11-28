"""
State of journal
"""
S_RUNNING = 1
S_LOCKED = 2
S_FLUSH = 3
S_COMMIT = 4 
S_FINISHED = 5

"""
Type of operations 
Type of Journal?
"""
J_CHMOD = 1
J_CHOWN = 2
J_MKNOD = 3
J_RMDIR = 4
J_MKDIR = 5
J_UNLINK = 6
J_SYMLINK = 7
J_RENAME = 8
J_LINK = 9
J_WRITE = 10
J_TRUNCATE = 11
J_FULSH = 12

# Path we need to join 
PATH = "/"