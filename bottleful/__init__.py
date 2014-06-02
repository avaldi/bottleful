

HTTP_ACTIONS = {
    'list': {
        'method': 'GET',
        'path': '/%(resource_name)s'
    },
    'create': {
        'method': 'POST',
        'path': '/%(resource_name)s'
    },
    'retrieve': {
        'method': 'GET',
        'path': '/%(resource_name)s/<resource_id>'
    },
    'update': {
        'method': 'PUT',
        'path': '/%(resource_name)s/<resource_id>'
    },
    'destroy': {
        'method': 'DELETE',
        'path': '/%(resource_name)s/<resource_id>'
    }
}
