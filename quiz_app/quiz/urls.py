from rest_framework.routers import DefaultRouter

from quiz.api import QuizViewSet

router = DefaultRouter()
router.register('', QuizViewSet)

urlpatterns = router.urls
