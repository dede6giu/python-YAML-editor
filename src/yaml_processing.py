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

def startup(directory: str, *, extension: str = '.md', debugmode=False):
    if directory == '' or directory == None:
        ProcessError("Directory must not be empty")
    
    if not is_valid_filepath(directory):
        ProcessError("Directory must be valid")

    for filepath in glob.glob(directory + '/**/*' + extension, recursive=True):
        content: str = ""
        config: dict = {}

        if debugmode: print(f"Working on: {filepath}")

        # separating YAML from file content
        with open(filepath, "r", encoding='UTF8') as f:
            config = yaml.safe_load(get_yaml(f))
            if config == '' or config == None: 
                if debugmode: print("    Result: Empty / No YAML")
                continue
            content = get_content(f)
        
        # processing
        try:
            config = main_task(config)
        except:
            print(f"     ERROR: Some unkown ERROR ocurred while processing {filepath}")
            continue

        # yaml dump
        with open(filepath, "w", encoding='UTF8') as f:
            f.write('---\n')
            f.write(yaml.dump(config))
            f.write('---\n')
            f.write(content)
            if debugmode: print(f"    Result: Success!")
    else:
        print("----------\nAll finished!")