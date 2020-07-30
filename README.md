### Instalación

Creamos un nuevo ambiente virtual

    virtualenv -p python3 venv

Usa el siguiente comando para activar tu nuevo ambiente virtual:

    source venv/bin/activate

En Windows seria asi:

    venv/Scripts/activate.bat

    
Cuando activas un ambiente virtual, la configuración de tu sesión de terminal es modificada para que el interprete Python almacenado dentro sea el invocado cuando escribas python. Además, el promt del terminal es modificado para incluir el nombre del ambiente virtual activado. Los cambios realizados a tu sesión de terminal son todos temporales y privados a esa sesión, por lo que no se mantendrán cuando cierres la sesión de terminal. Si trabajas con múltiples ventanas de terminal abiertas al mismo tiempo, es completamente posible tener diferentes ambientes virtuales activados en cada una de ellas. Además, el prompt del terminal es modificado para incluir el nombre del ambiente virtual activado.

Ahora que tienes un ambiente virtual creado y activado, puedes finalmente instalar Flask en él:

    (venv) $ pip install flask

Si quieres confirmar que tu ambiente virtual tiene instalado Flask, puedes iniciar el intérprete Python e importar Flask en él:

    >>> import flask
    >>> _

Ahora supongamos que estas en Windows habria que escribir esto:

    set FLASK_DEBUG=1
    set FLASK_APP=app.py
    flask run 

Y ahora cada vez que actualices algun archivo Flask se reiniciará.