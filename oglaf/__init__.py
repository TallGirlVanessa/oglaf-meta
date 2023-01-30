from flask import Flask, render_template, request
from flask_talisman import Talisman
from oglaf.features.tag_search.tag_search_forms import TagSearchForm
from oglaf.features.tag_search.tag_search_utils import titles_tag_hits_from_tag_search
from oglaf.knowledge import get_tome


def create_app():
    app = Flask(__name__)

    app.config["WTF_CSRF_ENABLED"] = False

    Talisman(app)

    @app.route("/")
    def home():
        form = TagSearchForm()
        return render_template("home.html", form=form)

    @app.route("/tag-search-results")
    def tag_search_results():
        form = TagSearchForm(request.args)
        tome = get_tome()
        hits = {}
        if form.validate():
            hits = titles_tag_hits_from_tag_search(form.search.data)
        return render_template(
            "tag_search_results.html", form=form, hits=hits, tome=tome
        )

    return app
