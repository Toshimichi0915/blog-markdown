# 1. Adapter Design Patternとユニットテスト

API間での差分を吸収するときに使う。また使用するAPIが余りにも巨大でユニットテストし辛いとき、Adapter Design Patternを使えば解決できる場合がある。

## 問題のコード

```java
public interface MoneyManager {

    // 所持金を取得する
    int balance(User user);

    // お金を引き出す
    void withdraw(User user, int amount);

    // お金を預ける
    void deposit(User user, int amount);

    // 新規口座を開設する
    BankAccount createBankAccount(User user);

    // 口座を閉鎖する
    void deleteBankAccount(BankAccount account);

    // 口座情報を更新する
    void updateBankAccount(BankAccount account, BankAccountUpdate update);
    
    // 口座を凍結する
    void freezeBankAccount(BankAccount account);

    ...
}
```

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final MoneyManager moneyManager;
    private final Logger logger;

    // 商品を購入する
    public void purchase(User user, Product... products) {
        for(Product product : products) {
            moneyManager.withdraw(product.getPrice());
            logger.debug(user.getName() + "の所持金が" + wallet.balance(user) + "になりました");
            user.addProperty(product);
        }
    }
}
```

上記のような、お金を管理する「MoneyManager」と商品を購入するのに必要な「ProductService」があるとする。この際ProductServiceをテストするためにはMoneyManagerをモックする必要があるが、withdrawを呼ばれた段階でbalanceの値は変化するはずで、そういった状態をモッキングライブラリで管理するのはなかなか大変な上に再利用性が低い。またMoneyManagerを実装するユニットテスト用のクラスを作成するという方法もあるが、メソッドが大量にある場合や副作用が予測しきれない場合、そういった手段が取れない場合がある。

ProductServiceがMoneyManagerの銀行口座管理機能を必要としていないことに着目すると、MoneyManagerから預金の確認、出金、入金機能だけ切り出すことで、簡潔かつ安全にユニットテストが行えるはずである。

そこで、預金の確認、出金、入金機能だけがあるWalletインターフェースを作成してProductServiceを書き換えてみる。

## ユニットテスト可能なコード

```java
public class Wallet {
    
    // 所持金を取得する
    int balance(User user);

    // お金を引き出す
    void withdraw(User user, int amount);

    // お金を預ける
    void deposit(User user, int amount);
}
```

```java
@RequiredArgsConstructor
public class MoneyManagerWallet implements Wallet {

    private final MoneyManager moneyManager;

    @Override
    public int balance(User user) {
        return moneyManager.balance(user);
    }

    @Override
    public void withdraw(User user, int amount) {
        return moneyManager.withdraw(user, amount);
    }

    @Override
    public void deposit(User user, int amount) {
        return moneyManager.deposit(user, amount);
    }
}
```

```java
@Service
@RequiredArgsConstructor
public class ProductService {

    private final Wallet wallet;
    private final Logger logger;

    // 商品を購入する
    public void purchase(User user, Product... products) {
        for(Product product : products) {
            wallet.withdraw(product.getPrice());
            logger.debug(user.getName() + "の所持金が" + wallet.balance(user) + "になりました");
            user.addProperty(product);
        }
    }
}
```

これでProductServiceはMoneyManagerの代わりにWalletインターフェースを使うようになった。従来通りMoneyManagerを使用してProductServiceを初期化したい際は、次のように呼び出せばいいだけである。。

```java
ProductService productService = new ProductService(new MoneyManagerWallet(...), logger);
```

次に、ユニットテスト用にWalletを実装するクラスを作ってみる。

```java
public class InMemoryWallet implements Wallet {

    private final HashMap<User, Integer> balanceMap = new HashMap<>();

    @Override
    public synchronized int balance(User user) {
        return balanceMap.getOrDefault(user, 0);
    }

    @Override
    public synchronized void deposit(User user, int amount) {
        balanceMap.put(balance(user) + amount);
    }

    @Override
    public synchronized void withdraw(User user, int amount) {
        if (balance(user) < amount) {
            throw new IllegalArgumentException("所持金が足りません");
        }

        balanceMap.put(balance(user) - amount);
    }
}
```

これだけである。使う際にはコンストラクタで

```java
ProductService productService = new ProductService(new InMemoryWallet(), logger);
```

とすれば良いだけである。

## 結論

以上により、ProductServiceのコンストラクタにInMemoryWalletを渡すことでメモリ上でユーザーの入金・出金を管理できるようになった。もし巨大なAPIに遭遇してユニットテストが行えないケースがある場合、Adapter Design Patternを使ってみるといいかもしれない。
