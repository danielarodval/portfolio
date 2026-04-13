#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct{
  int index;
  char name[100];
  int quantity;
  double price;
} chart;

void printchart();
void init(FILE *dat);
void save(FILE *dat);
int menu();
void additem();
void updateitem();
void deleteitem();
void line();

chart data[100];

int main(void) {
  FILE *dat = fopen("hardware.dat","r");
  init(dat);
  int input = menu();
  while(input != 5){
    switch(input){
      case 1:
      printchart();
      break;

      case 2:
      additem();
      save(dat);
      break;

      case 3:
      updateitem();
      save(dat);
      break;

      case 4:
      deleteitem();
      save(dat);
      break;
    }
    input = menu();
  }
  return 0;
}

void line(){
  for(int i = 0; i < 50; i++){
    printf("-");
  }
  printf("\n");
}

void linechart(){
  for(int i = 0; i < 50; i++){
    printf("=");
  }
  printf("\n");
}

int menu(){
  int input;
  printf("\n\t\tHardware Store Inventory\n");
  line();
  printf("1 - Print Hardware Inventory\n");
  printf("2 - Add Item to Inventory\n");
  printf("3 - Update Item in Inventory\n");
  printf("4 - Delete Item From Inventory\n");
  printf("5 - Exit Hardware Inventory\n");
  printf("Enter Selection: ");
  scanf("%d", &input);
  return input;
}

void init(FILE *fileToRead){
  for(int i = 0; i < 100; i++){
    data[i].index = i;
    strcpy(data[i].name,"_empty_");
    data[i].quantity = 0;
    data[i].price = 0.0;
  }

  long size;
  fseek(fileToRead,0,SEEK_END);
  size = ftell(fileToRead);

  if(size == 0){
    printf("Empty file!\n");
    save(fileToRead);
    return;
  }

  fseek(fileToRead, 0, SEEK_SET);
  int index;
  char name[100];
  int quantity;
  double price;

  for(int i = 0; i < 100; i++){
    name[0] = 0;
    fscanf(fileToRead, "%d,%d,%lf,%s[^\n]", &index, &quantity, &price, &name);
    data[i].name[100] = 0;
    strcpy(data[i].name, name);
    data[i].index = index;
    data[i].quantity = quantity;
    data[i].price = price;
  }
}

void save(FILE *dat){
  FILE *dats = fopen("hardware.dat","w");
  for(int i = 0; i < 100; i++){
    fprintf(dats, "%d,%d,%lf,%s\n",data[i].index,data[i].quantity,data[i].price,data[i].name);
  }
  fclose(dats);
}

void printchart(){
  printf("\n\nRecord # | Name\t\t\t|Quantity\t|Price\n");
  linechart();
  for(int i = 0; i < 100; i++){
    if(strcmp(data[i].name,"_empty_") == 0){
      continue;
    }
    printf("\t%d\t | %s\t\t|%d\t\t\t|%-5.2f\n",data[i].index,data[i].name,data[i].quantity,data[i].price);
    line();
  }
}


void additem(){
  int index;
  char name[100];
  int quantity;
  double price;

  printf("\n\nAdd New Item to Inventory\n");
  printf("Record #: ");
  scanf("%d",&index);
  printf("Name: ");
  scanf(" %[^\t\n]s",&name);
  printf("Quantity: ");
  scanf("%d",&quantity);
  printf("Price: ");
  scanf("%lf",&price);

  strcpy(data[index].name,name);
  data[index].quantity = quantity;
  data[index].price = price;

  printf("Item Added\n\n");
}


void updateitem(){
  int n = 0;
  printf("\n\nUpdating Item in Inventory\n");
  printchart();
  printf("Record Number: ");
  scanf("%d",&n);
  if(strcmp(data[n].name,"_empty_") == 0){
    printf("Record Does Not Exist\n\n");
    return;
  }
  int index;
  char name[100];
  int quantity;
  double price;
  printf("Update an Item\n");
  printf("Name: ");
  scanf(" %[^\t\n]s",&name);
  printf("Quantity: ");
  scanf("%d",&quantity);
  printf("Price: ");
  scanf("%lf",&price);
  strcpy(data[n].name,name);
  data[n].price = price;
  data[n].quantity = quantity;
  printf("Item Updated\n\n");
}

void deleteitem(){
  int n = 0;
  printf("Delete an Item\n");
  printchart();
  printf("Record Number: ");
  scanf("%d",&n);
  if(strcmp(data[n].name,"_empty_") == 0){
    printf("Record Nonexistant\n\n");
    return;
  }
  strcpy(data[n].name,"_empty_");
  data[n].price = 0.0;
  data[n].quantity = 0;
}