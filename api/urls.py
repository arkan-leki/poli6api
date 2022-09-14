from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Max, Sum

from api.models import Account, Answare, Question, Quize, Result

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# Serializers define the API representation.


class AccSerializer(serializers.ModelSerializer):
    highscore = serializers.ReadOnlyField()
    scores = serializers.ReadOnlyField()
    scorer  = serializers.ReadOnlyField()
    class Meta:
        model = Account
        fields = ['id', 'username', 'email',
                  'is_staff', 'phoneid', 'highscore','scores','scorer']

class ResultSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Result
        fields = '__all__'

class ResultXSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    highscore = serializers.ReadOnlyField(source='user.highscore')
    class Meta:
        model = Result
        fields = '__all__'

class QuizeSerializer(serializers.ModelSerializer):
    # top_scores = serializers.ReadOnlyField()
    top_scores = ResultXSerializer(read_only=True, many=True)

    class Meta:
        model = Quize
        fields = '__all__'


class AnswareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answare
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    a_question = AnswareSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['text', 'quize', 'a_question']


# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phoneid']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quize']


class QuizeViewSet(viewsets.ModelViewSet):
    queryset = Quize.objects.all()
    serializer_class = QuizeSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


 
# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccViewSet)
router.register(r'quizes', QuizeViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'result', ResultViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
