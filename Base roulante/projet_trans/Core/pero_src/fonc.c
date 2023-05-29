/*
 * File: fonc.c
 * Name: fonction de déplacement
 * Ver: 1.0
 * Author:     project_trans
 *
 *	clock à 16Mhz
 *	UART_1 Baud Rate 19200, interruption autorisée
 *	UART_2 Baud Rate 19200, interruption autorisée
 *	voir serialiser digo, mogo, vel, gpid
 */

#include "fonc.h"
#include <stdio.h>
#include <stdlib.h>
#include "../../Core/Inc/main.h"
#include "../../Drivers/STM32F4xx_HAL_Driver/Inc/stm32f4xx_hal.h"

unsigned char r;

UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;
UART_HandleTypeDef huart6;
TIM_HandleTypeDef htim2;

//note: 690 tick par tour on doit multiplier la distance voulu par 690/20 en cm
//angle: multiplie angle voulu par 12.25 pour avoir la distance de, puis multiplication par 690
// deplacement_clavier prend en entrée un caractère et effectue un déplacement

//cette fonction recois un caractère en entrée et en fonction de la valeur envoie une instruction sur
//l'huart 6 (avance, recule, droite, gauche, arrêt)
void Deplacement_Clavier(char c){

	if(c=='z'){
		HAL_UART_Transmit_IT(&huart6, (unsigned char*)"mogo 1:6 2:6\r", 13);
		}
	else if(c== 's'){
		HAL_UART_Transmit_IT(&huart6, (unsigned char*)"mogo 1:-6 2:-6\r", 15);
		}
	else if(c=='d'){
		HAL_UART_Transmit_IT(&huart6, (unsigned char*)"mogo 1:0 2:6\r", 13);
		}
	else if(c=='q'){
		HAL_UART_Transmit_IT(&huart6, (unsigned char*)"mogo 1:6 2:0\r", 13);
		}
	else if(c=='f'){
		HAL_UART_Transmit_IT(&huart6, (unsigned char*)"stop\r", 5);
		}
}

//récupère la distance de 6 caractères (type d'info, nul, distance sur 4 caractères)
//puis convertit distance cm en tick on multiplie la distance par (690/20) (nombre de tick
//pour un tour de roue on envoie la commande déplacement sur l'huart6
void Deplacement_Distance(char *dis){
	int x,y;
	int distance= 0;
	char c,n;
	char* d[100];
	sscanf(dis, "%c%c%2i%2i", &c, &n, &x, &y);
	distance = x*100+y;
	distance = distance*(690)/200;
	sprintf(d,"digo 1:%.1i:5 2:%.1i:5\r",distance,distance);
	HAL_UART_Transmit(&huart6,d,strlen(d),1000);
}

//récupère l'angle de 6 caractères (type d'info, sens rotation, angle sur 4 caractères)
//puis convertit distance cm en tick on multiplie par 77 (2piR) pour avoir la distance
//puis on convertit la distance en tick
//on envoie la commande déplacement sur l'huart6
void Deplacement_Angle(char *ang){
	int x,y,angle;
	float angleb= 0;
	char c,n;
	char* d[100];
	sscanf(ang, "%c%c %2i %2i", &c, &n, &x, &y);
	angleb = (x+y*0.01)*77;
	angle = angleb*(690)/200;
	if(n == '-'){
		sprintf(d,"digo 1:%.1i:2.5 2:-%.1i:2.5\r",angle,angle);
	}
	else{
		sprintf(d,"digo 1:-%.1i:2.5 2:%.1i:2.5\r",angle,angle);
	}
	HAL_UART_Transmit(&huart6,d,strlen(d),1000);
}

//actionne le moteur pour lever crayon
void ServoUp(){
	   htim2.Instance->CCR1 = 12;
   }

//actionne le moteur pour baisser crayon
void ServoDown(){
   htim2.Instance->CCR1 = 5;
}

//récupère 6 caractères puis renvoie au fonctions
//ci dessus en fonction de la valeur du premier caractère
void Reception_Deplacement(char *ins){

	if(ins[0]=='i'){
		Deplacement_Distance(ins);
	}
	else if(ins[0]=='v'){
		Deplacement_Angle(ins);
	}
	else if(ins[0]=='u'){
			ServoUp();
		}
	else if(ins[0]=='p'){
			ServoDown();
		}
	else{
		Deplacement_Clavier(ins[0]);
	}
}


