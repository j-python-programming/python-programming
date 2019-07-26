# Python によるプログラミング：第 15 章
#　サーカスゲーム
# --------------------------
# プログラム名: 15-circus.py
# 本文 第15章のサンプルプログラムです。

import pygame
import sys

WHITE, RED, GREEN = ((255, 255, 255), (255, 0, 0),(0, 255, 0))
BLUE, YELLOW, BLACK = ((0, 0, 255), (255, 255, 0), (0, 0, 0))
FPS = 40        # 描画更新速度(flame per second)

WIDTH = 800     # 画面全体幅
HEIGHT = 700    # 画面全体高さ
NORTH = 80      # 盤面トップ
WEST = 0        # 盤面左端
EAST = 800      # 盤面右端
SOUTH = 680     # 盤面ボトム
X_CENTER = (WEST + EAST)/2  # 画面Xの中心

BALLOON_TOP = 18 + NORTH  # バルーンのトップの高さ => 98
BALLOON_GAP = 35  # バルーンの列の間隔
BALLOON_GAP_Y = 20
BALLOON_DIAM = 45 # バルーンの直径
BALLOON_VX = 2    # バルーンの移動する速度
BALLOON_JUMP = WIDTH + BALLOON_DIAM + BALLOON_GAP
BALLOON_LAST_X = BALLOON_JUMP + 1          # 初期設定
BALLOON_STEP = BALLOON_DIAM + BALLOON_GAP  # バルーンのY加算

YELLOW_IMAGE1 = 'yellow1.png'
YELLOW_IMAGE2 = 'yellow2.png'
GREEN_IMAGE1 = 'green1.png'
GREEN_IMAGE2 = 'green2.png'
BLUE_IMAGE1 = 'blue1.png'
BLUE_IMAGE2 = 'blue2.png'

YELLOW_SCORE = 10
GREEN_SCORE = 20
BLUE_SCORE = 30
YELLOW_BONUS = 100
GREEN_BONUS = 200
BLUE_BONUS = 300

SEESAW_H = 20    # シーソーの高さ
SEESAW_W = 140   # シーソーの横幅
SEESAW_X = (EAST-SEESAW_W)/2 + WEST
SEESAW_Y = SOUTH - SEESAW_H - 15
SEESAW_VX = 8    # シーソーの移動スピード
SEESAW1_IMAGE = "seesaw1.png"
SEESAW2_IMAGE = "seesaw2.png"

FONT_SIZE = 24

SCORE_X = 0      # スコア表示位置
SCORE_Y = 0

MESSAGE_TOP = BALLOON_TOP + 3*BALLOON_DIAM + 2*BALLOON_GAP_Y + 50
MESSAGE_GAP = 40   # タイトルメッセージの表示位置

PERFORMER_H = 40 # パフォーマの伸長
PERFORMER_W = 20 # パフォーマの幅
PERFORMER1_IMAGE = "performer1.png"
PERFORMER2_IMAGE = "performer2.png"

# 落ちる人の初期位置
PERFORMER_X = (EAST-PERFORMER_W)/2 + WEST
PERFORMER_Y = BALLOON_TOP + 3*BALLOON_DIAM + 2*BALLOON_GAP_Y + 50
JUMP_CENTER = (SEESAW_W-PERFORMER_W)/2  # ジャンプ速度の計算に使用
STATE_JUMPING = 1
STATE_STANDING = 2
GRAVITY = 0.3
MAX_VX = SEESAW_VX/1.2
MAX_VY = SEESAW_H - 2

# ジャンプボード
JUMP_BOARD_HIGH = MESSAGE_TOP + 100
JUMP_BOARD_LOW = SEESAW_Y - 100
JUMP_BOARD_WIDTH = 50
JUMP_BOARD_HEIGHT = 5
LEFT_BOARD = 1
RIGHT_BOARD = 2

NUM_JUMPER = 5

# 状態遷移
STAGE_START = 1
STAGE_INTRO = 2
STAGE_RUN = 3
STAGE_DOWN = 4
STAGE_NEXT = 5
STAGE_OVER = 6
STAGE_QUIT = 7

# 風船クラス
class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, d, vx, score, image1, image2):
        pygame.sprite.Sprite.__init__(self)
        self.vx = vx     # 縦方向には動かない
        self.image = self.image1 = image1
        self.image2 = image2
        self.rect = pygame.Rect(x, y, d, d)
        self.score = score
        self.balloon_tilt = 0

    def update(self):
        # 描画位置を移動させる
        self.rect.move_ip(self.vx, 0)
        if self.rect.x < - BALLOON_DIAM:   # 左に消えるまで表示
            self.rect.move_ip(BALLOON_JUMP, 0)
        if self.rect.x > EAST:             # 右に消えるまで表示
            self.rect.move_ip(- BALLOON_JUMP, 0)
        if self.balloon_tilt < FPS/2:  # 0.5 秒ごとに傾く
            self.image = self.image1
        else:
            self.image = self.image2

    def bump(self, performer):   # パフォーマとの衝突
        performer.vy = - performer.vy
        return self.score

    def set_balloon_tilt(self, balloon_tilt):
        self.balloon_tilt = balloon_tilt

# シーソークラス
class Seesaw(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, speed, image1, image2):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed     # 縦方向には動かない
        self.image1 = pygame.image.load(image1)  # 左下がりの絵
        self.image1 = self.image1.convert()
        self.image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.image2 = pygame.image.load(image2)  # 右下がりの絵
        self.image2 = self.image2.convert()
        self.image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.image = self.image1
        self.rect = pygame.Rect(x, y, l, h)
        self.init_x = x
        self.vx = 0            # 初期状態は静止

    def back_origin(self):  # 1 ダウンの後、初期位置に戻す
        xmove = self.init_x - self.rect.x
        self.rect.move_ip(xmove, 0)
        self.image = self.image1
        self.vx = 0

    def update(self):
        if self.rect.x + self.vx < WEST:  # 左端
            self.rect.move_ip(-self.rect.x, 0)
            self.vx = 0
            self.rider.move(0)  # 立ってる人も停止させる
        elif self.rect.x + self.rect.w + self.vx > EAST: # 右端
            self.rect.move_ip(EAST - self.rect.w - self.rect.x, 0)
            self.vx = 0
            self.rider.move(0)
        else:
            self.rect.move_ip(self.vx, 0)

    def move_left(self):
        self.vx = -self.speed
        self.rider.move(self.vx)  # 立ってる人も同じスピードで移動させる

    def move_right(self):
        self.vx = self.speed
        self.rider.move(self.vx)

    def stop(self):
        self.vx = 0
        self.rider.move(0)

    def ride(self, performer):
        self.rider = performer   # こちらの人が着地した
        self.rider.move(self.vx)  # シーソーと同速度で水平異動
        if self.image == self.image2:  # シーソーの絵を切り替え
            self.image = self.image1   # 参照だけ切り替え
        else:
            self.image = self.image2

# 左右の壁ぎわの、ジャンプ台
class JumpBoard(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, w, h)
        self.id = id
        if x < X_CENTER:
            self.side = LEFT_BOARD   # 左と右の区別
        else:
            self.side = RIGHT_BOARD

    def bump(self, performer):
        if performer.vy < 0:    # 下からの衝突では、透過させる
            return
        performer.vy = - performer.vy
        # 少し浮かせる
        performer.rect.y = self.rect.y - performer.rect.h - 2
        if -1 <= performer.vx <= 1: # ジャンプ台で止まってしまわないように
            if self.side == LEFT_BOARD:
                performer.vx = -2
            else:
                performer.vx = 2

class Performer(pygame.sprite.Sprite):
    def __init__(self, id, x, y, w, h, status, image):
        pygame.sprite.Sprite.__init__(self)
        self.status = status    # 状態
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.image.set_colorkey((255, 255, 255))  # 白を透過色に指定
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = self.vy = 0
        self.init_x, self.init_y = (x, y)
        self.init_status = status
        self.id = id
        self.down = False
        self.inactive_y = 0

    def back_origin(self, seesaw):
        xmove = self.init_x - self.rect.x
        ymove = self.init_y - self.rect.y
        self.rect.move_ip(xmove, ymove)  # 初期位置に戻す
        self.vx = self.vy = 0
        if self.id == 1:    # Jumperの時
            self.vx = 2
        self.status = self.init_status
        self.down = False
        if self.id == 2:
            seesaw.ride(self)

    def update(self):
        if self.status == STATE_JUMPING:
            self.vy += GRAVITY
            self.vy = min(self.vy, MAX_VY)
            self.rect.move_ip(self.vx, self.vy)
        else:
            self.vy = 0
            self.rect.move_ip(self.vx, 0)
        if self.status == STATE_JUMPING:
            if self.rect.y + self.rect.h > SOUTH:
                self.vy = 0
                self.down = True
            if self.rect.x <= WEST:  # 壁で跳ね返る
                if self.vx < 0:
                    self.vx = -self.vx
                elif self.vx == 0:
                    self.vx = 1
            if self.rect.x + self.rect.w >= EAST:
                if self.vx > 0:
                    self.vx = -self.vx
                elif self.vx == 0:
                    self.vx = -1
            if self.rect.y <= NORTH:
                self.vy = -self.vy

    def move(self, vx):
        self.vx = vx

    # 着地点に応じて、加速する
    def check(self, seesaw):
        x_diff = self.rect.x - seesaw.rect.x
        # id:1は左に着地、id:2は右に着地しないと、アウト
        # はみ出したらアウト
        if self.id == 1:
            if (x_diff+self.rect.w < 0 \
                or x_diff + self.rect.w/2 > JUMP_CENTER):
                return (0, 0)
            x_offset = -1
        else:
            if (x_diff + self.rect.w/2 < JUMP_CENTER \
                or x_diff > seesaw.rect.w):
                return (0, 0)
            else:
                x_diff = seesaw.rect.w - x_diff - self.rect.w
            x_offset = 1
        # ここで、0 <= x_diff <= JUMP_CENTER となる。
        # 0の時2倍、JUMP_CENTERの時 0.5倍に線形に変換する。
        rate = 2 - 1.5 * x_diff / JUMP_CENTER
        x_offset *= rate
        return (x_offset, rate)

    def landed(self, seesaw):
        vy = self.vy
        vx = self.vx
        self.vy = 0
        self.status = STATE_STANDING
        # 現在座標から引き上げる分だけ移動
        ymove = seesaw.rect.y + seesaw.rect.h - self.rect.h - 1 - self.rect.y
        if self.id == 1:
            xmove = seesaw.rect.x - self.rect.x
        else:
            xmove = (seesaw.rect.x + seesaw.rect.w - self.rect.w) - self.rect.x
        self.rect.move_ip(xmove, ymove)
        seesaw.ride(self)  # vxの値を一致させる
        return (vx, vy)

    def jump(self, vx, vy, seesaw):
        self.vx = vx
        self.vy = vy
        self.status = STATE_JUMPING
        ymove = SEESAW_Y - PERFORMER_H - 1 \
                - self.rect.y - seesaw.rect.h
        self.rect.move_ip(self.vx, ymove)
        self.inactive_y = self.rect.y - seesaw.rect.y + self.rect.h

class Board():
    def __init__(self, width, height, num_jumper):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width, self.height = (width, height)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsansms', FONT_SIZE)
        self.score = 0
        self.balloon_tilt = 0
        self.num_jumper_org = self.num_jumper = num_jumper

    def setup_yellows(self):
        image1 = pygame.image.load(YELLOW_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(YELLOW_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP + 2*(BALLOON_DIAM + BALLOON_GAP_Y)
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.yellows.add(Balloon(x, y, BALLOON_DIAM, -BALLOON_VX,
                                     YELLOW_SCORE, image1, image2))

    def setup_greens(self):
        image1 = pygame.image.load(GREEN_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(GREEN_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP + BALLOON_DIAM + BALLOON_GAP_Y
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.greens.add(Balloon(x, y, BALLOON_DIAM, BALLOON_VX,
                                    GREEN_SCORE, image1, image2))

    def setup_blues(self):
        image1 = pygame.image.load(BLUE_IMAGE1).convert()
        image1.set_colorkey((255, 255, 255))  # 白を透過色に指定
        image2 = pygame.image.load(BLUE_IMAGE2).convert()
        image2.set_colorkey((255, 255, 255))  # 白を透過色に指定
        y = BALLOON_TOP
        for x in range(0, BALLOON_LAST_X, BALLOON_STEP):
            self.blues.add(Balloon(x, y, BALLOON_DIAM, -BALLOON_VX,
                                   BLUE_SCORE, image1, image2))

    def setup_jumpboards(self):
        y = JUMP_BOARD_HIGH
        self.jumpboards.add(JumpBoard(0, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        self.jumpboards.add(JumpBoard(EAST-JUMP_BOARD_WIDTH, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        y = JUMP_BOARD_LOW
        self.jumpboards.add(JumpBoard(0, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))
        self.jumpboards.add(JumpBoard(EAST-JUMP_BOARD_WIDTH, y, JUMP_BOARD_WIDTH, JUMP_BOARD_HEIGHT, WHITE))

    def setup(self):
        self.stage = STAGE_START
        # Groupを準備する
        self.yellows = pygame.sprite.Group()    # 一番下の列
        self.greens = pygame.sprite.Group()     # 真ん中の列
        self.blues = pygame.sprite.Group()      # 一番上の列
        seesaws = pygame.sprite.Group()    # シーソー
        self.performers = pygame.sprite.Group() # 二人のパフォーマー
        self.jumpboards = pygame.sprite.Group() # 四つのジャンプ台

        self.setup_blues()          # 青のバルーンを準備
        self.setup_greens()         # 緑のバルーンを準備
        self.setup_yellows()        # 黄色のバルーンを準備

        self.setup_jumpboards()     # ジャンプボードを準備

        # シーソーを準備する
        self.seesaw = Seesaw(SEESAW_X, SEESAW_Y, SEESAW_W, SEESAW_H,
                             SEESAW_VX, SEESAW1_IMAGE, SEESAW2_IMAGE)
        seesaws.add(self.seesaw)    # Eventを受ける為、Group以外を持つ

        # パフォーマを準備する(一人目はジャンプ中)
        self.performers.add(Performer(1, WEST, PERFORMER_Y,
                                      PERFORMER_W, PERFORMER_H,
                                      STATE_JUMPING, PERFORMER1_IMAGE))
        # 二人目はシーソーの右端に立つ
        performer = Performer(2, SEESAW_X + SEESAW_W - PERFORMER_W,
                              SEESAW_Y + SEESAW_H - PERFORMER_H,
                              PERFORMER_W, PERFORMER_H,
                              STATE_STANDING, PERFORMER2_IMAGE)
        self.performers.add(performer)
        # 二人目は、シーソーに乗っている事を伝える
        self.seesaw.ride(performer)

        # Groupの一括管理
        self.objects = [self.yellows, self.greens, self.blues, seesaws,
                        self.performers, self.jumpboards]
        self.balloons = [self.yellows, self.greens, self.blues]
        self.screen.fill(BLACK)
        self.frame()
        self.show_score()

    def show_score(self):
        text = self.font.render( ("SCORE : %d" % self.score), True, WHITE )
        self.screen.blit(text, (SCORE_X, SCORE_Y))
        text = self.font.render( ("PLAYER : %d" % self.num_jumper), True, WHITE )
        position = text.get_rect()
        position.y = SCORE_Y
        position.right = EAST
        self.screen.blit(text, position)

    def frame(self):
        pygame.draw.rect(self.screen, WHITE,
                         pygame.Rect(WEST, NORTH, EAST-WEST, SOUTH-NORTH), 1)

    def run(self):
        while (self.stage != STAGE_QUIT):
            if self.stage == STAGE_START:
                self.intro()
            self.animate()
            self.num_jumper -= 1
            if self.stage == STAGE_DOWN and self.num_jumper > 0:
                self.stage = STAGE_NEXT
                self.next()
            if self.stage != STAGE_QUIT:
                if self.num_jumper == 0:
                    self.stage = STAGE_OVER
                    self.game_over()
                else:       # 再開する
                    self.stage = STAGE_RUN

    def show_center_message(self, message, y):
        text = self.font.render(message, True, WHITE)
        position = text.get_rect()
        position.center = (X_CENTER, y)
        self.screen.blit(text, position)

    def intro_message(self):
        y = MESSAGE_TOP
        self.show_center_message("INSERT COIN", y)
        y += MESSAGE_GAP
        self.show_center_message("OR", y)
        y += MESSAGE_GAP
        self.show_center_message("PRESS 'SPACE' BAR", y)
        y += MESSAGE_GAP
        self.show_center_message("TO START", y)

    def intro(self):
        self.balloon_tilt = 0
        self.stage = STAGE_INTRO
        self.num_jumper = self.num_jumper_org
        self.score = 0
        while (self.stage == STAGE_INTRO):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.intro_message()

            # バルーンのアニメ
            self.balloon_anime() # 傾きを切り替える
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
        self.seesaw.back_origin()
        for performer in self.performers:
            performer.back_origin(self.seesaw)
        # self.seesaw.back_origin()

    def next_message(self):
        y = MESSAGE_TOP + MESSAGE_GAP
        self.show_center_message("JUMPER 1 DOWN", y)
        message = str(self.num_jumper) + "  JUMPER"
        if self.num_jumper > 1:
            message +="S"
        message += "  LEFT";
        y += MESSAGE_GAP
        self.show_center_message(message, y)

    def next(self):
        self.balloon_tilt = 0
        count = FPS * 2
        while (count > 0 and self.stage != STAGE_QUIT):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.next_message()

            # バルーンのアニメ
            self.balloon_anime()
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
            count -= 1
        self.seesaw.back_origin()
        for performer in self.performers:
            performer.back_origin(self.seesaw)

    def game_over_message(self):
        y = MESSAGE_TOP + MESSAGE_GAP
        self.show_center_message("GAME OVER!", y)
        y += MESSAGE_GAP*2
        self.show_center_message("PRESS 'SPACE' BAR", y)
        y += MESSAGE_GAP
        self.show_center_message("TO REPLAY", y)

    def game_over(self):
        self.balloon_tilt = 0
        count = FPS * 5
        while (count > 0 and self.stage != STAGE_RUN):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.stage = STAGE_RUN
            self.clock.tick(FPS)
            if self.balloon_tilt < FPS/2 :
                self.game_over_message()

            # バルーンのアニメ
            self.balloon_anime()
            for obj in self.balloons:
                obj.update()
                obj.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()
            count -= 1
        if self.stage == STAGE_RUN:
            self.seesaw.back_origin()
            for performer in self.performers:
                performer.back_origin(self.seesaw)
            self.stage = STAGE_START
        else:
            self.stage = STAGE_QUIT

    def balloon_anime(self):
        self.balloon_tilt += 1
        if self.balloon_tilt >= FPS:
            self.balloon_tilt = 0
        # バルーンのアニメ
        for color_groups in self.balloons:
            for balloon in color_groups:
                balloon.set_balloon_tilt( self.balloon_tilt)

    def animate(self):
        while (self.stage == STAGE_RUN):
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: self.stage = STAGE_QUIT
                if event.type == pygame.KEYDOWN:
                    # 「左」キーを処理する
                    if event.key == pygame.K_LEFT:
                        self.seesaw.move_left()
                    # 「右」キーを処理する
                    if event.key == pygame.K_RIGHT:
                        self.seesaw.move_right()
                if event.type == pygame.KEYUP:
                    # 「左」キーを処理する
                    if event.key == pygame.K_LEFT:
                        self.seesaw.stop()
                    # 「右」キーを処理する
                    if event.key == pygame.K_RIGHT:
                        self.seesaw.stop()
            self.clock.tick(FPS)
            # バルーンのアニメ
            self.balloon_anime()
            # オブジェクトの描画
            for obj in self.objects:
                obj.update()
                obj.draw(self.screen)
            # パフォーマの墜落を確認
            for performer in self.performers.sprites():
                if performer.down:
                    self.stage = STAGE_DOWN
            # パフォーマとジャンプ台の接触をチェック
            collided = pygame.sprite.groupcollide(self.jumpboards,
                                                  self.performers, False, False)
            if len(collided)>0:
                for jumpboard in collided:
                    performer = collided.get(jumpboard).pop()
                    jumpboard.bump(performer)

            # シーソーとパフォーマの接触をチェック
            collided = pygame.sprite.spritecollide(self.seesaw,
                                                   self.performers, False )
            if len(collided) > 1:  # 必ず1人は、接触していることに注意
                for person in self.performers.sprites():
                    if person.status == STATE_JUMPING:  # シーソーに着地
                        jumper = person
                    else: # 今、立ってる人
                        stand_by_player = person
                if jumper.inactive_y == 0: # ジャンパーが着地
                    x_offset, y_rate = jumper.check(self.seesaw)
                    #rateがゼロなら墜落
                    if y_rate==0:
                        self.stage = STAGE_DOWN
                    # 着地したジャンパーの情報を、立っているパフォーマにひき継ぐ
                    vx, vy = jumper.landed(self.seesaw)
                    vx = max(min((self.seesaw.vx + vx)/2 + x_offset, MAX_VX),
                             -MAX_VX)
                    vy = min(vy * y_rate, MAX_VY)
                    stand_by_player.jump(vx, -vy, self.seesaw)
                else:  # 今、飛びたてのjumperが一 ( 着地じゃない )
                    jumper.inactive_y += jumper.vy
                    if jumper.inactive_y <= 0:
                        jumper.inactive_y = 0 # シーソーを離れた
            # パフォーマと風船の接触をチェック
            for balloons in self.balloons:
                collided = pygame.sprite.groupcollide(
                    balloons, self.performers, False, False
                    )
                if len(collided)>0:
                    for balloon in collided:
                        performer = collided.get(balloon).pop()
                        self.score += balloon.bump(performer)
                        balloons.remove(balloon)
                    if len(balloons) == 0:
                        if balloons == self.yellows:
                            self.score += YELLOW_BONUS
                            self.setup_yellows()
                        elif balloons == self.greens:
                            self.score += GREEN_BONUS
                            self.setup_greens()
                        else:
                            self.score += BLUE_BONUS
                            self.setup_blues()

            # 表示の更新
            self.show_score()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.frame()

# メインプログラム
def main():
    board = Board(WIDTH, HEIGHT, NUM_JUMPER)
    board.setup()
    board.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
