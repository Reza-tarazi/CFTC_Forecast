import pandas as pd
import web_scraper
import cftc_data
#=====================
browser = cftc_data.setup_browser()
lines = cftc_data.scrape_text(browser)
pairs = cftc_data.extract_pairs(lines)
positions = cftc_data.extract_positions(lines)
change_positions = cftc_data.extract_change_positions(lines)
browser.quit()
#=========================================================
#======================DataFrames=========================
#=========================================================
topic = ['Long_Dealers','Short_Dealers','Spreading_Dealers',
        'Long_AssetManager','Short_AssetManager','Spreading_AssetManager',
        'Long_Leveraged','Short_Leveraged','Spreading_Leveraged',
        'Long_Reportables','Short_Reportables','Spreading_Reportables',
        'Long_Nonreportable','Short_Nonreportable']
df2 = pd.DataFrame(data=change_positions,index=pairs,columns=topic)

def evaluate_position(row):
    if (row['Long_Leveraged'] < row['Short_Leveraged']) & (row['Long_AssetManager'] < row['Short_AssetManager']):
        return "Bearish"
    elif (row['Long_Leveraged'] > row['Short_Leveraged']) & (row['Long_AssetManager'] > row['Short_AssetManager']):
        return "Bullish" 
    else: 
        return "Neutral" 

df2["Forecast"] = df2.apply(evaluate_position, axis=1)
df2_str_with_index = df2.to_string(index=True)
f = open("15Nov-CFTC.txt", "a")   
f.write(df2_str_with_index)
f.close()

Forecast_15nov = df2["Forecast"].to_frame()
Forecast_15nov_str_with_index = Forecast_15nov.to_string(index=True)
print(Forecast_15nov)
df3 = pd.DataFrame(data=Forecast_15nov,index=pairs,columns=["15Nov_Forecast"])
df3_str_with_index = df3.to_string(index=True)
f = open("Forecast_15Nov-CFTC.txt", "a")   
f.write(Forecast_15nov_str_with_index)
f.close()