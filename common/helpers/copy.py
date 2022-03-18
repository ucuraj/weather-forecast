# -*- coding: utf-8 -*-

"""Helper para copiar objetos.

A través de la funcion copy_object recibe una clase y un objeto, y retorna una copia del mismo.
Valida que el objeto recibido sea una instancia de la clase recibida.
"""


def copy_object(obj_class, obj_to_copy, atts_to_exclude: list = None, atts_to_copy: list = None, exclude=True):
    """Params:
        obj_class -> Clase del objeto a copiar.
        obj_to_copy -> Objeto a copiar
        atts_to_exclude(optional) -> Lista de atributos a exluir de la copia
        atts_to_copy(optional) -> Lista de atributos a copiar del objeto original
        exclude(default=True) -> Si es True, utiliza la lista de atributos a excluir

    Si solo se envia obj_class y obj_to_copy copia todos los campos.
    Si exclude=False utiliza la lista atts_to_copy

    Retorna el objeto copiado sin guardarlo en la db."""

    new_obj = obj_class()

    if type(obj_to_copy) != obj_class:
        raise ValueError(f"La clase del objeto a copiar no es de tipo {obj_class}")

    if exclude:
        atts_to_exclude = atts_to_exclude if atts_to_exclude else []
        atts_to_exclude.extend(('id', '_state'))
        for k, v in obj_to_copy.__dict__.items():
            if k not in atts_to_exclude:
                new_obj.__dict__[k] = v
    else:
        for k, v in obj_to_copy.__dict__.items():
            if k in atts_to_copy:
                new_obj.__dict__[k] = v

    return new_obj
