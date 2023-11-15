Feature: Como usuario quiero obtener una con todos los logs

    Scenario: Obtener lista de todos los logs registrados en el sistema
        Given El servicio de "Obtener lista de logs" debe estar activo
        When El usuario hace la solicitud al servicio "Obtener lista de logs"
        Then La API manda un código de estado "200" que indica que la operación ha sido exitosa
         And El usuario recibe una respuesta exitosa con la lista de todos los logs del sistema registrados en el momento

Feature: Como usuario quiero registrar logs

    Scenario: Registrar un nuevo logs
        Given El usuario debe ingresar la informacion requerida para registar los logs (Acción, Aplicación, Fecha, Ip, Metodo HTTP, Modulo, Ruta, Tipo de logs, Token, usuario)
        When El usuario haga la acción de "Registrar logs"
        Then La API manda un código de estado "201" que indica que la operación ha sido exitosa
         And El usuario recibe una respuesta exitosa indicando que se ha registrado el log

    Scenario: Registrar un log con un dato faltante
        Given El usuario debe ingresar la información requeridoa para registrar los logs (Acción, Aplicación, Fecha, Ip, Metodo HTTP, Modulo, Ruta, Tipo de logs, Token)
         And El usuario olvida ingresar un camo requerido como "Usuario"
        When El usuario haga la acción de "Registrar logs"
        Then La API manda un código de estado "400" que indica que la operación ha fallado
         And El usuario recibe un mensaje indicando que la operación ha fallado debido a un dato faltante
         And La API indica el dato faltante

Feature: Como usuario quiero obtener los logs de una aplicación en especifico

    Scenario: Obtener logs de una aplicación dado su nombre
        Given El usuario debe ingresar el nombre de la aplicación de la cual quiere obtener los logs
        When El usuario haga la acción de "Obtener Logs por nombre"
        Then La API manda un código de estado "200" que indica que la operación ha sido exitosa
         And El usuario recibe una lista con todos los logs de la aplicación que indico
    
    Scenario: El usuario ingresa el nombre una aplicación que no existe
        Given El usuario debe ingresar el nombre de la aplicación de la cual quiere obtener los logs
         And Ingresa un nombre de una aplicación que no existe
        When El usuario haga la acción de "Obtener Logs por nombre"
        Then La API manda un código de estado "200" 
         And El usuario recibe una lista la cual no contien no contiene nada
         
    