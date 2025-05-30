import re
from PIL import Image
import io

# numeric-aware sort key: tuples ensure floats only compare to floats,
# and strings only to strings
def numeric_key(val):
    try:
        # group 0 = real numbers
        return (0, float(val))
    except ValueError:
        # group 1 = anything else, sorted lexicographically
        return (1, val)

# helper to dedupe & sort uniformly
def process_items(items, dedupe=False, sort_order=None):
    if dedupe:
        items = list(dict.fromkeys(items))
    if sort_order == 'asc':
        items = sorted(items, key=numeric_key)
    elif sort_order == 'desc':
        items = sorted(items, key=numeric_key, reverse=True)
    return items

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
    lines = process_items(lines, dedupe=dedupe, sort_order=sort_order)

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
    
    # split on delimiter, strip whitespace, drop empty entries
    items = [
        item.strip()
        for item in text.strip().split(delimiter)
        if item.strip()
    ]

    # dedupe & sort using your shared helper
    items = process_items(items, dedupe=dedupe, sort_order=sort_order)

    # join into lines
    result = "\n".join(items)

    # wrap with prefix/suffix and return
    return f"{result_prefix}{result}{result_suffix}"

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

def convert_find_replace(text, find_str, replace_str):
    return text.replace(find_str, replace_str)

def extract_text_between_chars(text, start_char, end_char, dedupe=False, sort_order=None, reverse=False):

    # escape user inputs in case they include regex symbols
    re_start = re.escape(start_char)
    re_end   = re.escape(end_char)
    pattern = rf'{re_start}(.*?){re_end}'

    # clean up lines
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    
    if reverse:
        # Remove the matched portion (start_char through end_char)
        processed = [re.sub(pattern, '', line) for line in lines]
    else:
        # Extract only the matched content
        processed = [match.group(1) for line in lines if (match := re.search(pattern, line))]

    # Apply deduplication and sorting
    processed = process_items(processed, dedupe=dedupe, sort_order=sort_order)
    return "\n".join(processed)

def convert_image_dpi(image, new_dpi):
    buffer = io.BytesIO()
    image.save(buffer, format=image.format, dpi=(new_dpi, new_dpi))
    buffer.seek(0)
    return buffer, image.format
