int x;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
}
void loop() {
  if(Serial.available()){
    x = Serial.readString().toInt();
    if(x==1){
      Serial.print("Mover a la izquierda 100%");
    }
    else if(x==2){
      Serial.print("Mover a la izquierda 60%");
    }
    else if(x==3){
      Serial.print("Mover a la izquierda 30%");
    }
    else if(x==4){
      Serial.print("Centro");
    }
    else if(x==5){
      Serial.print("Mover a la derecha 30%");
    }
    else if(x==6){
      Serial.print("Mover a la derecha 60%");
    }
    else if(x==7){
      Serial.print("Mover a la derecha 100%");
    }
 }
}