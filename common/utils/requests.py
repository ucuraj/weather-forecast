def format_query_params(data: dict, valid_params=None):
    """Devuelve un string formado por una lista de query params a
    partir de las claves y valores de un diccionario"""
    if valid_params:
        data = {param: data[param] for param in valid_params}
    return '&'.join([f'{k}={v}' for k, v in data.items()])
