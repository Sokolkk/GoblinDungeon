import random

class Character:
    def __init__(self, name, health, attack, defense, speed, abilities):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.abilities = abilities

    def attack_action(self, enemy):
        damage = self.calculate_damage(enemy)
        enemy.take_damage(damage)
        print(f"{self.name} атакует {enemy.name} и наносит {damage} урона.")

    def defend_action(self):
        self.defense += 2
        print(f"{self.name} вступает в защитную позицию. Защита увеличена.")

    def take_damage(self, damage):
        damage -= self.defense
        self.current_health -= max(0, damage)
        if self.current_health <= 0:
            print(f"{self.name} был повержен!")

    def calculate_damage(self, enemy):
        return random.randint(1, self.attack) - enemy.defense

    def is_alive(self):
        return self.current_health > 0

    def use_ability(self, ability, target):
        if ability in self.abilities:
            print(f"{self.name} использует способность {ability} на {target.name}.")
            # Логика для использования способности
        else:
            print(f"{self.name} не обладает способностью {ability}.")

class Enemy:
    def __init__(self, name, health, attack, defense, speed, abilities):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.abilities = abilities

    def attack_action(self, target):
        damage = self.calculate_damage(target)
        target.take_damage(damage)
        print(f"{self.name} атакует {target.name} и наносит {damage} урона.")

    def defend_action(self):
        self.defense += 2
        print(f"{self.name} вступает в защитную позицию. Защита увеличена.")

    def take_damage(self, damage):
        damage -= self.defense
        self.current_health -= max(0, damage)
        if self.current_health <= 0:
            print(f"{self.name} был повержен!")

    def calculate_damage(self, target):
        return random.randint(1, self.attack) - target.defense

    def is_alive(self):
        return self.current_health > 0

class Battle:
    def __init__(self, heroes, enemies):
        self.heroes = heroes
        self.enemies = enemies
        self.current_turn = None

    def start(self):
        print("Бой начинается!")

    def round(self):
        print("\nНовый раунд!")
        self.current_turn = self.heroes + self.enemies
        self.current_turn.sort(key=lambda character: character.speed, reverse=True)

        for character in self.current_turn:
            if isinstance(character, Character) and character.is_alive():
                self.hero_turn(character)
            elif isinstance(character, Enemy) and character.is_alive():
                self.enemy_turn(character)

    def hero_turn(self, hero):
        print(f"\nХод {hero.name} (Герой)")
        print(f"Здоровье: {hero.current_health}")

        action = input("Выберите действие: 1 - Атака, 2 - Защита, 3 - Использовать способность: ")

        if action == '1':
            target = self.choose_target(hero, self.enemies)
            hero.attack_action(target)
        elif action == '2':
            hero.defend_action()
        elif action == '3':
            ability = input("Выберите способность: ")
            target = self.choose_target(hero, self.enemies)
            hero.use_ability(ability, target)

    def enemy_turn(self, enemy):
        print(f"\nХод {enemy.name} (Враг)")
        print(f"Здоровье: {enemy.current_health}")

        target = self.choose_target(enemy, self.heroes)
        enemy.attack_action(target)

    def choose_target(self, character, targets):
        print("Выберите цель:")
        for i, target in enumerate(targets, start=1):
            print(f"{i}. {target.name} (Здоровье: {target.current_health}/{target.max_health})")

        while True:
            try:
                choice = int(input("Введите номер цели: "))
                if 1 <= choice <= len(targets):
                    return targets[choice - 1]
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Введите число.")

    def is_over(self):
        return all(not character.is_alive() for character in self.heroes) or \
               all(not character.is_alive() for character in self.enemies)

    def is_heroes_win(self):
        return all(not enemy.is_alive() for enemy in self.enemies)

# Создайте героев и врагов
heroes = [
    Character("Reynauld", 100, 10, 5, 8, ["Holy Lance", "Crusader Strike"]),
    Character("Dismas", 100, 8, 6, 10, ["Headshot", "Pistol Shot"]),
    Character("Vestal", 100, 5, 7, 9, ["Heal", "Divine Grace"]),
    Character("Jester", 100, 6, 5, 11, ["Battle Ballad", "Stress Relief"]),
]

enemies = [
    Enemy("Skeleton", 50, 5, 2, 7, []),
    Enemy("Ghoul", 60, 6, 3, 6, []),
    Enemy("Cultist", 70, 7, 4, 5, []),
]

# Запустите бой
battle = Battle(heroes, enemies)
battle.start()

# Выполняйте раунды боя
while not battle.is_over():
    battle.round()

# Проверьте результат боя
if battle.is_heroes_win():
    print("Герои победили!")
else:
    print("Герои проиграли!")
