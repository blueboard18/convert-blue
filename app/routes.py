from flask import Blueprint, render_template, request
from .converter import convert_column_to_comma_list

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        column_text = request.form.get('column_data', '')
        result = convert_column_to_comma_list(column_text)
    return render_template('index.html', result=result)
