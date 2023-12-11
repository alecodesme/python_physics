from utils import *

# Clase que representa una pelota en el juego
class Ball:
    # Constructor que inicializa la pelota con la ventana (win) y su posición inicial (current_ball_pos)
    def __init__(self, win, current_ball_pos):
        self.win = win
        self.pos = current_ball_pos

    # Método para actualizar la posición de la pelota y opcionalmente dibujarla en la pantalla
    def update(self, current_ball_pos, draw_ball=True):
        self.pos = current_ball_pos
        if draw_ball:
            self.draw_ball()

    # Método para dibujar la pelota en la pantalla
    def draw_ball(self):
        pg.draw.circle(surface=self.win, color=BLACK, center=self.pos, radius=BALL_RADIUS)

    # Método para dibujar una línea entre la pelota y la posición del mouse
    def draw_line(self, mouse_pos):
        pg.draw.circle(surface=self.win, color=RED, center=mouse_pos, radius=2)
        pg.draw.line(surface=self.win, color=BLACK, start_pos=self.pos, end_pos=mouse_pos)

    # Método para dibujar la trayectoria de la pelota basada en una lista de posiciones
    def draw_ball_path(self, ball_loc_list):
        if ball_loc_list:
            for pos in ball_loc_list:
                pg.draw.circle(surface=self.win, color=RED, center=pos, radius=2)

    # Método para calcular el ángulo entre la posición actual del mouse y la posición de la pelota
    def calculate_angle(self, current_mouse_pos):
        # Desempaqueta las coordenadas x e y de la posición actual de la pelota y del mouse
        x1, y1, x2, y2 = [*self.pos, *current_mouse_pos]

        # Calcula y devuelve un ángulo de 90 grados si las coordenadas x son iguales (evita la división por cero)
        return 90 if x1 - x2 == 0 else math.atan(abs(y1 - y2) / -(x1 - x2)) * 180 / math.pi

    # Método para calcular la velocidad inicial en los ejes x e y para el lanzamiento de la pelota
    def launch(self, time, current_mouse_pos, acceleration_time=ACCELERATION_MULTIPLIER):
        # Calcula el ángulo de lanzamiento basado en la posición actual del mouse
        angle = self.calculate_angle(current_mouse_pos)

        # Ajusta el ángulo para asegurarse de que esté en el rango adecuado (0 a 180 grados)
        angle = 180 + angle if angle < 0 else angle

        # Obtiene el tiempo actual en milisegundos para ser utilizado como tiempo de inicio del lanzamiento
        start_time = pg.time.get_ticks()

        # Calcula la aceleración multiplicando el tiempo por un factor (100 en este caso)
        acceleration = time * 100

        # Calcula las velocidades iniciales en los ejes x e y usando la fórmula de movimiento parabólico
        # Se multiplica por -1 en el eje x para ajustar la dirección de acuerdo al ángulo calculado
        start_x_velocity = -acceleration_time * acceleration * math.cos(math.radians(angle))
        start_y_velocity = abs(acceleration_time * acceleration * math.sin(math.radians(angle)))

        # Devuelve los valores calculados: tiempo de inicio, velocidad inicial en x, velocidad inicial en y
        return start_time, start_x_velocity, start_y_velocity

# Función principal del juego
def main():
    # Inicialización de la ventana y el reloj
    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # Configuración inicial de la posición de la pelota y creación de la instancia de la clase Ball
    current_ball_pos = INITIAL_BALL_POSITION
    ball = Ball(win, current_ball_pos)

    # Lista para almacenar la trayectoria de la pelota, posición actual del mouse y bandera de lanzamiento
    ball_path_list = []
    current_mouse_pos = None
    launch = False

    # Función para cerrar la aplicación
    def exit():
        pg.display.quit()
        pg.quit()
        sys.exit()

    # Bucle principal del juego
    while 1:
        win.fill(WHITE)

        # Lógica del lanzamiento de la pelota
        if launch:
            time_passed = (pg.time.get_ticks() - start_time) / 1000 * TIME_MULTIPLIER
            if current_ball_pos[1] <= INITIAL_BALL_POSITION[1]:
                x, y = start_ball_pos
                change_x = start_x_velocity * time_passed

                # Fórmula de posición final en y teniendo en cuenta la gravedad
                change_y = start_y_velocity * time_passed - 0.5 * GRAVITY * pow(time_passed, 2)

                current_ball_pos = (x - change_x, y - change_y)
                ball_path_list.append(current_ball_pos)
            else:
                launch = False
                current_ball_pos = (current_ball_pos[0], INITIAL_BALL_POSITION[1])

        # Manejo de eventos de teclado y ratón
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    launch = False
                    current_ball_pos = INITIAL_BALL_POSITION
            elif event.type == pg.MOUSEMOTION:
                current_mouse_pos = event.pos
            elif event.type == pg.MOUSEBUTTONDOWN:
                start_count_time = pg.time.get_ticks()
            elif event.type == pg.MOUSEBUTTONUP:
                end_time = (pg.time.get_ticks() - start_count_time) / 1000
                start_time, start_x_velocity, start_y_velocity = ball.launch(end_time, current_mouse_pos)
                start_ball_pos = current_ball_pos
                ball_path_list = []
                launch = True

        # Actualización y dibujo de la pelota y la trayectoria
        ball.update(current_ball_pos)
        if current_mouse_pos is not None:
            ball.draw_line(current_mouse_pos)
        ball.draw_ball_path(ball_path_list)

        # Control de FPS y actualización de la pantalla
        clock.tick(FPS)
        pg.display.update()

# Entrada principal del programa
if __name__ == '__main__':
    main()