# オセロ
### 更新したらキャッシュをクリアする！
[https://ntaku256.github.io/AI/](https://ntaku256.github.io/AI/)

# PSO(粒子群最適化)
https://qiita.com/opticont/items/04a5b4ff41483966987f


```python
class PSO:
    n_iter = None
    n_swarm = None
    w = None
    c1 = None
    c2 = None
    vectors = None
    scores = None
    g_best_score = None
    g_best_vector = None
    p_best_scores = None
    p_best_vectors = None

    def __init__(self,n_iter,n_swarm,w,c1,c2):
        self.n_iter = n_iter
        self.n_swarm = n_swarm
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.InitSwarms()
        self.CalcScores()
```
