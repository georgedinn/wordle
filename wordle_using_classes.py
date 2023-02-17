import os
os.system('cls')
import random


class getting_from_file:
    def __init__(self, file_name: str):
        """"""
        self.file_name = file_name
        self.contents_of_file = list()
        try:
            fn = open(self.file_name, 'r') 
            for i in fn:
                i = i.strip()
                self.contents_of_file.append(i)                   
        except:
            fn = ''

    def get_random_word(self):
        """"""
        try:
            self.random_word = random.choice(self.contents_of_file)
        except:
            self.random_word = ''
        return self.random_word

    def get_list(self):
        """"""
        return self.contents_of_file

    def get_list_count(self):
        return len(self.contents_of_file)

    def see_if_file_real(self):
        crash = False
        try:
            i = open(self.file_name)
        except:
            crash = True
        return crash

  
class getting_users_guess:
    def __init__(self, users_guess: str, list_name: list):
        """"""
        self.users_guess = users_guess
        self.list_name = list_name

    def validate_guess(self):
        """"""
        if self.users_guess in self.list_name:
            return True
        else:
            return False

    def get_users_guess(self):
        """"""
        return self.users_guess

    def breaking_loop(self):
        """"""
        if self.users_guess == 'break':
            return True
        else: 
            return False

    def get_list(self):
        return self.list_name


class scoring:
    def __init__(self, users_guess: str, answer: str):
        """"""
        self.users_guess = users_guess
        self.answer = answer

    def comparing(self):
        """"""
        self.scoring = ''
        self.answer_list = list()
        not_crashed = True
        try:
            for i in self.answer:
                self.answer_list.append(i)  
            count = 0
            for i in self.users_guess:
                if i in self.answer_list:
                    if i == self.answer_list[count]:
                        self.scoring += "X "
                    else:
                        self.scoring += "O "
                else:
                    self.scoring += "_ "
                count += 1
        except: 
            not_crashed = False
            return ''
        if not_crashed:
            return self.scoring

    def seeing_if_input_match(self):
        """"""
        if self.users_guess == self.answer:
            return True
        else:
            return False
    
    def get_users_guess(self):
        """"""
        return self.users_guess
    
    def get_answer(self):
        """"""
        return self.answer

    def different_lengths(self):
        """"""
        if len(self.users_guess) == len(self.answer):
            return False
        else: 
            return True


class storing_progress:
    def __init__(self):
        """"""
        self.users_guess = list()
        self.score = list()

    def store_word_guessed(self, to_store: str):
        """"""        
        self.users_guess.append(to_store)

    def get_users_guess(self):
        """"""
        return self.users_guess

    def store_scoring(self, to_store: str):
        """"""
        self.score.append(to_store)

    def get_score(self):
        """"""
        return self.score


def users_guess(list_name: list):
    """"""  
    while True:
        users_guess = getting_users_guess(input("enter a word: "), list_name)
        if users_guess.validate_guess():
            return users_guess.get_users_guess()           
        else: 
            print(f'needs to be a valid word\n')


def wordle():
    """"""
    find_answer = getting_from_file('target_words.txt')
    find_possible_guess = getting_from_file('all_words.txt')  
    storage = storing_progress() 
    answer = find_answer.get_random_word()
    count = 0
    while True:
        os.system('cls')
        print(f'answer: {answer}\t\tattempt: {count + 1} / 6\n')
        count_2 = 0
        for i in storage.get_users_guess():
            print(f'  {i}\t\t\t', end='') 
            count_2 += 1
        print()
        for i in storage.get_score():
            print(f'{i}\t\t', end='')  
        print(f'\n')
        score = scoring(users_guess(find_possible_guess.get_list()), answer)
        storage.store_scoring(score.comparing())
        storage.store_word_guessed(score.get_users_guess())
        if count >= 5:
            break
        count += 1


def testing_class_getting_from_file():
    """"""

    print('test1')
    test1 = getting_from_file('all_words.txt')
    print('number of items:\t', test1.get_list_count())
    print('answer:\t\t\t', test1.get_random_word())

    print('\ntest2')
    test2 = getting_from_file('target_words.txt')
    print('number of items:\t', test2.get_list_count())
    print('answer:\t\t\t', test2.get_random_word())

    print('\ntest3')
    test3 = getting_from_file('not_real_file.txt')
    print('number of items:\t', test3.get_list_count())
    print('answer:\t\t\t', test3.get_random_word())


def testing_class_getting_users_guess():
    """"""

    print('test1')
    test_list = ['test1', 'test2', 'test3', 'break']
    test1 = getting_users_guess('test1', test_list) 
    print('users guess:\t\t', test1.get_users_guess())
    print('if word is in list:\t', test1.validate_guess())
    print('if word == break:\t', test1.breaking_loop())
    print('contents of list:\t', test1.get_list())

    print('\ntest2')
    test2 = getting_users_guess('break', test_list) 
    print('users guess:\t\t', test2.get_users_guess())
    print('if word is in list:\t', test2.validate_guess())
    print('if word == break:\t', test2.breaking_loop())
    print('contents of list:\t', test2.get_list())

    print('\ntest3')
    test3 = getting_users_guess('guess', test_list) 
    print('users guess:\t\t', test3.get_users_guess())
    print('if word is in list:\t', test3.validate_guess())
    print('if word == break:\t', test3.breaking_loop())
    print('contents of list:\t', test3.get_list())


def testing_class_scoring():
    """"""

    print('\ntest1')
    test1 = scoring('trees', 'tests')
    print('scoring:\t\t', test1.comparing())
    print('users_guess:\t\t', test1.get_users_guess())
    print('answer:\t\t\t', test1.get_answer())
    print('inputs match:\t\t', test1.seeing_if_input_match())
    print('different lengths:\t', test1.different_lengths())

    print('\ntest2')
    test2 = scoring('guess', 'answer')
    print('scoring:\t\t', test2.comparing())
    print('users_guess:\t\t', test2.get_users_guess())
    print('answer:\t\t\t', test2.get_answer())
    print('inputs match:\t\t', test2.seeing_if_input_match())
    print('different lengths:\t', test2.different_lengths())

    print('\ntest3')
    test3 = scoring('tests', 'tests')
    print('scoring:\t\t', test3.comparing())
    print('users_guess:\t\t', test3.get_users_guess())
    print('answer:\t\t\t', test3.get_answer())
    print('inputs match:\t\t', test3.seeing_if_input_match())
    print('different lengths:\t', test3.different_lengths())

    print('\ntest4')
    test4 = scoring('test', 'sample')
    print('scoring:\t\t', test4.comparing())
    print('users_guess:\t\t', test4.get_users_guess())
    print('answer:\t\t\t', test4.get_answer())
    print('inputs match:\t\t', test4.seeing_if_input_match())
    print('different lengths:\t', test4.different_lengths())

    print('\ntest5')
    test5 = scoring('sample', 'test')
    print('scoring:\t\t', test5.comparing())
    print('users_guess:\t\t', test5.get_users_guess())
    print('answer:\t\t\t', test5.get_answer())
    print('inputs match:\t\t', test5.seeing_if_input_match())
    print('different lengths:\t', test5.different_lengths())


def testing_class_storing_progress():
    """"""

    print('\ntest1')
    test1 = storing_progress()
    test1.store_scoring('hello')
    test1.store_scoring('world')
    test1.store_scoring('test')
    test1.store_scoring('sample')
    test1.store_scoring('truth32')    
    test1.store_word_guessed('test samples')
    test1.store_word_guessed('showcase')
    test1.store_word_guessed('12321')
    test1.store_word_guessed('gg420')
    print('in storage 1:\t\t', test1.get_score())
    print('in storage 2:\t\t', test1.get_users_guess())

    print('\ntest2')
    test2 = storing_progress()
    print('in storage 1:\t\t', test2.get_score())
    print('in storage 2:\t\t', test2.get_users_guess())

    print('\ntest3')
    test3 = storing_progress()
    test3.store_scoring(123)
    test3.store_scoring('letters')
    test3.store_scoring(True)
    test3.store_scoring([123, 'test'])
    test3.store_word_guessed([])
    print('in storage 1:\t\t', test3.get_score())
    print('in storage 2:\t\t', test3.get_users_guess())


def print_tests():
    """"""
    breaker = '\n________________________________________________________________________'
    print(breaker)
    print('getting_from_file\n')   
    testing_class_getting_from_file()
    print(breaker)
    print('getting_users_guess\n')
    testing_class_getting_users_guess()
    print(breaker)
    print('scoring\n')
    testing_class_scoring()
    print(breaker)
    print('storage\n')
    testing_class_storing_progress()
    print(breaker)


print_tests()
# wordle()

