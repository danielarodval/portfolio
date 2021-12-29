#include <stdio.h>
#include <string.h>

char *style[10] = {" ","Abstract","Fine Art","Figurative","Modern","Abstract Expressionism","Expressionism"};
char *subject[10] = {" ","Abstract","Landscape","People","Portrait","Nature","Animal"};
char *size[10] = {" ","Small","Medium","Large","Oversize"};
char *medium[10] = {" ","Acryllic","Oil","Watercolor","Ink","Paint","Spray paint"}; 
char *material[10] = {" ","Canvas","Paper","Wood","Cardboard","Soft","Other"}; 
char *orientation[10] = {" ","Portrait","Landscape","Square"}; 

typedef struct{
  char code[7];
  char artistname[30];
  int style;
  char paintingname[30];
  int subject;
  int size;
  int medium;
  int material;
  int orientation;
  double price;
}

painting;

painting specialpainting = {"All","All",0,"All",0,0,0,0,0,0};
painting blank = {"","",0,"",0,0,0,0,0,0};
painting database[1000] = {
{"","",0,"",0,0,0,0,0,0},
{"NT0001","Nestor Toro",1,"Late Spring",1,1,1,1,1,1000.00},
{"FM0001","Fabienne Monstier",2,"Sweet Roses",1,1,1,1,1,2300.00},
{"NL001","Nikos Lamprinos",1,"Untitled",1,1,1,1,1,1000.00}
};

char menuartgallery();
char menu();
void filterpaintings(void);
void printfilter();
void printfilteredpaintings();
void printall(void);
void addpainting();
void deleteitem();
void modifyitem();
void line();

double minprice = 0;
double maxprice = 1000000;
int availableitems;

painting newpainting, specialpainting;


int main(void) {

  availableitems = 3;
  char req = menuartgallery();

  while (req != 'x'){
    switch(req){
      case 's':
      filterpaintings();
      break;

      case 'a':
      addpainting();
      printall();
      break;

      case 'e':
      deleteitem();
      printall();
      break;

      case 'm':
      modifyitem();
      printall();
      break;

      case 'p':
      printall();
      break;

      default:
      printf("Please enter a valid selection.\n\n");
      break;
    }
    req = menuartgallery();
  }
  return 0;
}

void line(){
  for(int i = 0; i < 30; i++){
    printf("-");
  }
  printf("\n");
}

void linelong(){
  for(int i = 0; i < 70; i++){
    printf("-");
  }
  printf("\n");
}

void superlong(){
  for(int i = 0; i < 120; i++){
    printf("-");
  }
  printf("\n");
}

char menuartgallery(){
  char req;
  line();
  printf("Welcome To Virtual Art Gallery\n");
  line();
  printf("Menu - Select one of the following options:\n");
  printf("press 'a': To add a painting\n"); 
  printf("press 'e': To erase a painting\n"); 
  printf("press 'p': To print data for all paintings\n"); 
  printf("press 's': To print data for special paintings\n"); 
  printf("press 'm': To modify data for a painting.\n"); 
  printf("press 'x': To exit the program\n"); 
  printf("option: ? "); 
  scanf("%c", &req);
  
  return req;
}

void printall(){
  printf("\n\nList of all the available paintings in the gallery\n");
  superlong();
  printf("%-8s %-8s %-20s %-10s %-22s %-9s %-8s %-8s %-9s %-13s %-10s\n","Item","Code","Artist name","Style","Painting Name","Subject","Size","Medium","Material","Orientation","Price");
  superlong();

  for(int i = 1; i <= availableitems; i++){
    printf("%-8d %-8s %-20s %-10s %-22s %-9s %-8s %-8s %-9s %-13s %-10.2f\n\n",i,database[i].code,database[i].artistname,style[database[i].style],database[i].paintingname,subject[database[i].subject],size[database[i].size],medium[database[i].medium],material[database[i].material], orientation[database[i].orientation],database[i].price);
  }
}

void filterpaintings(void){
  char buffer;
  char correct;
  int style;

  superlong();
  printf("Are you are looking for special items? Please see the following help and then add your filters:\n");
  superlong();

  printf("\nhelp:\n"); 
  printf("Code: Two initials of the artist follwed by 4 digits. Example: ab0001\n"); 
  printf("Style:       1-Abstract 2-Fine art 3-Figurative 4-Modern 5-Abstract expressionism 6-Expressionism)\n"); 
  printf("Subject:     1-Abstract 2-Landscape 3-People 4-Portrait 5-Nature 6-Animal\n"); 
  printf("Size:        1-Small 2-Medium 3-Large 4-Oversize\n"); 
  printf("Medium:      1-Acryllic 2-Oil 3-Watercolor 4-Ink 5-Paint 6-Spray paint\n"); 
  printf("Material:    1-Canvas 2-Paper 3-Wood 4-Other 5-Cardboard 6-Soft\n"); 
  printf("Orientation: 1-Portrait 2-Landscape 3-Square\n"); 
  superlong();

  do{
    printf("\nStyle: ");
    scanf("%d", &specialpainting.style); 

    printf("\nSubject: "); 
    scanf("%d", &specialpainting.subject); 

    printf("\nSize: "); 
    scanf("%d", &specialpainting.size);

    printf("\nMedium: "); 
    scanf("%d", &specialpainting.medium);

    printf("\nMaterial: "); 
    scanf("%d", &specialpainting.material);

    printf("\nOrientation: "); 
    scanf("%d", &specialpainting.orientation);

    printf("\nYou applied the above filters. Do you verify them? (press 1 = yes or 0 = no) : "); 
    scanf("%d", &correct, &buffer);} while(!correct);

  printfilteredpaintings(); 
}

void printfilter(){
  superlong();
  printf("%-10s %-9s %-8s %-8s %-9s %-13s %-10s %-10s\n","Style","Subject","Size","Medium","Material","Orientation","Min Price","Max Price");
  linelong();
  printf("%-10s %-9s %-8s %-8s %-9s %-13s %-10.2f %-10.2f\n",style[specialpainting.style],subject[specialpainting.subject],size[specialpainting.size],medium[specialpainting.medium],material[specialpainting.material],orientation[specialpainting.orientation],minprice,maxprice); 
}

void printfilteredpaintings(){
  int item = 0;
  int conditions[10] = {0};
  int showitem = 0;
  int i = 1; 

  printf("\nThe list of the paintings that you are looking for:\n"); 
  superlong();
  printf("%-8s %-8s %-20s %-10s %-22s %-9s %-8s %-8s %-9s %-13s %-10s\n","Item","Code","Artist name","Style","Painting Name","Subject","Size","Medium","Material","Orientation","Price");
  superlong();

  for(int item = 1; item <= availableitems; item++){
    if(database[item].style==specialpainting.style || specialpainting.style==0){
      conditions[0]=1;
    }
    if(database[item].subject==specialpainting.subject ||specialpainting.subject==0){
      conditions[1]=1;
    } 
    if(database[item].size==specialpainting.size ||specialpainting.size==0){
      conditions[2]=1;
    }
    if(database[item].medium==specialpainting.medium ||specialpainting.medium==0){
      conditions[3]=1;
    }
    if(database[item].material==specialpainting.material ||specialpainting.material==0){
      conditions[4]=1;
    }
    if(database[item].orientation==specialpainting.orientation || specialpainting.orientation==0){
      conditions[5]=1;
    }
    if(database[item].price>=minprice && database[item].price<=maxprice){
      conditions[6]=1;
    }
    if(conditions[0] && conditions[1] && conditions[2] && conditions[3] && conditions[4] && conditions[5]&& conditions[6]){
      showitem=1;
    }
    if (showitem){
      printf("%-6d %-6s %-20s %-10s %-22s %-9s %-6s %-8s %-9s %-13s %-10.2f\n\n",i++,database[item].code,database[item].artistname,style[database[item].style],database[item].paintingname,subject[database[item].subject],size[database[item].size],medium[database[item].medium],material[database[item].material],orientation[database[item].orientation],database[item].price);
    }
  }
  if(!showitem){
    printf("Item not found.\n\n");
  }
}

void addpainting(){
  char buffer;
  char correct;
  int style;
  char firstname[10];
  char lastname[10];
  char fullname[30] = "";

  ++availableitems;

  linelong();
  printf("\nAdd Item : Please enter the required data for the new painting:\n");
  linelong();
  printf("\nhelp:\n"); 
  printf("Code: \t\tTwo initials of the artist followed by 4 digits. Example: ab0001\n"); 
  printf("Style: \t\t1-Abstract 2-Fine art 3-Figurative 4-Modern 5-Abstract expressionism 6-Expressionism\n"); 
  printf("Subject: \t1-Abstract 2-Landscape 3-People 4-Portrait 5-Nature 6-Animal\n"); 
  printf("Size: \t\t1-Small 2-Medium 3-Large 4-Oversize\n"); 
  printf("Medium: \t1-Acryllic 2-Oil 3-Watercolor 4-Ink 5-Paint 6-Spray paint\n");
  printf("Material: \t1-Canvas 2-Paper 3-Wood 4-Other 5-Cardboard 6-Soft\n"); 
  printf("Orientation: \t1-Portrait 2-Landscape 3-Square\n"); 
  printf("Price:\n");
  superlong();

  char str[7];

  printf("\nCode: "); 
  scanf("%s",str );strcpy(database[availableitems].code,str);

  printf("Artist Name: "); 
  scanf("%s%s", firstname, lastname);

  printf("Style: ");
  scanf("%d", &database[availableitems].style);

  printf("Painting's Name: "); 
  scanf("%s",str );strcpy(database[availableitems].paintingname,str);

  printf("Subject: "); 
  scanf("%d", &database[availableitems].subject);

  printf("Size: "); 
  scanf("%d", &database[availableitems].size);

  printf("Medium: "); 
  scanf("%d", &database[availableitems].material);

  printf("Orientation: "); 
  scanf("%d", &database[availableitems].medium);

  printf("Material: "); 
  scanf("%d", &database[availableitems].orientation);

  printf("Price:"); scanf("%lf", &database[availableitems].price); 
}

void deleteitem(){
  int item;

  printall();

  printf("\nWhich item should be deleted (item no.)?"); 
  scanf("%d", &item);

  database[item] = blank; 
}

void modifyitem(){
  int item;

  printall();

  printf("\nWhich item should be modified (item no.)?"); 
  scanf("%d", &item);

  int temp = availableitems;
  availableitems = item - 1;
  addpainting();
  availableitems = temp;

}