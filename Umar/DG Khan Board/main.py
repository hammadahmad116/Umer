from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import streamlit as st
from io import BytesIO

starting_roll_no = st.number_input('Starting Roll Number', min_value=0, value=762372)
ending_roll_no = st.number_input('Ending Roll Number', min_value=0, value=762380)
output_filename = st.text_input('Output File Name')

if st.button('Start Scraping') and output_filename:
    service = Service()

    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get('https://bisedgkhan.edu.pk/RESSUULT_NA200025/index.php')

    wait = WebDriverWait(driver, 10)

    data = []

    for roll_no in range(starting_roll_no, ending_roll_no):
        if roll_no:
            try:
                roll_no_input = wait.until(EC.presence_of_element_located((By.NAME, 'rno')))
                roll_no_input.clear()
                time.sleep(0.5)
                roll_no_input.send_keys(roll_no)
                time.sleep(0.5)

                submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Search for Result']")))
                submit_btn.click()


                registration_no = driver.find_element(By.XPATH, "//span[contains(text(), 'Reg No:')]").text
                registration_no = registration_no.split(':')[1].strip()
                
                detail = {
                    'roll_no': roll_no,
                    'registration_no': registration_no,
                }
                # institute_name = driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_LblDistOrInstWithGrade').text
                # detail = {
                #     'roll_no': roll_no,	
                #     'school_name': institute_name,
                #     'registration_no': institute_name
                # }
                data.append(detail)
                print(detail)
            except:
                pass

    driver.quit()

    # df = pd.DataFrame(data)
    # st.dataframe(df)
    # csv = df.to_csv(index=False)

    # # Create a download button
    # st.download_button(
    #     label="Download CSV",
    #     data=csv,
    #     file_name=f'{output_filename}.csv',
    #     mime='text/csv',
    # )
    # Create DataFrame and Display Results
    df = pd.DataFrame(data)
    st.dataframe(df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)

    st.download_button(
        label="Download Excel",
        data=output,
        file_name=f'{output_filename}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )