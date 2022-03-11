

# теория игр

print("Добро пожаловать в ТЕОРИЮ ИГР. Правила таковы:\n"
      "Есть одна куча камешков\n"
      "Вы соревнуетесь с ботом, Ваша задача - первее достичь более 32 камешков в кучке\n"
      "У Вас в распоряжении лишь два действия:\n"
      "1 - добавить 3 камешка\n"
      "2 - приумножить количество камешков в куче на 2")


bunch = 10

first_turn = input("Вы ходите первым, укажите ваше действие: ")

if first_turn == "1":
      bunch = bunch+3
      # ход бота:
      bunch = bunch+3 # 13
      third_turn = input("Ваш ход:")
      if third_turn == "1":
            bunch = bunch+3 # 16
            # ход бота:

      elif third_turn == "2":
            bunch = bunch*2 # 26


      # ход бота:
      elif bunch >= 15:
            bunch = bunch*2
            if bunch >= 30:
                  print("Выигрыш бота!")
      else:
            bunch = bunch+3
            if bunch >= 30:
                  print("Выигрыш бота!")


elif first_turn == "2":
      bunch = bunch*2
      if bunch > 15:
            bunch = bunch*2
            if bunch >= 30:
                  print("Выигрыш бота!")

# исключаем проверку на дурака, так как у нас будет колбэк

