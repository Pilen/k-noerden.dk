import datetime

from flask import Blueprint, render_template, request

blueprint = Blueprint("news", __name__, template_folder="/vagrant/knoerden/templates/news/", url_prefix="/news/")

@blueprint.route("/")
def index():
    return render_template("news.html")

@blueprint.route("/create/", methods=["GET", "POST"])
def create_news():
    if request.methods == "GET":
        return render_template("create.html")
    if request.method == "POST":
        data = request_data()
        title = data.title
        description = data.description
        if not title:
            abort("Missing title")
        if not description:
            abort("Mising content")
        database.create("news",
                        created_by=session["user_id"],
                        title=data.title,
                        description=data.description)
        return redirect(url_for("frontpage"))

@blueprint.route("/entry/<id>/")
def entry(id):
    news = database.execute("select * from news where id = ?", id).one()
    raw_comments = database.execute("select * from news_comments where id == ? order by created_at asc")
    comments_by_id = {comment.comment_id: comment for comment in raw_comments}
    toplevel = []
    # Remember comments can only reply to *older* comments
    for comment in raw_comments:
        comment.children = [] #This is the first time we see this comment
        if comment.reply_to:
            parent = comments_by_id[comment.reply_to]
            parent.children.append(comment)
        else:
            toplevel.append(comment)

    def calculate_depth(comments, depth):
        for comment in comments:
            comment.depth = depth
            calculate_depth(comment.children, depth + 1)
    calculate_depth(toplevel, 0)

    ordered_comments = []
    def recursive_flatten(comments):
        for comment in comments:
            ordered_comments.append(comment)
            recursive_flatten(comment.children)
    recursive_flatten(toplevel)

    return render_template("entry.html", news=news, comments=ordered_comments)

@blueprint.route("/entry/<id>/comment/", methods=["POST"])
def comment(id):
    data = request_data()
    database.create("news",
                    news_id=id,
                    reply_to=data.reply_to,
                    created_by=session["user_id"],
                    title=data.title,
                    content=data.content)
    return redirect(url_for("news.entry", id=id))
