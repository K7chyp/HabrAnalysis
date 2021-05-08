import joblib
 
bookmarks_intevals = joblib.load("intervals_bookmarks.joblib")
raiting_intevals = joblib.load("intervals_raiting.joblib")
viewers_intevals = joblib.load("intervals_viewers.joblib")
vectorier = joblib.load("vectorizer.joblib")
viewers = joblib.load("viewers.joblib")
raiting = joblib.load("raiting.joblib")
bookmarks = joblib.load("bookmarks.joblib")


def get_predict(sequence: str):
    assert isinstance(sequence, str), "Please input string"
    sequence = vectorier.transform([sequence])
    index = (
        int(bookmarks.predict(sequence)),
        int(raiting.predict(sequence)),
        int(viewers.predict(sequence)),
    )
    for idx, column_interval, column_name in zip(
        index,
        (bookmarks_intevals, raiting_intevals, viewers_intevals),
        ("bookmarks", "raiting", "viewers"),
    ):
        print(
            "Predicted count of {} between {} and {}".format(
                column_name, column_interval[idx].left, column_interval[idx].right
            )
        )

