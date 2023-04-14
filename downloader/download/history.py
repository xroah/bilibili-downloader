from ..db import Part


def print_downloaded_videos():
    query = Part.select(
        Part.title,
        Part.path,
        Part.finish_time
    ).where(Part.finished == True)

    for r in query:
        print(
            r.title,
            r.path,
            r.finish_time,
            sep=" " * 3 + "|" + " " * 3
        )
        print("-" * 100)
