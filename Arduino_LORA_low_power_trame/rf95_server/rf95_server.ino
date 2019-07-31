// rf95_client.pde
// -*- mode: C++ -*-

#include <SPI.h>
#include <RH_RF95.h>
#include <string.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
uint8_t inputString[RH_RF95_MAX_MESSAGE_LEN]={0};

void setup() 
{
  
  Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  Serial.println("Setup");
  
  if (!rf95.init())
    Serial.println("init failed");
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setFrequency(868);
  //rf95.setTxPower(23, false); // ne marche pas bien avec arduino nano et raspberry (fonctionne avec windows et aussi arduino mini/uno avec raspberry)
}

void loop()
{
  if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len))
    {      
      Serial.println((char*)buf);
    }
    else
    {
      Serial.println("recv failed");
    }
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() 
{
  static int i= 0 ;
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString[i++] = inChar;

    // if the incoming character is a newline ('\n') => send inputString by RF95    
    if (inChar == '\n') {
      
      rf95.send(inputString, sizeof(inputString));
      rf95.waitPacketSent();
    
      /*Serial.print("envoie : " );
      Serial.println((char *)inputString);*/
      // RAZ du tableau
      memset(inputString, '\0', strlen(inputString) - 1); 
      i=0;
    }      
  }
}
