from django.db import models
from django.core.exceptions import ValidationError
from django_cpf_cnpj.cpf import is_valid_cpf
from django_cpf_cnpj.cnpj import is_valid_cnpj


def validate_cpf(value):
    if not is_valid_cpf(value):
        raise ValidationError("CPF inválido")
    return True


def validate_cnpj(value):
    if not is_valid_cnpj(value):
        raise ValidationError("CNPJ inválido")
    return True


class CPFField(models.CharField):
    default_validators = [validate_cpf]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 11)
        super().__init__(*args, **kwargs)


class CNPJField(models.CharField):
    default_validators = [validate_cnpj]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 18)
        super().__init__(*args, **kwargs)
