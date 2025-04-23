def convert_column_to_comma_list(text, delimiter=',', item_prefix='', item_suffix='', result_prefix='', result_suffix=''):
    lines = text.strip().splitlines()
    processed = [f"{item_prefix}{line.strip()}{item_suffix}" for line in lines if line.strip()]
    processed = f"{result_prefix}{delimiter.join(processed)}{result_suffix}"
    return processed
