import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QMessageBox
)
import platform
import matplotlib

# 日本語＆マイナス記号対応
if platform.system() == "Darwin":
    matplotlib.rcParams["font.family"] = "AppleGothic"
elif platform.system() == "Windows":
    matplotlib.rcParams["font.family"] = "MS Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

class CSVPlotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSVグラフビューア")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.button = QPushButton("CSVファイルを選択してグラフ表示")
        self.button.clicked.connect(self.select_and_plot_csv)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def select_and_plot_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "CSVファイルを選択", "", "CSV files (*.csv)")
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path, encoding="cp932", encoding_errors="replace")

            if "日時" not in df.columns:
                QMessageBox.warning(self, "エラー", "CSVに『日時』列がありません。")
                return

            # 必要な処理のみ：数値列を抽出
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) == 0:
                QMessageBox.warning(self, "エラー", "数値列が見つかりませんでした。")
                return

            df = df[numeric_cols[:3]]  # 最大3列まで描画対象に
            df = df.dropna()

            # インデックスを 0, 1, 2, ... 秒とみなす（1行 = 1秒）
            df.reset_index(drop=True, inplace=True)
            df.index.name = "Time [s]"  # インデックスに名前を付けてx軸に使用

            colors = ['black', 'blue', 'magenta']
            ax = df.plot(legend=True, color=colors[:len(df.columns)])

            ax.set_xlabel("")      # X軸ラベルを非表示に強制
            plt.grid(True)         # グリッド（補助線）表示
            plt.box(True)          # 枠線表示
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "エラー", f"読み込みまたは表示中にエラーが発生しました:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVPlotApp()
    viewer.show()
    sys.exit(app.exec())
