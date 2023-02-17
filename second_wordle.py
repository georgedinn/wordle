import random                                                                                                                           
from random import randrange
import os
import time
import sqlite3
import socket
import sys

conn = sqlite3.connect('wordledatabasev2.sqlite')                                                                           
cur = conn.cursor()
database_empty = True
cur.execute('create table if not exists all_info (id integer primary key autoincrement, users_username varchar(18), answer_pc_chose varchar(5));')
cur.execute('create table if not exists users_guesses (id integer primary key autoincrement, users_username varchar(18), users_guess varchar(5), time_program_ran varchar(10));')
cur.execute('create table if not exists words_given_up_on (id integer primary key autoincrement, username varchar(18), score int);')

user_name = socket.gethostname()
class colours:                                                                                                                          
    _WHITE = '\33[37m'                                                                                                               
    _PURPLE = '\033[95m'                                                                                                             
    _RED = '\33[31m'                                                                                                                 
    _GREEN = '\33[92m'                                                                                                               
    _YELLOW = '\33[33m'  
_possible_answer = open("target_words.txt") 
all_possible_answers = list()
for line in _possible_answer:                                                                                                                    
    lines = line.split()                                                                                                            
    all_possible_answers.append(lines[0])
letters_of_answer = list()
_possible_guesses = open("all_words.txt") 
all_possible_guesses = list()
for line in _possible_guesses:                                                                                                                    
    lines = line.split()                                                                                                            
    all_possible_guesses.append(lines[0])
alphabet = list()
alphabet2 = list()
alphabet3 = list()
answer_dict = dict()
list_alphabet = ""
info = ""
about_game = ""
_hello_statement = f"{colours._WHITE}hello {user_name}, "
_instruction_statement = "you are to guess a 5 letter word. It has to be a valid word contained in the list of possible words\nenter\t- 'about game' to see what to do"
_word_hide = f"\n\t- 'hide' to remove answer"
_word_show = f"\n\t- 'show' to see what word is"
word_shown_or_hidden = _word_show
_getting_new_word = f"\n\t- 'new' for a new word"
_going_back_default = f"\n\t- 'back' to undo your last attempt"
_getting_most_common_guessed_correct_or_incorrect = f"\n\t- 'correct' to get most common words to get right and how many times its been or right or 'incorrect' for words wrong"
users_guess = ""
right_length = True
valid_word = True
restart = True
errors = False
keyword = False
first_run = True
first_run_for_print_statements = True
empty = True
go_back = False
already_used = False
just_started = True
go_back_allowed = True
replace_with_better_name = False
wasnt_a_guess = False
time_travel_statement = ""
answer = ""
all_possible_guesses_user = ""
_about_game = "in this wordle you are to enter a word, this word has to be a 5 letter word we have decided to be valid for this game \nwe will add the word you have entered to the 'words guessed so far' column, this program will replace each letter with either \ngreen - for if the letter if in this right place\nyellow - for if the letter is in the word but wrong place\nred - if the letter isnt in the word\nyou have 6 guesses to guess the word, good luck"  
print_statement_for_about_game = _about_game
keyword_count = 0
words_guessed_so_far = list()
scoring_list = list()
scoring_list_count = 0
while scoring_list_count < 5:
    scoring_list.append(' ')
    scoring_list_count += 1
keyword_print_statements = ('are you going to play the wordle or not?', 'stop abusing the keywords!', 'you wish I made a prgram with just keywords?')
_how_many_guesses = 6

typing_speed = 200 #wpm                                                                     # fast_type function from https://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
def fast_type(t):
    """enter a variable and function will make it look like its being type (200wpm)"""
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print(end="")

typing_speed_two = 50 #wpm                                                                     # fast_type function from https://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
def slow_type(t):
    """enter a variable and function will make it look like its being type (200wpm)"""
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed_two)
    print(end="")

def printing_info_from_database(table_name):
    """enter a table name and it will show you everything in table (for wordledatabase.sqlite)"""      
    cur.execute('select * from ' + table_name + ';')                   
    for i in cur:
        print(f"{table_name}: {i}")
        time.sleep(0.2)
    stop_seeing_database = input("enter anything to continue: ")


def how_long_program_ran(start_time):
    """enter in the time the program started using time.time() into the function and see how many seconds since then has passed"""
    end_time=time.time()
    total_time = end_time - start_time 
    return total_time


def getting_an_int_to_return():
    """doesnt take arguements; gets user to enter a number and returns the value of the number with error check"""
    wasnt_int = False
    while True:
        if wasnt_int:
            print('enter a number')
        try:
            how_long_word = int(input("enter a number showing how most common words right eg. enter 2 to see 2 most common words: "))
        except:
            wasnt_int = True
        if wasnt_int == False:
            break
    return how_long_word


top_words = dict()
def selecting_from_a_dict(how_long_word): 
    """enter how many items you wish to see as an arguement and it will find the most common occurances and print how many you specified \nwill need to fill a list called top_words with wanted words or alter to suit personal needs"""               
    count = 0       
    for j, h in sorted(top_words.items(), key=lambda x: x[1], reverse=True):
        if count < how_long_word:                                                         
            print(j, h) 
            count+=1                                                                       
    dummy = input('enter anything to continue: ')

def filling_dict(name_of_table, column_name, query_sufix):
    """takes name of table and then column name of data you wish to fill dict with \nwill need 'selecting_from_a_dict()' and 'getting_an_int_to_return()' functions to use this function or alter for personal needs"""
    cur.execute(f'select id, {column_name} from {name_of_table} {query_sufix}')
    top_words.clear()
    for u, i in cur:
        if i not in top_words:
            top_words[i] = 1
        elif i in top_words:
            top_words[i] += 1
    selecting_from_a_dict(getting_an_int_to_return())


def filling_dict_scores(name_of_table, name_of_table_2, name_of_table_3, column_name, query_sufix, username ):
    """enter name of table one, name of table 2, name of table 3, column name, the query sufix (where...) and then column containing username"""
    # cur.execute(f'select {username}, {column_name} from {name_of_table} {query_sufix}')
    # top_words.clear()
    # for u, i in cur:
    #     if u not in top_words:
    #         top_words[u] = i
    #     elif u in top_words:
    #         top_words[u] += i
    cur.execute(f'select {username}, {column_name} from {name_of_table_2} {query_sufix}')
    for u, i in cur:
        if u not in top_words:
            top_words[u] = 0
        elif u in top_words:           
            top_words[u] -= i
        # if top_words[u] < 0:
        #     top_words[u] = 0
    cur.execute(f'select {username}, {column_name} from {name_of_table_3} {query_sufix}')
    for u, i in cur:
        if u not in top_words:
            top_words[u] = 0
        elif u in top_words:           
            top_words[u] -= i
        # if top_words[u] < 0:
        #     top_words[u] = 0
    cur.execute(f'select {username}, {column_name} from {name_of_table} {query_sufix}')
    top_words.clear()
    for u, i in cur:
        if u not in top_words:
            top_words[u] = i
        elif u in top_words:
            top_words[u] += i
    selecting_from_a_dict(10)



all_accounts = list()
def filling_list(name_of_table, column_name):
    os.system('cls')
    cur.execute(f'select id, {column_name} from {name_of_table}')
    all_accounts.clear()
    for i, u in cur:
        if u not in all_accounts:
            all_accounts.append(u)
    for i in all_accounts:
        print(i)
    dummy_variable = input('enter anything to continue: ')


def finding_time_program_ran(table_name, column_name):
    cur.execute('select sum(' + column_name + ') from ' + table_name + '')
    for i in cur:
        if round(i[0]) == 1:
            print(f"it took you {round(i[0])} second to complete.... you cheating?")
        else:
            print(f"it took you {round(i[0])} seconds to complete")
    conn.commit()





os.system('cls')
while True:     
    cur.execute('create table if not exists wordle_progress (id integer primary key autoincrement, users_username varchar(18), attempt_number integer, number_of_goes integer, answer varchar(5), keyboard varchar(26));')
    cur.execute('create table if not exists all_info_list_items (id integer primary key autoincrement, words_wrong varchar(5));')
    cur.execute('create table if not exists all_info_list_items_keyboard (id integer primary key autoincrement, keyboard varchar(1));')
    cur.execute('create table if not exists wordle_progress_deleted_words (id integer primary key autoincrement, users_username varchar(18), attempt_number integer, number_of_goes integer, answer varchar(5), keyboard varchar(26));')
    cur.execute('create table if not exists words_wrong_history (id integer primary key autoincrement, words_wrong varchar(5));')
    cur.execute('create table if not exists keyboard_history (id integer primary key autoincrement, keyboard varchar(1));')
    cur.execute('create table if not exists guessed_correct (id integer primary key autoincrement, username varchar(18), word_to_get varchar(5), score int);')
    cur.execute('create table if not exists guessed_wrong (id integer primary key autoincrement, username varchar(18), word_to_get varchar(5), score int);')
    cur.execute('create table if not exists users_current_guesses (id integer primary key autoincrement, users_username varchar(18), users_guess varchar(5), time_program_ran varchar(10));')
    if restart == True: 
        if first_run == True: 
            cur.execute('select id, word_to_get from guessed_wrong')           
            cur.execute('select id, word_to_get from guessed_correct')                        
            game_over = False
            cur.execute('select count(id) from wordle_progress')
            for u in cur:
                if int(u[0]) > 0:
                    empty = False
                else:
                    empty = True
            if just_started == True:
                just_started = False
                if empty == False:
                    wish_to_resume = input("do you wish to resume [y for yes and anything else for no]: ")
                    wish_to_resume = wish_to_resume.lower()
                    if wish_to_resume != "y":
                        cur.execute('insert into words_given_up_on (score, username) values ( 1, "' + user_name + '")')
                if empty == True:
                    wish_to_resume = "" 
            if go_back == True:
                wish_to_resume = "y"
            if wish_to_resume == "y": 
                valid_word = True           
                cur.execute('select number_of_goes from wordle_progress where number_of_goes = (select max(number_of_goes) from wordle_progress)')
                for u in cur:      
                    _number_of_goes = int(u[0])
                    _attempt_number = int(u[0])
                cur.execute('select answer from wordle_progress where id = (select max(id) from wordle_progress)')                
                answer1 = cur.fetchall()
                answer = answer1[0][0]                
                words_guessed_so_far.clear()                                             
                cur.execute('select words_wrong from all_info_list_items')
                for j in cur:
                    words_guessed_so_far.append(j[0])
                cur.execute('select keyboard from all_info_list_items_keyboard where id >= (select max(id)-25 from all_info_list_items_keyboard)') 
                alphabet2.clear()
                alphabet3.clear() 
                alphabet.clear() 
                list_alphabet = ""         
                for q in cur:                                          
                    alphabet.append(q[0])                                                 
            if wish_to_resume != "y": 
                going_back = _going_back_default              
                _number_of_goes = 1
                _attempt_number = 1
                answer_index = random.randrange((len(all_possible_answers))) 
                answer = all_possible_answers[answer_index]
                words_guessed_so_far.clear()                 
                cur.execute('insert into all_info(users_username, answer_pc_chose) values ("' + user_name + '", "' + answer + '");')
                cur.execute('delete from all_info_list_items')
                cur.execute('delete from all_info_list_items_keyboard')
                cur.execute('delete from words_wrong_history')
                cur.execute('delete from keyboard_history')
                cur.execute('delete from wordle_progress')
                cur.execute('delete from wordle_progress_deleted_words')
                cur.execute('delete from users_current_guesses')
                conn.commit()
            number_of_goes = _number_of_goes
            attempt_number = _attempt_number
            score_for_right = _how_many_guesses  
            letters_of_answer.clear()  
            answer_dict.clear()          
            for i in answer:
                letters_of_answer.append(i)           
            info = ""          
            guesses = ""
        cur.execute('select count(id) from words_wrong_history')              
        conn.commit()  
        for i in cur:                      
            if i[0] == 0:
                furtherest_point = True
                can_undo = False 
                if attempt_number <= 1:
                    going_back = "" 
                else:
                    going_back = _going_back_default                                               
            if i[0] != 0:
                furtherest_point = False  
                can_undo = True
                if attempt_number <= 1:
                    going_back = "\n\t- 'undo' to redo what you undid"  
                else:
                    going_back = _going_back_default + "\n\t- 'undo' to redo what you undid"    
        instructions = _hello_statement + _instruction_statement + word_shown_or_hidden + _getting_new_word + going_back + _getting_most_common_guessed_correct_or_incorrect                          
        index_of_letters = 0
        keyboard = ""
        words_guessed = ""
        words_guessed_so_far_count = len(words_guessed_so_far)
        words_guessed_last_word = ""
        if keyword or right_length == False or valid_word == False or already_used == True or go_back_allowed == False:
            how_many_words_get_typed = 0
            wasnt_a_guess = True
        else:
            how_many_words_get_typed = 1
        for u in words_guessed_so_far:
            if words_guessed_so_far_count >= how_many_words_get_typed:
                if words_guessed == "":
                    words_guessed = "|   " + u + "   |"
                else:
                    words_guessed = words_guessed + "   " + u + "    |"
            else:
                words_guessed_last_word = "    " + u + "   |\n"           
            words_guessed_so_far_count-=1
        keyword = False
        # time.sleep(1)             # comment to stop the clearing of terminal for 1 sec
        os.system('cls')
        _letters = open("alphabet.txt")
        if len(alphabet) == 0:
            for line in _letters:                                                                                                                    
                lines = line.split()                                                                                                            
                alphabet.append(lines[0])   
        for t in alphabet:
            keyboard = keyboard + t + " "
        att_no = str(attempt_number)
        no_goes = str(number_of_goes)  
        cur.execute('insert into wordle_progress (users_username, attempt_number, number_of_goes, answer, keyboard) values ("this pc",' + att_no + ', ' + no_goes + ', "' + answer + '", "' + keyboard + '")')           
        conn.commit()
        if first_run_for_print_statements == True:         
            fast_type(instructions) 
            print('')  
            fast_type(info)
            print("") 
            fast_type(f"green means in word and right place, yellow means in word but wrong place, red means not in word \t\t\tattempt: {attempt_number} / {_how_many_guesses}\n")  
            fast_type(f"words guessed so far: {words_guessed}")
            fast_type(words_guessed_last_word)
            if words_guessed_last_word == "":
                print('')
            print('')
            if wasnt_a_guess:
                print(f"{keyboard}") 
            if wasnt_a_guess == False:
                fast_type(f"{keyboard}")
        if first_run_for_print_statements == False:                                
            print(f"{instructions}")   
            print(f"{info}")
            print(f"") 
            print("green means in word and right place, yellow means in word but wrong place, red means not in word \t\t\tattempt: ", end='')
            attempt_no = f"{attempt_number} / {_how_many_guesses}\n"
            slow_type(attempt_no)  
            print_statement = f"words guessed so far: {words_guessed}"
            print(f"words guessed so far: {words_guessed}", end='')
            fast_type(words_guessed_last_word)
            if words_guessed_last_word == "":
                print('')
            if right_length == False:
                print(f"{colours._RED}word has to be 5 letters long{colours._WHITE}")
                right_length = True
            if valid_word == False:
                print(f"{colours._RED}word must be a valid word{colours._WHITE}")
                valid_word = True
            if already_used == True:
                print(f"{colours._RED}word already been used{colours._WHITE}")
                already_used = False
            if go_back_allowed == False:
                print(f"{colours._RED}{time_travel_statement}{colours._WHITE}")
                go_back_allowed = True
            if keyword_count >= 3:
                keyword_index = random.randrange(len(keyword_print_statements))
                keyword_statement = keyword_print_statements[keyword_index]
                print(f'{colours._PURPLE}{keyword_statement}{colours._WHITE}')               
            if wasnt_a_guess:
                print(f"{keyboard}", end='')             
            if wasnt_a_guess == False:
                fast_type(f"{keyboard}")              
        first_run_for_print_statements = False  
        first_run = False  
        start_time = time.time()
        fast_type("\nenter your guess: ")                       
        users_guess = input("")
        users_guess = users_guess.lower()                   
        if users_guess == "back":
            keyword = True
            if attempt_number > 1:
                cur.execute('insert into words_wrong_history (words_wrong) values ((select words_wrong from all_info_list_items where id = (select max(id) from all_info_list_items)))')
                for g in alphabet:
                    cur.execute('insert into keyboard_history (keyboard) values ("' + g + '");')
                cur.execute('insert into wordle_progress_deleted_words (users_username, attempt_number, number_of_goes, answer, keyboard) values ("this pc",' + att_no + ', ' + no_goes + ', "' + answer + '", "' + keyboard + '")')                   
                cur.execute('delete from wordle_progress where attempt_number >= ' + att_no + ';')
                cur.execute('delete from all_info_list_items where id = (select max(id) from all_info_list_items);')  
                cur.execute('delete from all_info_list_items_keyboard where id >= (select max(id)-25 from all_info_list_items_keyboard)')                   
                go_back = True 
                first_run = True   
                empty = False
                can_undo = True                                                 
                conn.commit()
            else:
                go_back_allowed = False
            time_travel_statement = "what are you trying to go back to"
        if users_guess != "back":
            wish_to_resume = ""
            go_back = False   
            go_back_allowed = True                    
        if users_guess in words_guessed_so_far:
            keyword = True
        if users_guess == "show":
            info = f"{colours._PURPLE}the answer is: {answer}{colours._WHITE}"
            word_shown_or_hidden = _word_hide 
            keyword = True
        if users_guess == "hide":
            info = ""
            word_shown_or_hidden = _word_show 
            keyword = True
        if users_guess == "new":               
            alphabet.clear()
            cur.execute('insert into words_given_up_on (score, username) values (1, "' + user_name + '")')
            right_length = True
            keyword = True
            first_run = True
            go_back_allowed = True
            already_used = False
            valid_word = True
        if users_guess == "incorrect":
            top_words.clear()            
            keyword = True
            os.system('cls')  
            filling_dict('guessed_wrong', 'word_to_get', '')                        
        if users_guess == "correct":
            top_words.clear()           
            keyword = True
            os.system('cls')  
            filling_dict('guessed_correct', 'word_to_get', '')                       
        if users_guess == "my guesses":
            top_words.clear()
            keyword = True
            os.system('cls')
            filling_dict('users_guesses', 'users_guess', 'where users_username == "' + user_name + '"') 
        if users_guess == "guesses":
            top_words.clear()
            keyword = True
            os.system('cls')
            filling_dict('users_guesses', 'users_guess', '') 
        if users_guess == "chosen":
            top_words.clear()
            keyword = True           
            os.system('cls')       
            filling_dict('all_info', 'answer_pc_chose', '')  
        if users_guess == "accounts":
            top_words.clear()
            keyword = True           
            os.system('cls')       
            filling_list('all_info', 'users_username') 
        if users_guess == "scores":
            keyword = True
            filling_dict_scores('guessed_correct', 'guessed_wrong', 'words_given_up_on', 'score', '', 'username')
        if users_guess == "undo":
            keyword = True
            first_run = True
            go_back = True
            go_back_allowed = True
            if can_undo: 
                if furtherest_point == False:                   
                    cur.execute('select users_username, attempt_number, number_of_goes, answer, keyboard from wordle_progress_deleted_words where id = (select max(id) from words_wrong_history)')
                    for usrnme, attempt, no_go, ans, kb in cur:
                        attempt = str(attempt)
                        no_go = str(no_go)
                        cur.execute('insert into wordle_progress (users_username, attempt_number, number_of_goes, answer, keyboard) values ("' + usrnme + '", "' + attempt + '", "' + no_go + '", "' + ans + '", "' + kb + '");')                    
                    cur.execute('select id, words_wrong from words_wrong_history where id = (select max(id) from words_wrong_history)')
                    for u, iq in cur:                    
                        iq = str(iq)
                        cur.execute('insert into all_info_list_items (words_wrong) values ("' + iq + '")')
                    cur.execute('delete from words_wrong_history where id = (select max(id) from words_wrong_history)')
                    alph_loop_count = 25
                    while alph_loop_count >= 0:
                        alph_count = str(alph_loop_count)
                        cur.execute('select keyboard from keyboard_history where id >= (select max(id)-"' + alph_count + '" from keyboard_history)')
                        for x in cur:                     
                            cur.execute('insert into all_info_list_items_keyboard (keyboard) values ("' + x[0] + '")')
                        alph_loop_count-=1
                        alph_count = int(alph_count) - 1
                    cur.execute('delete from keyboard_history where id >= (select max(id)-25 from keyboard_history)')
                    conn.commit()
                    go_back_allowed = True
            if can_undo == False or furtherest_point:
                go_back_allowed = False
                time_travel_statement = "cant undo what you havent undone yet"
            go_back = True 
            first_run = True   
            empty = False           
        if users_guess == "about game":
            keyword = True
            while True:
                os.system('cls')
                print(f"{print_statement_for_about_game}")
                to_allow_you_to_keep_reading = input("\n\nenter anything to resume your wordle: ")       
                try:
                    printing_info_from_database(to_allow_you_to_keep_reading)
                except:
                    break 
        if keyword:
            keyword_count +=1                  
        if keyword == False:
            keyword_count = 0
            wasnt_a_guess = False
            go_back_allowed = True
            going_back = _going_back_default
            cur.execute('delete from keyboard_history')
            cur.execute('delete from words_wrong_history')
            cur.execute('delete from wordle_progress_deleted_words')
            cur.execute('insert into users_guesses values (null, "' + user_name + '","' + users_guess + '", "' + str(how_long_program_ran(start_time)) + '")')
            cur.execute('insert into users_current_guesses values (null, "' + user_name + '","' + users_guess + '", "' + str(how_long_program_ran(start_time)) + '")')
            conn.commit()
            time_travel_statement = ""
            go_back = False
            can_undo = False
            empty = False               
            scoring = ""
            if len(users_guess) != 5:         
                right_length = False
            if len(users_guess) == 5:
                right_length = True 
                if users_guess in all_possible_guesses:                   
                    valid_word = True          
                    if number_of_goes <= 6:
                        answer_dict.clear()
                        for r in answer:
                            if r in answer_dict:
                                answer_dict[r] += 1
                            if r not in answer_dict:
                                answer_dict[r] = 1    
                        index_of_letters = 0                                                  
                        for i in users_guess:                                                                                 
                            ya = colours._GREEN + i + colours._WHITE + " "   
                            yb = colours._YELLOW + i + colours._WHITE + " "
                            yc = colours._RED + i + colours._WHITE + " "                       
                            scoring_list[index_of_letters] = yc
                            if i in letters_of_answer:
                                if answer_dict[i] > 0:                                                               
                                    if i == letters_of_answer[index_of_letters]:                       
                                        scoring_list[index_of_letters] = ya                                
                                        for x in range(len(alphabet)):
                                            if alphabet[x] == i or alphabet[x] == yb:
                                                alphabet[x] = ya 
                                        answer_dict[i] = answer_dict[i] - 1
                            index_of_letters += 1
                        index_of_letters = 0  
                        for i in users_guess:  
                            ya = colours._GREEN + i + colours._WHITE + " "   
                            yb = colours._YELLOW + i + colours._WHITE + " "
                            yc = colours._RED + i + colours._WHITE + " " 
                            if i in letters_of_answer and answer_dict[i] > 0:   
                                if i != letters_of_answer[index_of_letters]:                       
                                    scoring_list[index_of_letters] = yb
                                    for x in range(len(alphabet)):
                                        if alphabet[x] == i:
                                            if alphabet[x] != ya:
                                                alphabet[x] = yb 
                                    answer_dict[i] = answer_dict[i] - 1
                            if i not in letters_of_answer:                                                              
                                for x in range(len(alphabet)):
                                    if alphabet[x] == i:
                                        alphabet[x] = yc                                                      
                            index_of_letters += 1   
                        for b in scoring_list:
                            scoring = scoring + b                        
                        if scoring in words_guessed_so_far:
                            already_used = True
                        else:
                            already_used = False
                            words_guessed_so_far.append(scoring)                            
                            cur.execute('insert into all_info_list_items (words_wrong) values ("' + scoring + '")')
                            for v in alphabet:
                                cur.execute('insert into all_info_list_items_keyboard (keyboard) values ("' + v + '")')
                            conn.commit()                                                                                                                           
                            if users_guess == answer:
                                print(f"{colours._GREEN}you got the word right!{colours._WHITE}")                               
                                game_over = True
                                cur.execute('insert into guessed_correct (word_to_get, score, username) values ("' + answer + '", ' + str(score_for_right) + ', "' + user_name + '")')
                                finding_time_program_ran("users_current_guesses", "time_program_ran")                               
                            attempt_number += 1
                            number_of_goes += 1 
                            score_for_right -= 1                      
                    conn.commit()                     
                    if number_of_goes > 6:
                        print(f"out of guesses, answer was {answer}") 
                        game_over = True
                        finding_time_program_ran("users_current_guesses", "time_program_ran")
                        cur.execute('insert into guessed_wrong (word_to_get, score, username) values ("' + answer + '", 3, "' + user_name + '")')                                                    
                else:
                    valid_word = False                   
    if restart == False:
        os.system('cls')
        print(f"thank you for playing")
        time.sleep(3)
        break
    if game_over == True:
        wish_to_resume = ""
        cur.execute('drop table wordle_progress')
        cur.execute('drop table all_info_list_items')
        cur.execute('drop table all_info_list_items_keyboard')
        cur.execute('drop table users_current_guesses')
        while True:                          
            if errors == True:
                os.system('cls')
                print(f"{colours._RED}has to be yes or no{colours._WHITE}")
            wish_to_continue = input(f"do you wish to keep playing? enter yes if you do or no if you dont: ")
            wish_to_continue.lower()
            if wish_to_continue == "yes":
                alphabet.clear()
                first_run = True
                empty = True
                break                              
            if wish_to_continue == "no":
                restart = False
                break
            else:
                errors = True 
            info = "" 
conn.close()