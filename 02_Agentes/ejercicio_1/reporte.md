# Respuestas

- ¿Qué agentes lograron salir con el oro en tu mapa y cuáles no?
> Solo el utility based model

- ¿Por qué el agente de reflejo simple falla (o tiene suerte) en tu diseño?
> Porque no tiene memoria. Cuando el agente detecta una brisa o hedor, gira a la derecha pero no recuerda que casillas ya visito, creando ciclos infinitos

- ¿Cómo cambia el resultado del agente basado en modelo si acercas o alejas un pit de la casilla inicial?
> Cuando esta mas lejos esten los pozos del inicio, mas opciones sin brisa tiene la posicion inicial, aumentando las opciones de exploracion segura, por lo que aumenta la probabilidad de encontrar una ruta al oro