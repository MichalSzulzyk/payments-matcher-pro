def main():
    payments = load_payments("Datasets/Bank_Payments.csv")
    invoices = load_invoices("Datasets/Property_DB_Invoices.csv")
    match_payments_invoices(payments, invoices)
 
if __name__ == "__main__":
    main()
