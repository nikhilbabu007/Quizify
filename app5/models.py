from django.db import models

# Create your models here.
class user(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phno=models.IntegerField()
    password=models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class ScienceQuestion(models.Model):
    version = models.PositiveIntegerField(default=1)
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    marks = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):

        if self.difficulty == "Easy":
            self.marks = 1
        elif self.difficulty == "Medium":
            self.marks = 2
        else:
            self.marks = 3

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

from django.db import models


class MathematicsQuestion(models.Model):
    version = models.PositiveIntegerField(default=1)
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    marks = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):

        if self.difficulty == "Easy":
            self.marks = 1
        elif self.difficulty == "Medium":
            self.marks = 2
        else:
            self.marks = 3

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


from django.db import models


class GeneralKnowledgeQuestion(models.Model):
    version = models.PositiveIntegerField(default=1)
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    marks = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):

        if self.difficulty == "Easy":
            self.marks = 1
        elif self.difficulty == "Medium":
            self.marks = 2
        else:
            self.marks = 3

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

from django.db import models


class ComputerScienceQuestion(models.Model):
    version = models.PositiveIntegerField(default=1)
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    marks = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):

        if self.difficulty == "Easy":
            self.marks = 1
        elif self.difficulty == "Medium":
            self.marks = 2
        else:
            self.marks = 3

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

from django.db import models


class HistoryQuestion(models.Model):
    version = models.PositiveIntegerField(default=1)
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ]
    )

    marks = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):

        if self.difficulty == "Easy":
            self.marks = 1
        elif self.difficulty == "Medium":
            self.marks = 2
        else:
            self.marks = 3

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

class QuizResult(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)

    category = models.CharField(max_length=50)

    score = models.IntegerField()

    total_marks = models.IntegerField(default=30)

    attempted = models.IntegerField()

    correct = models.IntegerField()

    wrong = models.IntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.score}"

class QuizSettings(models.Model):

    CATEGORY_CHOICES = [

        ("Science","Science"),
        ("Mathematics","Mathematics"),
        ("General Knowledge","General Knowledge"),
        ("Computer Science","Computer Science"),
        ("History","History"),

    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True
    )

    active_version = models.PositiveIntegerField(default=1)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - Version {self.active_version}"



class QuizAttempt(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)

    category = models.CharField(max_length=50)

    version = models.PositiveIntegerField(default=1)

    score = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField(default=30)

    attempted_questions = models.PositiveIntegerField()

    correct_answers = models.PositiveIntegerField()

    wrong_answers = models.PositiveIntegerField()

    percentage = models.FloatField()

    completed_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE
    )

    question_id = models.IntegerField()
    question = models.TextField(default="")

    option_a = models.TextField(default="")
    option_b = models.TextField(default="")
    option_c = models.TextField(default="")
    option_d = models.TextField(default="")









    selected_answer = models.CharField(
        max_length=1,
        blank=True
    )

    correct_answer = models.CharField(max_length=1)

    marks_awarded = models.IntegerField()

    is_correct = models.BooleanField()

    def get_selected_text(self):

        if self.selected_answer == "A":
            return self.option_a

        elif self.selected_answer == "B":
            return self.option_b

        elif self.selected_answer == "C":
            return self.option_c

        elif self.selected_answer == "D":
            return self.option_d

        return "Not Attempted"

    def get_correct_text(self):

        if self.correct_answer == "A":
            return self.option_a

        elif self.correct_answer == "B":
            return self.option_b

        elif self.correct_answer == "C":
            return self.option_c

        elif self.correct_answer == "D":
            return self.option_d

        return ""