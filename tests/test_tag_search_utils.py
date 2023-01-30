import pytest
from oglaf.features.search.search_utils import titles_tag_hits_from_tag_search


@pytest.mark.parametrize(
    "search,expected_hits",
    [
        (
            "chess",
            {
                "the Automaton": ["Chess"],
                "Lair of the Grandmaster": ["Lethal Chessboard"],
                "the Cyprian defence": ["Chess"],
            },
        )
    ],
)
def test_tag_search(search, expected_hits):
    hits = titles_tag_hits_from_tag_search(search)

    assert hits == expected_hits
