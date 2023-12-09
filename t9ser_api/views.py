from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Sport, Match, UserMatch
from .serializers import SportSerializer, MatchSerializer, UserMatchSerializer,LoginSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
class SportList(APIView):
    """
    List all sports, or create a new sport.
    """
    def get(self, request, format=None):
        sports = Sport.objects.all()
        serializer = SportSerializer(sports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_BAD_REQUEST)

class PendingApprovalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # Fetch all matches where the current user is the host
        hosted_matches = Match.objects.filter(host_user=request.user)
        # Fetch all user match relations that are pending approval for these matches
        pending_approvals = UserMatch.objects.filter(
            match__in=hosted_matches,
            is_approved=False  # Assuming there is an 'is_approved' field in UserMatch model
        )
        serializer = UserMatchSerializer(pending_approvals, many=True)
        return Response(serializer.data)
class MatchList(APIView):
    """
    List all matches, or create a new match.
    """
    def get(self, request, format=None):
        matches = Match.objects.all()
        sport_id = request.query_params.get('sport')
        if sport_id:
            matches = matches.filter(sport_id=sport_id)

        location = request.query_params.get('location')
        if location:
            matches = matches.filter(location__icontains=location)
        price = request.query_params.get('price')
        
        if price:
            matches = matches.filter(price__lte=price)

        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.save(status='ongoing')
            UserMatch.objects.create(user=match.host_user, match=match)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchDetail(APIView):
    """
    Retrieve, update or delete a match instance.
    """
    def get_object(self, pk):
        try:
            return Match.objects.get(pk=pk)
        except Match.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        match = self.get_object(pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        match = self.get_object(pk)
        serializer = MatchSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        match = self.get_object(pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMatchList(APIView):
    """
    List all user matches, or create a new user match.
    """
    def get(self, request, format=None):
        usermatches = UserMatch.objects.all()
        serializer = UserMatchSerializer(usermatches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        match_id = request.data.get('match')
        user_id = request.data.get('user')

        if not user_id or not match_id:
            return Response({'error': 'User and Match IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already a participant
        if UserMatch.objects.filter(user_id=user_id, match_id=match_id).exists():
            return Response({'error': 'This user is already a participant in the match'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the match exists and the number of participants
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

        if UserMatch.objects.filter(match=match).count() >= match.players_needed:
            return Response({'error': 'This match already has the required number of players'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the UserMatch instance
        serializer = UserMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Request to join the match has been sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserMatchDetail(APIView):
    """
    Retrieve, update or delete a user match instance.
    """
    def get_object(self, pk):
        try:
            return UserMatch.objects.get(pk=pk)
        except UserMatch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        usermatch = self.get_object(pk)
        serializer = UserMatchSerializer(usermatch)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        usermatch = self.get_object(pk)
        serializer = UserMatchSerializer(usermatch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        usermatch = self.get_object(pk)
        usermatch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MatchParticipants(APIView):
    """
    View to list all participants of a specific match.
    """
    def get(self, request, pk, format=None):
        match = get_object_or_404(Match, pk=pk)
        user_matches = UserMatch.objects.filter(match=match)
        serializer = UserMatchSerializer(user_matches, many=True)
        return Response(serializer.data)

class UserCreate(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        data = request.data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        if user:
            token = Token.objects.create(user=user)
            json = {'token': token.key}
            return Response(json, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        json = {'token': token.key}
        return Response(json, status=status.HTTP_202_ACCEPTED)

class ApproveParticipant(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        usermatch = get_object_or_404(UserMatch, pk=pk)

        if request.user != usermatch.match.host_user:
            return Response({'error': 'You are not authorized to approve participants'}, status=status.HTTP_403_FORBIDDEN)

        usermatch.is_approved = True
        usermatch.save()
        return Response({'message': 'Participant approved.'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    # Ensures that only authenticated users can access this view
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # As the user is authenticated, request.user will be the User instance
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return Response(data)

class MyMatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request, format=None):
        user = request.user
        user_matches = UserMatch.objects.filter(user=user)
        matches = [user_match.match for user_match in user_matches]
        serializer = MatchSerializer(matches,many=True)

        return Response(serializer.data)

class WithdrawFromMatch(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        usermatch = get_object_or_404(UserMatch, pk=pk, user=request.user)
        usermatch.delete()
        return Response({'message': 'Successfully withdrawn from the match.'}, status=status.HTTP_204_NO_CONTENT)
