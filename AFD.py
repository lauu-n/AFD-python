import sys


def parse_config(path):
    lines = []
    with open(path) as f:
        for l in f:
            l = l.split('#')[0].strip()   # quitamos el comentario primero, y luego los espacios
            if l:                          # solo agregamos si queda algo -> evita que una línea
                lines.append(l)            # de puro comentario descuadre los índices fijos

    # líneas fijas: 0=states, 1=alphabet, 2=start, 3=accept, 4="transitions:", 5+ = transiciones
    start = lines[2].split(':')[1].strip()
    accept = set(lines[3].split(':')[1].strip().split(','))

    delta = {}
    for line in lines[5:]:
        origen_sim, destino = line.split('->')
        origen, sim = origen_sim.split(',')
        delta[(origen.strip(), sim.strip())] = destino.strip()

    return start, accept, delta


def run(cadena, start, accept, delta):
    estado = start
    pasos = [f"  Estado inicial: {estado}"]
    for c in cadena:
        if (estado, c) not in delta:
            pasos.append(f"  No hay transición desde {estado} con '{c}' -> se rechaza")
            return False, pasos
        destino = delta[(estado, c)]
        pasos.append(f"  {estado} --{c}--> {destino}")
        estado = destino
    return estado in accept, pasos


def main():
    conf, cad = sys.argv[1], sys.argv[2]
    start, accept, delta = parse_config(conf)

    with open(cad) as f:
        for linea in f:
            s = linea.rstrip('\n')
            if not s:
                continue
            aceptada, pasos = run(s, start, accept, delta)
            print(f"Cadena: {s if s else 'ε'}")
            for p in pasos:
                print(p)
            print('Resultado:', 'ACEPTADA' if aceptada else 'RECHAZADA')
            print()


if __name__ == '__main__':
    main()