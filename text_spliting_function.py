# Define helper function to split text
import re

def split(txt, seps):

    
    """
    Splits a given text string based on multiple separators, extracts date patterns, and converts numeric substrings to integers.
    
    Args:
        txt (str): The input text string to split.
        seps (list): A list of separator characters to use for splitting the input text.
    
    Returns:
        list: A list containing the split text elements, with numeric elements converted to integers and date patterns as integers.
    
    Example:
        >>> split("Invoice 123, 10/11/2022", [',', ';', ' ', '_'])
        ['Invoice', 123, 10112022]
    """
    
    default_sep = seps[0]

    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)

    pattern = r"\d{2}/\d{2}/\d{4}"
    matches = re.findall(pattern, txt)
    txt = re.sub(pattern, "", txt)

    lst = [i.strip() for i in txt.split(default_sep)]

    for i in range(len(lst)):
        if lst[i].isdigit():
            lst[i] = int(lst[i])
        elif lst[i].replace(".", "", 1).isdigit():
            lst[i] = int(float(lst[i]))

    for match in matches:
        match_int = int(match.replace("/", ""))
        lst.append(match_int)

    return lst

