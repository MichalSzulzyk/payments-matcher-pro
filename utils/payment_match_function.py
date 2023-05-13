import re
from utils.text_splitting_function import split
from utils.string_similarity import get_similarity

def match_payments_invoices(payments, invoices):

    # Initialize match status columns
    payments['Merged'] = "Not Merged"
    invoices['Transaction Number'] = 0
    invoices['Matched With'] = "Not Matched"
    invoices['Status'] = "Not Matched"

    # # To be deleted (Only for synthetic data)
    payments = payments.sample(frac=1, random_state=42).reset_index(drop=True)

    # Define separators for payment names
    separators = [',', ';', ' ', '_']


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
                            invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
                            invoices.at[j, 'Status'] = "ACCEPTED"
                            payments.at[i, "Merged"] = "Correct Amount, Payment data ok"
                            break

                    # Checking if any of the numbers connected to the propery is present 
                    # in the Payment Name but payment amount is wrong
                        elif num in payment_name_list and payment['Payed Amount'] != invoice['Payment Amount']:
                            invoices.at[j, "Matched With"] = payment['Unique Change Code']
                            invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
                            invoices.at[j, 'Status'] = "TO BE CHECKED"
                            payments.at[i, "Merged"] = "Wrong Amount, Payment data ok"
                            break

    # Checking Name and a Surname on the Incoming Payment and the Invoice list and checking the Amount
    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice["Matched With"] == "Not Matched":

                    if payment['Name and Surname'] == invoice['Name and Surname'] and payment['Payed Amount'] == invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payment['Unique Change Code']   
                        invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
                        invoices.at[j, 'Status'] = "ACCEPTED"
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
            invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
            invoices.at[j, 'Status'] = "ACCEPTED"
            payments.at[i, "Merged"] = "Similar Address, Amount Ok"
        else:
            invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
            invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
            invoices.at[j, 'Status'] = "TO BE CHECKED"
            payments.at[i, "Merged"] = "Address Match, but Check VALUE !"


    # Checking only proper Amount (1007_PN_NS_Adr)

    for i, payment in payments.iterrows():
        if payment['Merged'] == "Not Merged":
            for j, invoice in invoices.iterrows():
                if invoice['Matched With'] == "Not Matched":
                    if payment['Payed Amount'] == invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
                        invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
                        invoices.at[j, 'Status'] = "TO BE CHECKED"
                        payments.at[i, "Merged"] = "Amount Correct, Data Wrong !"
                        break

    # Checking the Payments which does not make sense at all (1013_PN_NS_Adr_PA)

                    elif payment['Payed Amount'] != invoice['Payment Amount']:
                        invoices.at[j, "Matched With"] = payments['Unique Change Code'][i]
                        invoices.at[j, 'Transaction Number'] = payment['Transaction Number']
                        invoices.at[j, 'Status'] = "TO BE CHECKED"
                        payments.at[i, "Merged"] = "Wrong Transfer"
                        break   


    payments.to_csv('Datasets/merged_payments.csv', index=False)
    invoices.to_csv('Datasets/matched_invoices.csv', index=False)
