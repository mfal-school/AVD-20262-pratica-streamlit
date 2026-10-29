"""Reproduz as transformações do Colab e exporta o CSV usado pelo app.

Execute da raiz: python scripts/prepare_data.py
"""

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/"
    "lucasyukioimafuko/brasileirao-serie-a-2006-2022?datasetVersionNumber=19"
)


def main():
    raw_path = ROOT / "data/raw/brasileirao.csv"
    if not raw_path.exists():
        with urlopen(SOURCE_URL, timeout=60) as response:
            with ZipFile(BytesIO(response.read())) as archive:
                raw_bytes = archive.read("brasileirao.csv")
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw_bytes)

    df = pd.read_csv(raw_path)
    # Mesmas transformações da EDA: mantém registros e outliers originais.
    df["saldo_resultado"] = np.where(
        df["goals_diff"] > 0, "Saldo positivo", "Saldo não positivo"
    )
    df["goals_log"] = np.log1p(df["goals"])

    destination = ROOT / "data/clean/dataset.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    print(f"Exportadas {len(df)} campanhas para {destination}")


if __name__ == "__main__":
    main()
