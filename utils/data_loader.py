import pandas as pd

def load_payments(file_path):
    ''' 
    Loads payment data from a given CSV file.

    This function reads a CSV file containing payment data, converts the 'Payment Date' column
    to datetime format, the 'Payed Amount' column to float after replacing commas with dots, 
    and the 'Transaction Number' column to integer. The CSV file is expected to be semicolon 
    delimited and encoded in UTF-8.

    Args:
        file_path (str): The location of the CSV file to be read.

    Returns:
        pandas.DataFrame: A DataFrame containing the payment data.
    '''

    payments = pd.read_csv(file_path, delimiter=';', encoding="utf-8")
    payments['Payment Date'] = pd.to_datetime(payments['Payment Date'])
    payments['Payed Amount'] = payments['Payed Amount'].str.replace(',', '.').astype(float)
    payments['Transaction Number'] = payments['Transaction Number'].astype(int)
    
    return payments

def load_invoices(file_path):
    '''
    Loads invoice data from a given CSV file.

    This function reads a CSV file containing invoice data, converts the 'Invoice Number' and
    'Client ID' columns to integer, the 'Invoice Date' and 'Sale Date' columns to datetime format,
    and the 'Payment Amount' column to float after replacing commas with dots. The CSV file is 
    expected to be semicolon delimited and encoded in UTF-8.

    Args:
        file_path (str): The location of the CSV file to be read.

    Returns:
        pandas.DataFrame: A DataFrame containing the invoice data.
    '''

    invoices = pd.read_csv(file_path, delimiter=';', encoding="utf-8")
    invoices['Invoice Number'] = invoices['Invoice Number'].astype(int)
    invoices['Client ID'] = invoices['Client ID'].astype(int)
    invoices['Invoice Date'] = pd.to_datetime(invoices['Invoice Date'])
    invoices['Sale Date'] = pd.to_datetime(invoices['Sale Date'])
    invoices['Payment Amount'] = invoices['Payment Amount'].str.replace(',', '.').astype(float)

    return invoices
