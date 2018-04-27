import os
import jinja2
from uuid import uuid4
from subprocess import call, STDOUT
from App import app


latex_jinja2_env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    trim_blocks=True,
    line_comment_prefix='%#',
    autoescape=False,
    loader=jinja2.FileSystemLoader('DB/templates')
)


def escape(s):
    escaped_chars = {
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
        '\n': "\\\\"  # xkcd.com/1638/
    }
    res = ""
    for c in s:
        res += escaped_chars.get(c, c)
    return res


def latexify(bill):
    id = str(uuid4())

    tositteet = [{
                    'summa': escape(str(t.amount)),
                    'liite': app.config['RECEIPTS_FOLDER'] + t.filename,
                    'kuvaus': escape(t.description)
                } for t in bill.receipts]

    template = latex_jinja2_env.get_template('template.tex')
    formatted = template.render(
        nimi=escape(bill.submitter),
        iban=escape(bill.iban),
        peruste=escape(bill.description),
        tositteet=tositteet,
        hyvaksytty=bill.accepted,
        kokous=bill.accepted_at,
        pvm=bill.date.strftime('%d-%m-%Y'),
        yhteensa=sum(float(tosite['summa']) for tosite in tositteet)
    )

    texf = id + '.tex'
    with open(texf, 'w') as f:
        f.write(formatted)

    # Kutsutaan kahdesti, jotta saadaan kuvat ja refit oikein
    dev = open(os.devnull, 'w')
    ret = call(
            ['pdflatex', '-halt-on-error', '-output-directory', app.config['TMP_FOLDER'], texf],
            stdout=dev, stderr=STDOUT)
    ret |= call(
            ['pdflatex', '-halt-on-error', '-output-directory', app.config['TMP_FOLDER'], texf],
            stdout=dev, stderr=STDOUT)

    os.unlink(texf)

    return id + '.pdf' if not ret else None
