# import time
# import pandas as pd
# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import re
# from io import BytesIO

# # Input fields
# starting_roll_no = st.number_input('Starting Roll Number', min_value=0, value=400001)
# ending_roll_no = st.number_input('Ending Roll Number', min_value=0, value=400005)
# output_filename = st.text_input('Output File Name')

# if st.button('Start Scraping') and output_filename:
#     # Sanitize output filename
#     output_filename = re.sub(r'[<>:"/\\|?*]', '_', output_filename)

#     # Configure Chrome WebDriver
#     # NOTE: Update the path to your actual ChromeDriver location
#     service = Service()
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')  # Uncomment for headless mode
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.maximize_window()
#     driver.set_page_load_timeout(30)  # Set page load timeout to 30 seconds

#     # Navigate to the website with error handling
#     try:
#         driver.get('https://result.biselahore.com/')
#     except TimeoutException:
#         st.error("The website took too long to load. Please check your connection and try again.")
#         driver.quit()
#         st.stop()

#     wait = WebDriverWait(driver, 10)

#     # Select Matric option
#     try:
#         matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
#         driver.execute_script("arguments[0].click();", matric_option)
#     except Exception as e:
#         st.error(f"Error clicking matric option: {e}")
#         driver.quit()
#         raise

#     data = []  # Initialize data storage

#     def scrape_roll_number(roll_no):
#         try:
#             # Input Roll Number
#             roll_number = wait.until(EC.presence_of_element_located((By.ID, 'txtFormNo')))
#             roll_number.clear()
#             time.sleep(0.5)
#             roll_number.send_keys(roll_no)
#             time.sleep(0.5)

#             # Select Exam Type
#             exam_type = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamType')))
#             select_exam_type = Select(exam_type)
#             select_exam_type.select_by_visible_text('Part-I (ANNUAL)')  # Adjust if needed

#             # Select Year
#             exam_year = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamYear')))
#             select_exam_year = Select(exam_year)
#             select_exam_year.select_by_visible_text('2025')  # Adjust if needed

#             # Submit Form
#             submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Button1")))
#             driver.execute_script("arguments[0].click();", submit_button)

#             # Wait for Results
#             registration_no = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '#lblBFARM'))
#             ).text
            
#             # Wait for Date of Birth
#             date_of_birth = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '#lblDOB'))
#             ).text

#             # Collect Data
#             detail = {
#                 'roll_no': roll_no,
#                 'registration_no': registration_no,
#                 'date_of_birth' : date_of_birth
#             }
            
#             data.append(detail)
#             print(detail)

#             # Navigate back to the form page
#             driver.back()
#             time.sleep(2)  # Give time for the form page to reload

#             return True

#         except TimeoutException:
#             st.warning(f"No data found for Roll No: {roll_no}")
#             driver.get('https://result.biselahore.com/')
#             time.sleep(2)
#             try:
#                 matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
#                 driver.execute_script("arguments[0].click();", matric_option)
#             except Exception as inner_e:
#                 st.error(f"Error refreshing matric option: {inner_e}")
#             return False
#         except Exception as e:
#             st.warning(f"Failed to scrape data for Roll No: {roll_no} - {e}")
#             driver.get('https://result.biselahore.com/')
#             time.sleep(2)
#             try:
#                 matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
#                 driver.execute_script("arguments[0].click();", matric_option)
#             except Exception as inner_e:
#                 st.error(f"Error refreshing matric option: {inner_e}")
#             return False

#     for roll_no in range(starting_roll_no, ending_roll_no + 1):
#         scrape_roll_number(roll_no)

#     # Close the browser
#     driver.quit()

#     # Create DataFrame and Display Results
#     df = pd.DataFrame(data)
#     st.dataframe(df)

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Sheet1')
#     output.seek(0)

#     st.download_button(
#         label="Download Excel",
#         data=output,
#         file_name=f'{output_filename}.xlsx',
#         mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#     )


import time
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from io import BytesIO
from datetime import datetime

# Input fields
starting_roll_no = st.number_input('Starting Roll Number', min_value=0, value=400001)
ending_roll_no = st.number_input('Ending Roll Number', min_value=0, value=400005)

# Add date filtering option
filter_by_date = st.checkbox('Filter by Date of Birth (>=2011)', value=True)
cutoff_year = st.number_input('Cutoff Year', min_value=1900, max_value=2030, value=2011)

output_filename = st.text_input('Output File Name')

def parse_date(date_str):
    """Parse date string and return datetime object"""
    try:
        # Handle different date formats (dd/mm/yyyy, dd-mm-yyyy, etc.)
        for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y/%m/%d']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
    except:
        return None

def is_date_after_cutoff(date_str, cutoff_year):
    """Check if date is after the cutoff year"""
    parsed_date = parse_date(date_str)
    if parsed_date:
        return parsed_date.year > cutoff_year
    return False

if st.button('Start Scraping') and output_filename:
    # Sanitize output filename
    output_filename = re.sub(r'[<>:"/\\|?*]', '_', output_filename)

    # Configure Chrome WebDriver
    service = Service()
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(30)

    # Navigate to the website with error handling
    try:
        driver.get('https://result.biselahore.com/')
    except TimeoutException:
        st.error("The website took too long to load. Please check your connection and try again.")
        driver.quit()
        st.stop()

    wait = WebDriverWait(driver, 10)

    # Select Matric option
    try:
        matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
        driver.execute_script("arguments[0].click();", matric_option)
    except Exception as e:
        st.error(f"Error clicking matric option: {e}")
        driver.quit()
        raise

    data = []  # Initialize data storage
    filtered_data = []  # Store filtered data

    def scrape_roll_number(roll_no):
        try:
            # Input Roll Number
            roll_number = wait.until(EC.presence_of_element_located((By.ID, 'txtFormNo')))
            roll_number.clear()
            time.sleep(0.5)
            roll_number.send_keys(roll_no)
            time.sleep(0.5)

            # Select Exam Type
            exam_type = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamType')))
            select_exam_type = Select(exam_type)
            select_exam_type.select_by_visible_text('Part-I (ANNUAL)')

            # Select Year
            exam_year = wait.until(EC.presence_of_element_located((By.ID, 'ddlExamYear')))
            select_exam_year = Select(exam_year)
            select_exam_year.select_by_visible_text('2025')

            # Submit Form
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "Button1")))
            driver.execute_script("arguments[0].click();", submit_button)

            # Wait for Results
            registration_no = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#lblBFARM'))
            ).text
            
            # Wait for Date of Birth
            date_of_birth = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#lblDOB'))
            ).text

            # Collect Data
            detail = {
                'roll_no': roll_no,
                'registration_no': registration_no,
                'date_of_birth': date_of_birth
            }
            
            # Always add to main data
            data.append(detail)
            
            # Filter by date if option is enabled
            if filter_by_date:
                if is_date_after_cutoff(date_of_birth, cutoff_year):
                    filtered_data.append(detail)
                    st.success(f"✓ Roll No: {roll_no} - DOB: {date_of_birth} (After {cutoff_year})")
                else:
                    st.info(f"○ Roll No: {roll_no} - DOB: {date_of_birth} (Before/At {cutoff_year}) - Filtered out")
            else:
                filtered_data.append(detail)
            
            print(detail)

            # Navigate back to the form page
            driver.back()
            time.sleep(2)

            return True

        except TimeoutException:
            st.warning(f"No data found for Roll No: {roll_no}")
            driver.get('https://result.biselahore.com/')
            time.sleep(2)
            try:
                matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
                driver.execute_script("arguments[0].click();", matric_option)
            except Exception as inner_e:
                st.error(f"Error refreshing matric option: {inner_e}")
            return False
        except Exception as e:
            st.warning(f"Failed to scrape data for Roll No: {roll_no} - {e}")
            driver.get('https://result.biselahore.com/')
            time.sleep(2)
            try:
                matric_option = wait.until(EC.presence_of_element_located((By.ID, 'rdlistCourse_0')))
                driver.execute_script("arguments[0].click();", matric_option)
            except Exception as inner_e:
                st.error(f"Error refreshing matric option: {inner_e}")
            return False

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_rolls = ending_roll_no - starting_roll_no + 1
    current_progress = 0

    for roll_no in range(starting_roll_no, ending_roll_no + 1):
        status_text.text(f'Processing Roll No: {roll_no}')
        scrape_roll_number(roll_no)
        
        current_progress += 1
        progress_bar.progress(current_progress / total_rolls)

    # Close the browser
    driver.quit()

    # Create DataFrames
    df_all = pd.DataFrame(data)
    df_filtered = pd.DataFrame(filtered_data)

    # Display results
    st.subheader("Results Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Records", len(df_all))
    with col2:
        st.metric("Filtered Records (After 2011)", len(df_filtered))

    # Show filtered data
    if filter_by_date and len(df_filtered) > 0:
        st.subheader(f"Filtered Data (Date of Birth > {cutoff_year})")
        st.dataframe(df_filtered)
    elif not filter_by_date:
        st.subheader("All Data")
        st.dataframe(df_all)
    else:
        st.warning(f"No records found with date of birth after {cutoff_year}")

    # Download options
    st.subheader("Download Options")
    
    # Choose which dataset to download
    download_choice = st.radio(
        "Choose data to download:",
        ["Filtered Data Only", "All Data", "Both (Separate Sheets)"]
    )

    if download_choice == "Filtered Data Only" and len(df_filtered) > 0:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Filtered_Data')
        output.seek(0)
        
        st.download_button(
            label="Download Filtered Data Excel",
            data=output,
            file_name=f'{output_filename}_filtered.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    
    elif download_choice == "All Data":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_all.to_excel(writer, index=False, sheet_name='All_Data')
        output.seek(0)
        
        st.download_button(
            label="Download All Data Excel",
            data=output,
            file_name=f'{output_filename}_all.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    
    elif download_choice == "Both (Separate Sheets)":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_all.to_excel(writer, index=False, sheet_name='All_Data')
            if len(df_filtered) > 0:
                df_filtered.to_excel(writer, index=False, sheet_name='Filtered_Data')
        output.seek(0)
        
        st.download_button(
            label="Download Complete Excel (Both Sheets)",
            data=output,
            file_name=f'{output_filename}_complete.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    # Show final statistics
    if len(data) > 0:
        st.subheader("Final Statistics")
        
        # Convert dates for analysis
        dates_parsed = []
        for item in data:
            parsed_date = parse_date(item['date_of_birth'])
            if parsed_date:
                dates_parsed.append(parsed_date.year)
        
        if dates_parsed:
            st.write(f"Date Range: {min(dates_parsed)} - {max(dates_parsed)}")
            st.write(f"Records after {cutoff_year}: {len(df_filtered)}")
            st.write(f"Records at/before {cutoff_year}: {len(df_all) - len(df_filtered)}")