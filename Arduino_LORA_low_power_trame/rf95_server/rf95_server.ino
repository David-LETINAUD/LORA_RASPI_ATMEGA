// rf95_client.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messageing client
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf95_server
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with
// the RFM95W, Adafruit Feather M0 with RFM95

#include <SPI.h>
#include <RH_RF95.h>
#include <string.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
uint8_t cpt = 0;
bool sendComplete = true;  // whether the string is complete
uint8_t inputString[RH_RF95_MAX_MESSAGE_LEN]={0};
//RH_RF95 rf95(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W
//RH_RF95 rf95(8, 3); // Adafruit Feather M0 with RFM95 

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

  Serial.begin(9600);
  
  while (!Serial) ; // Wait for serial port to be available
  if (!rf95.init())
    Serial.println("init failed");
  
  Serial.println("Setup");
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setFrequency(868);
  rf95.setTxPower(23, false);
  // If you are using Modtronix inAir4 or inAir9,or any other module which uses the
  // transmitter RFO pins and not the PA_BOOST pins
  // then you can configure the power transmitter power for -1 to 14 dBm and with useRFO true. 
  // Failure to do that will result in extremely low transmit powers.
//  driver.setTxPower(14, true);
}

void loop()
{
  //rf95.sleep();
  //Serial.println("Wait reception");
  if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len))
    {
      //Serial.print("recu: ");
      //Serial.println(buf[0]);
      
      // Protection de l'envoie
      sendComplete = false ;
      
      Serial.println((char*)buf);
      // clear the string:
      sendComplete = true ;
      
      // Send a reply
      /*rf95.send(&cpt, sizeof(cpt));
      rf95.waitPacketSent();
      Serial.print("Mesure : ");
      Serial.println(cpt);
      ++cpt;*/
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
  if (sendComplete)
  {
    while (Serial.available()) {
      // get the new byte:
      char inChar = (char)Serial.read();
      // add it to the inputString:
      inputString[i] = inChar;
      //Serial.print((char)inputString[i]);
      // if the incoming character is a newline, set a flag so the main loop can
      // do something about it:
      ++i;
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
}
