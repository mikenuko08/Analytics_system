# python3.6.5以上で時刻を扱う時のノウハウをまとめる  
今回実装したい動作を以下に示す．  
## 1. 現在時刻を取得してそれを文字列に変換する  
## 2. 文字列になった時刻をdatetime型まで戻す.(awareなデータで返す)  

pythonで時刻を扱う時の事前知識として，nativeとawareがある．nativeとは，時刻の情報にタイムゾーン情報が付加されていないデータ型である．一方，awareは，タイムゾーンの情報が付いている．  

次にこれらの時刻を扱う為に必要なモジュールを以下に示す．  
```
from datetime import datetime  
```
-> 現在時刻などを呼び出せる(fromをつけて記述することで，メソッドを呼び出す時に，datetime.datetime.now()などとしなくて済む) 
``` 
from pytz import timezone  
```
-> タイムゾーンに関わる情報を付加できる  
```
from tzlocal import get_localzone  
```
-> 実行する環境化でのタイムゾーンがわかる  

続いて，今回実装した内容を以下に示す．  

## 1.現在時刻を取得してそれを文字列に変換する    
現在時刻を取得して文字列に変換する   
```
str_date = datetime.now().strftime('%s')  
```

## 2.文字列になった時刻をdatetime型に変換して秒を切り捨てる(awareなデータで返す)  
2-1. 実行している環境のタイムゾーンを保持する  
2-2. 文字列になっている時刻データを整数値に変換する  
2-3. 文字列になっている時刻データをawareなデータに変換する  
```
ja = get_localzone()  
int_date = int(str_date)
datetime_date = datetime.fromtimestamp(int_date)
awaretime_date = ja.localize(datetime_date)  
date = awaretime_date.replace(second=0, microsecond=0)  
```

## 今回の全てのソースコード
```
from datetime import datetime 
from pytz import timezone  
from tzlocal import get_localzone  

str_date = datetime.now().strftime('%s')  
ja = get_localzone()  
int_date = int(str_date)
datetime_date = datetime.fromtimestamp(int_date)
awaretime_date = ja.localize(datetime_date)  
date = awaretime_date.replace(second=0, microsecond=0)  
```