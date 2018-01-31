import shutil
import os
from datetime import datetime
import time
import jinja2
from uuid import uuid4
from werkzeug.utils import secure_filename
from subprocess import call, STDOUT


latex_jinja2_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('./src/templates'))
)

def escape(s):
    map = {
        '$':  "\\$",
        '%':  "\\%",
        '&':  "\\&",
        '#':  "\\#",
        '_':  "\\_",
        '{':  "\\{",
        '}':  "\\}",
        '[':  "{[}",
        ']':  "{]}",
        '"':  "{''}",
        '\\': "\\textbackslash{}",
        '~':  "\\textasciitilde{}",
        '<':  "\\textless{}",
        '>':  "\\textgreater{}",
        '^':  "\\textasciicircum{}",
        '`':  "{}`",
        '\n': "\\\\" # xkcd.com/1638/
    }
    res = ""
    for c in s:
        res += map.get(c, c)
    return res


def latexify(nimi, iban, peruste, tositteet):
    base = str(uuid4())
    folder = 'tmp/' + base + '/'
    os.mkdir(folder)

    for tosite in tositteet:
        fn = folder + secure_filename(tosite['liite'].filename)
        tosite['liite'].save(fn)
        tosite['liite'] = fn

    tositteet = [dict([(k, escape(v)) for (k,v) in t.items()]) for t in tositteet]

    template = latex_jinja2_env.get_template('template.tex')
    formatted = template.render(
        nimi=escape(nimi),
        iban=escape(iban),
        peruste=escape(peruste),
        tositteet=tositteet,
        yhteensa=sum(int(tosite['summa']) for tosite in tositteet)
    )

    texf = folder + base + '.tex'
    with open(texf, 'w') as f:
        f.write(formatted)

    # Kutsutaan kahdesti, jotta saadaan kuvat ja refit oikein
    dev = open(os.devnull, 'w')
    ret = call(['pdflatex', '-halt-on-error','-output-directory', folder, texf], stdout=dev, stderr=STDOUT)
    ret |= call(['pdflatex', '-halt-on-error', '-output-directory', folder, texf], stdout=dev, stderr=STDOUT)

    if not ret:
        shutil.copy(folder + base + '.pdf', 'bills/')
    shutil.rmtree(folder)

    return base + '.pdf' if not ret else None
