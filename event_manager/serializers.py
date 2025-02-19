from rest_framework import serializers
from event_manager.models import Event
from user.models import User
from user.serializers import UserSerializer, UserListSerializer


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username",)



class EventSerializer(serializers.ModelSerializer):
    organizer = UserListSerializer()
    members = MemberSerializer(many=True)
    class Meta:
        model = Event
        fields = ('id', 'title' , 'description' , 'date' ,'location' ,"organizer" ,'members', )



class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'location', 'members',)




class EventHandlersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',)

