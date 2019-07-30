from designpattern import songs
from designpattern import serializers

song = songs.Song('1', 'water of love', 'dire straits')
serializer = serializers.ObjectSerializer()
print(serializer.serialize(song, 'JSON'))