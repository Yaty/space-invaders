from tkinter import *
from random import *


class Item:
        def __init__(self, x, y, id):
                self.x = x
                self.y = y
                self.id = id


class Missile(Item):
        def __init__(self, x, y, id):
                super(Missile, self).__init__(x, y, id)


bonus_types = {
        'NUKE': 'NUKE',
        'LASER': 'LASER',
        'TRIPLE': 'TRIPLE',
        'AMMUNITION': 'AMMUNITION',
}


class Bonus(Item):
        def __init__(self, x, y, id, type):
                super(Bonus, self).__init__(x, y, id)
                self.type = type


class Enemy(Item):
        def __init__(self, x, y, id):
                super(Enemy, self).__init__(x, y, id)
                self.missile = None


class SpaceInvader:
        def __init__(self):
                self.score = 0
                self.laser_activated = False
                self.triple_missile_shot_activated = False
                self.x = 0
                self.y = 470
                self.stop = 0
                self.remaining_bonus_time = 0
                self.ammunition = 100
                self.score = 0
                self.playing = False
                self.enemies = []
                self.bonuses = []
                self.increment = 10
                self.missiles = []
                self.laser = None

                self.fen = Tk()
                self.fen.bind("<Left>", self.left)
                self.fen.bind("<Right>", self.right)
                self.fen.bind("<space>", self.shoot)
                self.fen.bind("<s>", self.start)

                self.can = Canvas(self.fen, height=500, width=700, bg="blue")
                self.can.grid(column=0, row=1)
                fond = PhotoImage(file="../assets/star_de.GIF")
                self.can.create_image(0, 0, anchor=NW, image=fond)

                self.textscore = self.can.create_text(
                        700,
                        0,
                        font="ubuntu 20",
                        text="Score : " + str(self.score),
                        fill="red",
                        anchor=NE
                )

                self.textammo = self.can.create_text(
                        0,
                        0,
                        font="ubuntu 20",
                        text="Munitions : " + str(self.ammunition),
                        fill="red",
                        anchor=NW
                )
                self.textstart = self.can.create_text(340, 250, font="arial 20", text="Press S to start", fill="red")
                self.photoenemi = PhotoImage(file="../assets/enemi.GIF")
                self.photolaser = PhotoImage(file="../assets/bonus_laser.GIF")
                self.photoammo = PhotoImage(file="../assets/ammo.GIF")
                self.photonuke = PhotoImage(file="../assets/nuke.GIF")
                self.photoammobonus = PhotoImage(file="../assets/ammo bonus.GIF")
                self.photo = PhotoImage(file="../assets/vaisseau.GIF")
                self.vaisseau = self.can.create_image(self.x, 450, image=self.photo, anchor=W)

                self.fen.mainloop()

        def nuke(self):
                if not self.playing:
                        return

                explosion = self.can.create_rectangle(0, 0, 700, 500, fill="white")
                self.fen.after(300, self.can.delete, explosion)

                for enemy in self.enemies:
                        self.remove_enemy(enemy)

                for bonus in self.bonuses:
                        self.remove_bonus(bonus)

        def remove_enemy(self, enemy):
                self.enemies.remove(enemy)
                self.can.delete(enemy.id)

                if enemy.missile is not None:
                        self.can.delete(enemy.missile.id)

        def remove_missile(self, missile):
                self.missiles.remove(missile)
                self.can.delete(missile.id)

        def remove_bonus(self, bonus):
                self.bonuses.remove(bonus)
                self.can.delete(bonus.id)

        def create_triple_missile(self):
                if not self.playing:
                        return

                id = self.can.create_rectangle(self.x + 39, self.y, self.x + 42, self.y - 10, fill="yellow")
                self.missiles.append(Missile(self.x, self.y, id))

                id = self.can.create_rectangle(self.x - 1, self.y, self.x + 2, self.y - 10, fill="yellow")
                self.missiles.append(Missile(self.x, self.y, id))

                id = self.can.create_rectangle(self.x + 19, self.y, self.x + 22, self.y - 10, fill="yellow")
                self.missiles.append(Missile(self.x, self.y, id))

        def stop_bonus(self, aff_temps):
                if not self.playing:
                        return

                self.can.delete(aff_temps)

                if self.remaining_bonus_time >= 0:
                        self.stop = 1
                        self.remaining_bonus_time -= 1

                        if self.laser_activated:
                                aff_temps = self.can.create_text(
                                        350,
                                        0,
                                        text="laser: " + str(self.remaining_bonus_time),
                                        font="ubuntu 20",
                                        anchor=N,
                                        fill="red"
                                )
                        elif self.triple_missile_shot_activated:
                                aff_temps = self.can.create_text(
                                        350,
                                        0,
                                        text="create_triple_missile: " + str(self.remaining_bonus_time),
                                        font="ubuntu 20",
                                        anchor=N,
                                        fill="red"
                                )

                        self.fen.after(1000, self.stop_bonus, aff_temps)
                else:
                        self.stop = 0
                        self.triple_missile_shot_activated = False
                        self.laser_activated = False

        def enable_bonus(self, bonus_type):
                if not self.playing:
                        return

                if bonus_type == bonus_types.get("LASER"):
                        self.laser_activated = True
                        self.remaining_bonus_time = 30

                        if self.stop == 0:
                                self.stop += 1
                                self.fen.after(3, self.stop_bonus, 0)
                elif bonus_type == bonus_types.get("AMMUNITION"):
                        self.ammunition += 100
                        self.display_ammunition()
                elif bonus_type == bonus_types.get("NUKE"):
                        self.fen.after(1, self.nuke)
                        self.score += 1000
                        self.display_score()
                elif bonus_type == bonus_types.get("TRIPLE"):
                        self.triple_missile_shot_activated = True
                        self.remaining_bonus_time = 30
                        if self.stop == 0:
                                self.stop += 1
                                self.fen.after(3, self.stop_bonus, 0)

        def enable_laser(self):
                if self.laser is not None and not self.laser_activated:
                        self.can.delete(self.laser)
                        return

                if not self.playing or not self.laser_activated:
                        return

                if self.laser is not None:
                        self.can.delete(self.laser)

                self.laser = self.can.create_rectangle(self.x + 18, 450, self.x + 23, 0, fill="blue")

                for enemy in self.enemies:
                        if self.x == enemy.x:
                                self.score += 1000
                                self.remove_enemy(enemy)

                for bonus in self.bonuses:
                        if self.x == bonus.x:
                                self.enable_bonus(bonus.type)
                                self.remove_bonus(bonus)

                self.display_score()
                self.fen.after(100, self.enable_laser)

        def display_score(self):
                self.can.delete(self.textscore)

                self.textscore = self.can.create_text(
                        700,
                        0,
                        font="ubuntu 20",
                        text="Score : " + str(self.score),
                        fill="red",
                        anchor=NE
                )

        def right(self, a):
                if not self.playing:
                        return

                if self.x < 660:
                        self.x += 20
                        self.can.delete(self.vaisseau)
                        self.vaisseau = self.can.create_image(self.x, 450, image=self.photo, anchor=W)

        def left(self, a):
                if not self.playing:
                        return

                if self.x > 0:
                        self.x -= 20
                        self.can.delete(self.vaisseau)
                        self.vaisseau = self.can.create_image(self.x, 450, image=self.photo, anchor=W)

        def display_ammunition(self):
                self.can.delete(self.textammo)

                self.textammo = self.can.create_text(
                        0,
                        0,
                        font="ubuntu 20",
                        text="Munitions : " + str(self.ammunition),
                        fill="red",
                        anchor=NW
                )

        def shoot(self, a):
                if not self.playing:
                        return

                if self.laser_activated:
                        self.enable_laser()
                elif self.ammunition > 0:
                        if self.triple_missile_shot_activated and self.ammunition >= 3:
                                self.ammunition -= 3
                                self.create_triple_missile()
                        else:
                                self.ammunition -= 1
                                self.launch_missile()

                        self.display_ammunition()

        def stop_game(self):
                self.can.delete(self.textstart)

                self.textstart = self.can.create_text(
                        340,
                        250,
                        font="arial 20",
                        text="game over press s to restart",
                        fill="red"
                )

                for missile in self.missiles:
                        self.can.delete(missile.id)

                self.missiles.clear()

                self.nuke()
                self.playing = False

        def move_missiles(self):
                if not self.playing:
                        return

                # Move current missiles
                for missile in self.missiles:
                        missile.y -= self.increment

                        self.can.move(missile.id, 0, -self.increment)

                        if missile.y < 0:
                                self.can.delete(missile.id)
                                continue

                        for enemy in self.enemies:
                                if (missile.x - 20 <= enemy.x <= missile.x + 20) and missile.y == enemy.y:
                                        self.remove_enemy(enemy)
                                        self.remove_missile(missile)
                                        self.score += 1000

                        for bonus in self.bonuses:
                                if (missile.x - 20 <= bonus.x <= missile.x + 20) and missile.y == bonus.y:
                                        self.enable_bonus(bonus.type)
                                        self.remove_bonus(bonus)
                                        self.remove_missile(missile)

                self.display_score()
                self.fen.after(20, self.move_missiles)

        def launch_missile(self):
                if not self.playing:
                        return

                id = self.can.create_rectangle(self.x + 19, self.y, self.x + 22, self.y - 10, fill="yellow")
                self.missiles.append(Missile(self.x, self.y, id))

        def start(self, event):
                if not self.playing:
                        self.playing = True
                        self.can.delete(self.textstart)
                        self.score = 0
                        self.ammunition = 100
                        self.bonuses = []
                        self.missiles = []
                        self.enemies = []
                        self.display_score()
                        self.create_enemies()
                        self.create_bonuses()
                        self.move_bonuses()
                        self.move_missiles()

        def create_bonuses(self):
                if not self.playing:
                        return

                rand = randrange(100)

                x = randrange(1, 34) * 20
                y = 0
                bonus = None

                if 0 <= rand < 3:
                        bonus = Bonus(
                                x,
                                y,
                                self.can.create_image(x + 10, y, anchor=NW, image=self.photolaser),
                                bonus_types.get("LASER")
                        )
                elif 3 <= rand < 6:
                        bonus = Bonus(
                                x,
                                y,
                                self.can.create_image(x + 10, y, anchor=NW, image=self.photoammo),
                                bonus_types.get("AMMUNITION")
                        )
                elif 6 <= rand < 9:
                        bonus = Bonus(
                                x,
                                y,
                                self.can.create_image(
                                        x + 10,
                                        y,
                                        anchor=NW,
                                        image=self.photoammobonus
                                ),
                                bonus_types.get("TRIPLE")
                        )
                elif 9 <= rand < 12:
                        bonus = Bonus(
                                x,
                                y,
                                self.can.create_image(x + 10, y, anchor=NW, image=self.photonuke),
                                bonus_types.get("NUKE"),
                        )

                if bonus is not None:
                        self.bonuses.append(bonus)

                self.fen.after(1000, self.create_bonuses)

        def is_touching_spaceship(self, x, y):
                return y == self.y and (self.x - 10 <= x <= self.x + 10)

        def move_bonuses(self):
                if not self.playing:
                        return

                for bonus in self.bonuses:
                        bonus.y += self.increment

                        self.can.move(bonus.id, 0, self.increment)

                        if bonus.y > 500:
                                self.can.delete(bonus.id)
                                continue

                        if self.is_touching_spaceship(bonus.x, bonus.y):
                                self.enable_bonus(bonus.type)
                                self.remove_bonus(bonus)
                                continue

                self.fen.after(750, self.move_bonuses)

        def launch_enemy_missiles(self, enemy):
                if not self.playing:
                        return

                if enemy not in self.enemies:
                        return

                if enemy.missile is None:
                        if randrange(20) == 1:
                                id = self.can.create_rectangle(
                                        enemy.x + 19,
                                        enemy.y + 20,
                                        enemy.x + 22,
                                        enemy.y + 30,
                                        fill="white"
                                )

                                enemy.missile = Missile(enemy.x + 20, enemy.y + 20, id)
                else:
                        enemy.missile.y += self.increment

                        self.can.move(enemy.missile.id, 0, self.increment)

                        if (self.x - 20 <= enemy.missile.x <= self.x + 20) and enemy.missile.y == self.y:
                                self.stop_game()
                        elif enemy.missile.y > 500:
                                self.can.delete(enemy.missile.id)
                                enemy.missile = None
                        else:
                                for bonus in self.bonuses:
                                        if bonus.x == enemy.missile.x and bonus.y == enemy.missile.y:
                                                self.remove_bonus(bonus)

                self.fen.after(50, self.launch_enemy_missiles, enemy)

        def move_enemy(self, enemy):
                if not self.playing:
                        return

                if enemy not in self.enemies:
                        return

                enemy.y += self.increment

                self.can.move(enemy.id, 0, self.increment)

                if (self.x - 20 <= enemy.x <= self.x + 20) and enemy.y == self.y:
                        self.stop_game()
                elif enemy.y > 500:
                        self.stop_game()
                else:
                        self.fen.after(450, self.move_enemy, enemy)

        def handle_enemy(self, enemy):
                self.enemies.append(enemy)
                self.move_enemy(enemy)
                self.launch_enemy_missiles(enemy)

        def create_enemies(self, time=3000):
                if not self.playing:
                        return

                x = randrange(1, 34) * 20
                y = 0

                time = max(time - 100, 500)

                id = self.can.create_image(x + 10, y, anchor=NW, image=self.photoenemi)
                enemy = Enemy(x, y, id)
                self.handle_enemy(enemy)
                self.fen.after(time, self.create_enemies, time)


if __name__ == "__main__":
        SpaceInvader()
