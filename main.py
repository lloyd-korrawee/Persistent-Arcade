import ipstw
import time
import _thread
import neopixel
from machine import Pin
import random

# ============================================================
# INITIAL SETUP
# ============================================================

w = ipstw.IPSTW()
np = neopixel.NeoPixel(Pin(26), 12)

inied = False

DO = const(523)
RE = const(587)
ME = const(659)
FA = const(698)
SO = const(783)
RA = const(880)
TE = const(987)

odeode = [
    ME, 0.5, ME, 0.5, FA, 0.5, SO, 0.5,
    SO, 0.5, FA, 0.5, ME, 0.5, RE, 0.5,
    DO, 0.5, DO, 0.5, RE, 0.5, ME, 0.5,
    ME, 1.0, RE, 0.5, RE, 1.0,

    ME, 0.5, ME, 0.5, FA, 0.5, SO, 0.5,
    SO, 0.5, FA, 0.5, ME, 0.5, RE, 0.5,
    DO, 0.5, DO, 0.5, RE, 0.5, ME, 0.5,
    RE, 1.0, DO, 0.5, DO, 1.0
]

ode = False
speaker = 34

button1 = 5
button2 = 19
button3 = 23

curgame = 2


# ============================================================
# MUSIC / SOUND
# ============================================================

def odetojoy():
    global ode

    while ode:
        for i in range(0, len(odeode), 2):
            if not ode:
                break

            w.sound(odeode[i], odeode[i + 1])

        time.sleep(0.5)


_thread.start_new_thread(odetojoy, ())


def win_sound():
    w.sound(523, 0.12)
    w.sound(659, 0.12)
    w.sound(784, 0.12)
    w.sound(1047, 0.25)


# ============================================================
# MENU
# ============================================================

def showgamename(x):
    w.fill(0)
    w.sound(750, 0.1)

    np.fill((3, 3, 3))
    np.write()

    if x == 1:
        w.text("Reflex Test", 15, 10, 1)
        w.text("1 Player", 15, 20, 1)

    elif x == 2:
        w.text("Light Race", 15, 10, 1)
        w.text("2 Player", 15, 20, 1)

    elif x == 3:
        w.text("Hail Mary FAKE", 15, 10, 1)
        w.text("1 Player", 15, 20, 1)

    elif x == 4:
        w.text("Pong", 15, 10, 1)
        w.text("2 Player", 15, 20, 1)

    elif x == 5:
        w.text("Basketball", 15, 10, 1)
        w.text("1 Player", 15, 20, 1)

    w.text("<-", 15, 40, 1)
    w.text("->", 108, 40, 1)
    w.text("A", 15, 50, 1)
    w.text("B", 113, 50, 1)

    w.show()

    time.sleep(0.01)

    np.fill((0, 0, 0))
    np.write()


def tomenu():
    w.fill(0)
    w.text("Going back", 25, 20, 1)
    w.show()
    time.sleep(2)


def endgame(game_id):
    w.fill(0)
    w.text("Back in 3", 25, 20, 1)
    w.text("Start: Replay", 15, 40, 1)
    w.show()

    w.sound(500, 0.15)

    start = time.ticks_ms()
    last_sec = 3

    while time.ticks_diff(time.ticks_ms(), start) <= 3000:
        elapsed = time.ticks_diff(time.ticks_ms(), start)

        if elapsed >= 2000 and last_sec == 2:
            last_sec = 1

            w.fill(0)
            w.text("Back in 1", 25, 20, 1)
            w.text("Start: Replay", 15, 40, 1)
            w.show()

            w.sound(500, 0.15)

        elif elapsed >= 1000 and last_sec == 3:
            last_sec = 2

            w.fill(0)
            w.text("Back in 2", 25, 20, 1)
            w.text("Start: Replay", 15, 40, 1)
            w.show()

            w.sound(500, 0.15)

        if w.input(button3) == 0:
            while w.input(button3) == 0:
                time.sleep(0.01)

            play(game_id)
            return

        time.sleep(0.01)

    w.sound(300, 0.3)
    tomenu()


# ============================================================
# SPACE SHOOTER
# ============================================================

def show_hp(hp):
    if hp >= 7:
        np.fill((0, 30, 0))

    elif hp >= 4:
        np.fill((30, 30, 0))

    else:
        np.fill((30, 0, 0))

    np.write()


def select_mode():
    time.sleep(0.2)

    mode = 2

    while True:
        w.fill(0)

        if mode == 1:
            w.text("VERY EASY", 25, 15, 1)
            w.text("2 ENEMIES", 30, 30, 1)

        elif mode == 2:
            w.text("EASY", 45, 15, 1)
            w.text("3 ENEMIES", 30, 30, 1)

        elif mode == 3:
            w.text("MID", 48, 15, 1)
            w.text("5 ENEMIES", 30, 30, 1)

        elif mode == 4:
            w.text("HARD", 45, 15, 1)
            w.text("5 ENEMIES", 30, 30, 1)

        elif mode == 5:
            w.text("YOUR MUM", 25, 15, 1)
            w.text("7 ENEMIES", 30, 30, 1)

        w.text("A/B SELECT", 25, 45, 1)
        w.show()

        # A = ย้อน
        if w.input(button1) == 0:
            mode -= 1

            if mode == 0:
                mode = 5

            while w.input(button1) == 0:
                time.sleep(0.01)

        # B = ถัดไป
        if w.input(button2) == 0:
            mode += 1

            if mode == 6:
                mode = 1

            while w.input(button2) == 0:
                time.sleep(0.01)

        # Start = เลือก
        if w.input(button3) == 0:
            while w.input(button3) == 0:
                time.sleep(0.01)

            return mode

        time.sleep(0.01)


def play_space():
    mode = select_mode()

    if mode == 1:
        enemy_count = 2
        enemy_speed = 1
        player_speed = 6

    elif mode == 2:
        enemy_count = 3
        enemy_speed = 1
        player_speed = 5

    elif mode == 3:
        enemy_count = 5
        enemy_speed = 1
        player_speed = 4

    elif mode == 4:
        enemy_count = 5
        enemy_speed = 2
        player_speed = 3

    else:
        enemy_count = 7
        enemy_speed = 3
        player_speed = 3

    player_x = 64
    player_y = 55
    score = 0
    health = 10

    bullets = []
    enemies = []

    for _ in range(enemy_count):
        enemies.append([
            random.randint(5, 122),
            random.randint(-40, -5),
            random.randint(3, 5)
        ])

    last_fire_time = 0

    # HOW TO PLAY
    w.fill(0)
    w.text("SPACE SHOOTER", 20, 5, 1)
    w.text("A : LEFT", 25, 20, 1)
    w.text("B : RIGHT", 25, 30, 1)
    w.text("START : FIRE", 25, 40, 1)
    w.text("Press START", 25, 52, 1)
    w.show()

    time.sleep(0.2)

    while w.input(button3) == 1:
        time.sleep(0.01)

    while w.input(button3) == 0:
        time.sleep(0.01)

    # COUNTDOWN
    for i in range(3, 0, -1):
        w.fill(0)
        w.text(str(i), 60, 25, 1)
        w.show()

        w.sound(500, 0.15)
        time.sleep(1)

    w.fill(0)
    w.text("GO!", 50, 25, 1)
    w.show()

    w.sound(1000, 0.2)
    time.sleep(0.5)

    show_hp(health)

    # GAME LOOP
    while health > 0:
        if w.input(button1) == 0 and player_x > 5:
            player_x -= player_speed

        if w.input(button2) == 0 and player_x < 123:
            player_x += player_speed

        if mode == 1:
            bullet_delay = 100
            shot_allow = 10

        else:
            bullet_delay = 200
            shot_allow = 5

        # ยิง
        if w.input(button3) == 0:
            now = time.ticks_ms()

            if time.ticks_diff(now, last_fire_time) >= bullet_delay:
                if len(bullets) < shot_allow:
                    bullets.append([player_x, player_y])
                    last_fire_time = now
                    w.sound(1200, 0.03)

        # UPDATE BULLETS
        i = 0

        while i < len(bullets):
            bullets[i][1] -= 5

            if bullets[i][1] < 0:
                bullets.pop(i)

            else:
                i += 1

        # UPDATE ENEMIES
        for enemy in enemies:
            enemy[1] += enemy_speed

            if enemy[1] > 64:
                health -= 1
                show_hp(health)

                enemy[0] = random.randint(5, 122)
                enemy[1] = random.randint(-40, -5)
                enemy[2] = random.randint(3, 5)

            # ชนยาน
            if (
                enemy[1] + enemy[2] >= player_y
                and abs(enemy[0] - player_x) <= 5
            ):
                health = 0

        # BULLET COLLISION
        i = 0

        while i < len(bullets):
            bx = bullets[i][0]
            by = bullets[i][1]
            hit = False

            for enemy in enemies:
                ex = enemy[0]
                ey = enemy[1]
                size = enemy[2]

                if (
                    ex - size <= bx <= ex + size
                    and ey - size <= by <= ey + size
                ):
                    score += 5
                    hit = True

                    w.sound(800, 0.02)

                    enemy[0] = random.randint(5, 122)
                    enemy[1] = random.randint(-40, -5)
                    enemy[2] = random.randint(3, 5)

                    if score % 25 == 0 and enemy_speed < 5:
                        enemy_speed += 1

                    break

            if hit:
                bullets.pop(i)

            else:
                i += 1

        # DRAW
        w.fill(0)

        # Player
        w.pixel(player_x, player_y, 1)

        w.pixel(player_x - 1, player_y + 1, 1)
        w.pixel(player_x, player_y + 1, 1)
        w.pixel(player_x + 1, player_y + 1, 1)

        w.pixel(player_x - 2, player_y + 2, 1)
        w.pixel(player_x - 1, player_y + 2, 1)
        w.pixel(player_x, player_y + 2, 1)
        w.pixel(player_x + 1, player_y + 2, 1)
        w.pixel(player_x + 2, player_y + 2, 1)

        # Bullets
        for bullet in bullets:
            bx = bullet[0]
            by = bullet[1]

            w.pixel(bx, by, 1)
            w.pixel(bx, by + 1, 1)
            w.pixel(bx, by + 2, 1)

        # Enemies
        for enemy in enemies:
            ex = enemy[0]
            ey = enemy[1]

            w.pixel(ex, ey, 1)
            w.pixel(ex - 1, ey, 1)
            w.pixel(ex + 1, ey, 1)
            w.pixel(ex, ey - 1, 1)
            w.pixel(ex, ey + 1, 1)

            w.pixel(ex - 2, ey, 1)
            w.pixel(ex + 2, ey, 1)
            w.pixel(ex, ey - 2, 1)
            w.pixel(ex, ey + 2, 1)

        w.text("S:" + str(score), 0, 0, 1)
        w.text("HP:" + str(health), 88, 0, 1)

        w.show()
        time.sleep(0.03)

    # GAME OVER
    np.fill((0, 0, 0))
    np.write()

    w.fill(0)
    w.text("GAME OVER", 30, 20, 1)
    w.text("Score: " + str(score), 25, 35, 1)
    w.text("Press Start", 25, 50, 1)
    w.show()

    w.sound(200, 0.3)

    while w.input(button3) == 0:
        time.sleep(0.01)

    while w.input(button3) == 1:
        time.sleep(0.01)

    endgame(3)


# ============================================================
# BASKETBALL
# ============================================================

def play_basket():
    score = 0
    shot = 0
    angle = 45

    hoop_x = 105
    hoop_y = 19

    start_x = 20
    start_y = 55

    old_a = 1
    old_b = 1

    power = random.randint(1, 4)

    # HOW TO PLAY
    w.fill(0)
    w.text("BASKET", 35, 5, 1)
    w.text("A : LEFT", 10, 20, 1)
    w.text("B : RIGHT", 65, 20, 1)
    w.text("START : SHOOT", 20, 35, 1)
    w.text("Press START", 25, 52, 1)
    w.show()

    while w.input(button3) == 1:
        time.sleep(0.01)

    while w.input(button3) == 0:
        time.sleep(0.01)

    # COUNTDOWN
    for i in range(3, 0, -1):
        w.fill(0)
        w.text(str(i), 60, 25, 1)
        w.show()

        w.sound(500, 0.15)
        time.sleep(1)

    # GAME
    while shot < 10:
        a = w.input(button1)
        b = w.input(button2)
        start = w.input(button3)

        # A = เล็งซ้าย
        if old_a == 1 and a == 0:
            angle -= 3

            if angle < 30:
                angle = 30

            w.sound(400, 0.03)

        # B = เล็งขวา
        if old_b == 1 and b == 0:
            angle += 3

            if angle > 75:
                angle = 75

            w.sound(500, 0.03)

        old_a = a
        old_b = b

        # SHOOT
        if start == 0:
            while w.input(button3) == 0:
                time.sleep(0.01)

            shot += 1

            vx = power * 10

            ball_x = start_x * 10
            ball_y = start_y * 10

            vy = -(angle * 2)
            gravity = 2

            scored = False

            # BALL PHYSICS
            while True:
                ball_x += vx
                ball_y += vy
                vy += gravity

                draw_x = ball_x // 10
                draw_y = ball_y // 10

                # ตรวจเข้าห่วง
                if (
                    hoop_x - 2 <= draw_x <= hoop_x + 2
                    and hoop_y - 2 <= draw_y <= hoop_y + 2
                    and vy > 0
                ):
                    scored = True
                    break

                if draw_x > 127:
                    break

                if draw_y >= 56:
                    break

                # DRAW
                w.fill(0)

                w.text("S:" + str(score), 0, 0, 1)
                w.text("POWER:" + str(power), 0, 10, 1)
                w.text(str(shot) + "/10", 100, 0, 1)

                # พื้น
                for x in range(0, 128, 4):
                    w.pixel(x, 57, 1)

                # เสา
                for y in range(18, 58):
                    w.pixel(110, y, 1)

                # แป้น
                for x in range(102, 111):
                    w.pixel(x, 15, 1)

                # ห่วง
                for x in range(102, 110):
                    w.pixel(x, 19, 1)

                # ลูก
                w.pixel(draw_x, draw_y, 1)
                w.pixel(draw_x + 1, draw_y, 1)
                w.pixel(draw_x, draw_y + 1, 1)
                w.pixel(draw_x + 1, draw_y + 1, 1)

                w.show()
                time.sleep(0.03)

            # RESULT
            if scored:
                score += 1

                w.fill(0)
                w.text("SWISH!", 40, 20, 1)
                w.text("Score:" + str(score), 30, 35, 1)
                w.show()

                w.sound(900, 0.08)
                w.sound(1100, 0.15)

                time.sleep(0.7)

            else:
                w.fill(0)
                w.text("MISS!", 45, 25, 1)
                w.show()

                w.sound(200, 0.2)
                time.sleep(0.5)

            if shot < 10:
                power = random.randint(1, 4)

        # AIM SCREEN
        w.fill(0)

        w.text("S:" + str(score), 0, 0, 1)
        w.text("POWER:" + str(power), 0, 10, 1)
        w.text(str(shot) + "/10", 100, 0, 1)

        # พื้น
        for x in range(0, 128, 4):
            w.pixel(x, 57, 1)

        # เสา
        for y in range(18, 58):
            w.pixel(110, y, 1)

        # แป้น
        for x in range(102, 111):
            w.pixel(x, 15, 1)

        # ห่วง
        for x in range(102, 110):
            w.pixel(x, 19, 1)

        # ลูก
        w.pixel(start_x, start_y, 1)
        w.pixel(start_x + 1, start_y, 1)
        w.pixel(start_x, start_y + 1, 1)
        w.pixel(start_x + 1, start_y + 1, 1)

        # เส้นเล็ง
        aim_x = start_x + 15
        aim_y = start_y - (angle // 3)

        w.line(
            start_x,
            start_y,
            aim_x,
            aim_y,
            1
        )

        w.text("ANGLE:" + str(angle), 30, 45, 1)
        w.show()

        time.sleep(0.03)

    # GAME OVER
    w.fill(0)

    w.text("GAME OVER", 30, 15, 1)
    w.text("SCORE:" + str(score), 25, 30, 1)

    if score >= 8:
        w.text("AMAZING!", 35, 45, 1)

    elif score >= 5:
        w.text("GOOD!", 45, 45, 1)

    else:
        w.text("KEEP TRYING", 25, 45, 1)

    w.show()

    if score >= 5:
        win_sound()

    else:
        w.sound(200, 0.3)

    time.sleep(1)

    endgame(5)


# ============================================================
# PONG
# ============================================================

def play_pong():
    ball_x = 64
    ball_y = 32

    ball_dx = 2
    ball_dy = 1

    left_score = 0
    right_score = 0

    left_paddle = 0
    right_paddle = 0

    last_left = 0
    last_right = 0

    paddle_time = 150
    cooldown = 300

    old_a = 1
    old_b = 1

    # HOW TO PLAY
    w.fill(0)
    w.text("PONG", 50, 5, 1)
    w.text("A : LEFT", 10, 20, 1)
    w.text("B : RIGHT", 65, 20, 1)
    w.text("HIT THE BALL!", 25, 35, 1)
    w.text("START", 50, 52, 1)
    w.show()

    while w.input(button3) == 1:
        time.sleep(0.01)

    while w.input(button3) == 0:
        time.sleep(0.01)

    # COUNTDOWN
    for i in range(3, 0, -1):
        w.fill(0)
        w.text(str(i), 60, 25, 1)
        w.show()

        w.sound(500, 0.15)
        time.sleep(1)

    w.fill(0)
    w.text("GO!", 50, 25, 1)
    w.show()

    w.sound(1000, 0.2)
    time.sleep(0.5)

    # GAME LOOP
    while left_score < 5 and right_score < 5:
        now = time.ticks_ms()

        a = w.input(button1)
        b = w.input(button2)

        hit_a = old_a == 1 and a == 0
        hit_b = old_b == 1 and b == 0

        old_a = a
        old_b = b

        # LEFT
        if hit_a:
            if time.ticks_diff(now, last_left) >= cooldown:
                left_paddle = now
                last_left = now

        # RIGHT
        if hit_b:
            if time.ticks_diff(now, last_right) >= cooldown:
                right_paddle = now
                last_right = now

        # MOVE BALL
        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 2:
            ball_y = 2
            ball_dy *= -1

        if ball_y >= 61:
            ball_y = 61
            ball_dy *= -1

        # LEFT PADDLE
        if ball_x <= 6 and ball_dx < 0:
            if time.ticks_diff(now, left_paddle) <= paddle_time:
                ball_x = 7

                if abs(ball_dx) < 15:
                    ball_dx = abs(ball_dx) + 1

                else:
                    ball_dx = 15

                if abs(ball_dy) < 4:
                    if ball_dy > 0:
                        ball_dy += 1

                    else:
                        ball_dy -= 1

                w.sound(700, 0.04)

            elif ball_x < 0:
                right_score += 1

                w.sound(200, 0.2)

                ball_x = 64
                ball_y = random.randint(10, 54)

                ball_dx = -2
                ball_dy = random.choice([-1, 1])

                left_paddle = 0
                right_paddle = 0

                time.sleep(0.3)

        # RIGHT PADDLE
        if ball_x >= 121 and ball_dx > 0:
            if time.ticks_diff(now, right_paddle) <= paddle_time:
                ball_x = 120

                if abs(ball_dx) < 7:
                    ball_dx = -(abs(ball_dx) + 1)

                else:
                    ball_dx = -7

                if abs(ball_dy) < 4:
                    if ball_dy > 0:
                        ball_dy += 1

                    else:
                        ball_dy -= 1

                w.sound(700, 0.04)

            elif ball_x > 127:
                left_score += 1

                w.sound(200, 0.2)

                ball_x = 64
                ball_y = random.randint(10, 54)

                ball_dx = 2
                ball_dy = random.choice([-1, 1])

                left_paddle = 0
                right_paddle = 0

                time.sleep(0.3)

        # DRAW
        w.fill(0)

        w.text(str(left_score), 25, 0, 1)
        w.text(str(right_score), 100, 0, 1)

        # เส้นกลาง
        for y in range(10, 64, 6):
            w.pixel(64, y, 1)

        # LEFT PADDLE
        if time.ticks_diff(now, left_paddle) <= paddle_time:
            for y in range(0, 64):
                w.pixel(2, y, 1)
                w.pixel(3, y, 1)
                w.pixel(4, y, 1)
                w.pixel(5, y, 1)

        else:
            w.pixel(2, 32, 1)
            w.pixel(3, 32, 1)

        # RIGHT PADDLE
        if time.ticks_diff(now, right_paddle) <= paddle_time:
            for y in range(0, 64):
                w.pixel(122, y, 1)
                w.pixel(123, y, 1)
                w.pixel(124, y, 1)
                w.pixel(125, y, 1)

        else:
            w.pixel(124, 32, 1)
            w.pixel(125, 32, 1)

        # BALL
        w.pixel(ball_x, ball_y, 1)
        w.pixel(ball_x + 1, ball_y, 1)
        w.pixel(ball_x, ball_y + 1, 1)
        w.pixel(ball_x + 1, ball_y + 1, 1)

        w.show()
        time.sleep(0.03)

    # WIN
    w.fill(0)

    if left_score >= 5:
        w.text("LEFT WIN!", 35, 20, 1)

    else:
        w.text("RIGHT WIN!", 30, 20, 1)

    w.text(
        str(left_score) + " - " + str(right_score),
        45,
        35,
        1
    )

    w.show()

    win_sound()

    time.sleep(1)

    endgame(4)


# ============================================================
# REFLEX TEST
# ============================================================

def play_reflect():
    np.fill((0, 0, 0))
    np.write()

    w.fill(0)
    w.show()

    for i in range(3, 0, -1):
        w.fill(0)
        w.text(str(i), 60, 25, 1)
        w.show()

        w.sound(500, 0.15)
        time.sleep(1)

    w.fill(0)
    w.text("Press When", 10, 20, 1)
    w.text("Lights Out", 10, 30, 1)

    np.fill((30, 30, 30))
    np.write()

    w.show()
    w.sound(1000, 0.2)

    rnd = random.randint(1, 10)

    # รอช่วงสุ่มก่อนดับไฟ
    wait_start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), wait_start) < rnd * 1000:
        if w.input(button1) == 0 or w.input(button2) == 0:
            w.fill(0)
            np.fill((0, 0, 0))
            w.text("FALSE START", 15, 20, 1)
            w.text("You Lose!", 30, 40, 1)
            w.show()
            np.write()

            w.sound(200, 0.5)
            time.sleep(1.5)

            endgame(1)
            return

        time.sleep(0.01)

    np.fill((0, 0, 0))
    np.write()

    start = time.ticks_ms()

    while w.input(button1) == 1 and w.input(button2) == 1:
        time.sleep(0.001)

    end = time.ticks_ms()

    reaction = time.ticks_diff(end, start)

    score = 100 - reaction // 10

    if score < 0:
        score = 0

    w.fill(0)
    w.text("Time: " + str(reaction) + " ms", 0, 20, 1)
    w.text("Score: " + str(score), 0, 35, 1)
    w.show()

    time.sleep(3)

    endgame(1)


# ============================================================
# LIGHT RACE
# ============================================================

def play_lightrace():
    w.fill(0)
    w.text("Starting", 25, 20, 1)
    w.show()

    time.sleep(0.2)

    for i in range(3, 0, -1):
        w.fill(0)
        w.text(str(i), 60, 25, 1)
        w.show()

        w.sound(500, 0.15)
        time.sleep(1)

    w.fill(0)
    w.text("GO!", 50, 25, 1)
    w.show()

    w.sound(1000, 0.2)

    cur_b = 1
    cur_r = 11

    np.fill((0, 0, 0))
    np.write()

    old_r = 1
    old_b = 1

    while True:
        r = w.input(button1)
        b = w.input(button2)

        # Red
        if old_r == 1 and r == 0:
            if cur_r >= 0:
                np[cur_r] = (255, 0, 0)
                cur_r -= 1
                np.write()

        # Blue
        if old_b == 1 and b == 0:
            if cur_b <= 11:
                np[cur_b] = (0, 0, 255)
                cur_b += 1
                np.write()

        old_r = r
        old_b = b

        # Blue win
        if cur_b >= 7:
            win_sound()

            w.fill(0)
            w.text("Blue Win", 30, 20)
            w.show()

            np.fill((0, 0, 0))
            np.write()

            for i in range(12):
                np[i] = (0, 0, 255)
                np.write()
                time.sleep(0.05)

            time.sleep(0.5)

            for _ in range(3):
                np.fill((0, 0, 0))
                np.write()
                time.sleep(0.25)

                np.fill((0, 0, 255))
                np.write()
                time.sleep(0.25)

            break

        # Red win
        elif cur_r <= 5:
            win_sound()

            w.fill(0)
            w.text("Red Win", 30, 20)
            w.show()

            np.fill((0, 0, 0))
            np.write()

            for i in range(11, -1, -1):
                np[i] = (255, 0, 0)
                np.write()
                time.sleep(0.05)

            time.sleep(0.5)

            for _ in range(3):
                np.fill((0, 0, 0))
                np.write()
                time.sleep(0.25)

                np.fill((255, 0, 0))
                np.write()
                time.sleep(0.25)

            break

        time.sleep(0.005)

    np.fill((0, 0, 0))
    np.write()

    endgame(2)


# ============================================================
# GAME DISPATCHER
# ============================================================

def play(x):
    if x == 1:
        play_reflect()

    elif x == 2:
        play_lightrace()

    elif x == 3:
        play_space()

    elif x == 4:
        play_pong()

    elif x == 5:
        play_basket()


# ============================================================
# GAME SELECTOR
# ============================================================

def selgame():
    global curgame

    while True:
        showgamename(curgame)

        while w.input(button3) == 1:
            if w.input(button1) == 0:
                curgame -= 1

                if curgame == 0:
                    curgame = 5

                while w.input(button1) == 0:
                    time.sleep(0.01)

                showgamename(curgame)

            elif w.input(button2) == 0:
                curgame += 1

                if curgame == 6:
                    curgame = 1

                while w.input(button2) == 0:
                    time.sleep(0.01)

                showgamename(curgame)

            time.sleep(0.01)

        # กด Start
        while w.input(button3) == 0:
            time.sleep(0.01)

        play(curgame)


# ============================================================
# INITIALIZATION
# ============================================================

def ini():
    global inied
    global ode

    if not inied:
        inied = True
        ode = True

        w.text("Persistent", 30, 1, 1)
        w.text("Arcade", 30, 10, 1)
        w.show()

        while w.input(button3) == 1:
            w.text("Hold Start", 25, 32, 1)
            w.show()

            time.sleep(0.3)

            w.text("Hold Start", 25, 32, 0)
            w.show()

            time.sleep(0.3)

        ode = False

        w.fill(0)
        w.show()

        while w.input(button3) == 0:
            time.sleep(0.02)

        selgame()


# ============================================================
# MAIN
# ============================================================

np.fill((0, 0, 0))
np.write()

ini()
