# Static factory methodの使い所

## 結論

副作用があるコンストラクタが必要な場合は、代わりにStatic factory methodを用いる。

## だめな例

```java
public class World {

    private final AnimalController animalController;
    private final TerrainController terrainController;

    public World() {
        this.animalController = new AnimalController();
        this.terrainController = new TerrainController();
        ExecutorService executorService = Executors.newWorkStealingPool();
        executorService.submit(animalController::spawnRandom);
        executorService.submit(terrainController::generateSurface);
    }
}
```

この例では、Worldのコンストラクタが呼ばれると、AnimalControllerとTerrainControllerが初期化され、非同期で地形を生成して動物を出現させている。この例がなぜだめなのかというと、Worldの内部実装を知らないプログラマーが

```java
new World();
```

したときに、おそらくそのプログラマーは同時に地形や動物が出現するとは想定できないところである。またそれ以外にもスレッドプールを作成しているため、プログラマーはコンストラクタを呼び出したときにスレッドの処理や破棄のタイミングといった方法まで考えなくてはいけない。コンストラクタは非常に高い頻度で使用されるため、コンストラクタを呼び出したときに一々副作用を考えなくてはいけないのはプログラマーにとって理想的でない。

プログラマーはデフォルトコンストラクタを見ると、そのオブジェクトがPOJOとして利用されているか、少なくともコンストラクタは外部に対して影響を及ぼさないと考えることが多い。

したがってコンストラクタを呼び出したときに、外部に副作用をもたらすコードは望ましくない。

## 良い例

```java
public class World {

    private final AnimalController animalController;
    private final TerrainController terrainController;

    public World(AnimalController animalController, TerrainController terrainController) {
        this.animalController = animalController;
        this.terrainController = terrainController;
    }

    public static World createEarth() {
        AnimalController animalController = new AnimalController();
        TerrainController terrainController = new TerrainController();
        World world = new World(animalController, terrainController);

        ExecutorService executorService = Executors.newWorkStealingPool();
        executorService.submit(animalController::spawnRandom);
        executorService.submit(terrainController::generateSurface);

        return world;
    }
}
```

上のコードでは、Worldがコンストラクタの他にもStatic Factoryメソッドを持っている。これによりWorldのコンストラクタを呼んでも副作用が発生しないだけでなく、ユニットテストのしやすさを上げることにもつながる。

## 注意点

### クラス名から副作用があることを推測できる場合はコンストラクタに副作用があっても良い

InputStream、OutputStream、Writer、Reader等の接尾辞がクラス名に付く場合は、コンストラクタに副作用があっても良い。コンストラクタを呼び出すとき、クラス名から副作用があることが推測でき、副作用の存在を忘れて不具合を発生させることがないためである。

### 副作用がない場合でもStatic method factoryは使用できる。

Boolean#of、Integer#valueOfといったメソッドは副作用がないがStatic method factoryである。これら副作用のないStatic method factoryの多くは、慣用的なメソッド名（of、valueOf等）を使用していることが特徴である。
