from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: int
    MESSAGE: str = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def show_training_info(self) -> None:
        pass

    def get_message(self) -> str:
        return (self.MESSAGE.format(*asdict(self).values()))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = Training.get_distance(self) / self.duration
        return speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Переопроедлите метод get_spent_calories в {type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        massage: InfoMessage = InfoMessage(type(self).__name__,
                                           self.duration,
                                           self.get_distance(),
                                           self.get_mean_speed(),
                                           self.get_spent_calories()
                                           )
        return massage


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * Training.get_mean_speed(self)
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM
                           * (self.duration * self.H_IN_MIN))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KMH_IN_MS: float = 0.278
    CM_IN_M = 100
    CONST_SWALK1: float = 0.035
    CONST_SWALK2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories: float = ((self.CONST_SWALK1 * self.weight
                            + ((Training.get_mean_speed(self)
                                * self.KMH_IN_MS)**2 / (self.height
                                                        / self.CM_IN_M))
                            * self.CONST_SWALK2 * self.weight)
                           * (self.duration * self.H_IN_MIN))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    CONST_MMEDIUM_SPEED: float = 1.1
    CONST_SPEED: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.CONST_MMEDIUM_SPEED)
                           * self.CONST_SPEED * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict() = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        training_class: Training = training_type[workout_type](*data)
        return training_class
    except KeyError:
        raise ValueError('Неверный ввод')


def main(training: Training) -> None:
    """Главная функция."""
    into: InfoMessage = training.show_training_info()
    print(into.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
