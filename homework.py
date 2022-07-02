class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self, training_type: str, duration: float, distance: float,
        speed: float, calories: float
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')

        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    C_1 = 18
    C_2 = 20

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        spent_calories = (
            self.C_1 * mean_speed - self.C_2
        ) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    STEPEN_2 = 2
    C_3 = 0.035
    C_4 = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()

        spent_calories = (
            self.C_3 * self.weight + (
                mean_speed ** self.STEPEN_2 // self.height
            ) * self.C_4 * self.weight
        ) * self.duration * self.MIN_IN_H
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    
    M_IN_KM: int = 1000
    LEN_STEP: float = 1.38
    C_4: float = 1.1
    C_5: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_spead = (
            self.length_pool * self.count_pool / self.M_IN_KM
        ) / self.duration
        return mean_spead

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        spent_calories = (mean_speed + self.C_4) * self.C_5 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    instance = None
    if workout_type == "SWM":
        mapping = {
            "action": data[0],
            "duration": data[1],
            "weight": data[2],
            "length_pool": data[3],
            "count_pool": data[4]
        }
        instance = Swimming(**mapping)
    if workout_type == "RUN":

        mapping = {
            "action": data[0],
            "duration": data[1],
            "weight": data[2]
        }
        instance = Running(**mapping)
    if workout_type == "WLK":
        mapping = {
            "action": data[0],
            "duration": data[1],
            "weight": data[2],
            "height": data[3]
        }
        instance = SportsWalking(**mapping)
    return instance


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training, workout_type)
