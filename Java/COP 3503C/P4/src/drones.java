/*
 * Daniel Rodriguez
 * COP 3503C
 * Section Number: 0001
 */

 import java.util.*;
 
public class drones {
    static final int MAX_STATE = 1 << 24;
    static int[] distance = new int[MAX_STATE];
    static int[][] moves = {{-1,0},{1,0},{0,-1},{0,1}};
    static int n;
    static int[] tP; //target positions

    public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);
        n = stdin.nextInt();
        stdin.nextLine();

        tP = new int[n]; //target positions
        boolean[][] nFZ = new boolean[8][8]; //no fly zones
        int init = 0;
        
        for(int i = 0; i < 8; i++){
            String[] line = stdin.nextLine().split(" ");

            for(int j = 0; j < 8; j++){
                if(line[j].charAt(0) == 'D'){
                    int droneId = line[j].charAt(1) - '1';
                    init |= (i * 8 + j) << (droneId * 6);
                }else if(line[j].charAt(0) == 'G'){
                    int groupId = line[j].charAt(1) - '1';
                    tP[groupId] = i * 8 + j;
                }else if(line[j].equals("XX")){
                    nFZ[i][j] = true;
                }
            }
        }

        System.out.println(bfs(init, nFZ));
        stdin.close();
    }

    static int bfs(int init, boolean[][] noFlyZones){
        Arrays.fill(distance, -1);
        Queue<Integer> q = new LinkedList<>();
        q.offer(init);
        distance[init] = 0;

        while(!q.isEmpty()){
            int curr = q.poll(); //current state

            if(isFinalState(curr)) return distance[curr]; //if finalstate, return distance

            for(int[] move : moves){
                int nS = getNextState(curr, move, noFlyZones); //next state
                
                if(nS != -1 && distance[nS] == -1){ //if next state is valid and not visited
                    distance[nS] = distance[curr] + 1; //update distance
                    q.offer(nS); //add to queue
                }
            }
        }
        return -1; // no solution
    }

    static boolean isFinalState(int state){
        for(int i = 0; i < n; i++){
            int x = (state >> (i * 6)) & 63;
            if(x != tP[i]) return false;
        }
        return true;
    }

    static int getNextState(int state, int[] move, boolean[][] noFlyZones){
        int nextState = state;

        for(int i = 0; i < n; i++){
            int pos = (state >> (i * 6)) & 63; // current position of drone i
            if(pos == tP[i]) continue; //if drone is already at target position

            int row = pos / 8;
            int col = pos % 8;
            int newRow = row + move[0];
            int newCol = col + move[1];

            // validate new position
            if(newRow >= 0 && newRow < 8 && newCol >= 0 && newCol < 8 && !noFlyZones[newRow][newCol]){
                nextState &= ~(63 << (i * 6)); //clear current position
                nextState |= ((newRow * 8 + newCol) << (i * 6)); //update position
            }
        }
        return nextState;
    }
}