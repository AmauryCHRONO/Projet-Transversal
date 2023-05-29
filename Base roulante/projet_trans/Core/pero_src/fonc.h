/*
 * File: fonc.h
 * Name: fonction de déplacement
 * Ver: 1.0
 * Author:     project_trans
 *
 */

#define HAL_TIM_MODULE_ENABLED


/*-----[ Prototypes For All Functions ]-----*/

void Deplacement_Clavier(char c);
void Deplacement_Distance(char *dis);
void Reception_Deplacement(char *ins);
void Reception_Angle(char *ang);
void ServoUp();
void ServoDown();
