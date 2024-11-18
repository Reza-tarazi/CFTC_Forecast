from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_browser(url='https://www.cftc.gov/dea/options/financial_lof.htm'):
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(2)
    return browser

def scrape_text(browser):
    s = str(browser.find_element(By.XPATH, '/html/body/pre').text)
    lines = s.split("\n")
    return [line for line in lines if line.strip()]

def extract_pairs(lines):
    pairlist = []
    text = "Pair:" + "\n" + "\n"
    for i in range(6, len(lines) - 1, 17):
        dash_index2 = lines[i].find("- ")
        key = lines[i][:dash_index2].strip()
        text += str(key) + "\n"
        pairlist.append(key)
    return pairlist

def extract_positions(lines):
    positions = []
    text1 = "positions:" + "\n" + "\n"
    for i in range(9, len(lines) - 1, 17):
        dash_index2 = lines[i].find("- ")
        key = lines[i][:dash_index2].strip()
        key2 = key.replace(',', '')
        positions2 = key2.split()
        float_numbers = [safe_float_conversion(comp) for comp in positions2 if safe_float_conversion(comp) is not None]
        text1 += str(float_numbers) + "\n"
        positions.append(float_numbers)
    return positions

def extract_change_positions(lines):
    Changepositions = []
    text2 = "Changepositions:" + "\n" + "\n"
    for i in range(11, len(lines) - 1, 17):
        dash_index2 = lines[i].find("- ")
        key = lines[i][:dash_index2].strip()
        key2 = key.replace(',', '')
        components = key2.split()
        float_numbers = [safe_float_conversion(comp) for comp in components if safe_float_conversion(comp) is not None]
        text2 += str(float_numbers) + "\n"
        Changepositions.append(float_numbers)
    return Changepositions

def safe_float_conversion(s):
    try:
        return float(s)
    except ValueError:
        return None

# Example usage:
"""if __name__ == "__main__":
    browser = setup_browser()
    lines = scrape_text(browser)
    pairs = extract_pairs(lines)
    positions = extract_positions(lines)
    change_positions = extract_change_positions(lines)
    browser.quit()"""
