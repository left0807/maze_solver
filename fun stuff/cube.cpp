#include <bits/stdc++.h>
using namespace std;

typedef vector<vector<vector<int> > > cube;
typedef vector<vector<int> > face;
typedef vector<int> row;

cube state(6, face(3, row(3)));
face tmp_face(3, row(3));
row tmp_row(3);
int tmp;
int bound = 20;
stack<int> path, shortest;

void print_cube2(){
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 3; j++){
            for(int k = 0; k < 3; k++) cout << state[i][j][k] << ' ';
            cout << '\n';
        }
    }
}
void print_cube(){
    for(int i = 0; i < 9; i++){
    for(int j = 0; j < 9; j++){
        if(j >= 3 && j < 6 && i < 3) cout << state[1][i][j%3] << ' ';
        else if(i>=3 && i < 6) {
            if(j>= 0 && j < 3) cout << state[2][i%3][j%3] << ' ';
            if(j>= 3 && j < 6) cout << state[0][i%3][j%3] << ' ';
            if(j>= 6 && j < 9) cout << state[4][i%3][j%3] << ' ';
        }
        else if(j >= 3 && j < 6 && i >=6) cout << state[3][i%3][j%3] << ' ';
        else cout << "  ";
    }
    cout << '\n';
    }

    for(int i = 0; i < 3; i++){
    for(int j = 0; j < 9; j++){
        if(j >= 3 && j < 6) cout << state[5][i][j%3] << ' ';
        else cout << "  ";
    }
    cout << '\n';
    }
    cout << '\n';
}

void SW(int i, int j){
    swap(state[i], state[j]);
}

void rotate_row(bool clockwise){
    if(clockwise){
        tmp_row = state[1][2];
        for(int i = 0; i <= 2; i++) state[1][2][i] = state[2][2-i][2];
        for(int i = 0; i <= 2; i++) state[2][i][2]=state[3][0][i];
        for(int i = 0; i <= 2; i++) state[3][0][i] = state[4][2-i][0];
        for(int i = 0; i<=2; i++) state[4][i][0]=tmp_row[i];
    }
    else{
        tmp_row = state[1][2];
        for(int i = 0; i <= 2; i++) state[1][2][i] = state[4][i][0];
        for(int i = 0; i <= 2; i++) state[4][i][0]=state[3][0][2-i];
        for(int i = 0; i <= 2; i++) state[3][0][i]=state[2][i][2];
        for(int i = 0; i <= 2; i++) state[2][i][2]=tmp_row[2-i];
    }
}

void rotate_face(int face, bool clockwise){
    if(clockwise){
        tmp = state[face][0][0];
        state[face][0][0]=state[face][2][0];state[face][2][0]=state[face][2][2];state[face][2][2]=state[face][0][2];state[face][0][2]=tmp;
        tmp = state[face][0][1];
        state[face][0][1] = state[face][1][0];state[face][1][0]=state[face][2][1];state[face][2][1]=state[face][1][2];state[face][1][2]=tmp;
    }
    else{
        tmp = state[face][0][0];
        state[face][0][0]=state[face][0][2];state[face][0][2]=state[face][2][2];state[face][2][2]=state[face][2][0];state[face][2][0]=tmp;
        tmp = state[face][0][1];
        state[face][0][1]=state[face][1][2];state[face][1][2]=state[face][2][1];state[face][2][1]=state[face][1][0];state[face][1][0]=tmp;
    }
}

void rotate_cube(int face, bool clockwise){
    if(face == 1){SW(1,0);SW(5,1);SW(3,5);rotate_face(2,1);rotate_face(4,0);}
    if(face == 3){SW(3,5);SW(5,1);SW(1,0);rotate_face(2,0);rotate_face(4,1);}
    if(face == 2){SW(0,2);SW(5,2);SW(4,5);rotate_face(3,1);rotate_face(1,0);}
    if(face == 4){SW(4,5);SW(2,5);SW(2,0);rotate_face(3,0);rotate_face(1,1);}
    if(face == 5){
        SW(0, 5);SW(2,4);
        for(int i = 0; i < 2; i++){rotate_face(3,1);rotate_face(1,1);}
    }

    rotate_face(0, clockwise);
    rotate_row(clockwise);

    if(face == 3){SW(1,0);SW(5,1);SW(3,5);rotate_face(2,1);rotate_face(4,0);}
    if(face == 1){SW(3,5);SW(5,1);SW(1,0);rotate_face(2,0);rotate_face(4,1);}
    if(face == 4){SW(0,2);SW(5,2);SW(4,5);rotate_face(3,1);rotate_face(1,0);}
    if(face == 2){SW(4,5);SW(2,5);SW(2,0);rotate_face(3,0);rotate_face(1,1);}
    if(face == 5){
        SW(0, 5);SW(2,4);
        for(int i = 0; i < 2; i++){rotate_face(3,1);rotate_face(1,1);}
    }
}

bool valid(){
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 3; j++)
        for(int k = 0; k < 3; k++)
        if(state[i][j][k] != state[i][0][0]) return false;
    }
    return true;
}

void dfs(int s, int pre, int b){
    if(valid()){
        if(s < bound){
        shortest = path;
        bound = s;
        }
        return;
    }

    if(s>b) {
        return;
    }

    for(int i = 0; i < 6; i++)
        for(int j = 0; j <= 1; j++){
            if(pre == (i<<4+(!j))) continue;

            path.push((1<<4)+j);
            rotate_cube(i, j);
            dfs(s+1, (i<<4)+j, b);
            rotate_cube(i, !j);

            path.pop();
        }
}

int main(){
    ifstream fin("test.in");
    for(int i = 0; i < 6; i++)
    for(int j = 0; j < 3; j++)
    for(int k = 0; k < 3; k++){
        fin >> state[i][j][k];
    }

    print_cube();
    // while(true){
    //     int f, c;
    //     cin >> f >> c;
    //     rotate_cube(f, c);
    //     print_cube2();
    // }

    for(int i = 1; i <= bound; i++){
        dfs(0, -1, i);
    }
    vector<int> out;
    while(!shortest.empty()){
        out.push_back(shortest.top());
        shortest.pop();
    }
    // for(int i : out) 
    // {
    //     cout << (i>>4) << ' ' << i%2 << '\n';
    // }
}