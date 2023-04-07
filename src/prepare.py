# しりとりの辞書作成
import sudachipy


def load_text(path: str):
    """ファイルからテキスト読み込み

    Args:
        path (str): 読み込むテキストファイルのパス

    Returns:
        str: 読み込んだテキスト
    """
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()


def create_dict(text: str):
    tokenizer = sudachipy.Dictionary().create()
    res_dict: dict[str, set[str]] = {}

    text.replace("/n", "")  # テキストから改行を削除
    sentences = text.split("。")  # [。]で分けて文章ごとにリストにする

    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)  # 形態素解析実行
        for token in tokens:
            # その単語が名詞(ID: 4)ではないならループの先頭に戻る
            if token.part_of_speech_id() != 4:
                continue

            # 最後が"ん"なら無視
            if token.reading_form()[-1] == "ン":
                continue

            key = token.reading_form()[0]  # 読みの初めの文字
            res_dict.setdefault(key, set())
            res_dict[key].add(token.surface())

    return res_dict


if __name__ == "__main__":
    import pickle
    import config as conf

    config = conf.get_config()

    text = load_text(config["text_path"])
    with open(config["dict_path"], mode="wb") as file:
        pickle.dump(create_dict(text), file)
