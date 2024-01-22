from django.db import models

# Create your models here.
class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length = 12)

    def __str__(self) -> str:
        return self.Email

gender_choices = (
    ('m', 'male'),
    ('f', 'female'),
    ('o', 'other'),
)
class UserProfile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    ProfileImage = models.FileField(upload_to='profile_images/', default='avatar.png')
    FullName = models.CharField(max_length=25, null=True, default='')
    Mobile = models.CharField(max_length=10, null=True, default='')
    Gender = models.CharField(choices=gender_choices, max_length=2, default='')
    BirthDate = models.DateField(auto_created=True, default='1990-01-01')
    City = models.CharField(max_length=25, null=True, default='')
    State = models.CharField(max_length=25, null=True, default='')
    Country = models.CharField(max_length=25, null=True, default='')
    Pincode = models.CharField(max_length=25, null=True, default='')

    def __str__(self) -> str:
        return self.FullName.title() if self.FullName else 'Profile Not Updated'

# model for quiz and options

class QuizCategory(models.Model):
    Category = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Quiz Categories'

    def __str__(self) -> str:
        return self.Category

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


difficulty_level_choices = (
    ('1', 'easy'),
    ('2', 'midium'),
    ('3', 'hard')
)



class Quiz(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    Title = models.CharField(max_length=100)
    Duration = models.IntegerField(default=0)
    DifficultyLevel = models.CharField(max_length=25, choices=difficulty_level_choices)
    TotalScore = models.IntegerField()
    

    class Meta:
        verbose_name_plural = 'Quizes'

class QuesAns(models.Model):
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    QuesImage = models.FileField(upload_to='ques_images/', default='avatar.png')

    Question = models.TextField(max_length=2500)
    Options = models.TextField(max_length=255)
    
    IsMultiSelect = models.BooleanField(default=False)

    Answer = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Ques n Answers'

remark_level_choices = (
    ('25', 'poor'),
    ('50', 'average'),
    ('75', 'good'),
    ('100', 'excellent')
)
class QuizPlay(models.Model):
    QuesAns = models.ForeignKey(QuesAns, on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    Score = models.IntegerField()
    # Remark = models.CharField(max_length=10)
    RemarkLevel = models.CharField(max_length=25, choices=remark_level_choices)