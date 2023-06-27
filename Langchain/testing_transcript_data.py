import re
import json

data = "\n® AAFP\n\n2021\nDate Title\n03/28/2021 UpToDate\nUpToDate Inc\n05/04/2021 Continuous Knowledge Self-Assessment (CKSA) :\nCKSA Q1\nAmerican Board of Family Medicine\n06/23/2021 Continuous Knowledge Self-Assessment (CKSA) :\nCKSA Q2\nAmerican Board of Family Medicine\n07/02/2021 Continuous Knowledge Self-Assessment (CKSA) :\nCKSA Q3\nAmerican Board of Family Medicine\n10/22/2021 Continuous Knowledge Self-Assessment (CKSA) :\nCKSA Q4\nAmerican Board of Family Medicine\n12/15/2021 UpToDate\nUpToDate Inc\n12/15/2021 Formal Activity - AMA/AOA Approved: UptoDate\nTotal Credits:\nCME Credits for\n\nTotal Prescribed Credits: 50.00\nTotal Elective Credits: 10.00\nTotal Credits: 60.00\n\nTroy Lane Potthoff MD\n\nTroy Lane Potthoff MD\n1551 Ala Wai Blvd Apt 1803\nHonolulu, HI 96815-1044\n\nUS\nCurrent as of 3/28/2022\n\nP Credits E Credits\n\n20.00 0.00\n\n2.50 0.00\n\n2.50 0.00\n\n2.50 0.00\n\n2.50 0.00\n\n20.00 0.00\n\n0.00 10.00\nPrescribed Elective Total P&E\n50.00 10.00 60.00\n\nProvided to AAFP members\non a complimentary basis\nas a membership service.\n\nR. Shawn Martin\nExecutive Vice President/CEO\nAmerican Academy of Family Physicians\n\nPage: 1\n\n"

output = []
matches = re.findall(r"([A-Za-z\s]+):\s*([A-Za-z0-9.,/()™-]+)\n", data)

for i in range(0, len(matches), 5):
    provider_name = matches[i][1]
    credit_type = matches[i+1][1]
    total_credit = matches[i+4][1]
    issued_date = matches[i+3][1]
    title = matches[i+2][1]
    
    entry = {
        "provider name": provider_name,
        "Credit Type": credit_type,
        "Total Credit": total_credit,
        "Issued date": issued_date,
        "Title": title
    }
    output.append(entry)

output_json = json.dumps(output, indent=2)
print(output_json)
