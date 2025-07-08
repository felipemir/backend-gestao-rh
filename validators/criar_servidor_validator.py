from cerberus import Validator
from datetime import time, datetime


def validate_time(field, value, error):
    try:
        if len(value) == 7:
            value = f"0{value}"
        time.fromisoformat(value)
    except ValueError:
        error(field, "Formato de horário inválido. Use H:MM:SS ou HH:MM:SS")


def validate_date(field, value, error):
    try:
        datetime.fromisoformat(value)
    except ValueError:
        error(field, "Formato de data inválido. Use YYYY-MM-DD")


schema = {
    "setor": {"type": "string", "required": True, "minlength": 3},
    "nome": {"type": "string", "required": True, "minlength": 3},
    "matricula": {"type": "string", "required": False},
    "cargo": {"type": "string", "required": True, "minlength": 3},
    "funcao": {"type": "string", "required": False},
    "horario": {"type": "string", "required": True},
    "entrada": {"type": "string", "required": True, "check_with": validate_time},
    "saida": {"type": "string", "required": True, "check_with": validate_time},
    # *** Campos que faltavam no schema ***
    "feriasinicio": {
        "type": "string",
        "required": False,
        "check_with": validate_date,
    },  # Note o nome SEM underline
    "feriasfinal": {
        "type": "string",
        "required": False,
        "check_with": validate_date,
    },  # Nome corrigido para bater com o JSON
    "data_nascimento": {
        "type": "string",
        "required": False,
        "check_with": validate_date,
    },
    "sexo": {
        "type": "string",
        "required": False,
        "allowed": ["MASCULINO", "FEMININO"],
    },  # Valores permitidos
    "estado_civil": {
        "type": "string",
        "required": False,
        "allowed": ["SOLTEIRO", "CASADO", "DIVORCIADO", "VIUVO"],
    },  # Valores permitidos
    "naturalidade": {"type": "string", "required": False},
    "nacionalidade": {"type": "string", "required": False},
    "identidade": {"type": "string", "required": False},
    "titulo_eleitor": {"type": "string", "required": False},
    "cpf": {"type": "string", "required": False, "minlength": 11, "maxlength": 11},
    "pis": {"type": "string", "required": False},
    "data_admissao": {"type": "string", "required": False, "check_with": validate_date},
}

validator = Validator(schema)
