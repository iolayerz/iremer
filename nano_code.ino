char c;

void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
}

void loop() {
  if(Serial.available())
  {
    c = Serial.read();
    
    if(c == 's')
    {
      Serial.println("Arduino:Stop");
    }

    if(c == 'f')
    {
      Serial.println("Arduino:Forward");
    }

    if(c == 'b')
    {
      Serial.println("Arduino:Backward");
    }

    if(c == 'r')
    {
      Serial.println("Arduino:Right");
    }

    if(c == 'l')
    {
      Serial.println("Arduino:Left");
    }
  }
  
  delay(500);
  
}
