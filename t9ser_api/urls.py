from django.urls import path
from .views import SportList,MatchList, MatchDetail, UserMatchList, UserMatchDetail,MatchParticipants,LoginView,UserCreate,ApproveParticipant,UserProfileView,MyMatchView,WithdrawFromMatch# Import other views as needed

urlpatterns = [
    path('sports/', SportList.as_view(), name='sport-list'),
    path('matches/', MatchList.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetail.as_view(), name='match-detail'),
    path('usermatches/', UserMatchList.as_view(), name='usermatch-list'),
    path('usermatches/<int:pk>/', UserMatchDetail.as_view(), name='usermatch-detail'),
    path('matches/<int:pk>/participants/', MatchParticipants.as_view(), name='match-participants'),
    path('login/', LoginView.as_view()),
    path('register/', UserCreate.as_view(), name='user-create'),
    path('usermatches/approve/<int:pk>/', ApproveParticipant.as_view(), name='approve-participant'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('my-matches/', MyMatchView.as_view(), name='my-matches'),
    path('usermatches/withdraw/<int:pk>/', WithdrawFromMatch.as_view(), name='withdraw-match'),
]
