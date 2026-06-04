import gradio as gr
import torch
import soundfile as sf
import numpy as np
from TTS.api import TTS

# بارگذاری مدل با مدیریت خطا
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔧 Using device: {device}")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
except Exception as e:
    print(f"❌ خطا در بارگذاری مدل: {e}")
    print("لطفاً اتصال اینترنت و نسخه‌ی پایتون (۳.۹-۳.۱۱) را بررسی کنید.")
    exit(1)

def recite_quran(verse, voice_file):
    """تولید تلاوت قرآن با کلونینگ صدا"""
    if voice_file is None:
        return "❌ لطفاً فایل صدای مرجع را بارگذاری کنید.", None
    if not verse or not verse.strip():
        return "❌ لطفاً متن آیه را وارد کنید.", None

    try:
        # خواندن فایل صوتی
        data, sr = sf.read(voice_file, dtype="float32")
        # تبدیل به mono (مدل XTTS بهتر با mono کار می‌کند)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # تولید تلاوت
        wav = tts.tts(text=verse.strip(), speaker_wav=data, language="ar")

        out_path = "recited.wav"
        sf.write(out_path, wav, tts.synthesizer.output_sample_rate)
        return "✅ تلاوت با موفقیت تولید شد.", out_path
    except Exception as e:
        return f"❌ خطا: {str(e)}", None

# رابط کاربری Gradio
iface = gr.Interface(
    fn=recite_quran,
    inputs=[
        gr.Textbox(
            label="📖 متن آیه (با اعراب کامل)",
            placeholder="بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
            lines=2,
        ),
        gr.Audio(label="🎤 صدای مرجع (WAV/MP3)", type="filepath")
    ],
    outputs=[
        gr.Textbox(label="وضعیت"),
        gr.Audio(label="تلاوت تولید شده", type="filepath")
    ],
    title="🕌 تلاوت قرآن با شبیه‌سازی صدا",
    description="متن آیه را با اعراب کامل وارد کنید و یک نمونه صدای ۶ تا ۳۰ ثانیه‌ای از قاری مورد نظر بارگذاری نمایید.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
