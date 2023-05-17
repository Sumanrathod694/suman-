import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import wbdata


def retrieve_data(indicator_codes):
    # Retrieve the data from the World Bank API
    data = wbdata.get_dataframe(indicator_codes, convert_date=True)
    # Clean up the dataframe
    data = data.reset_index()
    data = data.rename(columns={'country': 'Country', 'date': 'Year'})
    return data
def save_data(data, filename):
    # Save the data to a CSV file
    data.to_csv(filename, index=False)

def read_worldbank_data(filename):
    # Read the data from the CSV file
    df = pd.read_csv(filename)
    
    # Clean up the dataframe
    df = df.rename(columns={'country': 'Country', 'date': 'Year'})
    df = df.dropna()
    
    return df

def manipulate_data(df):
    # Pivot the dataframe to have years as columns
    df_years = df.pivot(index='Country', columns='Year')
    
    # Pivot the dataframe again to have countries as columns
    df_countries = df.pivot(index='Year', columns='Country')
    
    # Clean up the transposed dataframes
    df_years.columns = df_years.columns.droplevel()
    df_countries.columns = df_countries.columns.droplevel()
    
    return df_years, df_countries

def explore_indicators(df, countries):
    # Select specific indicators of interest
    indicators = ['CO2 emissions (kt)', 'GDP (current US$)', 'Population, total', 'Energy use per capita (kg of oil equivalent)', 'Arable land (hectares per person)', 'Forest area (sq. km)', 'Population growth (annual %)']
    
    # Filter the data for the selected countries and indicators
    df_selected = df[df['Country'].isin(countries)][['Country', 'Year'] + indicators]
    
    # Calculate summary statistics for the selected indicators
    summary_stats = df_selected.groupby('Country')[indicators].describe().transpose()
    
    return df_selected, summary_stats

def analyze_correlations(df_selected):
    # Select specific indicators of interest
    indicators = ['CO2 emissions (kt)', 'Energy use per capita (kg of oil equivalent)', 'GDP (current US$)', 'Population, total']
    
    # Calculate correlations between indicators
    correlation_matrix = df_selected[indicators].corr()
    
    return correlation_matrix

def plot_time_series(df, indicator, countries, title=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(8, 6))
    for country in countries:
        sns.lineplot(data=df[df['Country'] == country], x='Year', y=indicator, label=country)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def plot_heatmap(data, title=None):
    plt.figure(figsize=(8, 6))
    sns.heatmap(data, cmap='YlGnBu', annot=True)
    plt.title(title)
    plt.show()


def main():
    # Specify the filename of the World Bank data
    filename = 'worldbank_data.csv'
    
    # Read the World Bank data
    df = read_worldbank_data(filename)
    
    # Manipulate the data
    df_years, df_countries = manipulate_data(df)
    
    # Explore indicators for selected countries
    countries = ['United States', 'China', 'India']
    df_selected, summary_stats = explore_indicators(df, countries)
    
    # Analyze correlations for selected countries
    correlation_matrix = analyze_correlations(df_selected)
    
    # Plot CO2 emissions time series for selected countries
    plot_time_series(df_selected, 'CO2 emissions (kt)', countries, title='CO2 Emissions Over Time', xlabel='Year', ylabel='CO2 emissions (kt)')
    
    # Plot GDP time series for selected countries
    plot_time_series(df_selected, 'GDP (current US$)', countries, title='GDP Over Time', xlabel='Year', ylabel='GDP (current US$)')

    # Plot Population growth time series for selected countries
    plot_time_series(df_selected, 'Population growth (annual %)', countries, title='Population Growth Over Time', xlabel='Year', ylabel='Population growth (annual %)')

    # Plot Energy use per capita time series for selected countries
    plot_time_series(df_selected, 'Energy use per capita (kg of oil equivalent)', countries, title='Energy Use per Capita Over Time', xlabel='Year', ylabel='Energy use per capita (kg of oil equivalent)')

    # Plot Arable land per person time series for selected countries
    plot_time_series(df_selected, 'Arable land (hectares per person)', countries, title='Arable Land per Person Over Time', xlabel='Year', ylabel='Arable land (hectares per person)')

    # Plot Forest area time series for selected countries
    plot_time_series(df_selected, 'Forest area (sq. km)', countries, title='Forest Area Over Time', xlabel='Year', ylabel='Forest area (sq. km)')

    # Plot correlation heatmap
    plot_heatmap(correlation_matrix, title='Correlation Heatmap')
    
    # Print summary statistics for selected indicators
    print(summary_stats)

# Define the indicator codes for the data we want to retrieve
indicator_codes = {
    'EN.ATM.CO2E.KT': 'CO2 emissions (kt)',
    'EG.USE.PCAP.KG.OE': 'Energy use per capita (kg of oil equivalent)',
    'NY.GDP.MKTP.CD': 'GDP (current US$)',
    'SP.POP.TOTL': 'Population, total',
    'SP.POP.GROW': 'Population growth (annual %)',
    'AG.LND.ARBL.HA.PC': 'Arable land (hectares per person)',
    'AG.LND.FRST.K2': 'Forest area (sq. km)',
}

# Retrieve and save the data
data = retrieve_data(indicator_codes)
save_data(data, 'worldbank_data.csv')


if __name__ == '__main__':
    # Specify the filename of the World Bank data
    filename = 'worldbank_data.csv'
    
    # Run the main program
    main()
