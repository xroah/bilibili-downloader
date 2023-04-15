from ..db import Part, Episode


def _print(item: Part | Episode):
    print(
        item.title,
        item.path,
        item.finish_time,
        sep=" " * 3 + "|" + " " * 3
    )
    print("-" * 100)


def print_downloaded_videos():
    query = Part.select(
        Part.title,
        Part.path,
        Part.finish_time
    ).where(Part.finished == True)
    e_query = Episode.select(
        Episode.title,
        Episode.path,
        Episode.finish_time
    ).where(Episode.finished == True)

    for r in query:
        _print(r)

    for r in e_query:
        _print(r)
