font = "Arial"
border_radius = "10"
# "#1e1c23" old
m_main_background_color = "#303030"
# "#2b2b2b" old
m_button_background_color = "#801336"
# "801336" old
m_second_button_background_color = "#c72c41"
# "#ffffff" old
m_border_color = "#610a32"
# "#ffffff" old
m_standard_text_color = "#ffffff"

#############################
# New CocktailWindow Styles #
#############################


css_style = {
    "font": font,
    "border_radius": border_radius,
    "main_background_color": m_main_background_color,
    "button_background_color": m_button_background_color,
    "second_button_background_color": m_second_button_background_color,
    "border_color": m_border_color,
    "standard_text_color": m_standard_text_color
}

windowStyle = """
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

dialogStyle = """

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
