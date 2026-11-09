# Cajuí Hardware

[English](README.md) | Português brasileiro

**Caixas impressas em 3D para os transmissores de sensores do Cajuí, modeladas como scripts
paramétricos do FreeCAD.**

Este repositório é a camada de hardware do [Cajuí](https://github.com/cajui/docs). O firmware
dos transmissores fica no [cajui-firmware](https://github.com/cajui/cajui-firmware).

| Caixa | Placa | Bateria | Revisão | Situação |
| --- | --- | --- | --- | --- |
| [Ampla](enclosures/wide/README.pt-BR.md) | Heltec Wireless Stick Lite V3 | Uma célula 18650 protegida | `wide-r05` | Ensaio físico pendente |

**Desenhos experimentais.** Cada revisão é conferida no modelo (malhas fechadas, sem colisões
entre as peças montadas), mas o encaixe só se conhece depois de imprimir. A resistência à água
não foi ensaiada: use as caixas em local coberto.

## Organização

Cada caixa tem sua pasta:

- **`model.py`:** o modelo paramétrico, com todas as medidas num dicionário.
- **`export.py`:** gera os STLs, já orientados para impressão, e o `verification.json`.
- **`render.py`:** gera a imagem de prévia; precisa da interface do FreeCAD.
- **`print/`:** os STLs para imprimir e a imagem de prévia.
- **`revision.json`:** a revisão, o SHA-256 de cada STL e os limites conhecidos.
- **`README.md`:** o que imprimir, as ferragens, a montagem e o que conferir.

Os nomes dos STLs se mantêm entre revisões. Cada revisão recebe a tag `<caixa>-rNN`, por
exemplo `wide-r05`.

## Requisitos

[FreeCAD](https://www.freecad.org/) 1.1 para regerar as peças. Testado com o 1.1.4. Para
imprimir, bastam os STLs.

## Licença

[Apache License 2.0](LICENSE).
