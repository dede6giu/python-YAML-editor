from yaml_processing import startup

if __name__ == '__main__':
    # Choose the directory to apply the effect, use relative path.
    # The code in task.py will process on every .md file in the directory
    # Optionally, run the parameter 'extension' to choose some other extension
    # Do note the code will only work in pure text files!
    
    directory: str = 'test/'
    startup(directory, extension='.md')