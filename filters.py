import arrow


def datetimeformat(date_str):
    dt = arrow.get(date_str).shift(hours=3)
    return dt.humanize(locale='pt_br')