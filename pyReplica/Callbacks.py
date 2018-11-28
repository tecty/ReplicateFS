import traceback
import Constants
import os 
import json 
import base64
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

    dump_data(data)
    return os.chmod(get_full_path(data['path']), data['mode'])

def do_chown(data):
    """
    data['path']
    data['uid']
    data['gid']
    """
    dump_data(data)
    return os.chown(get_full_path(data['path']), data['uid'], data['gid'])

def do_mknod(data):
    """
    data['path']
    data['mode'] 
    data['dev'] 
    """
    dump_data(data)
    return os.mknod(get_full_path(data['path']),data['mode'],data['dev'])

def do_rmdir(data):
    """
    data['path']
    """
    dump_data(data)
    return os.rmdir(get_full_path(data['path']))
def do_mkdir(data):
    """
    data['path']
    data['mode']
    """
    dump_data(data)
    return os.mkdir(data['path'], data['mode'])
def do_unlink(data):
    """
    data['path']
    """
    dump_data(data)
    return os.unlink(get_full_path(data['path']))
def do_symlink(data):
    """
    data['src']
    data['dest']
    """
    dump_data(data)
    return os.symlink(
        data['src'],
        get_full_path(data['dest'])
    )
def do_rename(data):
    """
    data['old']
    data['new']
    """
    dump_data(data)
    return os.rename(
        get_full_path(data['old']),
        get_full_path(data['new'])
    )
def do_link(data):
    """
    data['target']
    data['name']
    """
    dump_data(data)
    return os.link(
        get_full_path(data['target']),
        get_full_path(data['name'])
    )
def do_write(data):
    """
    data['offset']
    data['path']
    data['SEEK_SET']
    data['buf'] 
    """
    #! buf, fh may not be a string 
    dump_data(data)
    # open the path, use only once and close 
    fd = os.open(get_full_path(data['path']), os.O_WRONLY)
    # seek to position and write 
    os.lseek(fd, data['offset'], data['SEEK_SET'])
    # store the result temporary 
    res = os.write(fd, base64.standard_b64decode(data['buf']))
    # close the obj 
    os.close(fd)     
    return res 
def do_truncate(data):
    """
    data['path'] 
    data['length'] 
    """
    dump_data(data)
    with open(get_full_path(data['path'])) as f: 
        return f.truncate(data['length'])
    return False
    
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
}