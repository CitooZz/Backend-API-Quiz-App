from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

User = get_user_model()


class Quiz(models.Model):
    creator = models.ForeignKey(User, related_name='quiz', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    We save question answer choices to "options" field as

    [{"option": "answer choice", "is_correct_answer": true/false}]

    """

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    options = JSONField(help_text="option list for question answer")

    def __str__(self):
        return self.title


class Entry(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='entries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)


class Answer(models.Model):
    """
    Question answer will save to "answer" field, value will be one of the question options

    """
    entry = models.ForeignKey(Entry, related_name='entry_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
