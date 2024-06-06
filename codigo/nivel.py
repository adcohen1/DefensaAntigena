class Nivel:
    def __init__(self, datos, map_imagen):
        self.tile_map = []
        self.waypoints = []
        self.datos_nivel = datos
        self.imagen = map_imagen

    def pocesar_datos(self):
        # buscar la información relevante en el archivo json
        ruta = []
        for layer in self.datos_nivel['layers']:
            if layer['name'] == 'posiciones':
                self.tile_map = layer['data']
            elif layer['name'] == 'waypoints' or layer['name'] == 'waypoints2':
                for obj in layer['objects']:
                    xfix = obj['x']
                    yfix = obj['y']
                    waypoint_data = obj['polyline']
                    for punto in waypoint_data:
                        temp_x = punto.get('x') + xfix
                        temp_y = punto.get('y') + yfix
                        ruta.append((temp_x, temp_y))
                self.waypoints.append(ruta)
                ruta = []

    '''def procesar_waypoints(self, datos):
        # iterar sobre los waypoints para extraer los sets individuales de coordenadas x y y
        for punto in datos:
            temp_x = punto.get('x')
            temp_y = punto.get('y')
            self.waypoints.append((temp_x, temp_y))'''

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (0, 0))
