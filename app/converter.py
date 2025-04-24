def convert_column_to_comma_list(text, delimiter=',', item_prefix='', item_suffix='', result_prefix='', result_suffix='', dedupe=False):
    
    # split and strip; drop empty lines
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if dedupe:
        # use dict.fromkeys to remove duplicates but keep first-seen order
        lines = list(dict.fromkeys(lines))

    # wrap each line, then join
    processed_items = [f"{item_prefix}{line}{item_suffix}" for line in lines]
    return f"{result_prefix}{delimiter.join(processed_items)}{result_suffix}"
