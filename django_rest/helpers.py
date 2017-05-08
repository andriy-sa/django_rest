from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


def prepare_order(order, sort_list, default):
    if order in sort_list:
        return order

    return default
