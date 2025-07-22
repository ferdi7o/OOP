from abc import ABC, abstractmethod


class Playable(ABC):
    @abstractmethod
    def play(self):
        pass

class Downloadtable(ABC):
    @abstractmethod
    def download(self):
        pass

class Sharetable(ABC):
    @abstractmethod
    def share(self):
        pass

class Phone(Playable, Downloadtable, Sharetable):
    def play(self):
        print("Phone play Musik")

    def download(self):
        print("Phone download Musik")

    def share(self):
        print("Phone share Musik")

class Mp3Player(Playable, Downloadtable):
    def play(self):
        print("Mp3Player play Musik")

    def download(self):
        print("Mp3Player download Musik")

class SmartSpeaker(Playable):
    def play(self):
        print("SmartSpeaker play Musik")

handy = Phone()
mp3player = Mp3Player()
speaker = SmartSpeaker()

print("📱 Phone:")
handy.play()
handy.download()
handy.share()

print("\n🎵 MP3 Player:")
mp3player.play()
mp3player.download()

print("\n🔊 Smart Speaker:")
speaker.play()