# Validação de Cartões de Crédito 🔒

Projeto simples em Python para validar números de cartões de crédito.

## 🚀 Descrição
O script `src/card_validate.py` fornece:
- **Detecção de bandeira** (brand) por prefixo (IIN/BIN) usando expressões regulares.
- **Verificação de comprimento** por bandeira (número de dígitos esperado).
- **Validação pelo algoritmo de Luhn**.
- Um **CLI** simples para testar números pelo terminal.

---

## 📚 Tabela de verificação (IIN/BIN e comprimentos)

| Bandeira             | Início (IIN/BIN)                                       | Comprimento (Nº de dígitos) |
|----------------------|--------------------------------------------------------|------------------------------|
| Visa (Classic)       | 4                                                      | 16                           |
| Visa (Antigo/Especial)| 4                                                     | 13                           |
| Mastercard           | 51–55 ou 2221–2720                                     | 16                           |
| American Express     | 34 ou 37                                               | 15                           |
| Diners Club          | 300–305, 36 ou 38                                      | 14                           |
| Discover             | 6011, 622126–622925, 644–649 ou 65                     | 16                           |
| JCB                  | 3528–3589                                              | 16                           |
| EnRoute              | 2014 ou 2149                                           | 15                           |
| Voyager              | 8699                                                   | 15                           |
| Hipercard            | 3841, 606282 ou 637                                    | 13, 16 ou 19                 |
| Aura                 | 50                                                     | 16                           |

> Observação: a implementação prioriza os intervalos e prefixos mais usados; se precisar de cobertura extra, podemos ajustar as regex.

---

## 🧩 Principais funções (arquivo `src/card_validate.py`)

- `_clean_number(number: str) -> str` — limpa espaços e traços e valida dígitos.
- `detect_brand(number: str) -> Optional[str]` — detecta a bandeira usando regex.
- `luhn_check(number: str) -> bool` — aplica o algoritmo de Luhn.
- `validate_card(number: str) -> dict` — valida o cartão combinando limpeza, detecção de bandeira, verificação de comprimento e Luhn. Retorna:
  - `valid` (bool)
  - `brand` (str | None)
  - `errors` (list)
- `_format_result(n: str, res: dict) -> str` — formata a saída legível para CLI.

---

## ▶️ Como rodar (terminal)

1. Certifique-se de ter Python 3.8+ instalado.
2. No diretório do projeto (onde está este `README.md`) rode:

```bash
python src/card_validate.py <numero_cartao> [outros_numeros...]
```

Exemplo:

```bash
python src/card_validate.py 4111111111111111 378282246310005 30569309025904
```

Saída esperada (exemplo):

```
4111111111111111 -> OK ✅ - Bandeira: Visa
378282246310005 -> OK ✅ - Bandeira: American Express
30569309025904 -> OK ✅ - Bandeira: Diners Club
```

---

## ✅ Uso em scripts
Você pode importar `validate_card` em outro módulo:

```py
from src.card_validate import validate_card

res = validate_card('4111111111111111')
print(res)
# -> {'valid': True, 'brand': 'Visa', 'errors': []}
```

---

## 🛠️ Sugestões de melhorias
- Adicionar testes unitários com `pytest`.
- Aceitar arquivos CSV/JSON e processar em lote.
- Internacionalizar mensagens/saídas.

---

Se quiser, posso **adicionar testes unitários** e um comando `--file` para processar vários números de uma vez. ⚡
