Feature: Como usuario quiero registrarme

    Scenario: Registrar un nuevo usuario
        Given El usuario debe ingresar la información requerida para el registro como su nombre, apellido, fecha de nacimiento, Email y contraseña
        When El usuario haga la solicitud al servicio "Registrar usuario"
        Then La API responde con un codigo de estado "200"
        And El usuario recibe un mensaje de confirmación en donde le indica que su registro ha sido exitoso

    Scenario: El usuario no se puede registrar porque le falta algun dato
        Given El usuario debe ingresar la información requerida para el registro como su nombre, apellido, contraseña y Email,
        And No ingresar un dato obligatorio como su fecha de nacimiento
        When El usuario haga la solicitud al servicio "Registrar usuario"
        Then La API responde con un codigo de estado "401"
        And El usuario recibe un mensaje de aletar en donde le indica que no se ha podido completar su registro por un dato faltante
        And Le indica el dato faltante

    Scenario: El usuario intenta registrarse poniendo un de menera erronea el formato de fecha
        Given El usuario debe ingresar la información requerida para el registro como su nombre, apellido, fecha de nacimiento, Email y contraseña
        And Coloca un formato de fecha erroneo como por ejemplo "DD-MM-AAAA"
        When El usuario haga la solicitud al servicio "Registrar usuario"
        Then La API responde con un codigo de estado "401"
        And El usuario recibe un mensaje de error en donde se le indica que no se ha podido completar su registro por un error al ingresar el formato de fecha
        And Se le indica al usuario cual es el formato de fecha correcto

Feature: Como usuario quiero ingresar sesion

    Scenario: El usuario quiere ingresar sesion
        Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
        When El usuario haga uso de la acción "Iniciar sesion"
        Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
        And Se le entrega al usuario un token valido

    Scenario: El usuario quiere ingresar sesion con una contraseña incorrecta
        Given El usuario debe ingresar sesion con su Email y contraseña con la cual cree que se registro
        When Ingresa una contraseña incorrecta
        And El usuario haga uso de la acción "Iniciar sesion"
        Then La API responde con un código de estado "400" que indica que la operación ha tenido un fallo
        And Un mensaje indicando que no puede ingresar sesion debido a que la contraseña ingresada es invalida


Feature: Como usuario quiero ingresar sesion en el perfilx

    Scenario: El usuario quiere ingresar sesion
        Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
        When El usuario haga uso de la acción "Iniciar sesion"
        Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
        And Se le entrega la información de su perfil

    Scenario: El usuario quiere ingresar sesion con una contraseña incorrecta
        Given El usuario debe ingresar sesion con su Email y contraseña con la cual cree que se registro
        When Ingresa una contraseña incorrecta
        And El usuario haga uso de la acción "Iniciar sesion"
        Then La API responde con un código de estado "400" que indica que la operación ha tenido un fallo
        And Un mensaje indicando que no puede ingresar sesion debido a que la contraseña ingresada es invalida


Feature: Como usuario quiero actualizar los datos del perfil

    Scenario: El usuario quiere actualizar uno o más datos de su cuenta
        Given El usuario debe ingresar sesion con su credenciales con la cual se registró
        And Debe estar autenticado
        When El usaurio proporciona la información que desea actualizar, la cual puede ser nombre, apellido y Email
        And El usuario haga uso del servicio "Actualizar información"
        Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
        And Un mensaje de confirmación de que la operación fue exitosa

    Scenario: El usuario quiere actualizar su información sin autenticar su cuenta
        Given El usuario debe ingresar sesion con su apodo con la cual se registró
        And No esta autenticado o tiene la sesión vencida
        When El usaurio proporciona la información que desea actualizar, la cual puede ser nombre, apellido y Email
        And El usuario haga uso del servicio "Actualizar información"
        Then La API responde con un código de estado "400" que indica que la operación ha tenido un fallo
        And Un mensaje de error indicando que no es posible actualiza la informacion ya que la sesion ha ha expirado
        And Se le indica al usuario que debe autentucarse para actualiza la informacion



