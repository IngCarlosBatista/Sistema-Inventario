📦 Sistema de Control de Inventario
📝 Descripción del Proyecto
Este sistema surge como una solución tecnológica profesional diseñada para resolver las ineficiencias operativas comunes en la gestión de mercancías. La falta de automatización y el registro manual suelen generar pérdidas económicas, descuadres críticos en almacén y retrasos en la toma de decisiones estratégicas.

Esta aplicación optimiza y digitaliza por completo el flujo operativo de cualquier comercio, ofreciendo un control preciso, centralizado y en tiempo real sobre las entradas, salidas y existencias reales de productos.

🎯 Objetivos del Proyecto
Objetivo General
Desarrollar una aplicación de escritorio robusta para la gestión y control de inventarios, optimizando el registro de mercancías y garantizando la integridad de los datos de stock mediante un entorno seguro, intuitivo y eficiente.

Objetivos Específicos
Módulo CRUD Completo: Implementar un panel administrativo dinámico para la creación, lectura, actualización y eliminación de productos.

Alertas de Stock Crítico: Desarrollar un sistema automatizado de notificaciones visuales para advertir cuando un producto esté próximo a agotarse.

Persistencia Local Eficiente: Integrar SQLite para garantizar la consistencia de la información sin dependencias complejas.

Exportación de Datos: Funcionalidad integrada para generar reportes en formato Excel (XLSX) con un solo clic.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.x

Base de Datos: SQLite 3

Interfaz Gráfica: Ttkbootstrap

Manipulación de Datos: Pandas & Openpyxl

⚙️ Instrucciones de Instalación y Ejecución
1. Clonar el repositorio
Bash
git clone https://github.com/IngCarlosBatista/Sistema-Inventario.git
cd Sistema-Inventario
2. Instalación de dependencias
El sistema requiere librerías externas para la interfaz y la generación de reportes. Instálalas ejecutando el siguiente comando en tu terminal:

Bash
pip install ttkbootstrap pandas openpyxl
3. Ejecución del sistema
Para iniciar la aplicación, simplemente ejecuta el script principal:

Bash
python main.py
💡 Notas Adicionales
Reportes: Al utilizar el botón "Exportar a Excel", se abrirá una ventana emergente para que selecciones la ruta de destino donde deseas guardar el archivo.

Base de Datos: El archivo inventario.db se encuentra dentro de la carpeta /database/. Asegúrate de no moverlo para que el sistema mantenga la conexión correctamente.