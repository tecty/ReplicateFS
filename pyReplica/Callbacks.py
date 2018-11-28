import traceback
import Constants
import os 
import json 

def get_full_path(partial):
    if partial.startswith("/"):
        partial = partial[1:]
    path = os.path.join(Constants.PATH, partial)
    return path 

def dump_data(data):
    print (json.dumps(data))

def do_chmod(data):
    """
    data['path'] and data['mode']
    """
    print (Constants.PATH)

    dump_data(data)

    return os.chmod(get_full_path(data['path']), data['mode'])

def do_chown(data):
    """
    data['path']
    data['uid']
    data['gid']
    """
    return os.chown(get_full_path(data['path']), data['uid'], data['gid'])

def do_mknod(data):
    """
    data['path']
    data['mode'] 
    data['dev'] 
    """
    return os.mknod(get_full_path(data['path']),data['mode'],data['dev'])

def do_rmdir(data):
    """
    data['path']
    """
    return os.rmdir(get_full_path(data['path']))
def do_mkdir(data):
    """
    data['path']
    data['mode']
    """
    return os.mkdir(data['path'], data['mode'])
def do_unlink(data):
    """
    data['path']
    """
    return os.unlink(get_full_path(data['path']))
def do_symlink(data):
    """
    data['path']
    """
    return os.symlink(get_full_path(data['path']))
def do_rename(data):
    """
    data['old']
    data['new']
    """
    return os.rename(
        get_full_path(data['old']),
        get_full_path(data['new'])
    )
def do_link(data):
    """
    data.
    """
    return os.link(
        get_full_path(data['target']),
        get_full_path(data['name'])
    )
def do_write(data):
    """
    data['fh']
    data['offset']
    data['SEEK_SET']
    data['buf'] 
    data['fh']
    """
    os.lseek(data['fh'], data['offset'], data['SEEK_SET'])
    #! buf, fh may not be a string 
    return os.write(data['fh'], data['buf'])
def do_truncate(data):
    """
    data['path'] 
    data['length'] 
    """
    with open(get_full_path(data['path'])) as f: 
        return f.truncate(data['length'])
    return False
    
def do_fulsh(data):
    """
    data['path']
    data['fh']
    """
    #! the FH may not be the string
    return os.fsync(data['fh'])

# the mappings 
Callbacks = {
    Constants.J_CHMOD: do_chmod,
    Constants.J_CHOWN: do_chown,
    Constants.J_MKNOD: do_mknod,
    Constants.J_RMDIR: do_rmdir,
    Constants.J_MKDIR: do_mkdir,
    Constants.J_UNLINK: do_unlink,
    Constants.J_SYMLINK: do_symlink,
    Constants.J_RENAME: do_rename,
    Constants.J_LINK: do_link,
    Constants.J_WRITE: do_write,
    Constants.J_TRUNCATE: do_truncate,
    Constants.J_FULSH: do_fulsh
}