/*Project No. 12
Project Title: Generate and Solve a 9x9 Sudoku
Members: Daniel Rodriguez (4802087)
Project Points: 150 | Points Considered: 20 | Points Creativity: 5-15
Total Points Overall: 150-185*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct game{
  int p;
  int b;
};

int game(struct game board[9][9], int x, int y);
int load(struct game board[9][9]);
void line();
void linelarge();
int printgame(struct game board[9][9]);
int printsolution(struct game board[9][9]);

int i = 0;
int j = 0;

int fp1(){
  srand(time(NULL));
  struct game board[9][9];
  game(board,0,0);
  load(board);
  printgame(board);
  printsolution(board);
}

int game(struct game board[9][9], int x, int y){
  int n = 0;
  int * set2;
  int newy;
  int newx;
  int set[9] = {1,1,1,1,1,1,1,1,1};

  for(i = 0; i < y; i++){
    set[board[x][i].p - 1] = 0;
  }
  for(i = 0; i < x; i++){
    set[board[i][y].p - 1] = 0;
  }

  for(i = (3 * (x / 3)); i < (3 * (x / 3) + 3); ++i){
    for(j = (3 * (y / 3)); j < y; ++j){
      set[board[i][j].p - 1] = 0;
    }
  }

  for(i = 0; i < 9; i++){
    n = n + set[i];
  }

  set2 = (int*) malloc(sizeof(int)*n);
  j = 0;

  for(i = 0; i < 9; ++i){
    if(set[i] == 1){
      set2[j] = i + 1;
      j++;
    }
  }

  if(x == 8){
    newy = y + 1;
    newx = 0;
  }else{
    newy = y;
    newx = x + 1;
  }
 
 while(n > 0){
    int los = rand() % n;
    board[x][y].p = set2[los];
    set2[los] = set2[n-1];
    n--;
    
    if(x == 8 && y == 8){
      free(set2);
      return 1;
    }

    if(game(board,newx,newy) == 1){
      free(set2);
      return 1;
    }

  }
  free(set2);
  return 0;
}

int load(struct game board[9][9]){
  for(i = 0; i < 9; ++i){
    for(j = 0; j < 9; ++j){
      board[i][j].b = 0;
    }
  }

  for(i = 0; i < 28; ++i){
    board[rand() % 9][rand() % 9].b = 1;
  }
}

void line(){
  for(i = 0; i < 1; i++){
    printf("-");
  }
}

void linelarge(){
 for(i = 0; i < 21; i++){
    printf("-");
  }
  printf("\n");
}

int printgame(struct game board[9][9]){
  linelarge();
  line();
  printf("\t\tSudoku\t\t");
  line();
  printf("\n");
  linelarge();

  for(i = 0; i < 9; ++i){
    for(j = 0; j < 9; ++j){
      if(board[i][j].b == 0){
        printf("■ ");
      }else{
        printf("%d ", board[i][j].p);
      }
      if(j == 2 || j == 5){
        printf("| ");
      }
      if(i == 2 && j == 8 || i == 5 && j == 8){
        printf("\n- - - - - - - - - - -");
      }
    }
    printf("\n");
  }
}

int printsolution(struct game board[9][9]){
  linelarge();
  line();
  printf("\t  Solution!\t\t");
  line();
  printf("\n");
  linelarge();

  for(i = 0; i < 9; ++i){
    for(j = 0; j < 9; ++j){
      printf("%d ", board[i][j]);
      if(j == 2 || j == 5){
        printf("| ");
      }
      if(i == 2 && j == 8 || i == 5 && j == 8){
        printf("\n- - - - - - - - - - -");
      }
    }
    printf("\n");
  }
}