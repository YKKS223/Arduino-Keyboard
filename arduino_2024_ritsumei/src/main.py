import serial
from pynput.keyboard import Controller, Key
import simpleaudio
import time
from datetime import datetime

port = '/dev/tty.usbmodem2101'  # MacOS右側

keyboard = Controller()

# 音声ファイルのロード
wav_am = simpleaudio.WaveObject.from_wave_file("src/am.wav")
wav_pm = simpleaudio.WaveObject.from_wave_file("src/pm.wav")
wav_time = simpleaudio.WaveObject.from_wave_file("src/time.wav")
wav_obj_m = simpleaudio.WaveObject.from_wave_file("src/morning.wav")
wav_obj_h = simpleaudio.WaveObject.from_wave_file("src/hello.wav")
wav_obj_n = simpleaudio.WaveObject.from_wave_file("src/night.wav")
wav_obj = simpleaudio.WaveObject.from_wave_file("src/001_connect.wav")
wav2_obj = simpleaudio.WaveObject.from_wave_file("src/002_disconnect.wav")

number_wavs = [
    simpleaudio.WaveObject.from_wave_file(f"src/declaration_{i}.wav") for i in range(10)
]

numpad_keys = {i: str(i) for i in range(10)}

# 時間帯に応じた音声を選択する関数
def get_connection_sound():
    current_hour = datetime.now().hour
    if 5 <= current_hour <= 10:
        return wav_obj_m
    elif 11 <= current_hour <= 18:
        return wav_obj_h
    else:
        return wav_obj_n

# 現在の時刻に基づく音声オブジェクトを返す関数
def play_time_announcement():
    now = datetime.now()
    hour = now.hour
    am_pm_sound = wav_am if hour < 12 else wav_pm
    hour_12_format = hour % 12 or 12  # 12時間形式
    hour_sound = number_wavs[hour_12_format]
    return hour_sound, am_pm_sound

try:
    ser = serial.Serial(port, 9600, timeout=1)
    print(f"Connected to {port}")

    # 接続時の音声再生
    connection_sound = get_connection_sound()
    hour_sound, am_pm_sound = play_time_announcement()

    wav_obj.play()
    time.sleep(2)
    connection_sound.play()
    time.sleep(1)
    am_pm_sound.play()
    time.sleep(2)
    hour_sound.play()
    time.sleep(0.8)
    wav_time.play()
    time.sleep(1)

    # メインループ
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Received: {line}")
                    if line.isdigit():
                        number = int(line)
                        if number in numpad_keys:
                            keyboard.press(numpad_keys[number])
                            number_wavs[number].play()
                            time.sleep(0.5)
                            keyboard.release(numpad_keys[number])
                    elif "Enter" in line:
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
        except Exception as e:
            print(f"Error during communication: {e}")
            wav2_obj.play()
            time.sleep(2)
            break
except serial.SerialException as e:
    print(f"Failed to open port: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
