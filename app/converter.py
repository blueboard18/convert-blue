#converting functions

def convert_column_to_comma_list(text, delimiter=',', item_prefix='', item_suffix='', result_prefix='', result_suffix='', dedupe=False):
    # split and strip; drop empty lines
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if dedupe:
        # use dict.fromkeys to remove duplicates but keep first-seen order
        lines = list(dict.fromkeys(lines))

    # wrap each line, then join
    processed_items = [f"{item_prefix}{line}{item_suffix}" for line in lines]
    return f"{result_prefix}{delimiter.join(processed_items)}{result_suffix}"

def convert_comma_to_column(text, delimiter=',', result_prefix='', result_suffix='', dedupe=False):
    # strip off leading/trailing whitespace, then split
    items = [item.strip() for item in text.strip().split(delimiter)]

    if dedupe:
        # use dict.fromkeys to remove duplicates but keep first-seen order
        items = list(dict.fromkeys(items))
    
    # drop any empty strings
    lines = [item for item in items if item]
    
    result = "\n".join(lines)
    # strip any leading/trailing blank lines or spaces:
    return f"{result_prefix}{result.strip()}{result_suffix}"
