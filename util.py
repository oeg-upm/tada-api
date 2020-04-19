

# from OME
def get_headers_csv(file_dir):
    f = open(file_dir)
    header_str = ""
    for line in f.readlines():
        header_str = line
        break

    header = []
    start_q = False
    start_idx = 0
    print("header_string: "+header_str)
    for idx, ch in enumerate(header_str):
        if ch == '"' and start_q == True:
            start_q = False
        elif ch=='"':
            start_q = True
        elif ch=="," and start_q == False:
            curr = header_str[start_idx:idx]
            header.append(curr)
            start_idx = idx+1
    header.append(header_str[start_idx:])

    return header
