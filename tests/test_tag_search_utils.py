import pytest
from oglaf.features.search.search_utils import (
    titles_tag_hits_from_tag_search,
    title_hits_from_title_search,
    title_arc_hits_from_arc_search,
    merge_hits,
)


@pytest.mark.parametrize(
    "search,expected_hits",
    [
        (
            "chess",
            {
                "the Automaton": {"Chess"},
                "Lair of the Grandmaster": {"Lethal Chessboard"},
                "the Cyprian defence": {"Chess"},
            },
        ),
        (
            "jar",
            {"Theodicy": {"Jar"}},
        ),
    ],
)
def test_tag_search(search, expected_hits):
    hits = titles_tag_hits_from_tag_search(search)

    assert hits == expected_hits


@pytest.mark.parametrize(
    "search,expected_hits",
    [
        (
            "chess",
            {},
        ),
        (
            "jar",
            {"Jar, Lamp, Ham": {"Jar, Lamp, Ham"}},
        ),
    ],
)
def test_title_search(search, expected_hits):
    hits = title_hits_from_title_search(search)

    assert hits == expected_hits


@pytest.mark.parametrize(
    "search,expected_hits",
    [
        (
            "chess",
            {},
        ),
        (
            "jar",
            {},
        ),
        (
            "rise",
            {
                "A hundred tiny eyes": {"Rise of Apprentice"},
                "Blue Door": {"Rise of Apprentice"},
                "Book of Love": {"Rise of Apprentice"},
                "Cockhunt": {"Rise of Apprentice"},
                "Cumsprite": {"Rise of Apprentice"},
                "Glove": {"Rise of Apprentice"},
                "Rapunzel": {"Rise of Apprentice"},
                "Secret admirer": {"Rise of Apprentice"},
                "Some time ago...": {"Rise of Apprentice"},
                "emancipation": {"Rise of Apprentice"},
            },
        ),
    ],
)
def test_arc_search(search, expected_hits):
    hits = title_arc_hits_from_arc_search(search)

    assert hits == expected_hits


@pytest.mark.parametrize(
    "all_hits,expected_merged",
    [
        ([], {}),
        ([{"a title": {"a tag"}}], {"a title": {"a tag"}}),
        (
            [{"a title": {"a tag"}}, {"different title": {"different tag"}}],
            {"a title": {"a tag"}, "different title": {"different tag"}},
        ),
        (
            [{"a title": {"a tag"}}, {"a title": {"different tag"}}],
            {"a title": {"a tag", "different tag"}},
        ),
        (
            [{"a title": {"same tag"}}, {"a title": {"same tag"}}],
            {"a title": {"same tag"}},
        ),
    ],
)
def test_merge_hits(all_hits, expected_merged):
    merged_hits = merge_hits(*all_hits)

    assert merged_hits == expected_merged
