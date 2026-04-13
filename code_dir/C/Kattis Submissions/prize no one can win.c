//Daniel Rodriguez - 4802087
//COP 3502C-002

#include <stdio.h>
#include <stdlib.h>

// Swaps the values pointed to by a and b.
void swap(int *a, int *b) {
     int temp = *a;
     *a = *b;
     *b = temp;
}

// Pre-condition: low and high are valid indexes into values
// Post-condition: Returns the partition index such that all the values
//                 stored in vals from index low to until that index are
//                 less or equal to the value stored there and all the values
//                 after that index until index high are greater than that
//                 value.
//NOT USED ANYMORE
int partition(int* vals, int low, int high) {

    int temp;
    int i, lowpos;

    // Pick a random partition element and swap it into index low.
    i = low + rand()%(high-low+1);
    swap(&vals[low], &vals[i]);

    // Store the index of the partition element.
    lowpos = low;

    // Update our low pointer.
    low++;

    // Run the partition so long as the low and high counters don't cross.
    while (low <= high) {

        // Move the low pointer until we find a value too large for this side.
        while (low <= high && vals[low] <= vals[lowpos]) low++;

        // Move the high pointer until we find a value too small for this side.
        while (high >= low && vals[high] > vals[lowpos]) high--;

        // Now that we've identified two values on the wrong side, swap them.
        if (low < high)
           swap(&vals[low], &vals[high]);
    }
    // Swap the partition element into it's correct location.
    swap(&vals[lowpos], &vals[high]);

    return high; // Return the index of the partition element.
}


// Pre-condition: s and f are value indexes into numbers.
// Post-condition: The values in numbers will be sorted in between indexes s
//                 and f.
void quicksort(int* numbers, int low, int high) {
  // partition
  int i = low, j = high;

  //creates pivot point at median, where it will split
    int pivot = numbers[(low + high) / 2];
    
    //runs so long as low and high don't cross
    while (i <= j) {    

        //move low (i) until value too large
        while (numbers[i] < pivot)i++;

        //move high (j) until value too small
        while (numbers[j] > pivot)j--;


        //once two values are on wrong side they get swapped
        //i and j get incremented to move to next spot once quicksort is called again after this
        //equivalent of the quicksort(split-1)...
        if (i <= j) {
            swap(&numbers[i], &numbers[j]);
            i++;
            j--;
        }
    }
    // recurse
    if (low < j){
      //this runs through and sorts the lower partitioned half with j being the new high
      quicksort(numbers, low, j);
    }                 
        
    if (i < high){
      //this runs through and sort the higher partitioned half with i being the new low
      quicksort(numbers, i, high);
    }
    //after having done so this repeats and splits and sorts as quick sort does
        
}

int main(void) {
  int maxItems = 0, maxPrice = 0;
  while(scanf("%d %d", &maxItems, &maxPrice) != EOF){
    int sum = 0;
    int* items = malloc(sizeof(int*) * (maxItems+1));
    for(int i = 0; i < maxItems; i++){
    if(scanf("%d", &items[i])){};
    }

    /*for(int i = 0; i < maxItems; i++){
    printf("array[i] = %d ", items[i]);
    }*/

    quicksort(items, 0, maxItems);

    /*printf("\nafter\n");
    for(int i = 1; i < maxItems+1; i++){
      printf("array[i] = %d ", items[i]);
    }
    printf("\n");*/

    for(int j = 0; j < maxItems; j++){
     if(items[j]+items[j+1] <= maxPrice){
       sum++;
     }
    } 
    if(sum == 0){
      sum = 1;
    }

   printf("%d\n", sum);

    free(items);
  }

  //printf("Hello World\n");
  return 0;
}