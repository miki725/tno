import re

from cryptography.x509 import Name, ObjectIdentifier


def get_attribute_from_x509_by_oid(section: Name, oid: ObjectIdentifier, default: str = '') -> str:
    try:
        return section.get_attributes_for_oid(oid)[0].value
    except IndexError:
        return default


def get_json_from_x509_name(x509_name: Name) -> dict:
    return {
        i.oid._name: i.value
        for i in x509_name
    }


def set_attr_and_return(name: str, value):
    def wrapper(f):
        setattr(f, name, value)
        return f
    return wrapper


def underscorize(value: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
