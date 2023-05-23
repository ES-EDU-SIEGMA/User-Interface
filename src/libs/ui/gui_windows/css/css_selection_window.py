selection_window_background_color = "#303030"
selection_window_text_color = "#ffffff"

selection_window_header_label_text_color = "#ffffff"
selection_window_header_label_font_size = "30pt"
selection_window_header_label_font = "Arial"
selection_window_header_label_margin = "25%"

selection_window_sub_header_label_text_color = "#ffffff"
selection_window_sub_header_label_font_size = "15pt"
selection_window_sub_header_label_font = "Arial"

selection_window_description_label_text_color = "#ffffff"
selection_window_description_label_font_size = "12pt"
selection_window_description_label_font = "Arial"

style_selection_window: str = \
    f"background-color: {selection_window_background_color};"

# sw:= selection window
style_sw_header_label: str = \
    f"color: {selection_window_header_label_text_color};" \
    f"font-size: {selection_window_header_label_font_size};" \
    f"font-family: {selection_window_header_label_font};" \
    f"margin-top: {selection_window_header_label_margin};"

style_sw_sub_header_label: str = \
    f"color: {selection_window_sub_header_label_text_color};" \
    f"font-size: {selection_window_sub_header_label_font_size};" \
    f"font-family: {selection_window_sub_header_label_font};"

style_sw_description_label: str = \
    f"color: {selection_window_description_label_text_color};" \
    f"font-size: {selection_window_description_label_font_size};" \
    f"font-family: {selection_window_description_label_font};"

# Button styles

selection_window_button_exit_background_color = "#801336"
selection_window_button_exit_text_color = "#ffffff"
selection_window_button_exit_padding = "60%"
selection_window_button_exit_font_size = "11pt"
selection_window_button_exit_font = "Arial"
selection_window_button_exit_border = "2px solid #610a32"
selection_window_button_exit_border_radius = "10px"
selection_window_button_exit_margin_left = "20%"

selection_window_button_new_cocktail_background_color = "#801336"
selection_window_button_new_cocktail_text_color = "#ffffff"
selection_window_button_new_cocktail_padding = "60%"
selection_window_button_new_cocktail_font_size = "11pt"
selection_window_button_new_cocktail_font = "Arial"
selection_window_button_new_cocktail_border = "2px solid #610a32"
selection_window_button_new_cocktail_border_radius = "10px"
selection_window_button_new_cocktail_margin_left = "20%"

selection_window_button_edit_hoppers_background_color = "#801336"
selection_window_button_edit_hoppers_text_color = "#ffffff"
selection_window_button_edit_hoppers_padding = "60%"
selection_window_button_edit_hoppers_font_size = "11pt"
selection_window_button_edit_hoppers_font = "Arial"
selection_window_button_edit_hoppers_border = "2px solid #610a32"
selection_window_button_edit_hoppers_border_radius = "10px"
selection_window_button_edit_hoppers_margin_left = "20%"

style_sw_exit_button: str = \
    f"background-color: {selection_window_button_exit_background_color};" \
    f"color: {selection_window_button_exit_text_color};"\
    f"padding: {selection_window_button_exit_padding};" \
    f"font-size: {selection_window_button_exit_font_size};" \
    f"font:{selection_window_button_exit_font}"\
    f"border: {selection_window_button_exit_border};"\
    f"border-radius: {selection_window_button_exit_border_radius};" \
    f"margin-left: {selection_window_button_exit_margin_left};"

style_sw_new_cocktail_button: str = \
    f"background-color: {selection_window_button_new_cocktail_background_color};" \
    f"color: {selection_window_button_new_cocktail_text_color};"\
    f"padding: {selection_window_button_new_cocktail_padding};" \
    f"font-size: {selection_window_button_new_cocktail_font_size};" \
    f"font{selection_window_button_new_cocktail_font}"\
    f"border: {selection_window_button_new_cocktail_border };" \
    f"border-radius: {selection_window_button_new_cocktail_border_radius};" \
    f"margin-left: {selection_window_button_new_cocktail_margin_left};"

style_sw_edit_hoppers_button:str = \
    f"background-color: {selection_window_button_edit_hoppers_background_color};" \
    f"color: {selection_window_button_edit_hoppers_text_color};" \
    f"padding: {selection_window_button_edit_hoppers_padding};" \
    f"font-size: {selection_window_button_edit_hoppers_font_size};" \
    f"font: {selection_window_button_edit_hoppers_font}"\
    f"border: {selection_window_button_edit_hoppers_border };" \
    f"border-radius: {selection_window_button_edit_hoppers_border_radius};" \
    f"margin-left: {selection_window_button_edit_hoppers_margin_left};"

# Widgets

selection_window_all_drinks_frame_border = "0px solid #610a32"
selection_window_all_drinks_text_color = "#ffffff"

style_sw_all_drinks_frame: str = \
    f"border: {selection_window_all_drinks_frame_border };" \
    f"color: {selection_window_all_drinks_text_color};"

selection_window_button_beverage_background_color = "#c72c41"
selection_window_button_beverage_text_color = "#ffffff"
selection_window_button_beverage_padding_top = "70%"
selection_window_button_beverage_padding_bottom = "70%"
selection_window_button_beverage_font_size = "11pt"
selection_window_button_beverage_font = "Arial"
selection_window_button_beverage_margin = "5%"

selection_window_button_mix_drink_background_color = "#c72c41"
selection_window_button_mix_drink_text_color = "#ffffff"
selection_window_button_mix_drink_padding_top = "70%"
selection_window_button_mix_drink_padding_bottom = "70%"
selection_window_button_mix_drink_font_size = "11pt"
selection_window_button_mix_drink_font = "Arial"
selection_window_button_mix_drink_margin = "5%"

style_selection_window_drink_button: str = \
    f"background-color: {selection_window_button_beverage_background_color};"\
    f"color: {selection_window_button_beverage_text_color};" \
    f"padding-top: {selection_window_button_beverage_padding_top};" \
    f"padding-bottom: {selection_window_button_beverage_padding_bottom};" \
    f"font-size: {selection_window_button_beverage_font_size};" \
    f"font: {selection_window_button_beverage_font}" \
    f"margin: {selection_window_button_beverage_margin};"

style_sw_mix_drink_button: str = \
    f"background-color: {selection_window_button_mix_drink_background_color};" \
    f"color: {selection_window_button_mix_drink_text_color};" \
    f"padding-top: {selection_window_button_mix_drink_padding_top};" \
    f"padding-bottom: {selection_window_button_mix_drink_padding_bottom};" \
    f"font-size: {selection_window_button_mix_drink_font_size};" \
    f"font: {selection_window_button_mix_drink_font}" \
    f"margin: {selection_window_button_mix_drink_margin};" \

