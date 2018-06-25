
import datetime

from flask import Blueprint, render_template
# from lib.database import db

blueprint = Blueprint("frontpage", __name__)

@blueprint.route("/")
def frontpage():
    # print(db)
    about_knoerden = dict(headline="Om K-Nørden",
                          summary='K-Nørden er en forening for børn og unge hvor vi leger med elektronik, programmering og "nørderi"',
                          author="K-Nørden",
                          date=datetime.datetime.now(),
                          url="/",
                          image="static/images/stock/20180418_203511.jpg")
    about_fdf = dict(headline="Om FDF",
                     summary="FDF handler om fælleskab. Gennem lege, hygge, aktiviteter og meget andet møder vi børn og unge",
                     author="K-Nørden",
                     date=datetime.datetime.now(),
                     url="https://fdf.dk/om-fdf/hvad-er-fdf/",
                     image="static/images/stock/20180418_203511.jpg")
    about_k19 = dict(headline="Om K19 - Vanløse",
                     summary="K-Nørden er et projekt i FDF K19 - Vanløse som er en af landets største kredse. Du bliver dermed en del af et meget størrere fælleskab.",
                     author="K-Nørden",
                     date=datetime.datetime.now(),
                     url="http://fdfk19.dk",
                     image="static/images/stock/20180418_203511.jpg")
    items = ([about_knoerden, about_fdf, about_k19] +
             [dict(headline="foo", summary="Foo bar baz bar", author="me", date=datetime.datetime.now(), url="/", image="static/images/test100x100.png") for _ in range(10)])
    # items[2]["summary"] = "bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla " "bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla "
    # items[2]["headline"] = "Om KN"
    items[2]["image"] = "static/images/stock/20180418_203511.jpg"

    items[5]["summary"] = "bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla " "bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla "
    items[5]["headline"] = "Om KN"

    return render_template("frontpage.html", items=items)
