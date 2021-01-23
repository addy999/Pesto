import glob 
import os 

def test_suites(test_file: str):
    assert os.path.isfile(test_file)
    
    

def find_test_files(dir: str) -> list:
    '''
    Find test files that match the following naming patter:
    - *test.py
    - test*.py
    
    Search is recursive, so pass in only the parent directory for search
    '''
    assert os.path.isdir(dir)
    # abs_dir = os.path.abspath(dir)
    return glob.glob(dir + "**/*test*.py", recursive=True)
    