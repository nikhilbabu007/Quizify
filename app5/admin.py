from django.contrib import admin
from.models import *
admin.site.register(user)
admin.site.register(ScienceQuestion)
admin.site.register(MathematicsQuestion)
admin.site.register(GeneralKnowledgeQuestion)
admin.site.register(ComputerScienceQuestion)
admin.site.register(HistoryQuestion)
admin.site.register(QuizResult)
admin.site.register(QuizSettings)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)

