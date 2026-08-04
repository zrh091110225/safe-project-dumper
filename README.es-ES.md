# safe-project-dumper

> Extrae el conocimiento del proyecto en documentos Markdown estructurados sin copiar el código fuente.

Una habilidad de asistente de IA para codificación que analiza el código fuente para generar documentos de arquitectura, documentación de API, diseño de base de datos y diagramas de flujo. Diseñada para la transferencia de conocimiento cuando los empleados dejan una empresa: pueden llevarse la documentación, no el código.

## Plataformas compatibles

- **Claude Code** - Usa `/project-dumper` o describe tu necesidad
- **Codex** - Usa `/project-dumper` o describe tu necesidad
- **GStack** - Usa `/project-dumper` o describe tu necesidad

## Caso de uso

Cuando los empleados dejan una empresa, a menudo no pueden copiar el código fuente debido a políticas de seguridad. Esta herramienta les ayuda a extraer:

- Diseño de arquitectura
- Documentación de API
- Esquema de base de datos
- Flujos de negocio
- Destacados de diseño

Esto es **transferencia de conocimiento**, no robo de código.

## Características

- **Análisis automático** - Escanea la estructura del proyecto, detecta lenguaje/framework
- **Salida de múltiples documentos** - README, ARCHITECTURE, API, DATABASE, FLOWS
- **Diagramas Mermaid** - Diagramas de arquitectura, gráficos de flujo, máquinas de estados
- **Habilidad de IA** - Fácil de usar con asistentes de codificación con IA (Claude Code, Codex, GStack)
- **Sin copia de código** - Solo genera documentación, no código fuente
- **Amigable con ingeniería inversa** - Lo suficientemente detallado para reconstruir el proyecto

## Uso

```bash
# Uso básico (analizar el directorio actual)
/project-dumper

# Especificar directorio de salida
/project-dumper -o ./docs

# Especificar directorio del proyecto
/project-dumper -p /ruta/al/proyecto -o ./output

# Opciones completas
/project-dumper --project /ruta/al/proyecto --output ./docs
```

## Archivos de salida

La herramienta genera estos archivos Markdown:

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Descripción general del proyecto, pila tecnológica |
| `ARCHITECTURE.md` | Diseño de arquitectura, capas, patrones |
| `API.md` | Documentación de endpoints de API |
| `DATABASE.md` | Esquema y modelos de base de datos |
| `FLOWS.md` | Flujos de negocio con diagramas Mermaid |

## Proyectos compatibles

- Java / Spring Boot
- JavaScript / TypeScript / Node.js
- Python
- Go
- Y más...

## Ejemplos

Consulta el directorio `examples/` para ver muestras de salida.

- [mall-ecommerce](./examples/mall/) - Sistema de comercio electrónico Spring Boot
- [boss-auto-apply](./examples/boss-auto-apply/) - Extensión de Chrome

## Instalación

### Para Claude Code

```bash
# Copia SKILL.md al directorio de habilidades de Claude Code
cp SKILL.md ~/.claude/skills/project-dumper/
```

### Para Codex

```bash
# Copia SKILL.md al directorio de habilidades de Codex
cp SKILL.md ~/.codex/skills/project-dumper/
```

### Para GStack

```bash
# Copia al directorio de habilidades de GStack
cp SKILL.md ~/.claude/skills/project-dumper/
```

## Detalles técnicos

- **Lenguaje**: Definición de habilidad (funciona con Claude Code, Codex, GStack)
- **Framework**: API de Habilidad de Asistente de IA
- **Salida**: Archivos Markdown con diagramas Mermaid

## Opcional: Herramienta de división QR sin conexión

Este repositorio incluye un flujo de trabajo opcional de división de documentos sin conexión para transferencia multi-QR.

Usa este modo cuando la exportación directa de archivos está bloqueada por controles de seguridad corporativos más estrictos.
En ese caso, puedes convertir un documento en fragmentos QR ordenados, moverlos escaneándolos y reconstruir el contenido original en otro lado.

- Script: `tools/offline_qr_bundle.py`
- Modo: ruta de transferencia opcional puramente sin conexión (divide un documento en múltiples cargas útiles QR)
- Ordenación: nombre de archivo + índice incrustado (`name__003-of-012`)
- Integridad: CRC32 del fragmento + SHA256 del documento completo

### Cómo funciona

1. Lee el documento de entrada como bytes
2. Comprime una vez (zlib)
3. Divide los bytes comprimidos en fragmentos que quepan en `--max-qr-chars`
4. Escribe una carga útil por fragmento (`.txt`, y opcionalmente `.png`)
5. Reconstruye recopilando todos los fragmentos, validando CRC/SHA256 y luego descomprimiendo

### Empaquetar (dividir en fragmentos + archivos de carga útil)

```bash
python3 tools/offline_qr_bundle.py pack \
  --input ./docs/ARCHITECTURE.md \
  --outdir ./out/qr-chunks \
  --name architecture \
  --max-qr-chars 1200 \
  --no-png
```

Notas:
- De forma predeterminada, la herramienta escribe cargas útiles `.txt` para cada fragmento.
- Si `qrcode[pil]` está instalado y no estableces `--no-png`, se generarán imágenes QR PNG.
- Si `qrcode[pil]` falta, el comando ahora degrada gracefulmente a solo carga útil `.txt` (con advertencia).
- De forma predeterminada, la herramienta instala automáticamente `qrcode[pil]` cuando se solicita generación PNG y falta la dependencia.
- Agrega `--no-auto-install-qrcode` si deseas deshabilitar el comportamiento de instalación automática.
- En entornos Python con restricciones PEP 668, la instalación automática puede estar bloqueada; usa un virtualenv si es necesario.
- Para estabilidad al escanear con cámara, comienza con `--max-qr-chars 600~1200`.

### Parámetros de empaquetado

| Parámetro | Descripción | Predeterminado |
|-----------|-------------|----------------|
| `--input` | Ruta del documento de entrada | Requerido |
| `--outdir` | Directorio de salida para archivos de fragmentos | Requerido |
| `--name` | Prefijo de nombre de archivo de fragmento | nombre base del archivo de entrada |
| `--max-qr-chars` | Máximo de caracteres por carga útil QR | `1200` |
| `--compress-level` | Nivel de compresión zlib (`0-9`) | `9` |
| `--ecc` | Corrección de errores QR (`L/M/Q/H`) | `M` |
| `--no-png` | Solo escribir carga útil de texto (sin PNG) | deshabilitado |
| `--no-auto-install-qrcode` | Deshabilitar instalación automática de `qrcode[pil]` cuando se solicita PNG y falta la dependencia | deshabilitado |

### Desempaquetar (reensamblar)

```bash
python3 tools/offline_qr_bundle.py unpack \
  --indir ./out/qr-chunks \
  --output ./out/recovered-ARCHITECTURE.md
```

Opcional:
- `--doc-id <id>` para reconstruir solo un documento objetivo cuando hay varios documentos mezclados en un directorio.

### Archivos de salida

- `name__001-of-016.txt`: Texto de carga útil QR para un fragmento
- `name__001-of-016.png`: Imagen QR (solo cuando no se usa `--no-png`)
- `name__manifest.json`: resumen de metadatos (recuento de fragmentos, configuración)

### Verificación y casos de fallo

- Fragmentos faltantes: el desempaquetado falla con un error claro de índice faltante
- Documentos mixtos: el desempaquetado falla en caso de incompatibilidad de metadatos
- Carga útil manipulada: el desempaquetado falla si no coincide el CRC del fragmento o el SHA256 del documento

### Ejemplo de extremo a extremo

```bash
# empaquetar
python3 tools/offline_qr_bundle.py pack \
  --input README.md \
  --outdir ./out/qr-demo \
  --name readme \
  --max-qr-chars 350 \
  --no-png

# reconstruir
python3 tools/offline_qr_bundle.py unpack \
  --indir ./out/qr-demo \
  --output ./out/recovered-README.md

# verificar
shasum -a 256 README.md ./out/recovered-README.md
```

## ¿Por qué esta herramienta?

1. **Cumplimiento de seguridad** - Genera documentación, no código
2. **Transferencia de conocimiento** - Preserva la intención de diseño y la lógica de negocio
3. **Preparación para entrevistas** - Excelente para preparar resúmenes de proyectos
4. **Integración de nuevos miembros** - Ayuda a los nuevos miembros del equipo a entender el sistema
5. **Ingeniería inversa** - Lo suficientemente detallado para reconstruir el proyecto

## Descargo de responsabilidad / 免责声明

Esta herramienta se proporciona **gratuitamente** únicamente para fines legítimos de transferencia de conocimiento y documentación.

Cualquier uso que involucre acceso no autorizado, robo de datos, abuso de credenciales, violaciones de privacidad o cualquier otra actividad ilegal está estrictamente prohibido.
Los usuarios son los únicos responsables de cómo utilizan esta herramienta y de cumplir con todas las leyes aplicables, políticas empresariales y obligaciones contractuales.
Los autores y colaboradores no asumen **ninguna responsabilidad** por pérdidas, daños, disputas legales o consecuencias derivadas del uso indebido, incluyendo pero no limitado al robo de información u otra conducta ilícita.

Para un lenguaje legal más estricto en chino, consulta [DISCLAIMER.md](./DISCLAIMER.md).

## Licencia

MIT

## Autor

Creado para empleados que necesitan transferir conocimiento cuando dejan una empresa.
