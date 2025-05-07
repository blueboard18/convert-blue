from flask import Blueprint, render_template, request, make_response, url_for, current_app
from .converter import (
    convert_column_to_comma_list,
    convert_comma_to_column,
    convert_change_case,
    convert_find_replace,
    extract_text_between_chars,
    convert_image_dpi
)
from datetime import date
from . import limiter
from flask_wtf.csrf import CSRFError
from PIL import Image
import os


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

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(400)
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
        meta_description="Convert column data into comma-separated values for CSVs, SQL queries, or code — free, instant, no signup.",
        result=result,
        column_text=column_text,
        delimiter=delimiter,
        item_prefix=item_prefix,
        item_suffix=item_suffix,
        result_prefix=result_prefix,
        result_suffix=result_suffix,
        dedupe=dedupe,
        sort_order=sort_order,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)}
        ]
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
        meta_description="Convert comma-separated strings into clean column lists for spreadsheets, databases, and forms.",
        result=result,
        comma_list=comma_list,
        delimiter=delimiter,
        dedupe=dedupe,
        sort_order=sort_order,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)},
            {"name": "Comma-Separated List → Column", "url": request.base_url}
        ]
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
        meta_description="Change text case online — convert to UPPERCASE, lowercase, Title Case, snake_case, or kebab-case instantly.",
        result=result,
        text=text,
        case_option=case_option,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)},
            {"name": "Change Case", "url": request.base_url}
        ]
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
        meta_description="Find and replace text across your input instantly — perfect for bulk edits, formatting, and cleanup.",
        result=result,
        find_str=find_str,
        replace_str=replace_str,
        text=text,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)},
            {"name": "Find & Replace", "url": request.base_url}
        ]

    )

@main.route('/extract', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def extract():
    result = ""
    column_text = ""
    start_char = "["
    end_char = "]"
    dedupe = False
    sort_order = ""

    if request.method == 'POST':
        column_text = request.form.get('column_data', '')
        start_char = request.form.get('start_char', '')
        end_char = request.form.get('end_char', '')
        dedupe = request.form.get('dedupe') == 'on'
        sort_order = request.form.get('sort_order', '')

        if start_char and end_char:
            result = extract_text_between_chars(
                column_text, start_char, end_char,
                dedupe=dedupe,
                sort_order=sort_order
            )

    return render_template(
        'extract.html',
        page_title="Extract Text Between Characters",
        meta_description="Extract text between any two characters on each line — perfect for grabbing IDs, tags, values, or custom patterns from your data.",
        result=result,
        column_text=column_text,
        start_char=start_char,
        end_char=end_char,
        dedupe=dedupe,
        sort_order=sort_order,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)},
            {"name": "Extract Text", "url": request.base_url}
        ]

    )

@main.route('/dpi', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def dpi():
    result_image = None
    original_dpi = None
    original_name = ""

    # Define defaults for GET and POST rendering
    dpi_choice = "72"
    dpi = "72"

    if request.method == 'POST':
        uploaded_file = request.files.get('image_file')
        dpi_choice = request.form.get('dpi_choice', '72')
        if dpi_choice == 'other':
            dpi = request.form.get('dpi', '72')
        else:
            dpi = dpi_choice

        try:
            new_dpi = int(dpi)
        except ValueError:
            new_dpi = 72  # fallback/default

        if uploaded_file and new_dpi:
            try:
                # Open the image only once
                image = Image.open(uploaded_file)
                original_dpi = image.info.get('dpi', (72, 72))[0]

                # Use helper function (modified to take an image object)
                buffer, file_format = convert_image_dpi(image, new_dpi)

                original_name, _ = os.path.splitext(uploaded_file.filename)
                result_image = {
                    "data": buffer.read(),
                    "mimetype": f"image/{file_format.lower()}",
                    "filename": f"{original_name}_dpi{new_dpi}.{file_format.lower()}"
                }
            except Exception as e:
                print("DPI conversion error:", e)

    return render_template(
        'dpi.html',
        page_title="Image DPI Converter",
        meta_description="Change image DPI for print or web. Upload PNG, JPG, or more and set a new resolution — download instantly.",
        original_dpi=original_dpi,
        result_image=result_image,
        dpi_choice=dpi_choice,
        dpi=dpi,
        breadcrumb_items=[
            {"name": "Home", "url": url_for('main.index', _external=True)},
            {"name": "Image DPI Converter", "url": request.base_url}
        ]
    )


#@main.route('/test', methods=['GET', 'POST'])
#@limiter.limit("10 per minute")
#def test():
#    return render_template('400.html')
    