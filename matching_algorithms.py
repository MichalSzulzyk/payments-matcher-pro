import re
from data_loader import load_payments, load_invoices
from string_similarity import get_similarity

def main():
    payments = load_payments("Datasets/Bank_Payments.csv")
    invoices = load_invoices("Datasets/Property_DB_Invoices.csv")
    match_payments_invoices(payments, invoices)
 

def match_payments_invoices(payments, invoices):

    # Initialize match status columns
    payments['Merged'] = "Not Merged"
    invoices['Transaction Number'] = 0
    invoices['Matched With'] = "Not Matched"



    # Define helper function to split text
    def split(txt, seps):

        
        """
        Splits a given text string based on multiple separators, extracts date patterns, and converts numeric substrings to integers.
        
        Args:
            txt (str): The input text string to split.
            seps (list): A list of separator characters to use for splitting the input text.
        
        Returns:
            list: A list containing the split text elements, with numeric elements converted to integers and date patterns as integers.
        
        Example:
            >>> split("Invoice 123, 10/11/2022", [',', ';', ' ', '_'])
            ['Invoice', 123, 10112022]
        """
        
        default_sep = seps[0]

        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)

        pattern = r"\d{2}/\d{2}/\d{4}"
        matches = re.findall(pattern, txt)
        txt = re.sub(pattern, "", txt)

        lst = [i.strip() for i in txt.split(default_sep)]

        for i in range(len(lst)):
            if lst[i].isdigit():
                lst[i] = int(lst[i])
            elif lst[i].replace(".", "", 1).isdigit():
                lst[i] = int(float(lst[i]))

        for match in matches:
            match_int = int(match.replace("/", ""))
            lst.append(match_int)

        return lst

    # Define separators for payment names
    separators = [',', ';', ' ', '_']

    print(payments)
    print(invoices)



        # Perform matching operations
    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice["Matched With"] == "Not Matched":
                    
                    # Spliting strings in Payment Name, str numbers to integers, reformating Invoice Name 10/2023/2023 to int
                    payment_name_list = split(payment['Payment Name'], separators)
                    
                    # Extracting Int number from Invoice Name 10/2023/2023 -> 1020232023 (df2)
                    invoice_num_name = re.findall(r'\d+', invoice['Invoice Name'])[:3]
                    invoice_num = ''.join(invoice_num_name)
                    invoice_num = int(invoice_num)

                    # List of any numbers connected to the property 
                    nums_to_check = [invoice['Invoice Number'], invoice['Client ID'], invoice_num]

                    # Checking if any of the numbers connected to the propery is present in the Payment Name (proper entries)
                    for num in nums_to_check:
                        if num in payment_name_list and payment['Payed Amount'] == invoice['Payment Amount']:
                            invoices.at[j, "Matched With"] = payment['Unique Change Code']
                            payments.at[i, "Merged"] = "Correct Amount, Payment data ok"
                            break

                    
                    # Checking if any of the numbers connected to the propery is present 
                    # in the Payment Name but payment amount is wrong
                        elif num in payment_name_list and payment['Payed Amount'] != invoice['Payment Amount']:
                            invoices.at[j, "Matched With"] = payment['Unique Change Code']
                            payments.at[i, "Merged"] = "Wrong Amount, Payment data ok"
                            break

    # Checking Name and a Surname on the Incoming Payment and the Invoice list and checking the Amount
    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice["Matched With"] == "Not Matched":

                    if payment['Name and Surname'] == invoice['Name and Surname'] and payment['Payed Amount'] == invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payment['Unique Change Code']   
                        payments.at[i, "Merged"] = "Correct Amount, but only Name and Surname Match"
                        break
                    
    # Levenshtein Distance Threshold
    threshold = 0.6
    best_match = None
    max_similarity = 0

    # Checking the similarity in the Payment Name and the Property Adress and the Payed Amount 
    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice['Matched With'] == "Not Matched":
                    similarity = get_similarity(payment['Payment Name'], invoice['Property Adress'])

                    if similarity > max_similarity and similarity > threshold:
                        max_similarity = similarity
                        best_match = (i, j)

    if best_match:
        i, j = best_match
        if payments['Payed Amount'][i] == invoices['Payment Amount'][j]:
            invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
            payments.at[i, "Merged"] = "Similar Address, Amount Ok"
        else:
            invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
            payments.at[i, "Merged"] = "Address Match, but Check VALUE !"


    # Checking only proper Amount (1007_PN_NS_Adr)

    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice['Matched With'] == "Not Matched":
                    if payment['Payed Amount'] == invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
                        payments.at[i, "Merged"] = "Amount Correct, Data Wrong !"
                        break

    # Checking the Payments which does not make sense at all (1013_PN_NS_Adr_PA)

                    elif payment['Payed Amount'] != invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
                        payments.at[i, "Merged"] = "Wrong Transfer"
                        break   


    payments.to_csv('Datasets/merged_payments.csv', index=False)
    invoices.to_csv('Datasets/matched_invoices.csv', index=False)


if __name__ == "__main__":
    main()
