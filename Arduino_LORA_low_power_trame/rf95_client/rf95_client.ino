// rf95_server.pde
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messageing server
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95  if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf95_client
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with
// the RFM95W, Adafruit Feather M0 with RFM95

//#include <Adafruit_SleepyDog.h>
#include <SPI.h>
#include <RH_RF95.h>
#include <string.h>
#include <LowPower.h>

#define MY_ADDRESS 1
#define Server_ADDRESS 0
#define SENSOR_TYPE "TH"
#define V_REF 1.1
#define R_div 4 //pont diviseur de tension
#define NB_NOT_ACK 3 // Trame peut être renvoyée 3 fois jusqu'à ce que l'ack soit recu

uint8_t cpt_not_ack = 0 ;
// Singleton instance of the radio driver
RH_RF95 rf95;
//RH_RF95 rf95(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W
//RH_RF95 rf95(8, 3); // Adafruit Feather M0 with RFM95 

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

uint8_t trame[50] = {0};
uint8_t cpt = 0 ;
uint8_t it,ft,ih,fh,iv,fv ;

uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
uint8_t len = sizeof(buf);

char ack = 0 ;

void acquisition(uint8_t *it,uint8_t *ft, uint8_t *ih,uint8_t * fh,uint8_t * iv,uint8_t * fv);
void split_float(float *v, uint8_t *i,uint8_t *f);

float mesure_batterie();
float mesure_temperature();
float mesure_humiditee();

char ack_type();

void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

  analogReference(INTERNAL); // Utiliser V_ref=1.1V pour l'ADC
  Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  if (!rf95.init())
    Serial.println("init failed");  
  rf95.setFrequency(868);
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
//  driver.setTxPower(23, false);
  // If you are using Modtronix inAir4 or inAir9,or any other module which uses the
  // transmitter RFO pins and not the PA_BOOST pins
  // then you can configure the power transmitter power for -1 to 14 dBm and with useRFO true. 
  // Failure to do that will result in extremely low transmit powers.
//  driver.setTxPower(14, true);
}

void loop()
{
  //Serial.println("Demande d acquistion");
  // 1er envoie

//iv=3 ; fv=33;
  // A mettre avant le send!!!!
  /*ft=5; ih=50; fh=5; iv=3 ; fv=3;
  //sprintf(trame,"{\"t\":\"%d.%d\",\"h\":\"%d.%d\"}",it,ft,ih,fh);
  sprintf(trame, "%s%dT%d.%dH%d.%dV%d.%d",SENSOR_TYPE,MY_ADDRESS,it,ft,ih,fh,iv,fv);
  ++it ;*/
  acquisition(&it,&ft,&ih,&fh,&iv,&fv);
  sprintf(trame, "%d%s%d %d.%d %d.%d %d.%d",Server_ADDRESS,SENSOR_TYPE,MY_ADDRESS,it,ft,ih,fh,iv,fv);

  ack=0;
  rf95.send(trame, sizeof(trame));
  rf95.waitPacketSent();

  if (rf95.waitAvailableTimeout(1250)) // emetteur<-->recepteur à 1 mètre timeout minimum de 550ms
                                        // A la reception d'une trame renvoie 1 et attend x ms et renvoie 0 si rien est recu avant la fin des x ms
  { 
    // Should be a reply message for us now   
    if (rf95.recv(buf, &len))
   {
     // Serial.print("got reply: ");
     // Serial.println((char*)buf);

      //Serial.print("ack_type");
      ack = ack_type();
      //Serial.println((char)ack);

      memset(buf, '\0', strlen(buf) - 1);       
    }
    else
    {
      Serial.println("recv failed");
    }
  }
  else
  {
    Serial.println("No reply, is rf95_server running?");
  }

  if (ack=='A' or cpt_not_ack >= NB_NOT_ACK-1)
  {
    rf95.sleep();  
    delay(4000);
    //Watchdog.sleep(4000); //PAS TOP
    //LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF); //un peu mieux que watchdog mais plus de serial
    //LowPower.idle(SLEEP_4S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF,SPI_OFF, USART0_OFF, TWI_OFF); // moins bien que powerdown
    cpt_not_ack = 0;
  }
  else
  {
    Serial.print("NOT_ack : ");
    Serial.println(cpt_not_ack);
   ++cpt_not_ack;
  }
}
char ack_type()
{
  char temp ;
  //itoa(MY_ADDRESS,&temp ,10)
  //atoi(buf,&temp ,10);
  //Serial.println(atoi(&buf[0]));
  if ( (atoi(&buf[0])==MY_ADDRESS) and (atoi(&buf[3])==(char)Server_ADDRESS) and (buf[1]==(char)SENSOR_TYPE[0])and (buf[2]==(char)SENSOR_TYPE[1]) )
  {
    return buf[5];
  }
  return -1 ;  
}

void acquisition(uint8_t *it,uint8_t *ft, uint8_t *ih,uint8_t * fh,uint8_t * iv,uint8_t * fv)
{
  // Mesure température
  float temp=mesure_temperature() ;
  split_float(&temp,it,ft);

  // Mesure humidité
  float humd=mesure_humiditee() ;
  split_float(&humd,ih,fh);

  // Mesure tension
  float tension=mesure_batterie();
  split_float(&tension,iv,fv);
}
void split_float(float *v, uint8_t *i,uint8_t *f)
{
  *i = (uint8_t) *v;            // Make integer part
  *f = (uint8_t) ((*v - *i)*100);      // Fraction. Has same sign as integer part
  if (*f<0) *f = -*f;           // So if it is negative make fraction positive again.
}

float mesure_batterie()
{
  int sensorValue = analogRead(A0); //read the A0 pin value
  return R_div * V_REF * sensorValue / 1023.0 ;
  //Pour arrondir a 1 décimale prêt floor(10*f+0.5)/10 
}
float mesure_temperature()
{
  return 22.53 ;
}
float mesure_humiditee()
{
  return 52.50 ;
}
