
#define EN_PIN     8  //  LOW: Silnik włączony. HIGH: Silnik wyłączony
#define STEPx_PIN  2  //  Pin sterujący krokiem dla osi x
#define DIRx_PIN   5  //  Pin sterujący kierunkiem ruchu dla osi x
#define STEPz_PIN  4  //  Pin sterujący krokiem dla osi y
#define DIRz_PIN   7  //  Pin sterujący kierunkiem ruchu dla osi y


#include<Servo.h>                                  // Biblioteka służąca do obsługi serwomechanizmów
#include <TMC2208Stepper.h>                        // Biblioteka służąca do obsługi sterowników silników krokowych TMC2208
TMC2208Stepper driver = TMC2208Stepper(&Serial);   // Utworzenie obiektu o nazwie 'driver' typu TMC2208Stepper i przypisanie mu portu szeregowego jako argumentu konstruktora
  
Servo x, y;  // Obiekty klasy Servo dla osi x i y
int width = 640, height = 480;  // Szerokość i wysokość okna wyświetlającego obraz
void setup() {
  Serial.begin(9600); // Inicjalizacja portu szeregowego z predefiniowaną szybkością 9600 baudów 
  Serial.println("Start..."); // Wysłanie ciągu tekstowego "Start..." do portu szeregowego
  driver.push();  // Przesłanie danych z bufora do sterownika silnika krokowego
 // Ustawienie pinów jako wyjścia
  pinMode(EN_PIN, OUTPUT);
  pinMode(STEPx_PIN, OUTPUT);
  pinMode(DIRx_PIN, OUTPUT);   
  pinMode(STEPz_PIN, OUTPUT);
  pinMode(DIRz_PIN, OUTPUT);
  // Ustawienie stanów logicznych pinów jako wysokie
    digitalWrite(EN_PIN, HIGH);
  digitalWrite(DIRx_PIN, HIGH);
  digitalWrite(DIRz_PIN, HIGH);


  driver.pdn_disable(true);     // Wyłączenie używania pinu PDN/UART do komunikacji za pomocą metody pdn_disable()
  driver.I_scale_analog(false); // Użycie wewnętrznego napięcia referencyjnego za pomocą metody I_scale_analog()
  driver.rms_current(700);      // Ustawienie prądu sterującego na 500mA za pomocą metody rms_current(
  driver.toff(2);               // Włączenie sterownika w oprogramowaniu za pomocą metody toff()

  uint32_t data = 0;               // Zmienna przechowująca dane
  Serial.print("DRV_STATUS = 0x"); // Wysłanie ciągu tekstowego "DRV_STATUS = 0x" do portu szeregowego
  driver.DRV_STATUS(&data);        // Pobranie stanu sterownika za pomocą metody DRV_STATUS() i przekazanie wyniku do zmiennej data
  Serial.println(data, HEX);       // Wysłanie zmiennej data w formacie szesnastkowym do portu szeregowego
}
void loop() {
 
  if (Serial.available() > 0) //Jeśli dostępne są dane do odczytu z portu szeregowego, wykonaj kod wewnątrz bloku i
  {
    int x_mid, y_mid;         // Zadeklaruj zmienne do przechowywania współrzędnych x i y
    if (Serial.read() == 'X') // Jeśli pierwszy bajt danych to 'X'
    {
      x_mid = Serial.parseInt();   // Odczytaj i zapisz następny bajt jako współrzędną x
      if (Serial.read() == 'Y')    // Jeśli następny bajt danych to 'Y'
        y_mid = Serial.parseInt(); // Odczytaj i zapisz następny bajt jako współrzędną y
    }
   
    // Jeśli x_mid jest większe niż połowa szerokości kadru + 30, obróć silnik X w lewo
    if (x_mid > width / 2 + 30) {
     digitalWrite(EN_PIN, LOW);                        // Włącz silnik
     digitalWrite(DIRz_PIN, LOW);                      // Ustaw kierunek obrotu silnika na lewo
     digitalWrite(STEPz_PIN, !digitalRead(STEPz_PIN)); // Obróć silnik o jeden krok
     delayMicroseconds(20);                             // Zatrzymaj się na chwilę
    }
     // Jeśli x_mid jest mniejsze niż połowa szerokości kadru - 30, obróć silnik X w prawo
    if (x_mid < width / 2 - 30) {
      digitalWrite(EN_PIN, LOW);                       // Włącz silnik
     digitalWrite(DIRz_PIN, HIGH);                     // Ustaw kierunek obrotu silnika na prawo
     digitalWrite(STEPz_PIN, !digitalRead(STEPz_PIN)); // Obróć silnik o jeden krok
     delayMicroseconds(20);                             // Zatrzymaj się na chwilę
    }
    // Jeśli y_mid jest mniejsze niż połowa wysokości kadru + 30, obróć silnik y w lewo
    if (y_mid > height / 2 - 30) {
      digitalWrite(EN_PIN, LOW);                       // Włącz silnik
     digitalWrite(DIRx_PIN, LOW);                      // Ustaw kierunek obrotu silnika na lewo
     digitalWrite(STEPx_PIN, !digitalRead(STEPx_PIN)); // Obróć silnik o jeden krok
     delayMicroseconds(20);                             // Zatrzymaj się na chwilę
    }
    // Jeśli y_mid jest większe niż połowa wysokości kadru + 30, obróć silnik y w prawo
    if (y_mid < height / 2 + 30) {
     digitalWrite(EN_PIN, LOW);                        // Włącz silnik
     digitalWrite(DIRx_PIN, HIGH);                     // Ustaw kierunek obrotu silnika na prawo
     digitalWrite(STEPx_PIN, !digitalRead(STEPx_PIN)); // Obróć silnik o jeden krok
     delayMicroseconds(20);                             // Zatrzymaj się na chwilę
    }
  }
}
