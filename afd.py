#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
afd.py — Simulador de AFD (DFA)
Lee un archivo de configuración (Conf.txt) y un archivo de cadenas (Cadenas.txt),
y reporta si cada cadena es ACEPTADA o RECHAZADA.

Uso:
    python3 afd.py Conf.txt Cadenas.txt
Si omites argumentos, usa por defecto: Conf.txt y Cadenas.txt en el directorio actual.
"""

import sys
from dataclasses import dataclass
from typing import Dict, Set, Tuple

@dataclass
class DFA:
    states: Set[str]                      # Conjunto de estados
    alphabet: Set[str]                    # Conjunto del alfabeto (símbolos de 1 carácter)
    start: str                            # Estado inicial
    accept: Set[str]                      # Conjunto de estados de aceptación
    delta: Dict[Tuple[str, str], str]     # Función de transición: (estado, símbolo) -> estado destino

    def run(self, s: str) -> bool:
        """ Ejecuta el AFD sobre la cadena s y devuelve True si es aceptada, False en caso contrario. """
        cur = self.start
        for ch in s:
            if ch not in self.alphabet:
                # Si el símbolo no pertenece al alfabeto, rechaza
                return False
            nxt = self.delta.get((cur, ch))
            if nxt is None:
                # Si no hay transición definida, rechaza
                return False
            cur = nxt
        # La cadena es aceptada si termina en un estado de aceptación
        return cur in self.accept


def _strip_comment(line: str) -> str:
    """ Quita comentarios (todo lo que esté después de '#') y espacios extra. """
    if '#' in line:
        line = line.split('#', 1)[0]
    return line.strip()


def parse_config(path: str) -> DFA:
    """ Parsea el archivo Conf.txt y construye el AFD. """
    with open(path, 'r', encoding='utf-8') as f:
        lines = [_strip_comment(l) for l in f.readlines()]
    # descartar líneas vacías
    lines = [l for l in lines if l]

    i = 0
    def read_field(prefix: str) -> str:
        nonlocal i
        if i >= len(lines) or not lines[i].lower().startswith(prefix):
            raise ValueError(f"Se esperaba la línea '{prefix}...' en {path}")
        val = lines[i].split(':', 1)[1].strip() if ':' in lines[i] else ''
        i += 1
        return val

    # Leer secciones obligatorias
    states_s = read_field('states:').replace(' ', '')
    alphabet_s = read_field('alphabet:').replace(' ', '')
    start_s = read_field('start:').strip()
    accept_s = read_field('accept:').replace(' ', '')

    # Validar encabezado de transiciones
    if i >= len(lines) or lines[i].lower() != 'transitions:':
        raise ValueError("Se esperaba la línea 'transitions:'")
    i += 1

    # Construir conjuntos
    states = set([s for s in states_s.split(',') if s])
    alphabet = set([a for a in alphabet_s.split(',') if a])
    accept = set([a for a in accept_s.split(',') if a])

    # Validaciones básicas
    if start_s not in states:
        raise ValueError(f"El estado inicial '{start_s}' no pertenece a 'states'")
    if not accept.issubset(states):
        raise ValueError("Algún estado de aceptación no está en la lista de estados")

    # Leer transiciones
    delta: Dict[Tuple[str, str], str] = {}
    for line in lines[i:]:
        try:
            left, dest = line.split('->')
            origin, sym = left.split(',')
            origin = origin.strip()
            sym = sym.strip()
            dest = dest.strip()
        except Exception:
            raise ValueError(f"Transición mal formada: '{line}'")

        if origin not in states or dest not in states:
            raise ValueError(f"Estado desconocido en transición: {line}")
        if sym not in alphabet:
            raise ValueError(f"Símbolo '{sym}' fuera del alfabeto")

        key = (origin, sym)
        if key in delta:
            raise ValueError(f"Transición duplicada: {line}")
        delta[key] = dest

    return DFA(states=states, alphabet=alphabet, start=start_s, accept=accept, delta=delta)


def main(argv):
    conf = argv[1] if len(argv) > 1 else 'Conf.txt'
    cad = argv[2] if len(argv) > 2 else 'Cadenas.txt'

    dfa = parse_config(conf)

    total = 0
    aceptadas = 0
    with open(cad, 'r', encoding='utf-8') as f:
        for raw in f:
            s = raw.rstrip('\n')
            total += 1
            ok = dfa.run(s)
            if ok:
                aceptadas += 1
            etiqueta = 'ACEPTADA' if ok else 'RECHAZADA'
            mostrar = s if s != '' else 'ε'  # cadena vacía como ε
            print(f"{mostrar}: {etiqueta}")
    print(f"\nResumen: {aceptadas}/{total} aceptadas")


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
