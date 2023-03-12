from dataclasses import dataclass

@dataclass(slots=True)
class Budget:
    """
    amount - сумма
    category - id категории расходов
    time - промежуток времени в днях
    pk - id записи в базе данных
    """
    amount: int
    category: int
    time: int
    limit: int = 0
    pk: int = 0