class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self, training_type : str, duration : float, distance : float, 
        speed : float, calories : float
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        speed = self.speed * 1000 / 60
        message = f'''
            Тип тренировки: {self.training_type}; 
            Длительность: {self.duration:.3f} ч.; 
            Дистанция: {self.distance:.3f} км; 
            Ср. скорость: {self.speed:.3f} км/ч; 
            Потрачено ккал: {self.calories:.3f}.
        '''
        return message


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.len_step = 0.65
        self.m_in_km = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.len_step / self.m_in_km
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, training_type : str, duration : float) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        duration = self.duration
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info_message = InfoMessage(training_type, duration, distance, mean_speed, calories)
        return info_message


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action : int , duration : float, weight : float):

        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        duration = self.duration * 60
        mean_speed = self.get_mean_speed()
        spent_calories = (18 * mean_speed - 20) * self.weight / self.m_in_km * self.duration
        return spent_calories
    


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action : int , duration : float, weight : float, height : float):
        super().__init__(action, duration, weight)
        self.height = height 

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        duration = self.duration * 60

        spent_calories = (
            0.035 * self.weight + (mean_speed ** 2 // self.height) * 0.029 * self.weight
        ) * duration
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action : int , duration : float, weight : float, length_pool : int, count_pool : int):
        super().__init__(action, duration, weight)
        self.len_step = 1.38
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_spead = self.length_pool * self.count_pool / self.m_in_km / self.duration
        return mean_spead
        

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        duration = self.duration * 60
        spent_calories = (mean_speed + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == "SWM":
        instance = Swimming(**data)
    if workout_type == "RUN":
        instance = Running(**data)
    if workout_type == "WLK":
       instance = SportsWalking(**data)
    return instance


def main(training: Training, instance) -> None:
    """Главная функция."""
    info = instance.show_trainig_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

