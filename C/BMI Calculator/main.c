#include <stdio.h>
//declaration of functions
int bmiCalc();
int min();
void line();
//declartion of variables
double BMI, mina, minb;
int counter;
//declaration of arrays
double beforeDietBMI[1024], afterDietBMI[1024], weight[1024], height[1024];

int main(void) {
  //menu for user
  printf("\t\tBMI Progress Calculator\n");
  line();
  printf("\nPlease enter the weights and heights, in that respective \norder, of each patient below before the diet.\n");
  line();
  printf("\n\t\tInputs for Pre-Diet\n\n");
 //counter to get input from user and store in array
  for (counter = 0; counter < 5; counter++){
    printf("Patient %d:", counter + 1);
    scanf("%lf %lf", &weight[counter], &height[counter]);
    bmiCalc();
    beforeDietBMI[counter] = BMI;
  }

  printf("\n");
  line();
  printf("\n\t\tResults for Pre-Diet\n\n");
  //prints the results after the inputs
  for (int i = 0; i < 5; i++){
    printf("The BMI for Patient %d is: %lf\n",i + 1, beforeDietBMI[i]);
  }
  //prompts user for more input
  printf("\n");
  line();
  printf("\nNow please enter the weights and heights, in that \nrespective order, of each patient below after the diet.\n");
  line();
  printf("\n\t\tInputs for Post-Diet\n\n");
  //asks for new inputs from user
  for (counter = 0; counter < 5; counter++){
    printf("Patient %d:", counter + 1);
    scanf("%lf %lf", &weight[counter], &height[counter]);
    bmiCalc();
    afterDietBMI[counter] = BMI;
  }

  printf("\n");
  line();
  printf("\n\t\tResults for Post-Diet\n\n");
  //gives results of new inputs from user
  for (int i = 0; i < 5; i++){
    printf("The BMI for Patient %d is: %lf\n",i + 1, afterDietBMI[i]);
  }

  printf("\n");
  line();
  printf("\n\t\tFinal Results\n\n");
  //if there is a 15% or more reduction then the statement prints
  if ((minb - (minb * .15)) >= mina){
    printf("The diet has been effective to reduce the minimum BMI.");
  }else{
    printf("There is no signifcant change in BMI.");
  }
  return 0;
}

int bmiCalc(){
  //BMI calculator
  BMI = ((weight[counter] / (height[counter] * height[counter])) * 703);

  return BMI;
}

void line(){
  //line for breaking program
  for(int i = 0; i < 57; i++){
    printf("-");
  }

}

int min(){
  //finds the minimum of both arrays to compare them in the main
  minb = beforeDietBMI[0];

  for(int i = 0; i < 5; i++){
    if(beforeDietBMI[i] < minb){
      minb = beforeDietBMI[i];
    }
  }

  mina = afterDietBMI[0];

  for(int i = 0; i < 5; i++){
    if(afterDietBMI[i] < mina){
      mina = afterDietBMI[i];
    }
  }

  return minb, mina;
}