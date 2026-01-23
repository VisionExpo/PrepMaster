import whisper
from backend.config.setting import DEVICE

def load_whisper():
    # 'fp16=True' for 2x GPU speed. fp16 = Half Precision
    model = whisper.load_model("base", device=DEVICE)
    return model