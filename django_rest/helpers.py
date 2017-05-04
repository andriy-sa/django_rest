def prepare_order(order, sort_list, default):
    if order in sort_list:
        return order

    return default
