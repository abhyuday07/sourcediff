// #include <stdio.h>

int f1(){
    return 1;
}

int f2(){
    return f1();
}

int f3(int x){
    if(x == 0){
        return 0;
    }
    return f3(x - 1) + f2() + f1();
}

int f4(){
    return f1() + f2();
}

int main(){
    int x1 = f1();
    int x2 = f2();
    int x3 = f1();
    int x4 = f3(1);
    // printf("%d", x1);
    return 0;
}
