from openai import OpenAI
import requests
import pytesseract
from pdf2image import convert_from_path
import os








# OpenAI GPT model
with open(".env") as f:
    api_key = f.read().strip()
client = OpenAI(api_key=api_key)




# Save the entire job description in inputs/job_desc.pdf
# Get the job information
pages = convert_from_path("inputs/job_desc.pdf", 600)
text_data = ''
for page in pages:
    text = pytesseract.image_to_string(page)
    text_data += text + '\n'



# Load in the latex template
# with open("inputs/resume_template.tex") as f:
#     resume = f.read().strip()
with open("resume_template.tex") as f:
    resume = f.read().strip()




# Get the job information
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": "You will be given raw OCR output and will return all the information in this output that is relevant to the job description. The information should be returned in plain text. Make sure the output is concise and thorough."
        },
        {
        "role": "user",
        "content": f"{text_data}"
        }
    ],
    temperature=1,
    top_p=1
)
job_description = response.choices[0].message.content.strip()




# # Write the
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {
#         "role": "system",
#         "content": "You will be given a job description. Write a resume objective statement with key words that are relevant to the job description. The information should be returned in plain text."
#         },
#         {
#         "role": "user",
#         "content": f"{job_description}"
#         }
#     ],
#     temperature=1,
#     top_p=1
# )
# objective_statement = response.choices[0].message.content





# Write the new resume
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": "You will be given a job description and resume. Edit the resume by changing the content but without changing any formatting to make it more relevant to the job description such that I will get the job. Change lacking parts to sound better. Add important skills, change the wording to be much better, change the objective to be much better. Do not change the projects or articles themselves, just the style, formatting, and how it sounds. The output should be in latex in the exact format as the input resume."
        },
        {
        "role": "user",
        "content": f"JOB DESCRIPTION----------------------\n{job_description}\n\n\nRESUME----------------------\n{resume}\n\n\n"
        }
    ],
    temperature=1,
    top_p=1
)
output_resume = response.choices[0].message.content
output_resume = output_resume.replace("```latex", "").replace("```Latex", "").replace("```", "")


# Write the resume to a file
with open("output_resume.tex", "w") as f:
    f.write(output_resume)


# Use command line to compile the latex
os.system("pdflatex output_resume.tex")  

# Delete outputs
os.system("rm output_resume.aux")
os.system("rm output_resume.log")
os.system("rm output_resume.out")






# Optional cover letter
# Write the new resume
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": "You will be given a job description and resume. Write a cover letter catered toward the given job. The cover letter should be written in pure latex without any fancy formatting to prevent errors. Fill in ALL details from the resume and ensure it is completed. There should be no fields to fill in. For example, a field such as [Your Address] should be either filled in using resume details or not included at all."
        },
        {
        "role": "user",
        "content": f"JOB DESCRIPTION----------------------\n{job_description}\n\n\nRESUME----------------------\n{resume}\n\n\n"
        }
    ],
    temperature=1,
    top_p=1
)
output_cover_letter = response.choices[0].message.content
output_cover_letter = output_cover_letter.replace("```latex", "").replace("```Latex", "").replace("```", "")


# Write the resume to a file
with open("output_cover_letter.tex", "w") as f:
    f.write(output_cover_letter)


# Use command line to compile the latex
os.system("pdflatex output_cover_letter.tex")  

# Delete outputs
os.system("rm output_cover_letter.aux")
os.system("rm output_cover_letter.log")
os.system("rm output_cover_letter.out")