import re

#converting functions

def convert_column_to_comma_list(
    text, 
    delimiter=',', 
    item_prefix='', 
    item_suffix='', 
    result_prefix='', 
    result_suffix='', 
    dedupe=False,
    sort_order=None):
    # split and strip; drop empty lines
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if dedupe:
        # use dict.fromkeys to remove duplicates but keep first-seen order
        lines = list(dict.fromkeys(lines))

   # --- SORTING ---
    if sort_order == 'asc':
        lines = sorted(lines)
    elif sort_order == 'desc':
        lines = sorted(lines, reverse=True)

    # wrap each line, then join
    processed_items = [f"{item_prefix}{line}{item_suffix}" for line in lines]
    return f"{result_prefix}{delimiter.join(processed_items)}{result_suffix}"

def convert_comma_to_column(
    text, 
    delimiter=',', 
    result_prefix='', 
    result_suffix='', 
    dedupe=False,
    sort_order=None):
    
    # strip off leading/trailing whitespace, then split
    items = [item.strip() for item in text.strip().split(delimiter)]

    if dedupe:
        # use dict.fromkeys to remove duplicates but keep first-seen order
        items = list(dict.fromkeys(items))

       # --- SORTING ---
    if sort_order == 'asc':
        items = sorted(items)
    elif sort_order == 'desc':
        items = sorted(items, reverse=True)
    
    # drop any empty strings
    lines = [item for item in items if item]
    
    result = "\n".join(lines)

    # strip any leading/trailing blank lines or spaces:
    return f"{result_prefix}{result.strip()}{result_suffix}"

def convert_change_case(text, case_option):
    if case_option == 'upper':
        return text.upper()
    elif case_option == 'lower':
        return text.lower()
    elif case_option == 'title':
        return text.title()
    elif case_option == 'capitalize':
        return text.capitalize()
    elif case_option in ('snake', 'kebab'):
        # split on non-word chars, lowercase, then join with '_' or '-'
        sep = '_' if case_option == 'snake' else '-'
        words = re.findall(r'\w+', text.lower())
        return sep.join(words)
    else:
        return text 
