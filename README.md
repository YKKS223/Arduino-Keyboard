# Arduino-Keyboard
前提条件：Arduinoと回路がある。
サンプルでブレッドボードの配線イメージがあるので参考にどうぞ：
https://github.com/YKKS223/Arduino-Keyboard/blob/main/2025-01-14%204.04.35.png

使い方：
  必要なもの：

    VScode

    PlatformIO(VScodeに入れる)

  ダウンロードしたarduino_2024_ritsumeiをplatformIOで開く
  
  USBを指すポートを調べて書き換える：
  
    VScodeのターミナルで( ls /dev/tty.* ) を実行するとポートが出てきます

  必要なものをダウンロード：
  
    VScodeのターミナルで( pip3 install pyserial pynput pyautogui simpleaudio )　を実行

  あとはpythonを実行するだけ。

  
