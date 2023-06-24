import PyPDF2
import re
def extractDataFromPDF(pdfFile):
    pdfFileObj = open(pdfFile, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    pageObj = pdfReader.pages[0]
    data = pageObj.extract_text()
    pdfFileObj.close()
    return data

text = extractDataFromPDF("resume.pdf")

education_match = re.search(r"Education\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+", text, re.DOTALL)
university = education_match.group(1).strip()
education = education_match.group(2).strip()
education_duration = education_match.group(3).strip()

print("University:", university)
print("Education:", education)
print("Duration:", education_duration)

# Extracting work experience information
experience_matches = re.findall(r"Work Experience\s+(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+", text, re.DOTALL)
for match in experience_matches:
    job_title = match[0].strip()
    company = re.sub(r"\([^()]*\)", "", job_title).strip()  # Remove text within parentheses
    job_description = match[1].strip()

    print("Job Title:", job_title)
    print("Company:", company)
    print("Job Description:", job_description)
    print()

# Extracting email and phone number
email_match = re.search(r"(\S+@\S+)", text)
phone_match = re.search(r"\+\d{2}\s*\d{10}", text)

email = email_match.group(1) if email_match else None
phone_number = phone_match.group() if phone_match else None

print("Email:", email)
print("Phone Number:", phone_number)