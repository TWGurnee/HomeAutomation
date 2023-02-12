import sys
import tkinter
import tkinter.messagebox
import customtkinter

from scheduler import Scheduler

from shopping_list_generator import MEAL_PLAN_FILE, current_meal_plan_for_table, shopping_list_for_textbox, re_roll_meal

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end")

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


        # create sidebar frame with widgets
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
        self.scheduler_button.grid(row=0, column=0, padx=20, pady=10, sticky="ne")

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
        self.exercise_tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.exercise_tabview.add("Week's Plan")


        self.exercise_tabview.add("Today's Plan")

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
        else:
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


    ### Options Functions ###
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # need teardown functions.


    ### Exercise functions ###



    ### Meal Plan functions ###

    def display_meal_plan(self, MEAL_PLAN_FILE):

        self.meal_plan_tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.meal_plan_tabview.add("Weekly Plan")
        self.meal_plan_tabview.tab("Weekly Plan").grid_rowconfigure((0,1,2,3,4,5), weight=1) #type:ignore

        
        meal_plan = current_meal_plan_for_table(MEAL_PLAN_FILE)

        self.m_frame0 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame0.grid(row=0, padx=20, sticky='ew')
        self.m_frame0.grid_columnconfigure((0,1,2,), weight=1) # type:ignore
        self.m_frame0.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal0_category = customtkinter.CTkLabel(self.m_frame0, text=f'{meal_plan[0][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal0_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal0_name = customtkinter.CTkLabel(self.m_frame0, text=f'{meal_plan[0][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal0_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal0_ingredients = customtkinter.CTkLabel(self.m_frame0, text=f'{meal_plan[0][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal0_ingredients.grid(row=0, column=2, padx=10, sticky='w')
        self.meal0_button = customtkinter.CTkButton(self.m_frame0, corner_radius=0, text="Reroll", command=self.reroll_meal0_button_event)
        self.meal0_button.grid(row=0, column=3, padx=20, sticky="e")

        self.m_frame1 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame1.grid(row=1, padx=20, sticky='ew')
        self.m_frame1.grid_columnconfigure((0,1,2), weight=1) # type:ignore
        self.m_frame1.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal1_category = customtkinter.CTkLabel(self.m_frame1, text=f'{meal_plan[1][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal1_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal1_name = customtkinter.CTkLabel(self.m_frame1, text=f'{meal_plan[1][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal1_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal1_ingredients = customtkinter.CTkLabel(self.m_frame1, text=f'{meal_plan[1][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal1_ingredients.grid(row=0, column=2, padx=10, sticky='w')
        self.meal1_button = customtkinter.CTkButton(self.m_frame1, corner_radius=0, text="Reroll", command=self.reroll_meal1_button_event)
        self.meal1_button.grid(row=0, column=3, padx=20, sticky="e")

        self.m_frame2 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame2.grid(row=2, padx=20, sticky='ew')
        self.m_frame2.grid_columnconfigure((0,1,2), weight=1) # type:ignore
        self.m_frame2.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal2_category = customtkinter.CTkLabel(self.m_frame2, text=f'{meal_plan[2][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal2_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal2_name = customtkinter.CTkLabel(self.m_frame2, text=f'{meal_plan[2][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal2_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal2_ingredients = customtkinter.CTkLabel(self.m_frame2, text=f'{meal_plan[2][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal2_ingredients.grid(row=0, column=2, padx=10, sticky='w')
        self.meal2_button = customtkinter.CTkButton(self.m_frame2, corner_radius=0, text="Reroll", command=self.reroll_meal2_button_event)
        self.meal2_button.grid(row=0, column=3, padx=20, sticky="e")

        self.m_frame3 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame3.grid(row=3, padx=20, sticky='ew')
        self.m_frame3.grid_columnconfigure((0,1,2), weight=1) # type:ignore
        self.m_frame3.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal3_category = customtkinter.CTkLabel(self.m_frame3, text=f'{meal_plan[3][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal3_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal3_name = customtkinter.CTkLabel(self.m_frame3, text=f'{meal_plan[3][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal3_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal3_ingredients = customtkinter.CTkLabel(self.m_frame3, text=f'{meal_plan[3][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal3_ingredients.grid(row=0, column=2, padx=10, sticky='w')
        self.meal3_button = customtkinter.CTkButton(self.m_frame3, corner_radius=0, text="Reroll", command=self.reroll_meal3_button_event)
        self.meal3_button.grid(row=0, column=3, padx=20, sticky="e")

        self.m_frame4 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame4.grid(row=4, padx=20, sticky='ew')
        self.m_frame4.grid_columnconfigure((0,1,2,), weight=1) # type:ignore
        self.m_frame4.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal4_category = customtkinter.CTkLabel(self.m_frame4, text=f'{meal_plan[4][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal4_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal4_name = customtkinter.CTkLabel(self.m_frame4, text=f'{meal_plan[4][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal4_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal4_ingredients = customtkinter.CTkLabel(self.m_frame4, text=f'{meal_plan[4][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal4_ingredients.grid(row=0, column=2, padx=10, sticky='w')
        self.meal4_button = customtkinter.CTkButton(self.m_frame4, corner_radius=0, text="Reroll", command=self.reroll_meal4_button_event)
        self.meal4_button.grid(row=0, column=3, padx=20, sticky="e")

        self.m_frame5 = customtkinter.CTkFrame(self.meal_plan_tabview.tab("Weekly Plan"), height=50, width=940)
        self.m_frame5.grid(row=5, padx=20, sticky='ew')
        self.m_frame5.grid_columnconfigure((0,1,2), weight=1) # type:ignore
        self.m_frame5.grid_columnconfigure(3, weight=1, uniform="reroll") # type:ignore
        self.meal5_category = customtkinter.CTkLabel(self.m_frame5, text=f'{meal_plan[5][0]}', font=customtkinter.CTkFont(size=14, weight="bold"))
        self.meal5_category.grid(row=0, column=0, padx=10, sticky='w')
        self.meal5_name = customtkinter.CTkLabel(self.m_frame5, text=f'{meal_plan[5][1]}', font=customtkinter.CTkFont(size=18, weight="bold"))
        self.meal5_name.grid(row=0, column=1, padx=10, sticky='w')
        self.meal5_ingredients = customtkinter.CTkLabel(self.m_frame5, text=f'{meal_plan[5][2]}', font=customtkinter.CTkFont(size=10, weight="normal"))
        self.meal5_ingredients.grid(row=0, column=2, padx=10, sticky='w')        
        self.meal5_button = customtkinter.CTkButton(self.m_frame5, corner_radius=0, text="Reroll", command=self.reroll_meal5_button_event)
        self.meal5_button.grid(row=0, column=3, padx=20, sticky="e")


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
