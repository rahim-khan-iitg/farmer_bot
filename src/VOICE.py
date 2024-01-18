from pydub import AudioSegment
from io import BytesIO
import base64

def convert_ogg_bytes_to_wav(ogg_bytes):
    ogg_audio = AudioSegment.from_file(BytesIO(ogg_bytes), format="ogg")
    wav_bytes_io = BytesIO()
    ogg_audio.export(wav_bytes_io, format="wav")
    wav_bytes = wav_bytes_io.getvalue()
    return wav_bytes