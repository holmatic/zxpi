'''
File and directory handling 


Created on 19.03.2019

@author: Holmatic
'''


from pathlib import Path



def get_zxpi_root():
    #return Path.cwd()/'zxroot'
    return Path.cwd().parent/'zxroot'

def get_base_work_path():
    return get_zxpi_root()/'user-files'

def check_create_dirs():
    f=get_base_work_path()
    if f.exists():
        print("%s exist"%(str(f)))
    else:
        f.mkdir(parents=True)
        

def get_current_work_path():
    return get_base_work_path()