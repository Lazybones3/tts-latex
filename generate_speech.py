from TTS.api import TTS


with open('output.txt','r',encoding = 'utf-8') as f:
  text = f.read()

tts = TTS(model_path="./tts_models--en--ljspeech--tacotron2-DDC/model_file.pth", config_path="./tts_models--en--ljspeech--tacotron2-DDC/config.json")
tts.tts_to_file(text=text, file_path="output.wav")
