import yaml
import glob
from pathvalidate import is_valid_filepath
from task import main_task

class ProcessError(Exception):
    pass # custom class error

def get_yaml(f) -> str:
    result: str = ''
    nextl: str = f.readline()
    if (nextl != '---\n'):
        return result
    while True:
        nextl = f.readline()
        if (nextl != '---\n'):
            result += nextl
        else:
            return result[:-1]

def get_content(f) -> str:
    result: str = ''
    nextl: str = f.readline()
    while nextl:
        result += nextl
        nextl = f.readline()
    return result

def startup(directory: str, *, extension: str = '.md'):
    if directory == '' or directory == None:
        ProcessError("Directory must not be empty.")
    
    if not is_valid_filepath(directory):
        ProcessError("Directory must be valid")

    for filepath in glob.glob(directory + '/**/*' + extension, recursive=True):
        content: str = ""
        config: dict = {}

        # separating YAML from file content
        with open(filepath, "r") as f:
            config = yaml.safe_load(get_yaml(f))
            if config == '' or config == None: continue # no/empty YAML
            content = get_content(f)
        
        # processing
        config = main_task(config)
        
        # yaml dump
        with open(filepath, "w") as f:
            f.write('---\n')
            f.write(yaml.dump(config))
            f.write('---\n')
            f.write(content)
    else:
        print("All finished!")