from rest_framework import serializers
from event_manager.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title' , 'description' , 'date' ,'location' ,"organizer" ,'members' )



class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'location', 'members')




class EventHandlersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'members' )

