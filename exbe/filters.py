def _get_value(datum, name):
    names = name.split("/")
    value = datum
    for name in names:
        value = value[name]

    return value


def filter_by_eq(name, value):
    def filter_(datum):
        cmp_value = _get_value(datum, name)
        return cmp_value == value

    return filter_


def filter_by_is(name, value):
    def filter_(datum):
        cmp_value = _get_value(datum, name)
        return cmp_value is value

    return filter_


def apply_filters(data, filters):
    fdata = data

    for filter_ in filters:
        fdata = filter(filter_, fdata)

    return fdata
