import sys

from math import sqrt

from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QPen, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets

number_of_bots = 19
creation_interval = 120
steps_per_second = 70
step_length = 1

count_tower = 0
count_target = 19

coordinates = []
point_coordinates = []
towers_coordinates = {}
target_coordinates = []

shot_count_tower = [0, 0]

buy_tower = [False]

player_hp = ['5']
player_coin = ['100']

pause_resume_button = [False]
game_result = ['Победа', 'Поражение', '', 0]

track_list = [[(-creation_interval * step_length) * number_of_bots, 500],
              [200, 500],
              [200, 300],
              [400, 300],
              [400, 500],
              [500, 500],
              [500, 600],
              [750, 600],
              [750, (-creation_interval * step_length) * number_of_bots]]

class Form1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):

        self.setWindowTitle("Стреляющие башни")
        self.setStyleSheet('background: black;')
        self.move(500, 150)
        self.setFixedSize(800, 820)

        game_name = QLabel(self)
        game_name.resize(400, 50)
        game_name.setStyleSheet('font-size: 40px; color: white; background: black;')
        game_name.setAlignment(Qt.AlignCenter)
        game_name.setText("Стреляющие башни")
        game_name.move(200, 170)

        buttonPlay = QtWidgets.QPushButton("Играть", self)
        buttonPlay.setGeometry(200, 270, 400, 80)
        buttonPlay.setStyleSheet('border: 1px solid white; color: white; background: black;')
        buttonPlay.setFont(QFont('Arial', 14))
        buttonPlay.clicked.connect(self.switch_play)

        buttonRule = QtWidgets.QPushButton("Правила", self)
        buttonRule.setGeometry(200, 370, 400, 80)
        buttonRule.setStyleSheet('border: 1px solid white; color: white; background: black;')
        buttonRule.setFont(QFont('Arial', 14))
        buttonRule.clicked.connect(self.switch_rule)

        buttonExit = QtWidgets.QPushButton("Выйти", self)
        buttonExit.setGeometry(200, 470, 400, 80)
        buttonExit.setStyleSheet('border: 1px solid white; color: white; background: black;')
        buttonExit.setFont(QFont('Arial', 14))
        buttonExit.clicked.connect(self.switch_exit)

    def switch_play(self):

        form2.move(form1.x(), form1.y())
        form3.move(form1.x(), form1.y())

        form2.show()
        self.hide()

    def switch_rule(self):

        form2.move(form1.x(), form1.y())
        form3.move(form1.x(), form1.y())

        form3.show()
        self.hide()

    def switch_exit(self):

        sys.exit(app.exec_())

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.switch_exit()

class Form2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.bullet_interval = None
        self.bullet_trajectory = {}
        self.setWindowTitle("Игра «Стреляющие башни»")
        self.setStyleSheet('background: green')
        self.setFixedSize(800, 820)

        self.set_coordinates()

        self.bots = self.bots()

        self.scenery = self.scenery()

        self.towers = self.towers()

        self.targets = self.targets()

        self.weapons = self.weapons()

        self.bar = self.bar()

        for i in range(number_of_bots):
            self.towers[i][0].move(-50, -50)

        for j in range(3):
            self.targets[j].move(-50, -50)

        t = 0
        self.time_list = []
        for i in range(number_of_bots):
            self.time_list.append(t)
            t += creation_interval

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_track)
        self.timer.start(0)

        self.setupUi()

    def paintEvent(self, event):

        paint_road = QPainter()
        paint_road.begin(self)
        self.Road(paint_road)
        paint_road.end()

    def Road(self, paint_road):

        pen = QPen(Qt.darkRed, 46, Qt.SolidLine)

        for i in range(1, len(track_list)):
            paint_road.setPen(pen)
            paint_road.drawLine((track_list[i - 1][0]) + 19,
                                (track_list[i - 1][1]) + 19,
                                (track_list[i][0]) + 19,
                                (track_list[i][1]) + 19)

    def mousePressEvent(self, event):
        global count_tower, count_target

        if event.button() == Qt.LeftButton:

            if event.y() <= 720:
                if pause_resume_button[0] == True:
                    if buy_tower[0] == False:
                        if int(player_coin[0]) >= 100:
                            player_coin[0] = str(int(player_coin[0]) - 100)
                            self.towers[count_tower][0].move(event.x() - 20, event.y() - 20)
                            towers_coordinates[count_tower] = [event.x(), event.y()]
                            self.weapons[2].setText(player_coin[0])

                            count_tower += 1

                    else:
                        if int(player_coin[0]) >= 150:
                            player_coin[0] = str(int(player_coin[0]) - 150)
                            self.towers[count_tower][0].setStyleSheet('background-image: url("Tower2.png")')
                            self.towers[count_tower][1] = True
                            self.towers[count_tower][0].move(event.x() - 20, event.y() - 20)
                            towers_coordinates[count_tower] = [event.x(), event.y()]
                            self.weapons[2].setText(player_coin[0])

                            count_tower += 1

        elif event.button() == Qt.RightButton:

            if event.y() <= 720:
                if pause_resume_button[0] == True:

                    self.targets[0].move(event.x() - 2, event.y() - 20)
                    self.targets[1].move(event.x() - 20, event.y() - 2)
                    self.targets[2].move(event.x() - 2, event.y() - 2)


                    global target_coordinates
                    target_coordinates.clear()
                    target_coordinates.append(event.x())
                    target_coordinates.append(event.y())
                    self.zone_coverage()

                    shot_count_tower[0] = 0
                    shot_count_tower[1] = 0

                    self.attack_radius()

                    if count_target >= 0:
                        count_target -= 1

    def bar(self):

        bar = []
        buttonResume = QtWidgets.QPushButton(self)
        buttonResume.setGeometry(10, 730, 80, 80)
        buttonResume.setFont(QFont('Arial', 8))
        buttonResume.setIcon(QIcon('Resume_2.png'))
        buttonResume.setIconSize(QSize(80, 80))
        buttonResume.clicked.connect(self.pause_resume_click)
        bar.append(buttonResume)

        buttonRestart = QtWidgets.QPushButton(self)
        buttonRestart.setGeometry(100, 730, 80, 80)
        buttonRestart.setFont(QFont('Arial', 8))
        buttonRestart.setIcon(QIcon('Restart.png'))
        buttonRestart.setIconSize(QSize(80, 80))
        buttonRestart.clicked.connect(self.restart_click)

        buttonMenu = QtWidgets.QPushButton(self)
        buttonMenu.setGeometry(190, 730, 80, 80)
        buttonMenu.setFont(QFont('Arial', 8))
        buttonMenu.setIcon(QIcon('Menu.png'))
        buttonMenu.setIconSize(QSize(80, 80))
        buttonMenu.clicked.connect(self.switch_menu)

        buttonBuyTower1 = QtWidgets.QPushButton(self)
        buttonBuyTower1.setGeometry(280, 730, 60, 80)
        buttonBuyTower1.setIcon(QIcon('Tower1_on.png'))
        buttonBuyTower1.setIconSize(QSize(80, 80))
        buttonBuyTower1.clicked.connect(self.buy_tower1)
        bar.append(buttonBuyTower1)

        buttonBuyTower1 = QtWidgets.QPushButton(self)
        buttonBuyTower1.setGeometry(350, 730, 60, 80)
        buttonBuyTower1.setIcon(QIcon('Tower2_off.png'))
        buttonBuyTower1.setIconSize(QSize(80, 80))
        buttonBuyTower1.clicked.connect(self.buy_tower2)
        bar.append(buttonBuyTower1)

        return bar

    def pause_resume_click(self):

        if pause_resume_button[0] == False:
            pause_resume_button[0] = True
            self.bar[0].setIcon(QIcon('Pause_1.png'))
        else:
            pause_resume_button[0] = False
            self.bar[0].setIcon(QIcon('Resume_2.png'))

    def restart_click(self):
        global count_tower

        self.time_list.clear()

        t = 0
        self.time_list = []
        for i in range(number_of_bots):
            self.time_list.append(t)
            t += creation_interval

        for j in range(number_of_bots):
            self.bots[j][0].resize(40, 40)
            self.bots[j][0].setStyleSheet('background: red;')
            self.bots[j][0].setStyleSheet('background-image: url("Enemy.png")')
            self.bots[j][0].move(-50, -50)

            self.bots[j][1] = 100
            self.bots[j][2] = 0
            self.bots[j][3] = False

        for t in range(len(towers_coordinates)):
            self.towers[t][0].move(-50, -50)
            self.towers[t][1] = False

        pause_resume_button[0] = False

        player_coin[0] = str(100)
        player_hp[0] = str(5)

        self.weapons[1].setText(player_hp[0])
        self.weapons[2].setText(player_coin[0])

        count_tower = 0

        self.targets[0].move(-50, -50)
        self.targets[1].move(-50, -50)
        self.targets[2].move(-50, -50)

        towers_coordinates.clear()

        game_result[3] = 0

        self.weapons[3].setStyleSheet('font-size: 25px; color: white; background: black')
        self.weapons[3].setText(game_result[2])

        buy_tower[0] = False
        self.bar[1].setIcon(QIcon('Tower1_on.png'))
        self.bar[2].setIcon(QIcon('Tower2_off.png'))

        self.bar[0].setIcon(QIcon('Resume_2.png'))

    def buy_tower1(self):

        buy_tower[0] = False
        self.bar[1].setIcon(QIcon('Tower1_on.png'))
        self.bar[2].setIcon(QIcon('Tower2_off.png'))

    def buy_tower2(self):

        buy_tower[0] = True
        self.bar[2].setIcon(QIcon('Tower2_on.png'))
        self.bar[1].setIcon(QIcon('Tower1_off.png'))

    def zone_coverage(self):

        point_x = target_coordinates[0]
        point_y = target_coordinates[1]

        point_x -= 20
        point_y -= 20

        point_coordinates.clear()

        for i in range(point_y, point_y + 40):
            point_x = target_coordinates[0]
            for j in range(point_x, point_x + 40):
                point_coordinates.append([point_x, point_y])
                point_x += 1
            point_y += 1


    def show_track(self):

        if pause_resume_button[0] == True:
            if (int(player_hp[0]) == 5 and game_result[3] == 19 or
                    int(player_hp[0]) == 4 and game_result[3] == 18
                    or int(player_hp[0]) == 3 and game_result[3] == 17
                    or int(player_hp[0]) == 2 and game_result[3] == 16
                    or int(player_hp[0]) == 1 and game_result[3] == 15):
                pause_resume_button[0] = False
                self.weapons[3].setStyleSheet('font-size: 25px; color: green; background: black')
                self.weapons[3].setText(game_result[0])


        if pause_resume_button[0] == True:

            if int(player_hp[0]) > 0:
                for i in range(number_of_bots):

                    label_x = coordinates[self.time_list[i]][0]
                    label_y = coordinates[self.time_list[i]][1]
                    self.bots[i][0].move(label_x, label_y)


                    if self.bots[i][0].y() == -40 and self.bots[i][3] == False:
                        player_hp[0] = str(int(player_hp[0]) - 1)
                        self.weapons[1].setText(player_hp[0])
            elif int(player_hp[0]) == 0:
                self.weapons[3].setStyleSheet('font-size: 25px; color: red; background: black')
                self.weapons[3].setText(game_result[1])

            time_sleep = int(1000 / steps_per_second)
            self.timer.start(time_sleep)

            for i in range(number_of_bots):
                self.time_list[i] += 1



    def bots(self):

        bots = []
        for i in range(number_of_bots):
            bot = QLabel(self)
            bot.resize(40, 40)
            bot.setStyleSheet('background: red;')
            bot.setStyleSheet('background-image: url("Enemy.png")')
            bot.move(-50, -50)
            bots.append([bot, 100, 0, False])
        return bots

    def towers(self):

        towers = []
        for i in range(number_of_bots):
            tower = QLabel(self)
            tower.resize(40, 40)
            tower.setStyleSheet('background-image: url("Tower.png")')
            towers.append([tower, False])
        return towers

    def targets(self):

        targets = []

        target_x = QLabel(self)
        target_x.resize(4, 40)
        target_x.setStyleSheet('background: black')
        targets.append(target_x)

        target_y = QLabel(self)
        target_y.resize(40, 4)
        target_y.setStyleSheet('background: black')
        targets.append(target_y)

        target_point = QLabel(self)
        target_point.resize(4, 4)
        target_point.setStyleSheet('background: red')
        targets.append(target_point)

        return targets

    def attack_damage(self):

        if pause_resume_button[0] == True:

            for j in range(number_of_bots):
                for i in range(len(point_coordinates)):
                    if point_coordinates[i][0] == (self.bots[j][0].x() + 20) and point_coordinates[i][1] \
                            == (self.bots[j][0].y() + 20):
                        self.bots[j][1] = self.bots[j][1] - ((20 * shot_count_tower[0]) + (10 * shot_count_tower[1]))

                        if self.bots[j][1] <= 0:
                            self.bots[j][2] += 1
                            self.bots[j][3] = True
                            self.bots[j][0].resize(0, 0)
                            if self.bots[j][2] == 1:
                                player_coin[0] = str(int(player_coin[0]) + 50)
                                game_result[3] += 1
                            self.weapons[2].setText(player_coin[0])

    def hit_on_target(self):

        self.bullet_interval = QTimer(self)
        self.bullet_interval.timeout.connect(lambda: self.attack_damage())
        self.bullet_interval.start(1000)

        self.attack_damage()


    def attack_radius(self):

        for trae in range(len(towers_coordinates)):

            x1_bullet_coor = towers_coordinates[trae][0]
            y1_bullet_coor = towers_coordinates[trae][1]

            x2_bullet_coor = target_coordinates[0]
            y2_bullet_coor = target_coordinates[1]

            flight_path_bullet = sqrt(
                ((x2_bullet_coor - x1_bullet_coor) ** 2) + ((y2_bullet_coor - y1_bullet_coor) ** 2))

            if flight_path_bullet <= 200:
                shot_count_tower[0] += 1
                if self.towers[trae][1] == True:
                    shot_count_tower[1] += 1

        if shot_count_tower[0] > 0:
            self.targets[2].setStyleSheet('background: red')
        else:
            self.targets[2].setStyleSheet('background: cyan')
        self.hit_on_target()

    def scenery(self):

        trees = []
        for i in range(3):
            tree_1 = QLabel(self)
            pixmap = QPixmap('Tree_scenery_2.png')
            tree_1.setPixmap(pixmap)
            tree_1.resize(91, 77)
            trees.append(tree_1)
        trees[0].move(100, 50)
        trees[1].move(270, 350)
        trees[2].move(600, 500)

        return trees

    def weapons(self):
        weapons = []

        bar = QLabel(self)
        bar.resize(800, 100)
        bar.setStyleSheet('font-size: 30px; color: white; background: black')
        bar.move(0, 720)
        weapons.append(bar)

        heart = QLabel(self)
        heart.resize(100, 100)
        heart.setStyleSheet('font-size: 22px; color: white; background-image: url("Heart.png")')
        heart.setAlignment(Qt.AlignCenter)
        heart.setText(player_hp[0])
        heart.move(680, 720)
        weapons.append(heart)

        coin = QLabel(self)
        coin.resize(100, 100)
        coin.setStyleSheet('font-size: 22px; color: white; background-image: url("Coin.png")')
        coin.setAlignment(Qt.AlignCenter)
        coin.setText(player_coin[0])
        coin.move(580, 720)
        weapons.append(coin)

        view_result = QLabel(self)
        view_result.resize(200, 100)
        view_result.setStyleSheet('font-size: 25px; color: white; background: black')
        view_result.setAlignment(Qt.AlignCenter)
        view_result.setText(game_result[2])
        view_result.move(380, 720)
        weapons.append(view_result)

        return weapons

    def set_coordinates(self):
        for i in range(1, len(track_list)):
            x1 = track_list[i - 1][0]
            y1 = track_list[i - 1][1]

            x2 = track_list[i][0]
            y2 = track_list[i][1]

            coordinates.append([x1, y1])

            d = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

            k = step_length / d

            q = int(d / step_length)

            for j in range(q):
                if d > 0:
                    x3 = (x1 + (x2 - x1) * k)
                    y3 = (y1 + (y2 - y1) * k)
                    coordinates.append([int(x3), int(y3)])
                    x1 = x3
                    y1 = y3
                    d = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                    if d > 0:
                        k = step_length / d
                    else:
                        k = 1
                else:
                    coordinates.append([x2, y2])

    def setupUi(self):
        self.setWindowTitle("Игра_Стреляющие_Башни")
        self.setGeometry(form1.x(), form1.y(), 800, 820)

    def switch_menu(self):

        self.restart_click()

        form3.move(form2.x(), form2.y())
        form1.move(form2.x(), form2.y())

        form1.show()
        self.hide()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.switch_menu()


class Form3(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):

        self.setWindowTitle("Правила игры «Стреляющие башни» ")
        self.setFixedSize(800, 820)
        self.setStyleSheet('background: black ')

        text_label = QLabel(self)
        text_label.move(10, 60)
        text_label.resize(780, 650)

        text_label.setWordWrap(True)
        text_label.setText(" В игре есть две стороны, атакующая и защищающая. "
                           "Игрок управляет защищающейся стороной. У защищающейся "
                           "стороны есть стреляющие башни, а атакующую сторону представляют "
                           "монстры. Атакующая сторона начинает свой путь из левой стороны "
                           "игрового поля. Конец пути находится в правой части игрового поля."
                           "\n Для того чтобы выиграть, игроку потребуется не допустить "
                           "атакующей стороне дойти до конца пути. Для этого нужно ставить "
                           "башни на игровом поле кроме дороги, по которой передвигается "
                           "атакующая сторона. Стреляющие башни можно устанавливать за монеты, "
                           "количество которых показано на нижней части игрового поля. "
                           "Монеты можно зарабатывать, устраняя монстров. Если монстр "
                           "дойдет до конца пути, то игрок потеряет одну жизнь. В случае, "
                           "если жизней не осталось, игрок проигрывает, а игра заканчивается. "
                           "Игрок выигрывает, если устранил всех монстров атакующей стороны, "
                           "и игра заканчивается."
                           "\n Для того чтобы начать игру, игроку потребуется нажать кнопку "
                           "«Продолжить» на нижней панели игрового поля. После начала игры "
                           "игроку нужно установить башню кликом левой кнопки мыши, выбрав "
                           "ее тип. Тип башни вы можете выбрать на нижней панели игрового "
                           "поля. Стандартная башня стоит 100 монет, а улучшенная 150. "
                           "Далее игроку потребуется установить прицел на правую кнопку "
                           "мыши. После устранения одного монстра игрок получает 50 монет."
                           )
        text_label.setStyleSheet('font-size: 20px; color: white; background: black ')

        name_rule_label = QLabel(self)
        name_rule_label.move(10, 100)
        name_rule_label.resize(780, 30)

        name_rule_label.setWordWrap(True)
        name_rule_label.setText("Правила игры Стреляющие башни")
        name_rule_label.setStyleSheet('font-size: 30px; color: white; background: black ')

        buttonRule_Menu = QtWidgets.QPushButton("Назад", self)
        buttonRule_Menu.setGeometry(20, 20, 130, 60)
        buttonRule_Menu.setIcon(QIcon('Menu.png'))
        buttonRule_Menu.setStyleSheet('border: 1px solid white; font-size: 25px; color: white; background: black ')
        buttonRule_Menu.clicked.connect(self.switch_rule_menu)

    def switch_rule_menu(self):

        form2.move(form3.x(), form3.y())
        form1.move(form3.x(), form3.y())

        form1.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.switch_rule_menu()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    form1 = Form1()
    form2 = Form2()
    form3 = Form3()
    form1.show()
    app.exec_()