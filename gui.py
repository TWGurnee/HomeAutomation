import sys
import tkinter
import tkinter.messagebox
import customtkinter

from src.scheduler import Scheduler

import src.workout_reminder as workout_reminder
from src.exercise_plan_generator import EXERCISE_PLAN_SAVE, simplified_weekly_workout_plan
from src.shopping_list_generator import MEAL_PLAN_FILE, current_meal_plan_for_table, shopping_list_for_textbox, re_roll_meal, send_current_shopping_list

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end")

    def flush(self):
        pass

def redirect_stdout(text_widget):
    sys.stdout = StdoutRedirector(text_widget)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # initialise classes
        self.scheduler = Scheduler()
        self.teardown = False

        # configure window
        self.title("HomeAutomation")
        self.geometry(f"{1280}x{620}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        ### create sidebar frame with widgets ###
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")


        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="HomeAutomation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.exercise_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Exercise",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.exercise_button_event)
        self.exercise_button.grid(row=2, column=0, sticky="ew")

        self.meal_plan_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Meal Plan",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.meal_plan_button_event)
        self.meal_plan_button.grid(row=3, column=0, sticky="ew")


        ### create Home frame ###
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        self.home_tabview = customtkinter.CTkTabview(self.home_frame, width=1000, height=570)
        self.home_tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # Home menu
        self.home_tabview.add("Home")

        # scheduler start button
        self.scheduler_button = customtkinter.CTkButton(self.home_tabview.tab("Home"), corner_radius=0, height=40, border_spacing=10, text="Start scheduler",
                                           command=self.start_scheduler)
        self.scheduler_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # email today's workout button
        self.email_todays_workout_button = customtkinter.CTkButton(self.home_tabview.tab("Home"), corner_radius=0, height=40, border_spacing=10, text="Email today's workout",
                                           command=self.send_workout_reminder)
        self.email_todays_workout_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # email week's shopping list button
        self.email_shopping_list_button = customtkinter.CTkButton(self.home_tabview.tab("Home"), corner_radius=0, height=40, border_spacing=10, text="Email the shopping list",
                                           command=self.send_shopping_list)
        self.email_shopping_list_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.std_out = customtkinter.CTkTextbox(self.home_tabview.tab("Home"), width=750)
        self.std_out.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        redirect_stdout(self.std_out)
        
        #   - stop/reset button
        # email buttons

        # Options menu
        self.home_tabview.add("Options")

        self.appearance_mode_label = customtkinter.CTkLabel(self.home_tabview.tab("Options"), text="Appearance:")
        self.appearance_mode_label.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.home_tabview.tab("Options"), values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=2, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")


        # Scheduled time changes option
        # Scheduled date changes option
        # Email to send to update
        # -- config needed to update the email address this is sent from      
   



        ### create Exercise frame ###
        self.exercise_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.exercise_tabview = customtkinter.CTkTabview(self.exercise_frame, width=1000, height=570)


        ### create Meal Plan frame ###
        self.meal_plan_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.meal_plan_tabview = customtkinter.CTkTabview(self.meal_plan_frame, width=1000, height=570)




    ### Navigation functions ###
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Home" else "transparent")
        self.exercise_button.configure(fg_color=("gray75", "gray25") if name == "Exercise" else "transparent")
        self.meal_plan_button.configure(fg_color=("gray75", "gray25") if name == "Meal Plan" else "transparent")

        # show selected frame
        if name == "Home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()


        if name == "Exercise":
            self.exercise_frame.grid(row=0, column=1, sticky="nsew")
            try:
                self.display_workout_plan(EXERCISE_PLAN_SAVE)
            except ValueError:
                pass
        else:
            try:
                self.exercise_tabview.delete("Week's Plan")
                self.exercise_tabview.delete("Today's Plan")
            except ValueError:
                pass
            self.exercise_tabview.grid_forget()
            self.exercise_frame.grid_forget()


        if name == "Meal Plan":
            self.meal_plan_frame.grid(row=0, column=1, sticky="nsew")
            try:
                self.display_meal_plan(MEAL_PLAN_FILE)
            except ValueError:
                pass
        else:
            try:
                self.meal_plan_tabview.delete("Weekly Plan")
                self.meal_plan_tabview.delete("Shopping list")
            except ValueError:
                pass
            self.meal_plan_tabview.grid_forget()
            self.meal_plan_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("Home")

    def exercise_button_event(self):
        self.select_frame_by_name("Exercise")

    def meal_plan_button_event(self):
        self.select_frame_by_name("Meal Plan")



    ### Home functions ###
    def start_scheduler(self):
        self.scheduler.run()
        # print("scheduler running")

    def send_shopping_list(self):
        send_current_shopping_list(MEAL_PLAN_FILE)
    
    def send_workout_reminder(self):
        workout_reminder.main()

    
        ### Options Functions ###
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)



    ### Exercise functions ###
    def display_workout_plan(self, EXERCISE_PLAN_SAVE):
        self.exercise_tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.exercise_tabview.add("Week's Plan")

        days, workouts, exercises = simplified_weekly_workout_plan(EXERCISE_PLAN_SAVE)
        self.workout_frame=customtkinter.CTkFrame(self.exercise_tabview.tab("Week's Plan"), height=40 , width=940)
        self.workout_frame.grid(row=0, column=0, padx=20, sticky="nsew")
        self.workout_frame.grid_columnconfigure(0, weight=1)
        self.workout_frame.grid_columnconfigure(1, weight=1)
        
        for day, workout, exercise, i in zip(days, workouts, exercises, range(7)):
            self.w_label=customtkinter.CTkLabel(self.workout_frame, text=f'{day}:', font=customtkinter.CTkFont(size=18, weight="normal"), width=10, anchor="w")
            self.w_label.grid(row=i, column=0, pady=20, padx=20, sticky="w")
            self.w_label1=customtkinter.CTkLabel(self.workout_frame, text=f'{workout}', font=customtkinter.CTkFont(size=18, weight="bold"), width=20, anchor="w")
            self.w_label1.grid(row=i, column=1, pady=20, sticky="w")
            if isinstance(exercise, list):
                exercise = ', '.join(exercise)
            self.w_label1=customtkinter.CTkLabel(self.workout_frame, text=f'{exercise}', font=customtkinter.CTkFont(size=10, weight="normal"), width=640, anchor="w")
            self.w_label1.grid(row=i, column=2, pady=20, padx=10, sticky="w")

        self.exercise_tabview.add("Today's Plan")

        todays_plan_txt = workout_reminder.todays_workout_to_string(EXERCISE_PLAN_SAVE)
        self.todays_plan_frame = customtkinter.CTkFrame(self.exercise_tabview.tab("Today's Plan"), height=40, width=940)
        self.todays_plan_frame.grid(row=0, column=0, padx=20, sticky="nsew")
        self.todays_plan_text = customtkinter.CTkLabel(self.todays_plan_frame, text=todays_plan_txt, font=customtkinter.CTkFont(size=12), width=80, height=20)
        self.todays_plan_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


        


    ### Meal Plan functions ###
    def display_meal_plan(self, MEAL_PLAN_FILE):

        self.meal_plan_tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.meal_plan_tabview.add("Weekly Plan")
        self.meal_plan_tabview.tab("Weekly Plan").grid_rowconfigure((0,1,2,3,4,5), weight=1) #type:ignore

        self.m_frame = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame.grid(row=0, padx=20, sticky='ew')
        self.m_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1, pad=10)# type:ignore
        self.m_frame.grid_columnconfigure((0,1,2,), weight=1) # type:ignore
        self.m_frame.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore

        meal_plan = current_meal_plan_for_table(MEAL_PLAN_FILE)

        for meal, i in zip(meal_plan, range(6)):
            self.meal_category = customtkinter.CTkLabel(self.m_frame, text=f'{meal[0]}', font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w")
            self.meal_category.grid(row=i, column=0, padx=10, sticky='w')
            self.meal_name = customtkinter.CTkLabel(self.m_frame, text=f'{meal[1]}:', font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w")
            self.meal_name.grid(row=i, column=1, padx=10, sticky='w')
            self.meal_ingredients = customtkinter.CTkLabel(self.m_frame, text=f' {meal[2]}', font=customtkinter.CTkFont(size=10, weight="normal"), anchor="w")
            self.meal_ingredients.grid(row=i, column=2, padx=10, sticky='w')

        self.meal0_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal0_button_event)
        self.meal0_button.grid(row=0, column=3, padx=20, sticky="e")
        self.meal1_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal1_button_event)
        self.meal1_button.grid(row=1, column=3, padx=20, sticky="e")
        self.meal2_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal2_button_event)
        self.meal2_button.grid(row=2, column=3, padx=20, sticky="e")
        self.meal3_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal3_button_event)
        self.meal3_button.grid(row=3, column=3, padx=20, sticky="e")
        self.meal4_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal4_button_event)
        self.meal4_button.grid(row=4, column=3, padx=20, sticky="e")        
        self.meal5_button = customtkinter.CTkButton(self.m_frame, corner_radius=0, text="Reroll", command=self.reroll_meal5_button_event)
        self.meal5_button.grid(row=5, column=3, padx=20, sticky="e")


        self.meal_plan_tabview.add("Shopping list")

        self.shopping_list_box = customtkinter.CTkTextbox(self.meal_plan_tabview.tab("Shopping list"), width=1000, height=480)
        self.shopping_list_box.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.shopping_list_box.insert(index="0.0", text=shopping_list_for_textbox(MEAL_PLAN_FILE))



    def reroll_meal_by_index(self, index):
        re_roll_meal(MEAL_PLAN_FILE, index)

        try:
            self.meal_plan_tabview.delete("Weekly Plan")
            self.meal_plan_tabview.delete("Shopping list")
        except ValueError:
            pass
        self.meal_plan_tabview.grid_forget()
        self.meal_plan_frame.grid_forget()
        self.select_frame_by_name("Meal Plan")

    
    def reroll_meal0_button_event(self):
        self.reroll_meal_by_index(0)

    def reroll_meal1_button_event(self):
        self.reroll_meal_by_index(1)

    def reroll_meal2_button_event(self):
        self.reroll_meal_by_index(2)

    def reroll_meal3_button_event(self):
        self.reroll_meal_by_index(3)

    def reroll_meal4_button_event(self):
        self.reroll_meal_by_index(4)

    def reroll_meal5_button_event(self):
        self.reroll_meal_by_index(5)

    
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
