#include <Arduino.h>

const int buttonTop    = 9;
const int buttonCenter = 10;
const int buttonBottom = 11;

int number = 1;

// 関数プロトタイプ
void sendNumber(int num);
void displayNumber(int num);

// 7セグメント表示のパターン
int pattern[10][7] = {
  {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, LOW},  // 0
  {LOW, HIGH, HIGH, LOW, LOW, LOW, LOW},      // 1
  {HIGH, HIGH, LOW, HIGH, HIGH, LOW, HIGH},   // 2
  {HIGH, HIGH, HIGH, HIGH, LOW, LOW, HIGH},   // 3
  {LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH},    // 4
  {HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH},   // 5
  {HIGH, LOW, HIGH, HIGH, HIGH, HIGH, HIGH},  // 6
  {HIGH, HIGH, HIGH, LOW, LOW, LOW, LOW},     // 7
  {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH}, // 8
  {HIGH, HIGH, HIGH, HIGH, LOW, HIGH, HIGH}   // 9
};

// 7セグメントのピン番号
int pinNo[7] = {2, 3, 4, 5, 6, 7, 8};

// 数字を7セグメントに表示する関数
void display(int n) {
  for (int i = 0; i < 7; i++) {
    digitalWrite(pinNo[i], pattern[n == 10 ? 0 : n][i]);
  }
}

void setup() {
  // 7セグメント用ピンの設定
  for (int i = 0; i < 7; i++) {
    pinMode(pinNo[i], OUTPUT);
  }

  // ボタン用ピンの設定
  pinMode(buttonTop, INPUT_PULLUP);
  pinMode(buttonCenter, INPUT_PULLUP);
  pinMode(buttonBottom, INPUT_PULLUP);

  Serial.begin(9600);  // シリアル通信の開始
  display(number);     // 初期表示
}

void loop() {
  if (digitalRead(buttonTop) == LOW) {
    number--;
    if (number < 1) number = 10;
    display(number);
    delay(300);  // チャタリング防止
  }

  if (digitalRead(buttonBottom) == LOW) {
    number++;
    if (number > 10) number = 1;
    display(number);
    delay(300);  // チャタリング防止
  }

  if (digitalRead(buttonCenter) == LOW) {
    sendNumber(number);  // シリアル送信
    delay(300);  // チャタリング防止
  }
}

// シリアルで数値をPCに送信
void sendNumber(int num) {
  //Serial.print("Selected Number: ");
  Serial.println(num == 10 ? 0 : num);
}
