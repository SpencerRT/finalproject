#ctrl s to save
import pandas as pd
import dearpygui.dearpygui as dpg
import os

# A dictionary where the key is the name of the file, the value is path of the file
files = {}

# A list of the filenames we can use to index the dictionary and get the path
filenames = []

# A list of keys from the csv
columns = []

# A dictionary where the column names are the keys, the values are the values from the column
csv_df = {}

# Containers for the current keys from csv_df we are using for the graph 
column_x = ""
column_y = ""

# These will be axis widgets, we are just setting them as empty strings to access later
scatter_x_axis = ""  
scatter_y_axis = ""

def setup_dpg():
    dpg.create_context()
    dpg.create_viewport(title='Final Project', width=1000, height=800)
    #dpg.set_viewport_large_icon(os.path.abspath(os.path.dirname(__file__)) + "/site.ico")
    #dpg.set_viewport_small_icon(os.path.abspath(os.path.dirname(__file__)) + "/site.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()

    #with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        #default_font = dpg.add_font(os.path.abspath(os.path.dirname(__file__)) + "/BrixSansRegular.otf", 20)

    #dpg.bind_font(default_font)


def show_file_dialog():
    dpg.show_item("file_dialog_id")

def setup_window():
    global columns
    global scatter_x_axis
    global scatter_y_axis

    with dpg.theme(tag="plottheme"): # this theme can now be referenced as "plottheme" in dpg functions that use it
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 255), tag="plotcolor",category=dpg.mvThemeCat_Plots) # setting white to be the default plot color, this themecolor can be referenced by its tag "plotcolor" in dpg functions that use it
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (255,0,0,255), tag="legendcolor",category=dpg.mvThemeCat_Plots)

    #===============================Load Button===========================================
    dpg.push_container_stack(dpg.add_window(tag="Primary Window"))
    with dpg.group(horizontal=True):
        dpg.add_text("Files:")
        dpg.add_button(label="Load", callback=show_file_dialog)
    
    #=================================ListBoxes========================================
    window_width = dpg.get_item_width("Primary Window")
    with dpg.group(horizontal = True):
        dpg.add_text('X:', tag='X_text')
        with dpg.tooltip("X_text"):
            dpg.add_text("Select X-axis data")
        dpg.add_listbox(columns, num_items=len(columns), callback=on_listbox_dialog_ok, tag="listbox_x",  width=window_width/2)
        
        dpg.add_text('Y:', tag='Y_text')
        with dpg.tooltip("Y_text"):
            dpg.add_text("Select Y-axis data")
        dpg.add_listbox(columns, num_items=len(columns), callback=on_listbox_dialog_ok, tag="listbox_y", width=window_width/2)
    
    #============================File Dialog================================================
    # https://dearpygui.readthedocs.io/en/latest/documentation/file-directory-selector.html
    with dpg.file_dialog(directory_selector=False, show=False, callback=on_file_dialog_ok, cancel_callback=on_file_dialog_cancel, file_count=1, tag="file_dialog_id", width=800, height=600, modal=True):
        dpg.add_file_extension(".csv", color=(123, 255, 132, 255))

    #===========================Scatter Plot================================================
    with dpg.plot(tag="Scatter Plot", label="Scatter Plot", height=400, width=-1):
    
        scatter_x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="Scatter_x") #By default, the x-axis will be edited
        with dpg.plot_axis(dpg.mvYAxis, label="y", tag="Scatter_y") as yaxis:       #Specifying to edit the y-axis
            scatter_y_axis = yaxis
            dpg.add_scatter_series([],[], tag="Scatter Plot Data", label="ff")

        dpg.bind_item_theme("Scatter Plot", "plottheme")
    
    #============================Color Picker============================================
    dpg.add_color_picker((255, 0, 255, 255), callback = color_picker_callback, label="Color Picker", width=200, tag="_color_picker_id")
    dpg.pop_container_stack()
    dpg.set_primary_window("Primary Window", True)

    
#Color picker function

def color_picker_callback(sender, user_data):
    
    rgba32 = [255 * x for x in user_data]
    dpg.set_value("plotcolor", tuple(rgba32))

#File dialog functions

def on_file_dialog_ok(sender, user_data):
    global files
    global filenames
    print(sender, user_data)
    
    filename = user_data["file_name"]
    filepath = user_data["file_path_name"]
    filenames.append(filename)
    files.update({filename:filepath})

    print(files)
    print(filenames)

    populate_listboxes()

def on_file_dialog_cancel():
    print("user cancel")

#Listbox functions
    
def on_listbox_dialog_ok(sender, user_data):
    global column_x
    global column_y

    if sender == 'listbox_x':
        column_x = user_data
    elif sender == 'listbox_y':
        column_y = user_data

    print(column_x, column_y)
    update_plot_values()

def update_plot_values():
    global csv_df
    global column_x
    global column_y

    global scatter_x_axis
    global scatter_y_axis

    float_x = []
    float_y = []

    for x in csv_df.get(column_x):
        float_x.append(float(x))   #Need to be floats in dearpygui
        
    for y in csv_df.get(column_y):
        float_y.append(float(y))
    
    print(float_x)
    print(float_y)
    
    dpg.fit_axis_data(scatter_x_axis)
    dpg.fit_axis_data(scatter_y_axis)

    dpg.set_value("Scatter Plot Data", [float_x, float_y])

def populate_listboxes():
    global files
    global filenames
    global columns
    global csv_df

    #select the first file
    filepath = files[filenames[0]]
    print(filepath)
    csv_df = pd.read_csv(filepath, sep= ',')
    
    for column in csv_df.keys():
        columns.append(column)
        print(column)

    dpg.configure_item("listbox_x", items=columns, num_items=len(columns))
    dpg.configure_item("listbox_y", items=columns, num_items=len(columns))


def main():
    setup_dpg()

    setup_window()
    print("App Entered")
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue() # retrieves and clears queue
        dpg.run_callbacks(jobs)

        #anything you want to do every frame
        window_width = dpg.get_item_width("Primary Window")
        dpg.set_item_width("listbox_x", window_width/2)
        dpg.set_item_width("listbox_y", window_width/2)

        dpg.render_dearpygui_frame()
        
    print("App Terminate")
    dpg.destroy_context()


if __name__ == "__main__":
    main()