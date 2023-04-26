import tkinter as tk
from tkinter import ttk #mono  gia to ComboBox
import random
import os 

root = tk.Tk()
root.geometry("650x300")
root.title("10 Question Math Game")


file_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(file_dir, "game_score.txt") # eida oti to "\\".join(__file__.split("\\")[0:-1]) + "\\" + "game_score.txt" den einai crossplatform

start_button_text = "Start"
number_of_questions = tk.IntVar()
number_of_questions.set(10)
questions_remaining = number_of_questions.get()
question_string = None
user_input = "0a"
duration = 30 #apli arxikopoiisi, den xrhsimopoieitai kapou
counter = duration + 1 #gia na min emfanizetai pote to 0 
timer_running = True
score_var = tk.IntVar()
question_var = tk.IntVar()
congratulations_text = tk.StringVar()
question_points=50


previous_score = 0
after_events_list =[]
game_running = False
diff = tk.StringVar()


def result(a,operator,b):
    
    
    if (operator=='+'): result=a+b
    elif (operator=='-'): result=a-b
    elif (operator=='*'): result=a*b
    else: result=a//b
    return result


def setDifficulty(input):
    print(input)
    if (input=='Easy'): setdifficulty=1
    elif (input=='Medium'): setdifficulty=2.5
    elif (input=='Hard'): setdifficulty=5
    else:setdifficulty=10
    return setdifficulty


def create_question():

    difficulty=setDifficulty(diff.get())
    
    operator = random.choice(['+','-','*','/'])
    
    if (operator=='*'):
        max_limit= int(10*difficulty)
        
    else:
        max_limit=int(40*difficulty*difficulty)
        
    leftnumber = random.randrange(1,max_limit)
    rightnumber = random.randrange(1,max_limit)   

    answer = result(leftnumber,operator,rightnumber)
    if (operator=='/'):
        operator=" akeraia diairesi me "
    question_string = str(leftnumber)+" "+operator+" "+str(rightnumber)+" = ?"
   
    return question_string, answer


def is_an_int(a_string):
    if(a_string==""):
        return False
    if (a_string[0] in ['-','+']):
        a_string=a_string[1:]
    if (a_string.isnumeric()):
        return True
    return False


def set_new_question():
    global question_string, answer
    global questions_remaining
    global counter
    counter = duration+1 ############################# reset timer
    

    question_string, answer = create_question()
    question_label.config(text=question_string)
    print(answer)
    questions_remaining-=1


def end_question():
    global score_var, question_var,question_points
    if (questions_remaining>1): #has Questions
        entry.delete(0, tk.END)
        set_new_question()
    else:
        frame2.pack_forget()
        frame3.pack()
        root.bind('<Return>',lambda event:play_again())
        for x in after_events_list: #cleans scheduled after calls
            root.after_cancel(x)
        question_var.set(int((score_var.get()-previous_score)/question_points) )
        print("score = " + str(int(question_var.get())))
        congratulations()
        write_to_file(True)


def get_user_input(out_of_time):
    
    global answer, score_var, question_points
    user_input = entry.get().strip()
    #print("bindID: get_user_input")  ###############################################DEBUG

    if(out_of_time==False): #in Time 

        if (is_an_int(user_input)): #is Number

            if ( int(user_input) == answer ): #is Correct

                put_number_label.config(text="")
                score_var.set(score_var.get()+question_points)
                end_question()

            else:
                put_number_label.config(text="Wrong")
        else:
            put_number_label.config(text="Put Number")
    else:
        end_question()



def update_timer():
    global counter, timer_running, after_events_list
    if timer_running:
        if (counter==1):
            get_user_input(True)            
        counter -= 1
        timer.config(text=str(counter))
        temp = root.after(1000, update_timer) #temp -> identifier to pass as an argument in after_cancel
        after_events_list.append(temp)


def start_game():
    global counter, game_running, question_string, answer, duration, questions_remaining, previous_score
    #print("bindID: start") ###############################################DEBUG
    if game_running:
        questions_remaining = number_of_questions.get()
        for x in after_events_list: #cleans scheduled after calls
            root.after_cancel(x)
    question_string, answer = create_question()
    question_label.config(text=question_string)
    print(answer)
    entry.delete(0, tk.END)
    is_checked()
    duration = timer_slider.get()
    counter= duration+1
    game_running = True
    update_timer()
    frame1.pack_forget()
    frame2.pack(padx=5,pady=5)
    entry.focus_set()
    previous_score = score_var.get()
    root.bind('<Return>',lambda event:get_user_input(False))


def play_again():
    global game_running,score_var
    frame3.pack_forget()
    frame1.pack(padx=5,pady=5)
    root.bind('<Return>',lambda event:start_game())
    


def is_checked():
    global timer_running,checked
    if (checked.get()==1):
        timer_running=True
        timer.pack(padx=5,pady=5)
    else:
        timer_running=False
        timer.pack_forget()



def write_to_file(initialized): 
    global file_path, score_var, question_points
    try:
        with open(file_path, "r") as f:
            file_int=int(f.read())
    except:
        with open(file_path, "w") as f:
            f.write("0")
            file_int=0
            os.system("attrib +h " + file_path)
    finally:
        
        if (initialized):
            os.system("attrib -h " + file_path)
            with open(file_path, "w") as f:
                f.write(str(score_var.get()))
            os.system("attrib +h " + file_path)
        else:
            score_var.set(file_int)

        if (score_var.get() >= 1000):
            question_points=100
            gloden_label.grid(row=0, column=0)
        else:
            question_points=50
            gloden_label.grid_forget()
        


def score_reset():
    global file_path, score_var, question_points
    gloden_label.grid_forget()
    question_points=50
    if (os.path.isfile(file_path)):
        os.remove(file_path)
        score_var.set(0)


def congratulations():
    global congratulations_text
    if ((question_var.get()/number_of_questions.get())>=(0.75)):
        congratulations_text.set("Congratulations, you win!")     
    else:
        congratulations_text.set("You lost...")   
    

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)


##################################### Welcome Screen: frame1 ###########################################

welcome_label = tk.Label(frame1, text="Welcome to the game!",font=("Arial",25))
welcome_label.pack(padx=5,pady=5)

inner_frame = tk.Frame(frame1)

difficulty_label = tk.Label(inner_frame, text="Difficulty",font=("Arial",18))
difficulty_label.grid(row = 0, column = 0)

difficulty_frame = tk.Frame(inner_frame)
difficulty_frame.grid(row=0, column=1)

difficulty_combobox = ttk.Combobox(difficulty_frame, width=10, textvariable=diff)
difficulty_combobox.pack(padx=5,pady=5,)
difficulty_combobox["values"] = ("Easy", "Medium", "Hard", "Insane")
difficulty_combobox.current(0)

set_timer_label = tk.Label(inner_frame, text="Timer",font=("Arial",18))
set_timer_label.grid(row = 1, column = 0)

timer_frame = tk.Frame(inner_frame)
timer_frame.grid(row = 1, column = 1)

checked = tk.IntVar()
timer_check = tk.Checkbutton(timer_frame, variable=checked)
timer_check.grid(row=0, column=0)
checked.set(True)


timer_slider = tk.Scale(timer_frame, from_=5, to=30, orient=tk.HORIZONTAL)
timer_slider.grid(row=0, column=1)
timer_slider.set(10)

inner_frame.pack(padx=5,pady=5)
start_button = tk.Button(frame1, text = "Start", font=("Arial",18), command=start_game)
start_button.pack(padx=5,pady=5)
root.bind('<Return>',lambda event:start_game())


description_label = tk.Label(frame1, text="Rules: Just type your answers and hit enter before the time runs out!",font=("Arial",14))
description_label.pack(padx=5,pady=5)

reset_frame = tk.Frame(frame1)

gloden_label = tk.Label(reset_frame, text="Golden User!",fg="gold", bg="black")
gloden_label.grid(row=0, column=0)

reset_label = tk.Label(reset_frame,text="Current Score: ")
reset_label.grid(row=0, column=1)

reset_number = tk.Label(reset_frame,textvariable=score_var)
reset_number.grid(row = 0, column=2)

reset_button = tk.Button(reset_frame, text="Reset Score", command = score_reset)
reset_button.grid(row=0, column=3 )

reset_frame.pack(padx=5, pady=5)

frame1.pack(padx=5,pady=5)

write_to_file(False)

########################################## Game: frame2 ######################################################

restart_frame = tk.Frame(frame2)
restart_frame.pack(padx=5,pady=5,fill=tk.BOTH, expand=True)

restart_button = tk.Button(restart_frame, text = "Restart", font=("Arial",18), command=start_game)
restart_button.pack(padx=5,pady=5,side=tk.RIGHT)

question_label = tk.Label(frame2, text=question_string, font=("Arial",18),  width=40)
question_label.pack(padx=5,pady=5)

entry = tk.Entry(frame2, font = ("Arial",18))
entry.pack(padx=5,pady=5)

submit_button = tk.Button(frame2, text="Submit", font = ("Arial",18), command = lambda: get_user_input(False))
submit_button.pack(padx=5,pady=5)

put_number_label = tk.Label(frame2, text="", font=("Arial",18))
put_number_label.pack(padx=5,pady=5)

timer = tk.Label(frame2, text=10,font=("Arial,18"))
timer.pack(padx=5,pady=5)


##################################### score: frame3 ###########################################


congratulations_text.set("Congratulations, you won!")

congratulations_label =tk.Label(frame3, textvariable=congratulations_text, font=("Arial",30))
congratulations_label.pack(padx=5, pady=5)

score_frame = tk.Frame(frame3)

score_label = tk.Label(score_frame,text="Score: ",font=("Arial", 40))
score_label.grid(row=0, column=0)

score_number = tk.Label(score_frame,textvariable=score_var, font=("Arial",40))
score_number.grid(row = 0, column=1)

score_frame.pack(padx=5, pady=5)

correct_answers_frame = tk.Frame(frame3)

correct_answers_label1 = tk.Label(correct_answers_frame, text="Correct Answers: ",font=("Arial", 20))
correct_answers_label1.grid(row=0, column=0)

correct_answers_label2 = tk.Label(correct_answers_frame, textvariable=question_var,font=("Arial", 20))
correct_answers_label2.grid(row=0, column=1)

correct_answers_label3 = tk.Label(correct_answers_frame, text="/",font=("Arial", 20))
correct_answers_label3.grid(row=0, column=2)

correct_answers_label4 = tk.Label(correct_answers_frame, textvariable=number_of_questions,font=("Arial", 20))
correct_answers_label4.grid(row=0, column=3)

correct_answers_frame.pack(padx=5, pady=5)


play_again_button = tk.Button(frame3, text="Play Again", font=("Arial", 30), command=play_again)
play_again_button.pack(padx=5, pady=5)


root.mainloop()
