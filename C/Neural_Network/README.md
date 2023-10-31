# ニューラルネットワーク
### ニューラルネットワーク(Neural Network)
- 神経細胞(Neuron)をモデル化した計算素子である人口ニューロン(Artifical Neuron)を組み合わせたもの
### 人工ニューロン
- ニューロ素子やニューロセルとも呼ぶ。
### 神経細胞（ニューロン）
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/Neurons.png)
### 訂正！！人口ニューロン　→ 人工ニューロン
[画像の参考URL](https://hombre-nuevo.com/machinelearning/machinelearning0001/)

<br>

# 人工ニューロンの中
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/Function.png)
- 入力：X1 ~ Xn
- 重み(weight)：W1 ~ Wn
- しきい値：v
- 出力：z
<br>

- 積算値：u
- 伝達関数(または出力関数)：f
 
<br>

### 重みづけとしきい値
- 人工ニューロンは、神経細胞と似た役割を果たすために2種の数値を持っている。
1. 入力される複数の情報に重みづけをして足し合わせるための「重みづけの比率」
2. 足し合わされた情報から意味を引き出すのに必要な「閾値」

<br>

### 例題  -写真に写る風景が日本の大都市であるか否か-
- 判断のための条件
```
入力 X
a. 日本語の表記が多いか
b. ビジネススーツ姿の人が多いか
c. 建物が占める割合が樹木の2倍以上か
```
- a、 b、 cそれぞれについて、正であれば1、否であれば0が、人工ニューロンに入力される
```
重み W
a：b：c = 5：3：2 ( = Wa：Wb：Wc )

閾値 V
V = 6
```
- 計算
```
例えば写真の中に日本語表記が多く（a=1）、スーツ姿の人は少なく（b=0）、建物が樹木の2倍以上あれば（c=1）
入力から得られる値は1×5＋0×3＋1×2＝7。
閾値の6より大きいので、この写真は日本の大都市であるという判断になります（出力は7-6 =１）。

また、日本語表記が少なければ、スーツ姿の人も建物の割合も多くても（a=0、b=1、 c=1）、
得られる値＝5となり閾値より小さいため、日本の大都市ではないと判断されます（出力は0）。

ところが、閾値を4にするとどうでしょうか。
日本語が多ければ、他の条件に関わらず日本の大都市となり、
日本語がなくとも、スーツ姿の人が多く、建物の割合が高ければ
日本の大都市と判断するというモデルに変化するのです。
```
[参考文献](https://www.ctc-g.co.jp/bestengine/article/2018/0809a_01.html)

<br>

# 伝達関数
### ステップ関数(Step Function)
- 非線形関数で断片的
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/StepFunction.png" width="35%">

<br>

### シグモイド関数(Sigmoid Function)
- なめらかな関数で連続的
- バックプロパゲーションにおける学習の計算処理が容易
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/SigmoidFunction.png" width="70%">

<br>

### ステップ関数による論理演算
- OR
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/OR.png" width="50%">

- AND
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/AND.png" width="50%">

- そのほかにもNOTやXORなどの論理回路を構成可能

<br>
<br>

# ニューラルネット
### フィードフォワード型ネット(Feed Formard Neteork)または階層型ネットワーク(Layerd Network)
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/Layered_Network.png)

### ネットワークの計算例
- EOR ( 排他的論理和 )
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/EOR.png" width="80%">

### ニューラルネットの学習手続き
```
(1) すべての重みとしきい値を ( 例えばランダムに )　初期化する
(2) 以下を適当な回数繰り返す
   (2-1) 学習データセットから一つの学習例を選び、ニューラルネットワークに与えて出力を計算する
   (2-2) 教師データとニューラルネットの出力を比較し、誤差が小さくなるよう重みとしきい値を調節する
```
- ニューラルネットの出力と教師データが一致すれば学習を終了する
- 重みとしきい値の調節が問題
- 遺伝的アルゴリズムよりも、バックプロパゲーションのほうが効率的

<br>

# ニューラルネットの種類
### 2入力3階層のフィードフォワード型ネットワーク
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/2_3Feedback.png" width="80%">

- 人口ニューロンや階層を増やせる
- ネットワークの形式を変えれる
  - 層間の結合は必ずしも全結合させる必要がない
  
<br>

### リカレントネットワーク ( Recurrent Network )
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/Recurrent.png" width="80%">

- ホップフィールドモデルに基づく
- ネットワークを構成するすべてのニューロンの入力は、自分以外の人口ニューロンの出力となる

<br>

# サンプルプログラム
```C
/******************************************************/
/*          neuron.c                                  */
/*  単体の人工ニューロンの計算　　                       */
/*  適当な重みとしきい値を有する人工ニューロンを模擬します */
/*  使い方　　                                         */
/******************************************************/

/* Visual Studioとの互換性確保 */
#define _CRT_SECURE_NO_WARNINGS 

/* ヘッダファイルのインクルード */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* 記号定数の定義 */
#define INPUTNO 2       /* 入力層のセル数 */
#define MAXINOUTNO 100  /* データの最大個数 */

/* 関数のプロトタイプの宣言 */
double f(double u);                                         /* 伝達関数 */
void initw(double w[INPUTNO + 1]);                          /* 重みとしきい値の初期化 */
double forward (double w[INPUTNO + 1],double e[INPUTNO]);   /* 順方向の計算 */
int getdata(double e[][INPUTNO]);                           /* データの読み込み */


/************************/
/*      main()関数      */
/************************/
int main(){
    double w[INPUTNO + 1];              /* 中間層の重み */
    double e [MAXINOUTNO][INPUTNO];     /* データセット */
    double o;                           /* 出力 */
    int i,j;                            /* 繰り返しの制御 */
    int n_of_e;                         /* データの個数 */

    /* 重みの初期化 */
    initw(w);

    /* 入力データの読み込み */
    n_of_e = getdata(e);
    printf("データの個数:%d\n", n_of_e);

    /* 計算の本体 */
    for (i = 0; i < n_of_e; ++i){
        printf("%d ", i);
        for(j = 0; j < INPUTNO ; ++j){
            printf("%lf ", e[i][j]);
        }
        o = forward(w, e[i]);
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
double forward (double w[INPUTNO + 1],double e[INPUTNO])
{
    int i;      /* 繰り返しの制御 */
    double u,o; /* 途中の計算値uと出力o */

    /* 計算の本体 */
    u = 0;
    for (i = 0; i< INPUTNO; ++i)
    {
        u += e[i] * w[i];
    }
    u -= w[i]; /* しきい値の処理 */
    /* 出力値の計算 */
    o = f(u);
    return o;
}

/**************************/
/*      initw()関数      */
/*  中間層の重み初期化    　*/
/**************************/
void initw(double w[INPUTNO + 1])
{
    /* 荷重を定数として与える */
    w[0] = 1;
    w[1] = 1;
    w[2] = 1.5;
    // w[2] = 0.5;
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
```
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/Neuron_C.png)

### w2のしきい値を1.5にしたとき
- AND
```
c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram>cd "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\" && gcc -fexec-charset=CP932 neuron.c -o neuron && "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\"neuron
data24.txt
データの個数:4
0 0.000000 0.000000 0.000000
1 0.000000 1.000000 0.000000
2 1.000000 0.000000 0.000000
3 1.000000 1.000000 1.000000
```
### w2のしきい値を0.5にしたとき
- OR
```
C:\Users\TN256\OneDrive\ドキュメント\謝研>cd "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\" && gcc -fexec-charset=CP932 neuron.c -o neuron && "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\"neuron
data24.txt
データの個数:4
0 0.000000 0.000000 0.000000
1 0.000000 1.000000 1.000000
2 1.000000 0.000000 1.000000
3 1.000000 1.000000 1.000000
```


<br>

```C
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
```
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Source/nn_c.png)
### EOR ( 排他的論理和 )
```
C:\Users\TN256\OneDrive\ドキュメント\謝研>cd "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\" && gcc -fexec-charset=CP932 nn.c -o nn && "c:\Users\TN256\OneDrive\ドキュメント\謝研\AIProgram\"nn
data24.txt
データの個数:4
0 0.000000 0.000000 0.000000
1 0.000000 1.000000 1.000000
2 1.000000 0.000000 1.000000
3 1.000000 1.000000 0.000000
```
