from oglaf.knowledge import get_tome


def titles_tag_hits_from_tag_search(search):
    tome = get_tome()

    hits = dict()

    ltag = search.lower()
    for lctag in tome.lctags:
        if ltag in lctag:
            proper_tag = tome.lctags[lctag]
            for title in tome.tags[proper_tag]:
                if title not in hits.keys():
                    hits[title] = set()
                hits[title].add(proper_tag)

    return hits


def title_hits_from_title_search(search):
    tome = get_tome()

    hits = dict()

    search_title = search.lower()
    for lctitle in tome.lctitles:
        if search_title in lctitle:
            proper_title = tome.lctitles[lctitle]
            hits[proper_title] = {proper_title}

    return hits


def title_arc_hits_from_arc_search(search):
    tome = get_tome()

    hits = dict()

    search_arc = search.lower()
    for lcarc in tome.lcarcs:
        if search_arc in lcarc:
            proper_arc = tome.lcarcs[lcarc]
            for title in tome.arcs[proper_arc]:
                if title not in hits.keys():
                    hits[title] = set()
                hits[title].add(proper_arc)

    return hits


def merge_hits(*all_hits):
    merged_hits = {}
    for hits in all_hits:
        for title, tags in hits.items():
            if title not in merged_hits:
                merged_hits[title] = tags
            else:
                merged_hits[title] = merged_hits[title].union(tags)
    return merged_hits
