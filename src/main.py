import sudachipy
from util import PyColor


def load_dict(path: str) -> dict[str, set[str]]:
    import pickle

    with open(path, mode="rb") as file:
        return pickle.load(file)


def valid_word(morphemes: sudachipy.MorphemeList, pre_com_word: sudachipy.MorphemeList):
    if len(morphemes) != 1:
        raise Exception("Only one word, please.")
    if morphemes[0].part_of_speech_id() != 4:
        raise Exception("Use nouns.")

    if pre_com_word != None:
        # 前の言葉の最後とユーザーの言葉の最初が違うならエラー
        pre_com_end = pre_com_word[0].reading_form()[-1]
        if pre_com_end != morphemes[0].reading_form()[0]:
            raise Exception(
                f"Start with `{pre_com_end}` because the previous word was `{pre_com_word[0].surface()}`."
            )

    return morphemes[0]


def pick_com_word(user_word: str, word_dict: dict[str, set[str]]):
    if user_word[-1] not in word_dict:
        raise Exception(
            f"Words beginning with `{user_word[-1]}` have not been learned."
        )
    if len(word_dict[user_word[-1]]) == 0:
        raise Exception(
            f"All words beginning with `{user_word[-1]}` are used and no reply is possible."
        )

    word_set = word_dict[user_word[-1]]
    com_word = list(word_set)[0]
    word_set.remove(com_word)

    return com_word


if __name__ == "__main__":
    import config as conf

    config = conf.get_config()
    tokenizer = sudachipy.Dictionary().create()

    dic = load_dict(config["dict_path"])
    used_words: set[str] = set()
    pre_com_word = None

    while True:
        user_word = input("User -> ")
        # Endと入力されたら終了
        if user_word in ["End", "end"]:
            print("Thanks for playing.")
            break

        user_word = tokenizer.tokenize(user_word)
        try:
            user_word = valid_word(
                user_word,
                None if pre_com_word == None else tokenizer.tokenize(pre_com_word),
            ).reading_form()
        except Exception as err:
            print(f'{PyColor.RED}Error! -> "{err.args[0]}"{PyColor.END}')
            continue

        # "ん"で終わっているなら負け
        if user_word[-1] == "ン":
            print('You lost because you used an "N".')
            break
        # もし使用されている単語ならもう一回
        if user_word in used_words:
            print(f"`{user_word}` is already in use.")
            continue
        # もし学習している中に存在するならそれを削除
        if user_word[-1] in dic and user_word in dic[user_word[-1]]:
            dic[user_word[-1]].remove(user_word)
        used_words.add(user_word)

        try:
            com_word = pick_com_word(user_word, dic)
            pre_com_word = com_word
        except Exception as err:
            print(f'{PyColor.RED}Com Error! -> "{err.args[0]}"{PyColor.END}')
            break
        used_words.add(com_word)

        print(f"Com -> {com_word}")
