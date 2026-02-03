from __future__ import annotations

import re
import sys
from typing import Optional, Dict, Any

# Definições das bandeiras com regex para os prefixos e comprimentos válidos
BRANDS = {
    "Visa": {
        "pattern": re.compile(r"^4"),
        "lengths": {13, 16},
    },
    "Mastercard": {
        # 51-55 or 2221-2720
        "pattern": re.compile(r"^(5[1-5]|222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[01]\d|2720)"),
        "lengths": {16},
    },
    "American Express": {
        "pattern": re.compile(r"^(34|37)"),
        "lengths": {15},
    },
    "Diners Club": {
        # 300-305, 36, 38
        "pattern": re.compile(r"^(30[0-5]|36|38)"),
        "lengths": {14},
    },
    "Discover": {
        # 6011, 622126-622925, 644-649, 65
        # regex cobre os intervalos conhecidos
        "pattern": re.compile(r"^(6011|65|64[4-9]|622(?:12[6-9]|1[3-9]\d|[2-8]\d{2}|9[0-1]\d|92[0-5]))"),
        "lengths": {16},
    },
    "JCB": {
        # 3528-3589
        "pattern": re.compile(r"^(352[8-9]|35[3-8]\d)"),
        "lengths": {16},
    },
    "EnRoute": {
        "pattern": re.compile(r"^(2014|2149)"),
        "lengths": {15},
    },
    "Voyager": {
        "pattern": re.compile(r"^8699"),
        "lengths": {15},
    },
    "Hipercard": {
        # 3841, 606282, 637 - comprimentos 13,16,19
        "pattern": re.compile(r"^(3841|606282|637)"),
        "lengths": {13, 16, 19},
    },
    "Aura": {
        "pattern": re.compile(r"^50"),
        "lengths": {16},
    },
}


def _clean_number(number: str) -> str:
    """Remove espaços e traços e valida que restam só dígitos."""
    cleaned = re.sub(r"[\s-]", "", number)
    if not cleaned.isdigit():
        raise ValueError("Número contém caracteres inválidos, apenas dígitos, espaços e '-' são permitidos")
    return cleaned


def detect_brand(number: str) -> Optional[str]:
    """Detecta a bandeira (brand) pelo prefixo usando regex.

    Retorna nome da bandeira ou None se não reconhecida.
    """
    for brand, info in BRANDS.items():
        if info["pattern"].match(number):
            return brand
    return None


def luhn_check(number: str) -> bool:
    """Implementação do algoritmo de Luhn."""
    total = 0
    reverse_digits = number[::-1]
    for i, ch in enumerate(reverse_digits):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def validate_card(number: str) -> Dict[str, Any]:
    """Valida um número de cartão de crédito.

    Passos:
    - limpa string
    - detecta bandeira por prefixo
    - verifica se o comprimento é válido para a bandeira detectada
    - aplica Luhn

    Retorna um dict com campos: valid (bool), brand (str|None), errors (list)
    """
    errors = []
    try:
        cleaned = _clean_number(number)
    except ValueError as e:
        return {"valid": False, "brand": None, "errors": [str(e)]}

    brand = detect_brand(cleaned)
    if brand is None:
        errors.append("Bandeira não reconhecida")
    else:
        lengths = BRANDS[brand]["lengths"]
        if len(cleaned) not in lengths:
            errors.append(f"Comprimento inválido para {brand}: {len(cleaned)} (esperado: {sorted(lengths)})")

    if not luhn_check(cleaned):
        errors.append("Falha no algoritmo de Luhn")

    return {"valid": len(errors) == 0, "brand": brand, "errors": errors}


def _format_result(n: str, res: Dict[str, Any]) -> str:
    status = "OK ✅" if res["valid"] else "INVÁLIDO ❌"
    brand = res["brand"] or "desconhecida"
    errs = "; ".join(res["errors"]) if res["errors"] else ""
    return f"{n} -> {status} - Bandeira: {brand} {('- ' + errs) if errs else ''}"


def _main_from_cli(argv: list[str]) -> int:
    if len(argv) <= 1:
        print("Uso: python src/card_validate.py <card_number> [outros_numbers...]")
        print("Exemplo: python src/card_validate.py 4111111111111111 378282246310005")
        return 0

    for n in argv[1:]:
        try:
            res = validate_card(n)
        except Exception as e:
            print(f"{n} -> ERRO: {e}")
            continue
        print(_format_result(n, res))
    return 0


if __name__ == "__main__":
    sys.exit(_main_from_cli(sys.argv))
