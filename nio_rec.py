import firebase, urllib
import librosa, io

# firebase config
config = {
  'apiKey': "AIzaSyAAbWrX6aXoW5ykkFDEPDLl5BnqqMbBdKk",
  'authDomain': "nio-application.firebaseapp.com",
   "databaseURL": "gs://nio-application.appspot.com",
  'projectId': "nio-application",
  'storageBucket': "nio-application.appspot.com",
  'messagingSenderId': "738476225376",
  'appId': "1:738476225376:web:0e840888904b7891f4a405",
  'measurementId': "G-0PWN8WQ4CT"
}

config = firebase.initialize_app(config)
storage = config.storage()

# file config
raw_file = "2346bf197e72-d427-11ed-ada9-00155d86a7eb3429.wav"
cloud_path = 'recorded_audio/' + raw_file

# store file
# storage.child(cloud_path).put(raw_file)

# read file
audio_file = raw_file
# need a validation for this file url if exist
url = storage.child(cloud_path).get_url(None)
f = urllib.request.urlopen(url).read
response = urllib.request.urlopen(url)

# url for the firebase
print(url)
# actual file
print(f)
print()
print()

audio = io.BytesIO(response.read())



# transcription
# from project.scripts.transcribe import to_text
# trans = to_text(audio, use_temp_folder=False, use_cloud_storage=True)
# print(trans)

# emotion
# from project.scripts.emotion import emotion_detector, emotion_label

# predictions = emotion_detector.predict(raw_file, use_temp_folder=False, use_cloud_storage=True)
# score = emotion_label(predictions)

# print("emotion:",score['emotion1'], "| score: ", score['score1'])
# print("emotion:",score['emotion2'], "| score: ", score['score2'])
# print("emotion:",score['emotion3'], "| score: ", score['score3'])

# rate
# from project.scripts.rate import rate_score

# text = """
# Get the shaft like a steering column (Monster) Trigger happy, pack heat, but it's black ink Evil half of the Bad Meets Evil, that means take a back seat Take it back to Fat Beats with a maxi single Look at my rap sheet, what attracts these people Is my 'Gangsta Bitch' like Apache with a catchy jingle I stack chips, you barely got a half-eaten Cheeto Fill 'em with the venom and eliminate 'em Other words, I Minute Maid 'em I don't wanna hurt 'em, but I did, I'm in a fit of rage I'm murderin' again, nobody will evade I'm finna kill 'em and dump all their fuckin' bodies in the lake Obliterating everything, incinerate a renegade I'm here to make anybody who want it with the pen afraid But don't nobody want it, but they're gonna get it anyway 'Cause I'm beginnin' to feel like I'm mentally ill I'm Attila, kill or be killed, I'm a killer bee, the vanilla gorilla You're bringin' the killer within me outta me You don't wanna be the enemy of the demon who entered me And be on the receivin' end of me, what stupidity it'd be Every bit of me's the epitome of a spitter When I'm in the vicinity, motherfucker, you better duck Or you finna be dead the minute you run into me A hundred percent of you is a fifth of a percent of me I'm 'bout to fuckin' finish you, bitch, I'm unfadable You wanna battle, I'm available, I'm blowin' up like an inflatable I'm undebatable, I'm unavoidable, I'm unevadable I'm on the toilet bowl, I got a trailer full of money and I'm paid in full I'm not afraid to pull a— Man, stop Look what I'm plannin',
# """

# rate = rate_score(audio=audio, text=text, use_temp_folder=False, use_cloud_storage=True)
# print(rate)
# print(rate['score'])