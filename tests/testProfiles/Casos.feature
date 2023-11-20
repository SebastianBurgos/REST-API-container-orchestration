Feature: Como usuario quiero obtener una lista de los perfiles para mostrarlos

    Scenario: Obtener una lista de todos los perfiles 
        Given El servicio de "Obtener lista de perfiles" debe estar activo
        When El usuario hace la solicitud al servicio "obtener lista de perfiles"
        Then La API manda un código de estado "200" que indica que la operación ha sido exitosa
        And El usuario recibe una respuesta exitosa con la lista de perfiles


Feature: Como usuario quiero buscar un perfil por su ID

    Scenario: Buscar un perfil por su ID
        Given El usuario debe proporciona un ID que se coincida con al menos un usuario que este registrado en la base de datos
         And Debe estar  autenticado 
        When El usuario haga uso del servicio "Buscar perfi por ID"
        Then La API responde con un codigo de estado "200"
        And El usuario recibe un mensaje con la información del usuario que indico

    Scenario: El usuario intenta buscar a otro usuario que no se encuentra registrado
        Given El usuario debe proporciona un ID que NO coincida con al menos un usuario que este registrado en la base de datos
         And Debe estar  autenticado 
        When El usuario haga uso del servicio "Buscar usuario por ID"
        Then La API responde con un mensaje de estado "404"
        And El usuario recibe un mensaje de que no se ha podido encontrar el usuario debido a que el ID ingreado no coincide con el de un usuario registrado
    
    Scenario: Buscar un perfil por su ID sin autenticarse
        Given El usuario debe proporciona un ID que se coincida con al menos un usuario que este registrado en la base de datos
         And No esta autenticado 
        When El usuario haga uso del servicio "Buscar perfi por ID"
        Then La API responde con un codigo de estado "401"
        And El usuario recibe un mensaje que indica que debe estar autenticado

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



