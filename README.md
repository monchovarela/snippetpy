### Instalación

Creamos un nuevo ambiente virtual

    virtualenv -p python3 venv

Usa el siguiente comando para activar tu nuevo ambiente virtual:

    source venv/bin/activate

Cuando activas un ambiente virtual, la configuración de tu sesión de terminal es modificada para que el interprete Python almacenado dentro sea el invocado cuando escribas python. Además, el promt del terminal es modificado para incluir el nombre del ambiente virtual activado. Los cambios realizados a tu sesión de terminal son todos temporales y privados a esa sesión, por lo que no se mantendrán cuando cierres la sesión de terminal. Si trabajas con múltiples ventanas de terminal abiertas al mismo tiempo, es completamente posible tener diferentes ambientes virtuales activados en cada una de ellas. Además, el prompt del terminal es modificado para incluir el nombre del ambiente virtual activado.

Ahora que tienes un ambiente virtual creado y activado, puedes finalmente instalar Flask en él:

    (venv) $ pip install flask

Si quieres confirmar que tu ambiente virtual tiene instalado Flask, puedes iniciar el intérprete Python e importar Flask en él:

    >>> import flask
    >>> _

Si este enunciado no genera ningún error puedes felicitarte a ti mismo, ya que Flask está instalado y listo para usarse.

La aplicación estará en un paquete. En Python, un subdirectorio que incluye un archivo __init__.py es considerando un paquete, y puede ser importado. Cuando importas un paquete, el archivo  __init__.py ejecuta y define que símbolos el paquete expone al mundo.

Creemos un paquete llamado app, que alojará la aplicación. Asegúrate de estar en el directorio microblog y ejecuta el siguiente comando:

    (venv) $ mkdir app

El archivo  __init__.py para el paquete app va a contener el siguiente código:


    from flask import Flask

    app = Flask(__name__)

    from app import routes



El script anterior simplemente crea un objeto aplicación como una instancia de la clase  Flask importada desde el paquete flask. La variable __name__ pasada a la clase Flask es una variable predefinida de Python, la cual es establecida al nombre del módulo en la que es usada. Flask usa la ubicación del módulo enviado aquí como un punto de inicio cuando necesite cargar recursos asociados como archivos de plantilla, los cuales cubriré en el Capítulo 2.  Para todo propósito práctico, pasar __name__ casi siempre será la configuración correcta de Flask. La aplicación luego importa el módulo de routes, el cual aún no existe.

Un aspecto que puede parecer confuso en un primer momento es que hay dos entidades llamadas app. El paquete app está definido por el directorio app y el script __init__.py, y es referido en la sentencia from app import routes. La variable app es definida como una instancia de clase Flask en el script __init__.py, lo cual la hace miembro del paquete app.

Otro detalle es que el módulo routes es importado al final del script y  no al comienzo como siempre se hace. Importar al final es un solución a las importaciones circulares, un problema común con aplicaciones Flask. Verás que el módulo routes necesita importar la variable app definida en este script, por lo que colocando una de las importaciones recíprocas al final evita errores provenientes de la referencia mutua entre estos dos archivos.

Entonces, que va en el módulo routes? Las rutas son las distintas URLs que la aplicación emplea. En Flask, los manejadores para las rutas de aplicación están escritos como funciones Python, llamados funciones view. Las funciones Vista son mapeadas hacia una o mas rutas URLs para que Flask sepa que lógica ejecutar cuando un cliente requiera una URL dada.

Está es tu primera función vista, la cual debes escribir en el nuevo módulo llamado app/routes.py:


    from app import app

    @app.route('/')
    @app.route('/index')
    def index():
        return "Hello, World!"


Está función view en realidad es bastante simple, solo retorna un saludo en forma de string. Las dos lineas extrañas @app.route sobre la función son decoradores, una característica única del lenguaje Python. Un decorador modifica la función que le sigue. Un patrón comun con los decoradores es usarlos para registrar funciones como callbacks para ciertos eventos. En este caso, el decorador @app.route crea una asociación entre la URL dada como argumento y la función. En este ejemplo hay dos decoradores, los cuales asocian las URLs / e /index a la función. Esto significa que cuando un navegador web requiera cualquiera de estas dos URLs, FLask invocará esta función y pasará como respuesta al navegador el valor de retorno de la misma. Si esto no se entiende aún, lo hará en un momento cuando se corra la aplicación.

Para completar la aplicación, necesitas tener un script Python que defina la instansiación de aplicaicón Flask en el nivel mas alto. Llamemos a este script snippets.py, y definámoslo como una única linea que importa la instancia de aplicación:


    from app import app

Recuerdas las dos entidades app? Aquí las puedes ver a la dos juntas en una misma sentencia. La instancia de aplicación Flask es llamada app y es un miembro del paquete  app. La sentencia from app import app importa la variable app que es miembro del paquete app. Si te resulta confuso, puedes renombrar cualquiera de las dos, el paquete o la variable.

Solo para asegurarnos que estés haciendo todo correctamente, abajo puedes ver un diagrama de la estructura del proyecto hasta ahora:


    flask/
    venv/
    app/
        __init__.py
        routes.py
    snippets.py


Lo creas o no, esta primera versión de la aplicación está lista!. Sin embargo, antes de correrla, Flask necesita sabe como importarla mediante la configuración de la variable de ambiente FLASK_APP:


    (venv) $  export FLASK_DEBUG=1
    (venv) $  export FLASK_APP=app.py
    (venv) $  flask run
    
    -- windows --
    (venv) $  set FLASK_DEBUG=1
    (venv) $  set FLASK_APP=app.py
    (venv) $  flask run

Estás listo para volar? Con el siguiente comando puedes ya correr tu primera aplicación web:


    (venv) $ flask run
    * Serving Flask app "microblog"
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
