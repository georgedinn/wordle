

def wordle_scoring(self):
    self.answer = "brown"
    self.user_guess = "truth"
    answer_list = list()
    for i in self.answer:
        answer_list.append(i)
    count = 0
    scoring = ""
    for i in self.user_guess:
        if i in answer_list:
            if i == answer_list[count]:
                scoring += "X "
            else:
                scoring += "O "
        else: 
            scoring += "_ "
    return answer_list

print(wordle_scoring())