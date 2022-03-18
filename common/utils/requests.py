def format_query_params(data: dict):
    """Devuelve un string formado por una lista de query params a
    partir de las claves y valores de un diccionario"""

    return '&'.join([f'{k}={v}' for k, v in data.items()])
