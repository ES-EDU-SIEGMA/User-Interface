window_style = """
QWidget{
    background-color: #303030;
}

QPushButton{
    background-color: #801336;
    color: #ffffff;
    padding: 60%;
    font-size: 11pt;
    margin: 5%;
    font-size: 11pt;
    border: 2px solid #610a32;
    border-radius: 10px;
    margin-left: 20%;
}

QLabel{
    color: #ffffff;
    font-size: 15pt;
    font-family: Arial;
}

QLineEdit{
    color: #ffffff;
    font-size: 10pt;
}

QListWidget{
    show-decoration-selected: 1; /* make the selection span the entire width of the view */
    color: #ffffff;
}

QListView::item {
    font: Arial;
    font-size: 15pt;
    height: 100px;
}

QListView::item:alternate {
    background: #EEEEEE;
}

QListView::item:selected {
    background-color: #c72c41;
    border: 1px solid #610a32;
    border-color: #610a32;
}

QListView::item:selected:active {
    background-color: #801336;
    border-color: #610a32;
}



QListView::item:hover {
    background-color: #c72c41;
}
"""
new_drink_window_recipe_label_color = "#ffffff"
new_drink_window_recipe_font_size = "15pt"
new_drink_window_recipe_font_family = "Arial"

style_ndw_recipe_label: str = \
    f"color: {new_drink_window_recipe_label_color};" \
    f"font-size: {new_drink_window_recipe_font_size};" \
    f"font-family: {new_drink_window_recipe_font_family};"

new_drink_window_line_edit_recipe_color = "#ffffff"
new_drink_window_line_edit_font_size = "15pt"

style_ndw_line_edit_recipe_name: str = \
    f"color: {new_drink_window_line_edit_recipe_color};" \
    f"font-size: {new_drink_window_line_edit_font_size};"

dialog_style = """

QWidget{
    background-color: #303030;
}

QPushButton{
    background-color: #801336;
    color: #ffffff;
    padding: 5%;
    font-size: 11pt;
    margin: 5%;
    border: 2px solid #610a32;
    border-radius: 10px;
    margin-left: 20%;
}

QLabel{
    color: #ffffff;
    font-size: 11pt;
    font-family: Arial;
}

QLineEdit{
    color: #ffffff;
    font-size: 10pt;
}
"""
