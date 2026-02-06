def is_dangerous(query):
    """
    Detect dangerous SQL queries.
    Currently blocks DELETE without WHERE.
    """

    q = query.lower()

    if "delete" in q and "where" not in q:
        return True

    return False
