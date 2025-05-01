from flask import Blueprint, render_template, request, make_response, url_for, current_app
from .converter import (
    convert_column_to_comma_list,
    convert_comma_to_column,
    convert_change_case,
    convert_find_replace
)
from datetime import date
from . import limiter
from flask_wtf.csrf import CSRFError


main = Blueprint('main', __name__)

@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    # collect all public routes without parameters
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and not rule.arguments:
            pages.append(url_for(rule.endpoint, _external=True))

    # render a simple XML
    sitemap_xml = render_template(
      'sitemap_template.xml',
      pages=pages,
      lastmod=date.today().isoformat()
    )
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@main.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@main.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 419

@main.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def index():
    # defaults
    result=""
    column_text=""
    delimiter=","
    item_prefix=""
    item_suffix=""
    result_prefix=""
    result_suffix=""
    dedupe = False 
    sort_order = ''

    if request.method == 'POST':
        column_text = request.form.get('column_data', '')
        delimiter = request.form.get('delimiter', ',')
        item_prefix = request.form.get('item_prefix', '')
        item_suffix = request.form.get('item_suffix', '')
        result_prefix = request.form.get('result_prefix', '')
        result_suffix = request.form.get('result_suffix', '')
        dedupe = request.form.get('dedupe') == 'on'
        sort_order = request.form.get('sort_order', '')
        result = convert_column_to_comma_list(
            column_text, delimiter, item_prefix, item_suffix, result_prefix, result_suffix, dedupe=dedupe, sort_order=sort_order)



    return render_template(
        'index.html',
        page_title="Column → Comma-Separated List",
        meta_description="Paste your column entries and get a comma-separated string instantly.",
        result=result,
        column_text=column_text,
        delimiter=delimiter,
        item_prefix=item_prefix,
        item_suffix=item_suffix,
        result_prefix=result_prefix,
        result_suffix=result_suffix,
        dedupe=dedupe,
        sort_order=sort_order
    )

@main.route('/commalisttocolumn', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def commalisttocolumn():
    result = ""
    comma_list = ""
    delimiter = ","
    dedupe = False
    sort_order = ''

    if request.method == 'POST':
        comma_list = request.form.get('comma_list', '')
        delimiter = request.form.get('delimiter', ',')
        dedupe = request.form.get('dedupe') == 'on'
        sort_order = request.form.get('sort_order', '')
        result = convert_comma_to_column(comma_list, delimiter, dedupe=dedupe, sort_order=sort_order)

    return render_template(
        'commalisttocolumn.html',
        page_title="Comma-Separated List → Column",
        meta_description="Paste your comma-separated string and get column entries instantly.",
        result=result,
        comma_list=comma_list,
        delimiter=delimiter,
        dedupe=dedupe,
        sort_order=sort_order
    )

@main.route('/changecase', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def changecase():
    result = ""
    text = ""
    case_option = "upper"

    if request.method == 'POST':
        text = request.form.get('text_input', '')
        case_option = request.form.get('case_option', 'upper')
        result = convert_change_case(text, case_option)

    return render_template(
        'changecase.html',\
        page_title="Change Case",
        meta_description="Paste your text and change its case instantly.",
        result=result,
        text=text,
        case_option=case_option
    )

@main.route('/findreplace', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def findreplace():
    text, result, find_str, replace_str = "", "", "",""
    if request.method == 'POST':
        find_str    = request.form.get('find_str', '')
        replace_str = request.form.get('replace_str', '')
        text        = request.form.get('text_input', '')
        result      = convert_find_replace(text, find_str, replace_str)
    return render_template(
        'findreplace.html',
        page_title="Find & Replace",
        meta_description="Quickly search and replace text strings.",
        result=result,
        find_str=find_str,
        replace_str=replace_str,
        text=text
    )

#@main.route('/test', methods=['GET', 'POST'])
#@limiter.limit("10 per minute")
#def test():
#    return render_template('400.html')
    