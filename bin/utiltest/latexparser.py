from pylatexenc import latex2text
from pylatexenc.latexencode import UnicodeToLatexEncoder, UnicodeToLatexConversionRule, RULE_REGEX
import re

def extra_rules():
    return [
        (re.compile(r'ä'), r'{\\"a}'),
        (re.compile(r'Ä'), r'{\\"A}'),
        (re.compile(r'ö'), r'{\\"o}'),
        (re.compile(r'Ö'), r'{\\"O}'),
        (re.compile(r'ü'), r'{\\"u}'),
        (re.compile(r'Ü'), r'{\\"U}'),
        (re.compile(r'á'), r"{\\'a}"),
        (re.compile(r'Á'), r"{\\'A}"),
        (re.compile(r'ú'), r"{\\'u}"),
        (re.compile(r'Ú'), r"{\\'U}"),
        (re.compile(r'é'), r"{\\'e}"),
        (re.compile(r'É'), r"{\\'E}"),
        (re.compile(r'ó'), r"{\\'o}"),
        (re.compile(r'Ó'), r"{\\'O}"),
        (re.compile(r'í'), r"{\\'\\i}"),
        (re.compile(r'Í'), r"{\\'\\I}"),
        (re.compile(r'à'), r"{\\`a}"),
        (re.compile(r'À'), r"{\\`A}"),
        (re.compile(r'ù'), r"{\\`u}"),
        (re.compile(r'Ù'), r"{\\`U}"),
        (re.compile(r'è'), r"{\\`e}"),
        (re.compile(r'È'), r"{\\`E}"),
        (re.compile(r'ò'), r"{\\`o}"),
        (re.compile(r'Ò'), r"{\\`O}"),
        (re.compile(r'ì'), r"{\\`\\i}"),
        (re.compile(r'Ì'), r"{\\`I}"),
    ]

def latex_encoder():
    u = UnicodeToLatexEncoder(
        conversion_rules=[
            UnicodeToLatexConversionRule(rule_type=RULE_REGEX, rule=extra_rules()),
            'defaults'
        ]
    )
    return u.unicode_to_latex

def latex_parser():
    return latex2text.LatexNodes2Text().latex_to_text


class LatexParser():
    def __init__(self):
        self.latex_to_text = latex_parser()
        self.text_to_latex = latex_encoder()
        
    def encode(self, text):
        return self.text_to_latex(text)
    
    def decode(self, latex):
        return self.latex_to_text(latex)