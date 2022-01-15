class Main:
    def __init__(self) -> None:
        self.values = {} # переменные хранятся тут так: имя: значение
        self.get_code()
        self.commands_init()
        self.обработка_кода()
        self.обработка_сценариев()
        self.обработка_сценария_start()
        self.исполнение_сценария_start()

    def get_code(self):
        """ цель: получить код """
        self.code = open(
            input("FILENAME: ")+".sch", # sch расширение файлов языка
            "r", encoding="utf-8"
        ).readlines() # получить код по линиям
    
    def обработка_кода(self):
        """ цель: подгатовить код к чтению """
        print() # пропуск одной строки для разделения
        for line in range(len(self.code)):
            # убрать символ пропуска строк
            self.code[line] = self.code[line].replace("\n", "")
            # вывести строку в консоль
            print(self.code[line])
        print() # пропуск одной строки для разделения

    def обработка_сценариев(self):
        """ цель: получить сценарии """
        self.сценарии = {}
        linecount = 0
        for line in self.code:
            linecount += 1
            # проверка строки на то что она является началом сценария или нет
            if line[:4] != "    " and ":" in line:
                # обработка строки
                line = line.replace(":", "")
                line = line.split(" ", 1)
                name = line[0]
                endline = 0
                # поиск конца сценария
                for line_end in self.code[linecount::]:
                    endline += 1
                    if line_end == "    END":
                        endline = endline+linecount-1
                        break
                # добавление сценаря в список сценариев
                self.сценарии[name] = {
                    "args": None if len(line) == 1 else line[1].split(","),
                    "start_line": linecount,
                    "end_line": endline
                }

        # вывод сценариев в консоль
        for сценарий in self.сценарии:
            print(сценарий, self.сценарии[сценарий])
        print() # пропуск одной строки для разделения
    
    def обработка_сценария_start(self):
        """ цель: начать читать код """
        # получение значений сценария start
        start = self.сценарии["start"]["start_line"]
        end = self.сценарии["start"]["end_line"]
        print("START <->")
        # вывод обработка кода старта, добавление в отдельный список, и вывод в консоль
        self.start_code = []
        for line in self.code[start:end]:
            line = line[4:]
            self.start_code.append(line)
            print(line)
        print() # пропуск одной строки для разделения

    def исполнение_сценария_start(self):
        print("START RESULT <->")
        for line in self.start_code:
            name, args = self.значения_line(line)
            if name in self.commands:
                self.commands[name](args)
            elif name in self.сценарии:
                self.исполнение_сцнария(name, args)
    
    def исполнение_сцнария(self, name, args):
        start = self.сценарии[name]["start_line"]
        end = self.сценарии[name]["end_line"]
        # создание словаря аргументов
        new_args = {}
        i = 0
        for arg in self.сценарии[name]["args"]:
            new_args[arg] = args[i]
            i += 1
        # запуск кода сценария
        for line in self.code[start:end]:
            line = line[4:]
            com_name, com_args = self.значения_line(line)
            # переопределение аргументов в сценарии на указаные
            for i in range(len(com_args)):
                if com_args[i] in new_args:
                    com_args[i] = new_args[com_args[i]]
            # исполнение
            if com_name in self.commands:
                self.commands[com_name](com_args)
            elif com_name in self.сценарии:
                self.исполнение_сцнария(com_name, com_args)
    
    def значения_line(self, line: str):
        line = line.split(" ", 1)
        name = line[0]
        args = line[1].split(",")
        return name, args
    
    def commands_init(self):
        self.commands = {
            "ch.mov": self.ch_mov,
            "ch.add": self.ch_add,
            "ch.out": self.ch_out
        }
    
    def ch_mov(self, args):
        self.values[args[0]] = int(args[1])

    def ch_add(self, args):
        self.values[args[0]] += self.values[args[1]]
    
    def ch_out(self, args):
        print(self.values[args[0]])


if __name__ == '__main__':
    Main()