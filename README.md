# ABZ

ABZ es una utilidad escrita en Python para *comprimir* y *descomprimir* archivos con la opción de intercambiar los algoritmos que usa la herramienta.

## Requerimientos

* Python 3.13^

## Uso

Clone el proyecto, ingrese al directorio y en su terminal escriba `./abz -h`:

```bash
usage: abz [-h] -codec {wordmap} -i FILE [-o FILE] [-d]

ABZ: compresor de archivos

options:
  -h, --help        show this help message and exit
  -codec {wordmap}  algoritmo a utilizar
  -i FILE           archivo de entrada
  -o FILE           archivo de salida (si se omite, imprime en consola)
  -d                decodificar en lugar de codificar
```

En caso de estar en un sistema operativo Windows, use directamente el interprete de Python:

```bash
python abz -h
```

### Ejemplo: codificar

```bash
./abz -codec wordmap -i tmp/example.txt -o tmp/example.abz
```

### Ejemplo: decodificar:

```bash
./abz -codec wordmap -d -i tmp/example.abz
```

## Relevante

El presente software se entrega sin garantía de ningún tipo. La finalidad última de este script es servir como código de ejemplo para la asignatura de "*Programación Orientada a Objetos*" en el IES6017.
