# Persistent Data Containerなしでチェストにデータを保存する方法

チェストショップの仕組みを構築する際、本来1.17で作っていたものをとある事情で1.12.2に作り直さなければいけないことになりました。バージョンの移植自体はそう大した話ではないのですが、バージョンを下げる際にPersistent Data Containerがなくて困ったのでそのときの解決方法をメモっておきます。

## 結論
チェストにデータを保存する際は、

```java
chest.setCustomName("Chest " + ChatColorEncoder.encode(保存するデータ));
chest.update(true, false);
```

としてデータを見えない文字列に変換して保存してください。
ChatEncoderのクラスは下に貼り付けるのでそのまま使ってください（ユニットテスト済みです）。

```java
import org.bukkit.ChatColor;

import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class ChatColorEncoder {

    private static final ChatColor[] COLOR_CODES;
    private static final Map<String, Integer> INDEXES;

    static {
        COLOR_CODES = new ChatColor[16];

        HashMap<String, Integer> indexes = new HashMap<>(16);
        INDEXES = Collections.unmodifiableMap(indexes);

        for (int i = 0; i < 16; i++) {
            COLOR_CODES[i] = ChatColor.getByChar(Integer.toString(i, 16));
            indexes.put(COLOR_CODES[i].toString(), i);
        }
    }

    public static String encode(String str) {
        StringBuilder builder = new StringBuilder();
        for (byte b : str.getBytes(StandardCharsets.UTF_8)) {
            builder.append(COLOR_CODES[b >> 4]);
            builder.append(COLOR_CODES[b & 0xf]);
        }
        return builder.toString();
    }

    public static String decode(String str) {

        byte[] bytes = new byte[str.length() / 4];

        if (str.length() % 4 != 0) {
            throw new IllegalArgumentException("String length is invalid: " + str);
        }

        for (int i = 0; i < str.length() / 4; i++) {
            int offset = i * 4;

            String s1 = str.substring(offset, offset + 2);
            String s2 = str.substring(offset + 2, offset + 4);
            Integer d1 = INDEXES.get(s1);
            Integer d2 = INDEXES.get(s2);

            if (d1 == null) {
                throw new IllegalArgumentException("Invalid character: " + s1);
            }
            if (d2 == null) {
                throw new IllegalArgumentException("Invalid character: " + s2);
            }

            int data = (d1 << 4) + d2;
            bytes[i] = (byte) data;
        }

        return new String(bytes, StandardCharsets.UTF_8);
    }
}

```

## 詳細
チェストにデータを保存する場合はチェストの内部にデータが含まれたアイテムを置いて保存する方法もありますが、ホッパーと干渉するので今回のケースでは許容できませんでした。そして生み出した策が、「チェストのタイトルに見えない文字列を貼り付けてデータとして保存しよう」という作戦です。この作戦であれば、かまどといった他の一部ブロックでも使用可能です。

マインクラフトでは装飾コードはクライアントで表示されないため、それを利用して見えない場所にデータを大量に保存しています。ただし注意点として、本来日本語環境であればチェストのタイトルは「チェスト」と表示されますがタイトルを変更しているため日本語環境でも「Chest」と表示されます。またブロックが壊れた際にチェストのタイトルがそのまま残ってしまうのでスタックできなくなります。この問題は、チェストが壊れた際にタイトルをリセットすることで解決できます。

## ChatColorEncoderの仕組み
エンコード時は、

1. 文字列をbyte配列に変換
2. byte配列を4ビットずつに分割
3. 4ビットとChatColorを一対一で関連付ける

という手順でエンコードしています。デコード時は単に逆の方向にするだけで、

1. ChatColorを4ビットに変換
2. 2つの4ビットを組み合わせて一つのbyteを作成
3. ChatColorが尽きるまで読み込んで、byte配列に変換

という手順です。

