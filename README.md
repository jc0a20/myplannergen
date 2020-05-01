# myplannergen 0.01
<img width="800" src="./doc/01.jpg">

SVGのテンプレートファイルとCSVのコンテンツファイルを使って手帳のPDFを作るソフトウェアです。

## 大まかな使い方
1. SVGで手帳の原型(テンプレート)を作る
1. CSVで中身(何年・何月・何日・何曜日・何の日・何色...など)を作る
1. Pythonスクリプトで，SVGテンプレートの中身をCSVに従って置換し，中綴じを考慮したページ割り付けの手帳用SVGを作る
1. 手帳用SVGをバッチファイルなどでPDFに変換する
1. PDFを両面印刷して中綴じ製本する

現状，SVGの形を変えたりCSVの中身を変えたりするのは容易ですが，まだPythonスクリプト内埋め込みの要素が多く柔軟性が足りません。

## 詳しい使い方
上のバウンダリから順に作業を行っていきます。

<img width="800" src="./doc/abst.png">

|  図中の名前  |  ファイル名 or ディレクトリ名  |
| ---- | ---- |
|  テンプレートSVG  |  [template.svg](template.svg), [template_cutline.svg](template_cutline.svg)  |
|  コンテンツCSV  |  [contents.csv](contents.csv)  |
|  手帳用SVG生成Pythonスクリプト  |  [planner_svg_gen.py](planner_svg_gen.py)  |
|  手帳用SVG(1ページ1ファイル)  |  [export_svg/](export_svg)  |
|  SVG-PDF変換バッチファイル  |  [svg2pdf.bat](svg2pdf.bat)  |
|  変換対象SVGファイルリスト  |  [export_pdf/inkscape_export_pdf_list_svg.txt]()  |
|  手帳用PDF(1ページ1ファイル)  |  [export_pdf/](export_pdf)  |
|  手帳用PDF(結合済)  |  [doc/combined_pdf.pdf](doc/combined_pdf.pdf)  |

planner_svg_gen.pyは Python 3.6.8 で動作確認しました。なお，標準ライブラリのみで作成しています。

svg2pdf.batはwindows10で動作確認しました。


## 次の目標
* Python実行，バッチファイル実行，PDF結合をいちいちやらなくても良い様にする
* 他の人が作った手帳のデータを共有できるようにする

<img width="700" src="./doc/next_milestone.png">


## SVGに関する解説
SVG内の各パーツのIDに，以下のような名前を振っています。
Pythonスクリプトは，このIDを用いてSVG内の文字の置換をしています。

<img width="800" src="./doc/svg_template_comment.png">

裁断線は，少し大きめに引いてあります。大きめにしないと，裁断したときに内側のページの端が切れてしまいます。

<img width="800" src="./doc/template_cutline_comment.png">

## 印刷-製本に関する解説
印刷は以下のような設定で行いました。(EPSONのインクジェットプリンタの例)

<img width="500" src="./doc/print1.png">

片面を刷り終えたところで以下のようなダイアログが出たので指示通りに裏返して印刷しました。

<img width="300" src="./doc/print2.png">

印刷した結果は以下のようになります。

<img width="600" src="./doc/02.jpg">

使えそうな中綴じホッチキスが見つけられなかったので，穴をあけて手でホチキス針を通すことにしました。

<img width="600" src="./doc/03.jpg">

<img width="600" src="./doc/04.jpg">

最後に裁断して完成です。折り曲げた後に裁断した方が良いです。
裁断した後に折り曲げた場合，真ん中のページが外にはみ出てしまいページめくりがやりにくくなります。

<img width="600" src="./doc/05.jpg">

## License
本ソフトウェアは[MITライセンス](./LICENSE)の元提供されています。

## Acknowledgments
SVGをPDFに変換するバッチファイルについて，以下のサイトを参考にしました。
[複数のsvgをまとめてpdfへ変換する - Inkscape&バッチファイル](http://rorokuusou.hatenablog.com/entry/2016/12/20/000348)

今回のSVGテンプレート作成にあたって，左右に日付があるホリゾンタルの構成として以下を参考にしました。
[MIDORI 月間＋月間ホリゾンタル](https://www.midori-store.net/diary2018/item/for_month_h.html)
