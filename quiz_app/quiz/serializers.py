from rest_framework import serializers

from quiz.models import Quiz, Question, Entry, Answer


class OptionSerializerField(serializers.JSONField):

    def to_representation(self, values):
        for value in values:
            value.pop('is_correct_answer')

        return values


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializerField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'options')

    def get_options(self, instance):
        transform_options = list()
        for option in instance.options:
            option.pop("is_correct_answer")
            transform_options.append(option)

        return transform_options


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'creator', 'start_at', 'end_at', 'created_at', 'questions')
        read_only_fields = ('creator', )

    def create(self, validated_data):
        creator = self.context["user"]
        questions = validated_data.pop('questions')
        quiz = Quiz.objects.create(creator=creator, **validated_data)
        for question in questions:
            Question.objects.create(quiz=quiz, **question)

        return quiz


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'created_at')


class EntrySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='entry_answers')

    class Meta:
        model = Entry
        fields = ('id', 'quiz', 'user', 'created_at', 'answers')

    def create(self, validated_data):
        entry = Entry.objects.create(quiz=validated_data.get('quiz'), user=validated_data.get('user'))
        answers = validated_data.pop('entry_answers')
        for answer in answers:
            Answer.objects.create(entry=entry, question=answer['question'], answer=answer['answer'])

        return entry
