import streamlit as st
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from PIL import Image
import io

from prettifiers import get_prettifier_by_name

IMAGE_FORMAT = "png"
TITLE = "Code Formatter"
CODE_SAMPLE = "print('add your code here')"
LANGUAGES = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
]

# Define default options for each language
DEFAULT_OPTIONS = {
    "Python": {
        "line_length": 88,
        "string_normalization": True,
        "magic_trailing_comma": True,
        "indent_size": 4,
        "indent_style": "space",
    },
    "C": {},
    "C++": {},
    "Java": {},
    "JavaScript": {},
}

def format_code(code_input, language, options):
    # Get the appropriate code formatter
    prettify_func = get_prettifier_by_name(language)

    # Format the code
    code_formatted, format_success = prettify_func(code_input, options)

    return code_formatted, format_success

def display_output(code_formatted, language, line_numbers=True):
    lexer = get_lexer_by_name(language)
    code_image = highlight(
        code_formatted,
        lexer,
        ImageFormatter(image_format=IMAGE_FORMAT, line_numbers=line_numbers),
    )

    # Display the output
    st.header("Output")
    st.image(code_image, output_format=IMAGE_FORMAT.upper())
    st.code(code_formatted + "\n", language="python" if language == "Python" else language.lower())

    # Download button for code image
    if st.button("Download Image", key="download_image_button"):
        img_data = io.BytesIO()
        code_image.save(img_data, format='PNG')
        img_data.seek(0)
        st.download_button(label="Download Image", data=img_data, file_name="code_image.png", mime="image/png")

# Streamlit UI
st.set_page_config("Code Formatter")
st.title(TITLE)

# Input section
code_input = st.text_area("Code Input", placeholder=CODE_SAMPLE, height=200)
if not code_input:
    code_input = CODE_SAMPLE

language = st.sidebar.selectbox("Language", LANGUAGES, key="language_selectbox")

# Language-specific options
options = {}

if language != "Python":
    st.sidebar.header("Language-Specific Options")
    if language in ["C", "C++", "Java"]:
        options["line_length"] = st.sidebar.slider("Line Length", 20, 200, 80, key="line_length_slider")
        options["brace_style"] = st.sidebar.selectbox("Brace Style", ["Allman", "GNU", "K&R", "Stroustrup"], key="brace_style_selectbox")
        options["indent_style"] = st.sidebar.selectbox("Indent Style", ["tab", "space"], key="indent_style_selectbox")
        options["indent_size"] = st.sidebar.slider("Indent Size", 1, 8, 4, key="indent_size_slider")
        options["continuation_indent_size"] = st.sidebar.slider("Continuation Indent Size", 1, 8, 4, key="continuation_indent_size_slider")
    elif language == "JavaScript":
        options["insert_trailing_semicolon"] = st.sidebar.checkbox("Insert Trailing Semicolon", value=True, key="insert_trailing_semicolon_checkbox")
        options["space_before_function_parentheses"] = st.sidebar.checkbox("Space Before Function Parentheses", value=True, key="space_before_function_parentheses_checkbox")
else:
    st.sidebar.header("Language-Specific Options")
    options["line_length"] = st.sidebar.slider("Line Length", 20, 200, 88, key="line_length_slider")
    options["string_normalization"] = st.sidebar.checkbox("Normalize Strings", value=True, key="string_normalization_checkbox")
    options["magic_trailing_comma"] = st.sidebar.checkbox("Use Trailing Commas", value=True, key="magic_trailing_comma_checkbox")
    options["indent_size"] = st.sidebar.slider("Indent Size", 1, 8, 4, key="indent_size_slider")
    options["indent_style"] = st.sidebar.selectbox("Indent Style", ["tab", "space"], key="indent_style_selectbox")

# Format code
if st.button("Format", key="format_button"):
    code_formatted, format_success = format_code(code_input, language, options)
    if format_success:
        display_output(code_formatted, language)
    else:
        st.error("Auto-Format failed")
