def convert_column_to_comma_list(text):
    lines = text.strip().splitlines()
    return ','.join([line.strip() for line in lines if line.strip()])

