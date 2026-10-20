# ABZ

ABZ es una utilidad de línea de comandos escrita en Python que permite comprimir y descomprimir archivos. Su diseño admite intercambiar el algoritmo de compresión (códec) utilizado, de modo que sea posible incorporar nuevos métodos sin modificar el resto de la herramienta.

## Requisitos

* Python 3.13 o superior

## Instalación

Clone el repositorio e ingrese al directorio del proyecto:

```bash
git clone <URL-del-repositorio>
cd abz
```

No se requieren dependencias adicionales.

## Uso

Para ver la ayuda del programa, ejecute en su terminal:

```bash
./abz -h
```

```text
usage: abz [-h] -codec {wordmap} -i FILE [-o FILE] [-d]

ABZ: compresor de archivos

options:
  -h, --help        show this help message and exit
  -codec {wordmap}  algoritmo a utilizar
  -i FILE           archivo de entrada
  -o FILE           archivo de salida (si se omite, imprime en consola)
  -d                decodificar en lugar de codificar
```

En Windows, invoque directamente al intérprete de Python:

```bash
python abz -h
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `-codec` | Algoritmo a utilizar. Actualmente disponible: `wordmap`. |
| `-i FILE` | Archivo de entrada. Es obligatorio. |
| `-o FILE` | Archivo de salida. Si se omite, el resultado se imprime en la consola. |
| `-d` | Decodifica el archivo de entrada en lugar de codificarlo. |

### Ejemplo: codificar

```bash
./abz -codec wordmap -i tmp/example.txt -o tmp/example.abz
```

### Ejemplo: decodificar

```bash
./abz -codec wordmap -d -i tmp/example.abz
```

Para guardar el resultado en un archivo en lugar de mostrarlo en la consola, agregue la opción `-o`:

```bash
./abz -codec wordmap -d -i tmp/example.abz -o tmp/example.txt
```

## Aviso

Este software se entrega sin garantía de ningún tipo. Su finalidad es servir como código de ejemplo para la asignatura "*Programación Orientada a Objetos*" del IES6017.
