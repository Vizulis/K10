from tkinter import *
from tkinter import ttk  # Necessary for the modern dropdown (Combobox)
import random
# from main import Node, GameTree, build_tree, best_move

root = Tk()  # izmanto lai izveidotu logu
root.title("Sequence game")  # tas izveidos nosaukumu logam
root.geometry("1200x600+60+50")  # tas ir loga atrašanas un izmēra iestatījumi, kad logs paradas. Shēma: logaPlatumsxlogaAugstums+atkāpeNoKreisasPuses+atkāpeNoAugšas

############################################## "START MENU" DEVELOPMENT STARTS
l_length = Label(text="Enter sequence length (15-50)", width=80)
l_mode_dropdown = Label(text="Choose game mode:", width=80) # я переместила сюда, чтобы все label были в одном месте
mode_options = [
    "AI vs AI",
    "AI vs Human (Human starts)"
    "AI vs Human (AI starts)"
]
l_algo_dropdown = Label(text="Choose Algorithm:")
l_player1_points = Label(text="Player_1 points:") # наверное надо еще дописать в скобках, чтобы передать параметр того, сколько у игрока в данный момент очков
l_player2_points = Label(text="Player_2 points:") # наверное надо еще дописать, чтобы передать параметр того, сколько у игрока в данный момент очков
l_player1_move = Label(text="Player_1 removed:") # наверное надо еще дописать, чтобы передать параметр того, какую цифру убрал игрок
l_player2_move = Label(text="Player_2 removed:") # наверное надо еще дописать, чтобы передать параметр того, какую цифру убрал игрок
l_virkne = Label(text="virkne bus seit") # это поле, в котором будет храниться сначала сгенерированная virkne, и потом будет обновляться после ходов игроков
l_nodes_generated = Label(text="genereto virsotnu skaits") # будет показывать сколько вершин сгенерировал ии

get_choice_length = IntVar(value=15)  # Iestatām noklusējuma vērtību 15
get_choice_mode_text = StringVar()  # Šis glabās tekstu no dropdowna
get_choice_algorithm = StringVar()  # Šis glabās izvēlēto algoritmu

e_choice_length = Entry(textvariable=get_choice_length, width=40)  # lauki, kuros lietotājs ieraksta atbildi
e_choice_mode = ttk.Combobox(textvariable=get_choice_mode_text, values=mode_options, state="readonly", width=40)
e_choice_mode.current(1)  # Uzliek noklusējumu uz "AI vs Human (Human starts)"

algo_options = ["minimax", "alpha-beta"]
e_choice_algorithm = ttk.Combobox(textvariable=get_choice_algorithm, values=algo_options, state="readonly", width=40)
e_choice_algorithm.current(1)  # Uzliek noklusējumu uz "alpha-beta"


def start_game():
    sequence_length = get_choice_length.get()

    # Loģika, lai pārvērstu dropdown tekstu atpakaļ skaitļos dzinējam
    mode_text = get_choice_mode_text.get()
    algorithm = get_choice_algorithm.get()

    mode = 0
    who_first = 0

    if mode_text == "AI vs AI":
        mode = 1
        who_first = 2
    elif mode_text == "AI vs Human (Human starts)":
        mode = 2
        who_first = 1
    elif mode_text == "AI vs Human (AI starts)":
        mode = 2
        who_first = 2


    ########### Vremenno:
    print(f"Length: {sequence_length}, Mode: {mode}, Who starts: {who_first}, Algo: {algorithm}")
    ###########


def end_of_game(): # эта функция должна вызываться после последнего возможного хода и выводить очки обоих игроков, кто выиграл, и внизу должна быть кнопка b_start_new_game начать новую игру
    end_window = Toplevel()
    end_window.title("Game is over")
    end_window.geometry("600x600")
    #в Toplevel(), то есть в дочернем окне, всё создается точно так же, как и в основном окне, просто надо вместо root
    #писать имя окна, и в атрибутах всегда перым прописать окно, в котором все будет происходить
    l_p1_score = Label(end_window, text="Player_1 score:", width=40)
    l_p2_score = Label(end_window, text="Player_2 score:", width=40)
    l_winner = Label(end_window, text="Winner:", width=40)

    # b_start_new_game = Button(end_window, text="Start new game", command=new_game) Эту кнопку я хочу использовать как кнопку, которая все обнулит и можно будет начать новую игру.
    # #Эта кнопка должна появиться в окне номер 2, то есть в окне, где выводится инфо об финале игры, победителе и очках.
    l_p1_score.grid(row=1, column=1, pady=20)
    l_p2_score.grid(row=2, column=1, pady=20)
    l_winner.grid(row=2, column=1, pady=20)
    #b_start_new_game.grid(row=4, column=2, pady=20)


def statistics(): # эта функция должна появляться в конце каждой игры, и хранить в себе информацию о всех партиях. С плана- это окно номер три
    stats_window = Toplevel()
    stats_window.title("Statistics")
    stats_window.geometry("700x600")

    #таблица из 5 записей для минимакса(в эти строки потом будут вписываться записи про результаты):
    l_info_minmax = Label(stats_window, text="Minimax statistics", width=40)
    l_minm_seq1_length = Label(stats_window, text="", width=40)
    l_minm_seq2_length = Label(stats_window, text="", width=40)
    l_minm_seq3_length = Label(stats_window, text="", width=40)
    l_minm_seq4_length = Label(stats_window, text="", width=40)
    l_minm_seq5_length = Label(stats_window, text="", width=40)
    l_time_seq1_minmax = Label(stats_window, text="", width=40) #если получится, то я думала среднее время от построения деревьев сюда для каждой отдельной игры
    l_time_seq2_minmax = Label(stats_window, text="", width=40)
    l_time_seq3_minmax = Label(stats_window, text="", width=40)
    l_time_seq4_minmax = Label(stats_window, text="", width=40)
    l_time_seq5_minmax = Label(stats_window, text="", width=40)

    #таблица из 5 записей для альфа-беты
    l_info_alfbet = Label(stats_window, text="Alpha-beta statistics", width=40)
    l_alfbet_seq1_length = Label(stats_window, text="", width=40)
    l_alfbet_seq2_length = Label(stats_window, text="", width=40)
    l_alfbet_seq3_length = Label(stats_window, text="", width=40)
    l_alfbet_seq4_length = Label(stats_window, text="", width=40)
    l_alfbet_seq5_length = Label(stats_window, text="", width=40)
    l_time_seq1_alfbet = Label(stats_window, text="", width=40)
    l_time_seq2_alfbet = Label(stats_window, text="", width=40)
    l_time_seq3_alfbet = Label(stats_window, text="", width=40)
    l_time_seq4_alfbet = Label(stats_window, text="", width=40)
    l_time_seq5_alfbet = Label(stats_window, text="", width=40)

    l_info_minmax.grid(row=1, column=1, pady=20)
    l_minm_seq1_length.grid(row=2, column=1, pady=5)
    l_minm_seq2_length.grid(row=3, column=1, pady=5)
    l_minm_seq3_length.grid(row=4, column=1, pady=5)
    l_minm_seq4_length.grid(row=5, column=1, pady=5)
    l_minm_seq5_length.grid(row=6, column=1, pady=5)
    l_time_seq1_minmax.grid(row=2, column=2, pady=5)
    l_time_seq2_minmax.grid(row=3, column=2, pady=5)
    l_time_seq3_minmax.grid(row=4, column=2, pady=5)
    l_time_seq4_minmax.grid(row=5, column=2, pady=5)
    l_time_seq5_minmax.grid(row=6, column=2, pady=5)
    l_info_alfbet.grid(row=7, column=1, pady=20)
    l_alfbet_seq1_length.grid(row=8, column=1, pady=5)
    l_alfbet_seq2_length.grid(row=9, column=1, pady=5)
    l_alfbet_seq3_length.grid(row=10, column=1, pady=5)
    l_alfbet_seq4_length.grid(row=11, column=1, pady=5)
    l_alfbet_seq5_length.grid(row=12, column=1, pady=5)
    l_time_seq1_alfbet.grid(row=8, column=2, pady=5)
    l_time_seq2_alfbet.grid(row=9, column=2, pady=5)
    l_time_seq3_alfbet.grid(row=10, column=2, pady=5)
    l_time_seq4_alfbet.grid(row=11, column=2, pady=5)
    l_time_seq5_alfbet.grid(row=12, column=2, pady=5)


b_start_game = Button(text="Start", command=start_game)
b_one = Button(text="1", width=5) # DODELATJS VSE KNOPKI-CIFRI, например, добавить command(склоняюсь к комманд) или добавить части для bind(), чтобы кнопки стали функциональными
b_two = Button(text="2", width=5)
b_three = Button(text="3", width=5)
b_four = Button(text="4", width=5)
b_five = Button(text="5", width=5)
# эти кнопки нужны для того, чтобы пользователь выбирал цифру, которую хочет убрать из ряда, и нажав на кнопку, эта цифра была стерта

# все храниться в том порядке, в каком все появляется на окне
l_length.grid(row=1, column=6, pady=5)
e_choice_length.grid(row=2, column=6, pady=5)

l_mode_dropdown.grid(row=3, column=6, pady=5)
e_choice_mode.grid(row=4, column=6, pady=5)

l_algo_dropdown.grid(row=5, column=6, pady=5)
e_choice_algorithm.grid(row=6, column=6, pady=5)

b_start_game.grid(row=7, column=7, pady=20)

l_player1_points.grid(row=8, column=1, pady=20)
l_player2_points.grid(row=8, column=7, pady=20)
l_player1_move.grid(row=9, column=1, pady=20)
l_player2_move.grid(row=9, column=7, pady=20)
b_one.grid(row=10, column=1, padx=10, pady=10)
b_two.grid(row=10, column=2, padx=10, pady=10)
b_three.grid(row=10, column=3, padx=10, pady=10)
b_four.grid(row=10, column=4, padx=10, pady=10)
b_five.grid(row=10, column=5, padx=10, pady=10)
l_virkne.grid(row=12, column=6, pady=20)
l_nodes_generated.grid(row=13, column=6, pady=20)

############################################## "START MENU" DEVELOPMENT ENDS


root.mainloop()
