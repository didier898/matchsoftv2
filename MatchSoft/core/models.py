from django.db import models

class Question(models.Model):
    DIFFICULTY_CHOICES = [(i, f'Nivel {i}') for i in range(1, 21)]
    text = models.TextField()
    explanation = models.TextField(blank=True)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=1)

    def __str__(self):
        return f'Pregunta {self.id} (Nivel {self.difficulty})'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    label = models.CharField(max_length=1, choices=[(c, c) for c in 'ABCD'])
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'label')

    def __str__(self):
        return f'{self.question_id}-{self.label}'
