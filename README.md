# Urban Routes | Automatización web con POM

## Descripción del proyecto

Proyecto de automatización de pruebas de la plataforma Urban Routes, enfocado en validar el proceso completo de solicitud de un taxi mediante pruebas automatizadas.

Se implementó el patrón de diseño Page Object Model (POM) para organizar los localizadores y métodos de interacción con la aplicación.

## Pruebas automatizadas

Se desarrollaron 9 pruebas independientes para validar diferentes etapas del proceso de solicitud de un taxi.

Entre los escenarios cubiertos se encuentran:

- Configuración de las direcciones de origen y destino.
- Selección de la tarifa Comfort.
- Registro y confirmación del número telefónico.
- Configuración del método de pago.
- Selección de opciones adicionales del viaje.
- Confirmación de la solicitud del taxi.

## Técnicas y herramientas utilizadas

- **Python:** lenguaje utilizado para desarrollar las pruebas.
- **Selenium:** automatización de las interacciones con la aplicación web.
- **Pytest:** ejecución y organización de los casos de prueba.
- **Page Object Model (POM):** organización del código mediante clases y métodos.
- **WebDriverWait:** implementación de esperas explícitas.
- **expected_conditions:** condiciones para sincronizar las interacciones con los elementos de la página.
- **By:** localización de elementos mediante diferentes estrategias.

## Estructura del repositorio

```text
qa-project-Urban-Routes-es/
│
├── .gitignore
├── README.md
├── data.py
└── main.py
```

## Ejecución de las pruebas automatizadas

**1.** Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

**2.** Instalar las dependencias necesarias:

```bash
pip install selenium
pip install pytest
```

**3.** Ejecutar las pruebas desde PyCharm utilizando el botón Play o desde la terminal:

```bash
pytest
```

## Objetivo del proyecto

Aplicar técnicas de automatización web mediante Selenium y Pytest, utilizando el patrón Page Object Model para validar el proceso de solicitud de un taxi y mantener una estructura organizada del código.
