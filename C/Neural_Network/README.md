# ニューラルネットワーク
### ニューラルネットワーク(Neural Network)
- 神経細胞(Neuron)をモデル化した計算素子である人口ニューロン(Artifical Neuron)を組み合わせたもの
### 人工ニューロン
- ニューロ素子やニューロセルとも呼ぶ。
### 神経細胞（ニューロン）
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Sorce/Neurons.png)
[画像の参考URL](https://hombre-nuevo.com/machinelearning/machinelearning0001/)

<br>

# 人口ニューロンの中
![](https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Sorce/Function.png)
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
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Sorce/StepFunction.png" width="30%">

<br>

### シグモイド関数(Sigmoid Function)
- なめらかな関数で連続的
- バックプロパゲーションにおける学習の計算処理が容易
<img src="https://github.com/ntaku256/AI/blob/main/C/Neural_Network/Sorce/SigmoidFunction.png" width="70%">

<br>

### ステップ関数による論理演算
- AND

# 人口ニューロン - 1つのセルでの処理
# ニューラルネット - 複数の人口ニューロン
### フィードフォワード型ネット(Feed Formard Neteork)
### 階層型ネットワーク(Layerd Network)
