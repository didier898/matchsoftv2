from django.core.management.base import BaseCommand
from core.models import Question, Choice
import random

DATA_OK = [
    # Nivel básico
    (1,  "Resuelve: x + 3 = 8",                        "5",   ["6","4","8"],                 "x = 8 - 3 = 5"),
    (2,  "Resuelve: x - 7 = 2",                        "9",   ["5","8","7"],                 "x = 2 + 7 = 9"),
    (3,  "Resuelve: 3x = 15",                          "5",   ["3","4","6"],                 "x = 15 ÷ 3 = 5"),
    (4,  "Resuelve: 4x = 24",                          "6",   ["4","5","8"],                 "x = 24 ÷ 4 = 6"),
    (5,  "Resuelve: 2x + 4 = 10",                      "3",   ["2","4","6"],                 "2x = 10 - 4 = 6 → x = 3"),

    # Nivel intermedio
    (6,  "Resuelve: 5x - 10 = 20",                     "6",   ["4","5","8"],                 "5x = 30 → x = 6"),
    (7,  "Resuelve: 7x + 14 = 35",                     "3",   ["4","2","5"],                 "7x = 21 → x = 3"),
    (8,  "Resuelve: 8x - 16 = 48",                     "8",   ["6","9","7"],                 "8x = 64 → x = 8"),
    (9,  "Resuelve: 9x + 9 = 54",                      "5",   ["4","6","7"],                 "9x = 45 → x = 5"),
    (10, "Resuelve: 6x - 12 = 6",                      "3",   ["2","4","6"],                 "6x = 18 → x = 3"),

    # Nivel con términos en ambos lados
    (11, "Resuelve: 7x + 5 = 2x + 30",                 "5",   ["4","6","7"],                 "7x - 2x = 30 - 5 → 5x = 25 → x = 5"),
    (12, "Resuelve: 9x - 12 = 3x + 18",                "5",   ["4","6","7"],                 "9x - 3x = 18 + 12 → 6x = 30 → x = 5"),
    (13, "Resuelve: 4x + 8 = 2x + 20",                 "6",   ["5","7","4"],                 "4x - 2x = 20 - 8 → 2x = 12 → x = 6"),
    (14, "Resuelve: 5x + 15 = 2x + 24",                "3",   ["4","5","6"],                 "5x - 2x = 24 - 15 → 3x = 9 → x = 3"),
    (15, "Resuelve: 6x + 8 = 2x + 24",                 "4",   ["3","5","6"],                 "6x - 2x = 24 - 8 → 4x = 16 → x = 4"),

    # Nivel avanzado (paréntesis, x en ambos lados)
    (16, "Resuelve: 3(x + 2) = 2x + 12",               "6",   ["4","5","7"],                 "3x + 6 = 2x + 12 → x = 6"),
    (17, "Resuelve: 2(3x - 5) = 4x + 6",               "8",   ["6","7","9"],                 "6x - 10 = 4x + 6 → 2x = 16 → x = 8"),
    (18, "Resuelve: 2x + 33 - 2 = 33x - 27 - 2x",      "2",   ["1","3","4"],                 "2x + 31 = 33x - 27 - 2x → 4x = 8 → x = 2"),

    # Nivel problema contextual
    (19, "La edad del padre es 3 veces la edad del hijo. Si ambas edades suman 60 años, ¿cuántos años tiene el hijo?", 
          "15", ["10","12","18"], 
          "Sea x la edad del hijo. Entonces 3x es la del padre.\n3x + x = 60 → 4x = 60 → x = 15.\nEl hijo tiene 15 años."),

    (20, "Un número más su doble es igual a 36. ¿Cuál es ese número?", 
          "12", ["10","14","16"], 
          "Sea x el número.\n x + 2x = 36 → 3x = 36 → x = 12."),
]


class Command(BaseCommand):
    help = "Carga 20 preguntas de ecuaciones lineales (1 incógnita) en 'core'"

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        created = 0
        for diff, text, correct, wrongs, expl in DATA_OK:
            q = Question.objects.create(text=text, difficulty=diff, explanation=expl)
            options = [correct] + wrongs
            random.shuffle(options)
            labels = ['A','B','C','D']
            for i, opt in enumerate(options[:4]):
                Choice.objects.create(
                    question=q,
                    label=labels[i],
                    text=str(opt),
                    is_correct=(opt == correct)
                )
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Preguntas creadas: {created}'))
