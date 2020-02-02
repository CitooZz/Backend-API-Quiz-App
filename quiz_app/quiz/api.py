from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from quiz.models import Quiz
from quiz.serializers import QuizSerializer, EntrySerializer


class QuizViewSet(viewsets.ModelViewSet):
    model = Quiz
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        queryset = super(QuizViewSet, self).get_queryset()
        type = self.request.GET.get('type', 'creator')
        if type == 'creator':
            queryset = queryset.filter(creator=self.request.user)

        else:
            current_time = timezone.localtime(timezone.now())
            queryset = queryset.filter(start_at__lte=current_time,
                                       end_at__gte=current_time).exclude(creator=self.request.user)

        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=True, methods=['POST'])
    def answer_quiz(self, request, pk=None):
        payload = {
            'quiz': self.get_object().id,
            'user': self.request.user.id,
            'answers': self.request.data
        }

        serializer = EntrySerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)

    @action(detail=True, methods=['GET'])
    def results(self, request, pk=None):
        quiz = self.get_object()
        serializer = EntrySerializer(quiz.entries.all(), many=True)
        return Response(serializer.data)
