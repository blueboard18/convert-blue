from flask import Blueprint, render_template, request
from .converter import convert_column_to_comma_list

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    result=""
    column_text=""
    delimiter=","
    item_prefix=""
    item_suffix=""
    result_prefix=""
    result_suffix=""

    if request.method == 'POST':
        column_text = request.form.get('column_data', '')
        delimiter = request.form.get('delimiter', ',')
        item_prefix = request.form.get('item_prefix', '')
        item_suffix = request.form.get('item_suffix', '')
        result_prefix = request.form.get('result_prefix', '')
        result_suffix = request.form.get('result_suffix', '')
        result = convert_column_to_comma_list(column_text, delimiter, item_prefix, item_suffix, result_prefix, result_suffix)

    return render_template(
        'index.html',
        result=result,
        column_text=column_text,
        delimiter=delimiter,
        item_prefix=item_prefix,
        item_suffix=item_suffix,
        result_prefix=result_prefix,
        result_suffix=result_suffix
    )

