def go_over_file(file, action):
    """ 
    runs the provided callable on all lines of the provided file 
    """
    
    f = open(file)
    for line in f:
        # remove newline
        actual_line = line[:-1]
        action(actual_line)
    f.close()

