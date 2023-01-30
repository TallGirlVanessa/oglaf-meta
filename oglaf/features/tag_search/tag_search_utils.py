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
                    hits[title] = list()
                hits[title].append(proper_tag)

    return hits
