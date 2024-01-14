import os
import random

def read_file(file_path):
    try:
        # UTF-8 エンコーディングを指定してファイルを読み込む
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return None
    except UnicodeDecodeError:
        try:
            # UTF-8で読み込めなかった場合、CP932で再試行
            with open(file_path, 'r', encoding='cp932') as file:
                return file.read()
        except UnicodeDecodeError:
            print("File encoding is not supported.")
            return None

def create_binary_list(length, percentage):
    num_ones = int(length * (percentage / 100))
    num_zeros = length - num_ones

    # 0と1のリストを作成
    binary_list = [1] * num_ones + [0] * num_zeros
    # リストをランダムに並び替え
    random.shuffle(binary_list)

    return binary_list

def process_text(text, binary_list):
    modified_text = list(text)
    for i in range(len(modified_text)):
        if binary_list[i] == 0 and modified_text[i] != '\n':
            modified_text[i] = '*'
    return ''.join(modified_text)

def write_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def valid_percentage_input(input_str):
    try:
        percentage = int(input_str)
        if 0 <= percentage <= 100:
            return True
        else:
            return False
    except ValueError:
        return False

def get_percentage_input():
    while True:
        user_input = input("文章が読める割合を入力してください Enter a percentage (0-100): ")
        if valid_percentage_input(user_input):
            return int(user_input)
        else:
            print("Invalid input. Please enter an integer between 0 and 100.")

def process_all_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            file_content = read_file(file_path)

            if file_content is not None:
                text_length = len(file_content)
                percentage = get_percentage_input()  # ユーザーに入力してもらう
                binary_list = create_binary_list(text_length, percentage)
                processed_text = process_text(file_content, binary_list)

                new_file_path = os.path.join(directory, "Corrupt_" + filename)
                write_to_file(new_file_path, processed_text)
                print(f"Processed file saved as {new_file_path}")

# 現在のディレクトリを取得して、すべてのテキストファイルを処理
current_directory = os.getcwd()
process_all_txt_files(current_directory)