import pandas as pd
import time
import os
import datetime
import sys


def clean_lists(*lists):
    for lst in lists:
        lst.clear()


def add_lists_to_excel(choice, subChoice, thirdChoice, sequential_numbers, country_list, state_list, distance_list, zip_code, status_list, year_list, model_name, price_list, odometer_list, autonomy_list, trim_item_list, external_color_list, internal_color_list, wheel_item_list, vehicle_history_list, autopilot_list, additional_info_list, hyperlink_list):
    # Create a DataFrame from the lists
    data = {
        'ID': sequential_numbers,
        'Pays': country_list,
        'Etat/province': state_list,
        'Distance': distance_list,
        'Code Postal': zip_code,
        'Statut': status_list,
        'Annee du modele': year_list,
        'Modele': model_name,
        'Prix': price_list,
        'Odometre': odometer_list,
        'Autonomie': autonomy_list,
        'Garniture/trim ': trim_item_list,
        'Peinture extérieure': external_color_list,
        'Couleur intérieure ': internal_color_list,
        'Roues/Wheels ': wheel_item_list,
        'Historique du vehicule ': vehicle_history_list,
        'Autopilote ': autopilot_list,
        'Options supplémentaires ': additional_info_list,
        'Links': hyperlink_list
    }

    country_name_index = int(subChoice)
    brand_name_index = int(choice)
    status_option_list_index = int(thirdChoice)
    df = pd.DataFrame(data)
    now = datetime.datetime.now()
    datestamp = now.strftime('%Y-%m-%d')
    country_file_name = ['USA', 'Canada', 'USA_Canada']
    brand_name = ['BMW', 'Mercedes', 'Polestar', 'Tesla', 'Audi']
    status_options_list = ['New', 'Used', 'All']
    script_dir = os.path.dirname(sys.argv[0])
    file_path = os.path.join(script_dir, f'{brand_name[brand_name_index]}_{country_file_name[country_name_index]}_{status_options_list[status_option_list_index]}_{datestamp}.xlsx')

    # Create a new Excel writer
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    # Write the DataFrame to different sheets
    df.to_excel(writer, sheet_name=f'{brand_name[brand_name_index]}', index=False)
    # Save the Excel file and close the writer
    writer.close()

    print('#################### Program Complete #################### ')
