# pip install pygame
import tkinter as tk
import random

# 블럭깨기 게임을 tkinter로 만듭니다.
# 화면에 공과 막대, 블럭을 표시하고 공이 블럭을 맞히면 블럭이 사라집니다.

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 12
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

class BlockBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("블럭깨기 게임")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#222")
        self.canvas.pack()

        # 플레이어 막대 위치와 이동 속도
        self.paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) / 2
        self.paddle_y = WINDOW_HEIGHT - 40
        self.paddle_speed = 0

        # 공 위치와 속도
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2
        self.ball_dx = 4
        self.ball_dy = -4

        # 점수와 게임 상태
        self.score = 0
        self.game_over = False
        self.game_started = False

        self.bricks = []
        self.create_bricks()
        self.draw_objects()

        # 키 입력 바인딩
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<KeyRelease-Left>', self.stop_paddle)
        self.root.bind('<KeyRelease-Right>', self.stop_paddle)
        self.root.bind('<space>', self.start_game)

        self.update()

    def create_bricks(self):
        self.canvas.delete("brick")
        self.bricks.clear()
        colors = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x1 = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y1 = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                color = colors[row % len(colors)]
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=("brick",))
                self.bricks.append(brick)

    def draw_objects(self):
        self.canvas.delete("paddle")
        self.canvas.delete("ball")
        self.canvas.delete("ui")
        self.canvas.create_rectangle(self.paddle_x, self.paddle_y,
                                     self.paddle_x + PADDLE_WIDTH,
                                     self.paddle_y + PADDLE_HEIGHT,
                                     fill="#ecf0f1", outline="white", tags=("paddle",))
        self.canvas.create_oval(self.ball_x, self.ball_y,
                                self.ball_x + BALL_SIZE,
                                self.ball_y + BALL_SIZE,
                                fill="#ffffff", outline="#bdc3c7", tags=("ball",))

        self.canvas.create_text(110, 20, text=f"점수: {self.score}", fill="white", font=("Arial", 14), tags=("ui",))

        if not self.game_started and not self.game_over:
            self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                    text="스페이스바로 게임 시작",
                                    fill="white", font=("Arial", 18), tags=("ui",))

        if self.game_over:
            self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20,
                                    text="게임 오버",
                                    fill="red", font=("Arial", 32, "bold"), tags=("ui",))
            self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20,
                                    text="스페이스바로 다시 시작",
                                    fill="white", font=("Arial", 16), tags=("ui",))

    def move_left(self, event):
        self.paddle_speed = -8

    def move_right(self, event):
        self.paddle_speed = 8

    def stop_paddle(self, event):
        self.paddle_speed = 0

    def start_game(self, event):
        if self.game_over:
            self.reset_game()
        self.game_started = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) / 2
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2
        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -4
        self.create_bricks()

    def update(self):
        if self.game_started and not self.game_over:
            self.paddle_x += self.paddle_speed
            self.paddle_x = max(0, min(WINDOW_WIDTH - PADDLE_WIDTH, self.paddle_x))

            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy

            self.check_collisions()

        self.draw_objects()
        self.root.after(16, self.update)

    def check_collisions(self):
        if self.ball_x <= 0 or self.ball_x + BALL_SIZE >= WINDOW_WIDTH:
            self.ball_dx *= -1

        if self.ball_y <= 0:
            self.ball_dy *= -1

        if self.ball_y + BALL_SIZE >= WINDOW_HEIGHT:
            self.game_over = True

        paddle_top = self.paddle_y
        paddle_left = self.paddle_x
        paddle_right = self.paddle_x + PADDLE_WIDTH
        ball_bottom = self.ball_y + BALL_SIZE
        ball_center_x = self.ball_x + BALL_SIZE / 2

        if (ball_bottom >= paddle_top and
            self.ball_y <= paddle_top + PADDLE_HEIGHT and
            paddle_left <= ball_center_x <= paddle_right and
            self.ball_dy > 0):
            self.ball_dy *= -1
            self.ball_dx += random.uniform(-0.5, 0.5)

        self.check_brick_collisions()

    def check_brick_collisions(self):
        ball_box = (self.ball_x, self.ball_y, self.ball_x + BALL_SIZE, self.ball_y + BALL_SIZE)
        for brick in self.bricks.copy():
            brick_coords = self.canvas.coords(brick)
            if len(brick_coords) != 4:
                continue
            if self.overlaps(ball_box, brick_coords):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy *= -1
                self.score += 10
                break

        if not self.bricks:
            self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                    text="승리! 스페이스바로 다시 시작",
                                    fill="#2ecc71", font=("Arial", 18), tags=("ui",))
            self.game_over = True

    def overlaps(self, rect1, rect2):
        if len(rect2) != 4:
            return False
        x1, y1, x2, y2 = rect1
        a1, b1, a2, b2 = rect2
        return not (x2 < a1 or x1 > a2 or y2 < b1 or y1 > b2)


if __name__ == '__main__':
    root = tk.Tk()
    game = BlockBreakerGame(root)
    root.mainloop()
