/********************************************/
/*                  nn.c                    */
/*  単純な階層型ニューラルワークの計算         */
/*  1出力のネットワークを計算します(学習なし)  */
/*  使い方                                  */
/*                                          */
/********************************************/

/* Visual Studioとの互換性確保 */
#define _CRT_SECURE_NO_WARNINGS 

/* ヘッダファイルのインクルード */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* 記号定数の定義 */
#define INPUTNO 2       /* 入力層のセル数 */
#define HIDEENNO 2      /* 中間層のセル数 */
#define MAXINOUTNO 100  /* データの最大個数 */

/* 関数のプロトタイプの宣言 */
double f(double u);                             /* 伝達関数 */
void initwh(double wh[HIDEENNO][INPUTNO + 1]);  /* 中間層の重みの初期化 */
void initwo(double wo[HIDEENNO + 1]);           /* 出力層の重みの初期化 */
double forward (double wh[HIDEENNO][INPUTNO + 1],
                double wo[HIDEENNO + 1],
                double hi[],
                double e[INPUTNO]);             /* 順方向の計算 */
int getdata(double e[][INPUTNO]);               /* データの読み込み */


/************************/
/*      main()関数      */
/************************/
int main(){
    double wh[HIDEENNO][INPUTNO + 1];   /* 中間層の重み */
    double wo[HIDEENNO + 1];            /* 出力層の重み */
    double e [MAXINOUTNO][INPUTNO];     /* データセット */
    double hi[HIDEENNO + 1];            /* 中間層の出力 */
    double o;                           /* 出力 */
    int i,j;                            /* 繰り返しの制御 */
    int n_of_e;                         /* データの個数 */

    /* 重みの初期化 */
    initwh(wh);
    initwo(wo);

    /* 入力データの読み込み */
    n_of_e = getdata(e);
    printf("データの個数:%d\n", n_of_e);

    /* 計算の本体 */
    for (i = 0; i < n_of_e; ++i){
        printf("%d ", i);
        for(j = 0; j < INPUTNO ; ++j){
            printf("%lf ", e[i][j]);
        }
        o = forward(wh, wo, hi, e[i]);
        printf("%lf\n", o);
    }

    return 0;
}

/**************************/
/*      getdata()関数      */
/*  学習データの読み込み    */
/**************************/

int getdata(double e[][INPUTNO])
{
    int n_of_e = 0; /* データセットの個数 */
    int j = 0;      /* 繰り返しの制御用 */

    /* 追加(修正)        */
    /* ファイルの読み込み */
    char filename[20];
    FILE *fp;
    scanf("%s",&filename);
    if( (fp = fopen(filename,"r")) == NULL )
    {
        printf("\n Don't open file [%s]\n",filename);
        exit(1);
    }

    /* データの入力 */
    while (fscanf(fp,"%lf", &e[n_of_e][j]) !=  EOF) /* scanf("%lf", &e[n_of_e][j])を変更 */
    {
        ++j;
        if(j >= INPUTNO) /* 次のデータ */
        {
            j = 0;
            ++n_of_e;
        }
    }

    /* 追加(修正) */
    fclose(fp);

    return n_of_e;
}

/**************************/
/*      forward()関数      */
/*  順方向の計算          　*/
/**************************/
double forward (double wh[HIDEENNO][INPUTNO + 1],
                double wo[HIDEENNO + 1],
                double hi[],
                double e[INPUTNO])
{
    int i, j; /* 繰り返しの制御 */
    double u; /* 重み付き和の計算 */
    double o; /* 出力の計算 */

    /* hiの計算 */
    for (i = 0; i< HIDEENNO; ++i)
    {
        u = 0; /* 重み付き和を求める */
        for (j = 0; j < INPUTNO; ++j)
        {
            u += e[j] * wh[i][j];
        }
        u -= wh[i][j]; /* しきい値の処理 */
        hi[i] = f(u);
    }
    /* 出力oの計算 */
    o = 0;
    for (i = 0; i < HIDEENNO ; ++i)
    {
        o +=hi[i] * wo[i];
            }
    o -=wo[i]; /* しきい値の処理 */

    return f(o);
}

/**************************/
/*      initwh()関数      */
/*  中間層の重み初期化    　*/
/**************************/
void initwh(double wh[HIDEENNO][INPUTNO + 1])
{
    /* 荷重を定数として与える */
    wh[0][0] = -2;
    wh[0][1] = 3;
    wh[0][2] = -1;
    wh[1][0] = -2;
    wh[1][1] = 1;
    wh[1][2] = 0.5;
}

/**************************/
/*      initwo()関数      */
/*  出力層の重み初期化    　*/
/**************************/
void initwo(double wo[HIDEENNO + 1])
{
    /* 荷重を定数として与える */
    wo[0] = -60;
    wo[1] = 94;
    wo[2] = -1; 
}

/**************************/
/*      f()関数           */
/*      伝達関数    　   　*/
/**************************/
double f(double u)
{
    /* ステップ関数の計算 */
    if (u >= 0){
        return 1.0;
    }
    else
    {
        return 0.0;
    }

    /* シグモイド関数の計算 */
    // return 1.0 / (1.0 + exp(-u));
}