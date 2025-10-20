from django.core.management.base import BaseCommand
from core.models import Question, Choice
import random

# === SOLO 3 PREGUNTAS CON IMÁGENES ===
DATA_OK = [
    # 1️⃣ Triángulo turístico en la costa Caribe
    (
        1,
        "En el triángulo formado por Cartagena (C), Barranquilla (B) y Santa Marta (S): "
        "CB = 120 km, CS = 230 km y el ángulo ∠BCS en C es 40°. "
        "¿Cuál es la distancia entre Barranquilla y Santa Marta?",
        "158",
        ["150", "160", "155"],
        "Aplicando el teorema del coseno:\n"
        "d² = 230² + 120² − 2(230)(120)cos(40°)\n"
        "d² = 52900 + 14400 − 55200(0.766)\n"
        "d² = 67300 − 42200 = 25100\n"
        "d = √25100 ≈ 158.4 km\n"
        "✅ Distancia aproximada entre Barranquilla y Santa Marta ≈ 158 km.",
        "core/img/p1.png"
    ),
    # 2️⃣ En el eje cafetero
    (
        2,
        "En el triángulo formado por Pereira (P), Manizales (M) y Armenia (A): "
        "PM = 50 km, PA = 40 km y el ángulo ∠MPA en P es 60°. "
        "¿Cuál es la distancia entre Manizales y Armenia?",
        "46",
        ["45", "50", "48"],
        "Usando el teorema del coseno:\n"
        "d² = 50² + 40² − 2(50)(40)cos(60°)\n"
        "d² = 2500 + 1600 − 4000(0.5)\n"
        "d² = 4100 − 2000 = 2100\n"
        "d = √2100 ≈ 45.8 km\n"
        "✅ Distancia aproximada entre Manizales y Armenia ≈ 46 km.",
        "core/img/p2.png"
    ),
    # 3️⃣ Ingeniero topógrafo
    (
        3,
        "Desde un punto A se observan dos edificios. Las distancias son: "
        "A–E1 = 180 m y A–E2 = 210 m, con un ángulo ∠E1ÂE2 = 39.4°. "
        "¿Cuál es la distancia entre los dos edificios?",
        "135",
        ["130", "140", "138"],
        "Aplicando el teorema del coseno:\n"
        "d² = 180² + 210² − 2(180)(210)cos(39.4°)\n"
        "d² = 32400 + 44100 − 75600(0.773)\n"
        "d² = 76500 − 58400 = 18100\n"
        "d = √18100 ≈ 134.6 m\n"
        "✅ Distancia aproximada entre los dos edificios ≈ 135 m.",
        "core/img/p3.png"
    ),
]


class Command(BaseCommand):
    help = "Carga 3 preguntas con imágenes corregidas (respuestas 158, 46, 135)."

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        created = 0
        labels = ['A', 'B', 'C', 'D']

        for diff, text, correct, wrongs, expl, image in DATA_OK:
            q = Question.objects.create(
                text=text,
                difficulty=diff,
                explanation=expl,
                image=image
            )
            options = [correct] + wrongs
            random.shuffle(options)
            for i, opt in enumerate(options[:4]):
                Choice.objects.create(
                    question=q,
                    label=labels[i],
                    text=str(opt),
                    is_correct=(opt == correct)
                )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Preguntas creadas: {created}'))
