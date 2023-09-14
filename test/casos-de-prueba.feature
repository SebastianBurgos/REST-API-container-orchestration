Feature: Como usuario quiero obtener una lista de los usuarios para mostrarlos

Scenario: Obtener una lista de todos los usuarios
    Given El servicio de "Obtener lista de usuarios" debe estar activo
    When El usuario hace la solicitud al servicio "obtener lista de usuarios"
    Then La API manda un código de estado "200" que indica que la operación ha sido exitosa
     And El usuario recibe una respuesta exitosa con la lista de usuarios
    
Scenario: Obtener una lista de usuarios vacia 
    Given El servicio de "Obtener lista de usuarios" debe estar activo
    When El usuario hace la solicitud al servicio "obtener lista de usuarios"
     And El usuario llegue al final de la lista y  desea continuar
    Then La API responde con un codigo de estado "404"
     And El usuario recibe un mensaje de alerta que le informa que no existen más usuarios por ver 

Scenario: Obtener una lista de usuarios con un nombre especificado por el usuario
    Given El servicio de "Obtener lista de usuarios" debe estar activo
    When El usuario proporcine un nombre que se coincida con al menos un usuario que este registrado en la base de datos
     And El usuario hace la solicitud al servicio "obtener lista de usuarios"
    Then La API responde con un codigo de estado "200"
    And El usuario recibe una respuesta exitosa con la lista de usuarios con el nombre que ingreso en la consulta

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

Feature: Como usuario quiero buscar un usuario por su ID

Scenario: Buscar un usuario por su ID
    Given El usuario debe proporciona un ID que se coincida con al menos un usuario que este registrado en la base de datos
    When El usuario haga uso del servicio "Buscar usuario por ID"
    Then La API responde con un codigo de estado "200"
     And El usuario recibe un mensaje con la información del usuario que indico

Scenario: El usuario intenta buscar a otro usuario que no se encuentra registrado
    Given El usuario debe proporciona un ID que NO coincida con al menos un usuario que este registrado en la base de datos
    When El usuario haga uso del servicio "Buscar usuario por ID"
    Then La API responde con un mensaje de estado "404"
     And El usuario recibe un mensaje de que no se ha podido encontrar el usuario debido a que el ID ingreado no coincide con el de un usuario registrado

Feature: Como usuario quiero elminar mi cuenta

Scenario: El usuario quiere elminiar su cuenta
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
     And Debe estar autenticado
    When El usuario haga uso del servicio "Eliminar cuenta"
    Then La API responde con un un código de estado "200" que indica que la operación ha sido exitosa
     And Un mensaje de despedida informando que la cuenta ha sido eliminada de manera definitiva

Scenario: El usuario quiere elminiar su información y cuenta sin autenticarse 
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
     And No esta autenticado o tiene la sesión vencida
    When El usuario haga uso del servicio "Eliminar cuenta"
    Then La API responde con un un código de estado "401" que indica que la operación ha tenido un fallo
     And Un mensaje de error indicando que no es posible eliminar la cuenta ya su sesion ha expirado
     And Se le indica al usuario que debe autenticarse para eliminar la cuenta  
    
Feature: Como usuario quiero actualizar mi datos

Scenario: El usuario quiere actualizar uno o más datos de su cuenta
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
     And Debe estar autenticado
    When El usaurio proporciona la información que desea actualizar, la cual puede ser nombre, apellido y Email
     And El usuario haga uso del servicio "Actualizar información"
    Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
     And Un mensaje de confirmación de que la operación fue exitosa

Scenario: El usuario quiere actualizar su información sin autenticar su cuenta
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual se registró
     And No esta autenticado o tiene la sesión vencida
    When El usaurio proporciona la información que desea actualizar, la cual puede ser nombre, apellido y Email
     And El usuario haga uso del servicio "Actualizar información"
   Then La API responde con un código de estado "400" que indica que la operación ha tenido un fallo
     And Un mensaje de error indicando que no es posible actualiza la informacion ya que la sesion ha ha expirado
     And Se le indica al usuario que debe autentucarse para actualiza la informacion
    
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

Feature: Como usuario quiero cambiar mi ontraseña

Scenario: El usuario quiere cambiar la contraseña de su cuenta
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual cree que se registro
     And Debe estar autenticado
    When El usuario haga la solicitud al servicio "Actualizar contraseña"
     And Agregar la contraseña nueva
    Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
     And Un mensaje indicando que la contraseña ha sido actualizada de manera exitosa

Scenario: El usuario quiere cambiar la contraseña de su cuenta sin autenticarse
    Given El usuario debe ingresar sesion con su Email y contraseña con la cual cree que se registro
     And No se ha autenticado
    When El usuario haga la solicitud al servicio "Actualizar contraseña"
     And Agregar la contraseña nueva
    Then La API responde con un código de estado "400" que indica que la operación ha tenido un fallo
     And Un mensaje de error indicando que no es posible actualiza la contraseña ya que su sesion ha expirado
     And Se le indica al usuario que debe autenticarse para actualiza la contrseña
     

Feature: Como usuario quiero recuperar mi contraseña

Scenario: El usuario se le olvido la contraseña
    Given El usuario intenta ingresar sesion proporcionado su correo
     And Una contraseña erronea
    When El usuario haga uso del servicvo "Recuperar contraseña"
    Then La API responde con un código de estado "200" que indica que la operación ha sido exitosa
     And Un mensaje en donde se le indica que se le ha enviado al correo un link para recuperar su cuenta
     And Enviar un enlace de recuperación al correo del usuario







