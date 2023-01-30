from flask import Flask, render_template, request
from flask_talisman import Talisman
from oglaf.features.search.search_forms import SearchForm
from oglaf.features.search.search_utils import titles_tag_hits_from_tag_search
from oglaf.knowledge import get_tome


def create_app():
    app = Flask(__name__)

    app.config["WTF_CSRF_ENABLED"] = False

    Talisman(app)

    @app.route("/")
    def home():
        form = SearchForm()
        return render_template("home.html", form=form, title="Home")

    @app.route("/search-results")
    def search_results():
        form = SearchForm(request.args)
        tome = get_tome()
        hits = {}
        if form.validate():
            hits = titles_tag_hits_from_tag_search(form.search.data)
        return render_template(
            "search_results.html",
            form=form,
            hits=hits,
            tome=tome,
            title=f"Results for '{form.search.data}'",
        )

    return app
