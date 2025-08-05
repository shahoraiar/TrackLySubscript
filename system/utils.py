from django.core.paginator import Paginator

def paginate_data(model, data, request):
    if request.POST:
        search_value = request.POST.get('search[value]')
    else:
        search_value = request.GET.get('search[value]')


    if search_value:
        data = model.objects.search_by_data(search_value)

    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')

    if order_column:
        column_name = request.GET.get(f'columns[{order_column}][data]')
        reverse_data = False
        if order_dir == 'desc':
            reverse_data = True
        data = sorted(data, key=lambda p: getattr(p, column_name), reverse=reverse_data)
    if request.method == 'POST':
        start = request.POST.get('start')
        length = request.POST.get('length')
    else:
        start = request.GET.get('start')
        length = request.GET.get('length')

    if start and length:
        page = int(start) // int(length) + 1
    else:
        page = 0

    per_page = str(length if length else 25)
    paginator = Paginator(list(data), per_page)
    page_data = paginator.get_page(page)

    response_data = {
        'draw': request.GET.get('draw'),
        'recordsTotal': data.count(),
        'recordsFiltered': paginator.count,
        'data': []
    }
    if request.method == 'POST':
        response_data['draw'] = request.POST.get('draw')
    return response_data, page_data
 

# def paginate_data(model, data, request):
#     if request.method == 'POST':
#         search_value = request.POST.get('search[value]')
#     else:
#         search_value = request.GET.get('search[value]')

#     if search_value:
#         data = model.objects.search_by_data(search_value)

#     order_column = int(request.GET.get('order[0][column]', 0))
#     order_dir = request.GET.get('order[0][dir]', 'asc')

#     if order_column:
#         column_name = request.GET.get(f'columns[{order_column}][data]')
#         if order_dir == 'desc':
#             data = data.order_by(f'-{column_name}')
#         else:
#             data = data.order_by(column_name)
#     else:
#         data = data.order_by('id')  # Default ordering

#     if request.method == 'POST':
#         start = request.POST.get('start', '0')
#         length = request.POST.get('length', '25')
#     else:
#         start = request.GET.get('start', '0')
#         length = request.GET.get('length', '25')

#     if start and length:
#         page = int(start) // int(length) + 1
#     else:
#         page = 1

#     per_page = int(length) if length else 25
#     paginator = Paginator(data, per_page)
#     page_data = paginator.get_page(page)

#     response_data = {
#         'draw': request.GET.get('draw', '1') if request.method == 'GET' else request.POST.get('draw', '1'),
#         'recordsTotal': model.objects.count(),
#         'recordsFiltered': paginator.count,
#         'data': []
#     }
#     return response_data, page_data





