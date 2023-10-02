from dateutil.parser import parse as d_parse


def parse(date_str: str):
    return d_parse(date_str)


# def parse_from_time(time):
    # return datetime.datetime.fromtimestamp(time)
