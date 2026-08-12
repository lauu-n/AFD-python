# Autómata Finito Determinista (AFD) en Python

---

## Descripción

- Este proyecto implementa un simulador de Autómatas Finitos Deterministas (AFD) en Python. 
- El programa recibe dos archivos de texto:
  - *conf.txt*: describe la configuración del AFD: estados, alfabeto, estado inicial, estados finales y función de transición.
  - *cadenas.txt*: contiene las cadenas de entrada que se quieren evaluar, una por línea.

Con esta información, el autómata reconstruye y procesa cada cadena símbolo por símbolo.  

Se muestra en consola la secuencia de movimientos de estado a estado, cuando se mueve al leer cada símbolo.  

Su resultado final es ACEPTADO o RECHAZADO.  

Se basó en el ejercicio 3.16 del libro de Aho, para procesar la cadena **ababbab** 
<img width="527" height="227" alt="image" src="https://github.com/user-attachments/assets/635520b8-ff2c-4897-ad1e-794ffe81441d" />



### Objetivos
  - Implementar un programa en Python capaz de leer la definición de cualquier AFD desde un archivo de configuración.
  - Simular el procesamiento de cadenas de entrada mostrando la secuencia de movimientos.

### Resultados
#### a. (a|b)*  
  Tiene un único estado, que es a la vez inicial y final, con un lazo (self-loop) para a y b. Como el * permite cero o más repeticiones de cualquier combinación de a y b, el AFD acepta cualquier cadena sobre el alfabeto {a, b}.
  - Diagrama:
    <img width="503" height="575" alt="a" src="https://github.com/user-attachments/assets/667a699d-e88f-4fdc-8ba6-901ce3d6c6fc" />
  - Ejecución:
    <img width="613" height="705" alt="image" src="https://github.com/user-attachments/assets/684291f4-2181-4f7d-848f-3e18e03e70a2" />  

#### b. (a*|b*)*
  Se genera la cadena "a" sola y b* genera "b" sola. Al repetir esa unión con el * exterior, se puede formar cualquier cadena de a y b, así que el AFD resultante es el mismo.
  - Diagrama:
    <img width="503" height="575" alt="a" src="https://github.com/user-attachments/assets/667a699d-e88f-4fdc-8ba6-901ce3d6c6fc" />
  - Ejecución:
    <img width="594" height="699" alt="image" src="https://github.com/user-attachments/assets/878fb635-fc08-4844-b50f-30d8212c2043" />  

#### c. ((ε|a)b*)*
  a puede generar "a" sola (tomando 0 b) y "b" sola (sin la 'a', con 1 b). Repitiendo eso, se puede formar cualquier cadena sobre {a, b}, así que el autómata es equivalente.
  - Diagrama:
    <img width="503" height="575" alt="a" src="https://github.com/user-attachments/assets/667a699d-e88f-4fdc-8ba6-901ce3d6c6fc" />
  - Ejecución:
    <img width="645" height="698" alt="image" src="https://github.com/user-attachments/assets/20ab4522-4354-4095-aec6-de5ffaba22d1" />  

#### d. (b|b)*abb(a|b)*
  (b|b)* es equivalente a b* (unir b con b no agrega nada). El patrón real es: cero o más b, luego obligatoriamente abb, y después cualquiera. Este autómata sí es selectivo.
  - Diagrama:
    <img width="555" height="221" alt="d" src="https://github.com/user-attachments/assets/a3390f6e-d737-4d71-a89d-a03b7787146a" />
  - Ejecución:
    <img width="633" height="654" alt="image" src="https://github.com/user-attachments/assets/3673e3a3-cc66-490b-b8f4-b913b505cbbb" />

### Conclusiones
1. Los tres primeros incisos (a, b y c) parecen definir lenguajes distintos por tener expresiones  diferentes, pero al analizarlos se comprueba que los tres son equivalentes a (a|b)*: cualquier cadena sobre {a, b} es aceptada
2. El inciso d. sí tiene una condición: exige que, tras un prefijo de b, aparezca literalmente
3. Separar la lógica (en *conf_x.txt*) del autómata (AFD.py) permitió probar los cuatro incisos sin modificar el código, solo cambiando el archivo de configuración.
4. Usar cadenas de prueba adicionales (abb, bbabb, aab, bbb) además de la del enunciado ayudó a confirmar que el AFD del inciso d. diferencia correctamente entre cadenas aceptadas y rechazadas, y no solo "coincide".
 
---

## Código

### Directorio:
- Script principal: lee conf.txt y cadenas.txt, simula el AFD: *AFD.py*
- Configuraciones para cada inciso: *configs.txt*
  - *conf_a.txt*
  - *conf_b.txt*
  - *conf_c.txt*
  - *conf_d.txt*
- Cadenas de prueba: *cadenas.txt*

### *config.txt*
```
states: q0,q1,q2          # nombres de los estados, separados por coma
alphabet: a,b               # símbolos del alfabeto
start: q0                   # estado inicial
accept: q1,q2                # estados finales (de aceptación), separados por coma
transitions:
q0,a->q1                    # desde q0, leyendo 'a', se va a q1
q0,b->q0
...
```

### *cadenas.txt*
Una cadena por línea.
```
ababbab
abb
bbabb
```

### Configuración en Linux

Verificar Python instalado.
```
python3 --version
```

### Ejecución

1. Descargar los archivos en una carpeta.
2. Abrir una terminal y entrar a la carpeta.
```
cd ~/afd
```
3. Ejecutar pasando como argumentos el archivo de configuración y el de cadenas.
```
python3 AFD.py conf_a.txt cadenas.txt
```
*nota: cambiar conf_a.txt por conf_b.txt, conf_c.txt o conf_d.txt según el inciso*

---

#### Integrantes:
- David Avendaño
- Laura Niño
- Brayan Paredes
