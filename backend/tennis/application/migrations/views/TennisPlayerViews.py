from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tennis.application.models import TennisPlayer, TournamentRegistration
from tennis.application.serializer import TennisPlayerSerializer, TennisPlayerIdSerializer, CoachSerializer, \
    TournamentRegistrationSerializer


class TennisPlayerDetail(APIView):

    serializer_class = TennisPlayerSerializer

    def get(self, request):
        obj = TennisPlayer.objects.all()
        #ids_list = list(obj.values_list('id', flat=True))
        serializer = TennisPlayerSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TennisPlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TennisPlayerInfo(APIView):

    serializer_class = TennisPlayerIdSerializer

    def get(self, request, id):
        try:
            obj = TennisPlayer.objects.get(id=id)
            serializer_player = TennisPlayerIdSerializer(obj)
            serializer_coaches = CoachSerializer(obj.coaches.all(), many=True)

            serialized_player_data = serializer_player.data
            serialized_player_data['coaches'] = serializer_coaches.data

            for i in range(len(serialized_player_data['coaches'])):
                del serialized_player_data['coaches'][i]['player']

            serialized_data = serializer_player.data

            for tournament in serialized_data['tournaments']:
                tournament_reg_serializer = TournamentRegistrationSerializer(
                    TournamentRegistration.objects.get(tr_player=id,
                                                       tr_tournament=tournament['id']))
                tournament['tr_registration_date'] = tournament_reg_serializer.data['tr_registration_date']
                tournament['tr_last_year_performance'] = tournament_reg_serializer.data['tr_last_year_performance']
                del tournament['players']

        except TennisPlayer.DoesNotExist:
            msg = {"msg": "NOT FOUND"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized_player_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            obj = TennisPlayer.objects.get(id=id)
        except TennisPlayer.DoesNotExist:
            msg = {"msg": "NOT FOUND"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        serializer = TennisPlayerSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = TennisPlayer.objects.get(id=id)

        except TennisPlayer.DoesNotExist:
            msg = {"msg": "NOT FOUND"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        serializer = TennisPlayerSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = TennisPlayer.objects.get(id=id)

        except TennisPlayer.DoesNotExist:
            msg = {"msg": "NOT FOUND"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({"msg": "DELETED"}, status=status.HTTP_204_NO_CONTENT)

class TennisPlayerCoachListInfo(APIView):
    def post(self, request, id):

        coaches = request.data
        msg = "CREATED"

        for coach_data in coaches:
            coach_data['player'] = id
            print(coach_data)
            serializer = CoachSerializer(data=coach_data)
            if serializer.is_valid():
                serializer.save()
        return Response(msg, status=status.HTTP_201_CREATED)

class PlayersByAvgYearsOfExperienceOfCoaches(APIView):

    def get(self, request):
        avg_yoe = TennisPlayer.objects \
            .annotate(avg_yoe_coach=Avg('coaches__c_years_of_experience'))\
            .order_by('avg_yoe_coach')
        serializer = TennisPlayerSerializer(avg_yoe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)