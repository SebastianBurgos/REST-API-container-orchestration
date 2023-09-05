Feature: Como usuario quiero obtener una lista de los usuarios para mostrarlos

Scenario: Obtener una lista de usuarios paginada exitosamente
    Given: El usuario debe ingresar el número página "1" y el numero de usuarios por página "5"
    When: El usuario hace la solicitud al metodo get_users()
    Then: El usuario recibe una respuesta exitosa con la lista de usuarios, la API manda un código de estado "200"
    
Scenario: Obtener una lista de usuarios paginada con valores erroneos
    Given: El usuario debe ingresar el número de página "1000" y el numero de usu por página "1001"
    When: El usuario hace la solicitud al método get_users()
    Then: La API responde con un error y un código de estado "404"

Scenario: Obtener una lista de usuarios pagianada con un nombre de usuario especifico
    Given: El usuario debe ingresar el número de página "1", el número de usuario por página "5" y el nombre por el cual desea buscar "Juan"
    When: El usuario haga la solicitud al metodo get_users():
    Then: El usuario recibe una respuesta exitosa con la lista de usuarios con el nombre que ingreso

Scenario: Obtener una lista de usuarios pagianada con un nombre de usuario invalido
    Given: El usuario debe ingresar el número de página "1", el número de usuario por página "5" y el nombre por el cual desea buscar "Sebas"
    When: El usuario haga la solicitud al metodo get_users():
    Then: La API responde con un error y un código de estado "404"

Feature: Como usuario quiero registrarme

Scenario: Registrar un nuevo usuario
    Given: El usuario debe ingresar la información requerida: Nombre: "Alejandro", apellido: Zambrano, Email: "AlejandroZ@gmail.com", clave: "12345", fecha de nacimiento: "2002-11-18"
    When: El usuario haga la solicitud al metodo register_user()
    Then: La API responde con un mensaje de confimación y un código de estado "201"

Scenario: Registrar un nuevo usuario con datos faltantes
    Given: El usuario debe ingresar la información requerida: Nombre: " ", apellido: Zambrano, Email: " ", clave: "12345", fecha de nacimiento: " "
    When: El usuario haga la solicitud al metodo register_user()
    Then: La API responde con un mensaje de error y un código de estado "412"

Scenario: Registrar un nuevo usuario con formato de fecha invalido
    Given: El usuario debe ingresar la información requerida: Nombre: "Alejandro", apellido: Zambrano, Email: "AlejandroZ@gmail.com", clave: "12345", fecha de nacimiento: "11-18-2002"
    When: El usuario haga la solicitud al metodo register_user()
    Then: La API responde con un mensaje de error y un código de estado "406"

Feature: Como usuario quiero buscar un usuario por su ID

Scenario: Buscar un usuario
    Given: El usuario debe ingresar el ID del usuario que desea buscar "2"
    When: El usuario haga la solicitud al metodo get_user_by_id
    Then: El usuario recibe un mensaje con la información del usuario que indico

Scenario: Buscar un usuario por un ID invalido
    Given: El usuario debe ingresar el ID del usuario que desea buscar "A"
    When: El usuario haga la solicitud al metodo get_user_by_id
    Then: La API responde con un mensaje de error y un código de estado "401"

Scenario: Buscar un usuario por un ID no existe
    Given: El usuario debe ingresar el ID del usuario que desea buscar "1000"
    When: El usuario haga la solicitud al metodo get_user_by_id
    Then: La API responde con un mensaje de error y un código de estado "404"

Feature: Como usuario quiero elminar mi cuenta

Scenario: El usuario quiere elminiar su información 
    Given: El usuario debe ingresar sesion y tener un token valido
    When: El usuario haga la solicitud al metodo delete_user_by_id()
    Then: La API responde con un mensaje de confirmación y un código de estado "200"

Scenario: El usuario quiere elminiar su información con un token invalido
    Given: El usuario debe ingresar sesion y tener un token invalido
    When: El usuario haga la solicitud al metodo delete_user_by_id()
    Then: La API responde con un mensaje de eror y un código de estado "401"

Feature: Como usuario quiero actualizar mi datos

Scenario: El usuario quiere actualizar su nombre
    Given: El usuario debe ingresar sesion, tener un token valido, ingresar el nombre nuevo "Juan"
    When: El usuario haga la solicitud al metodo update_user_by_id()
    Then: La API responde con un mensaje de confirmación y un código de estado "200"

Scenario: El usuario quiere actualizar su información con un token invalido
    Given: El usuario debe ingresar sesion, tener un token invalido, ingresar el nombre nuevo "Jose"
    When: El usuario haga la solicitud al metodo delete_user_by_id()
    Then: La API responde con un mensaje de eror y un código de estado "401"

Feature: Como usuario quiero ingresar sesion

Scenario: El usuario quiere ingresar sesion con datos validos
    Given: El usuario debe proporcionar su correro: "ana@example.com" y contraseña: "12345"
    When: El usuario haga la solicitud al metodo login_user()
    Then: La API responde con un mensaje de confirmación, un código de estado "200" y un token

Scenario: El usuario quiere ingresar sesion con datos invalidos
    Given: El usuario debe proporcionar su correro: "ana@example.com" y contraseña: "54321"
    When: El usuario haga la solicitud al metodo login_user()
    Then: La API responde con un mensaje de error y un código de estado "401"

Feature: Como usuario quiero cambiar mi ontraseña

Scenario: El usuario quiere cambiar la contraseña de su cuenta con token valido
    Given: El usuario debe ingresar con su correro: "ana@example.com", contraseña: "54321" y debe tener un token valido
    When: El usuario haga la solicitud al change_password()
    Then: La API responde con un mensaje de confirmación y un código de estado "200", el usuario debera ingresar una contraseña nueva

Scenario: El usuario quiere cambiar la contraseña de su cuenta con token invalido
    Given: El usuario debe ingresar con su correro: "ana@example.com", contraseña: "54321" y debe tener un token invalido
    When: El usuario haga la solicitud al change_password()
    Then: La API responde con un mensaje de error y un código de estado "401"

Feature: Como usuario quiero recuperar mi contraseña

Scenario: El usuario se le olvido la contraseña
    Given: El usuario debe ingresar con su correro: "ana@example.com"
    When: El usuario haga la solicitud al forgot_password()
    Then: La API responde con un mensaje de confirmación, un código de estado "200" y enviar un token de recuperación al correo del usuario







