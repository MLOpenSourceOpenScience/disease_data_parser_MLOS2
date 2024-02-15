import re




def make_valid_filename(filename: str)-> str:
    #Remove invalid characters from filename
    for c in '#%&{}\<>*?/$!\'\":@+`|=,':
        filename = filename.replace(c,'')
    return filename
    #return re.sub('#%&{}\<>*?/$!\'\":@+`|=','', filename)


if __name__ == '__main__':
    filename = 'line 124, in <module>'
    print(make_valid_filename(filename))