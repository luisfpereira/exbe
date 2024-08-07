def get_value_by_name(datum, name):
    names = name.split("/")
    value = datum
    for name in names:
        value = value[name]

    return value


def filter_by_func(name, func):
    def filter_(datum):
        cmp_value = get_value_by_name(datum, name)
        return func(cmp_value)

    return filter_


def filter_by_eq(name, value):
    # syntax sugar only
    return filter_by_func(name, lambda cmp_value: cmp_value == value)


def filter_by_is(name, value):
    # syntax sugar only
    return filter_by_func(name, lambda cmp_value: cmp_value is value)


def apply_filters(data, filters):
    fdata = data

    for filter_ in filters:
        fdata = filter(filter_, fdata)

    return fdata
