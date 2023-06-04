import openai
import fitz
import pytesseract
import cv2
import tempfile
import os
from dotenv import load_dotenv
from questions import questions
import time

load_dotenv()
deployment_name = os.getenv("DEPLOYMENT-NAME")
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = os.getenv("ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("API-KEY")


def pdf_reader(pdf_path: str = None):
    doc = fitz.open(pdf_path)
    text = ""
    pages = doc.pages()
    for page in pages:
        with tempfile.TemporaryDirectory() as tmpdir:
            # page = doc.load_page(0)  # number of page
            pix = page.get_pixmap(dpi=300)
            path = f"{tmpdir}/image.jpg"
            pix.save(path)

            img = cv2.imread(path)
            img_text = pytesseract.image_to_string(img)
            text = text + "\n" + img_text
    doc.close()
    print(f"extracted text from {pdf_path}" + "\n")
    return text


def gpt_communicator(text: str = None, question: str = None, verbose=True):
    response = openai.ChatCompletion.create(
        engine=deployment_name,  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages=[
            {
                "role": "user",
                "content": f"""
    \"{text}\"

    Based on the CV above:
    {question}
    """,
            }
        ],
    )

    answer = response["choices"][0]["message"]["content"]
    if verbose:
        print(question)
        print(f"===> {answer}")
        print("----------------\n")
    time.sleep(3)
    return answer


def cv_text_to_yaml(
    cv_text: str = None,
    output_dir: str = "../gpt/yaml_output",
    output_file_name: str = None,
):
    yaml_text = ""
    text = cv_text

    first_name = gpt_communicator(text=text, question=questions["first_name"]).strip()
    yaml_text += "\n" + f'first_name: "{first_name}"'

    last_name = gpt_communicator(text, questions["last_name"]).strip()
    yaml_text += "\n" + f'last_name: "{last_name}"'

    role = gpt_communicator(text, questions["role"]).strip()
    yaml_text += "\n" + f'role: "{role}"'

    email_address = gpt_communicator(text, questions["email_address"]).strip()
    if email_address == "None":
        yaml_text += "\n" + f"email: "
    else:
        yaml_text += "\n" + f'email: "{email_address}"'

    phone_number = gpt_communicator(text, questions["phone_number"]).strip()
    if phone_number == "None":
        yaml_text += "\n" + f"phone: "
    else:
        yaml_text += "\n" + f'phone: "{phone_number}"'

    linkedin = gpt_communicator(text, questions["linkedin"]).strip()
    if linkedin == "None":
        yaml_text += "\n" + f"linkedin: "
    else:
        yaml_text += "\n" + f'linkedin: "{linkedin}"'

    github = gpt_communicator(text, questions["github"]).strip()
    if github == "None":
        yaml_text += "\n" + f"github: "
    else:
        yaml_text += "\n" + f'github: "{github}"'

    # website = gpt_communicator(text, questions['website']).strip()
    # if website == "None":
    #     yaml_text += '\n' + f'website: '
    # else:
    #     yaml_text += '\n' + f'website: "{website}"'

    about_me = (
        gpt_communicator(text, questions["about_me"])
        .replace("\n", " ")
        .replace("  ", " ")
        .strip()
    )
    yaml_text += "\n" + f'about_me: "{about_me}"'

    education_degrees = gpt_communicator(text, questions["education_degrees"]).strip()
    yaml_text += "\n" + f"education:"
    for degree in education_degrees.split(","):
        degree = degree.strip()
        education_year = gpt_communicator(
            text, questions["education_year"].format(degree=degree)
        ).strip()
        education_school = gpt_communicator(
            text, questions["education_school"].format(degree=degree)
        ).strip()
        yaml_text += "\n" + f'  - degree: "{degree}"'
        if education_school == "None":
            yaml_text += "\n" + f"    institution: "
        else:
            yaml_text += "\n" + f'    institution: "{education_school}"'
        if education_year == "None":
            yaml_text += "\n" + f"    year: "
        else:
            yaml_text += "\n" + f'    year: "{education_year}"'

    biography = (
        gpt_communicator(text, questions["biography"])
        .replace("\n", " ")
        .replace("  ", " ")
        .strip()
    )
    yaml_text += "\n" + f'biography: "{biography}"'

    roles = gpt_communicator(text, questions["roles"]).strip()
    yaml_text += "\n" + f"roles:"
    for role in roles.split(","):
        role = role.strip()
        role_description = gpt_communicator(
            text, questions["role_description"].format(role=role)
        ).strip()
        yaml_text += "\n" + f'  - title: "{role}"'
        yaml_text += "\n" + f'    description: "{role_description}"'

    certifications = gpt_communicator(text, questions["certifications"]).strip()
    yaml_text += "\n" + f"certifications:"
    if certifications != "None":
        for certification in certifications.split(","):
            certification = certification.strip()
            yaml_text += "\n" + f'  - title: "{certification}"'

    competences_titles = gpt_communicator(text, questions["competences_titles"]).strip()
    yaml_text += "\n" + f"competences:"
    for competences_title in competences_titles.split(","):
        competences_title = competences_title.strip()
        competences = gpt_communicator(
            text, questions["competences"].format(competences_title=competences_title)
        ).strip()
        yaml_text += "\n" + f'  - title: "{competences_title}"'
        yaml_text += "\n" + f'    description: "{competences}"'

    companies = gpt_communicator(text, questions["companies"]).strip()
    yaml_text += "\n" + f"experience:"
    for company in companies.split(","):
        company = company.strip()
        company_role = gpt_communicator(
            text, questions["company_role"].format(company=company)
        ).strip()
        company_start = gpt_communicator(
            text, questions["company_start"].format(company=company)
        ).strip()
        company_end = gpt_communicator(
            text, questions["company_end"].format(company=company)
        ).strip()
        company_work = (
            gpt_communicator(text, questions["company_work"].format(company=company))
            .strip()
            .replace("\n", "\n      ")
            .replace("¢", "•")
            .replace("* ", "• ")
            .replace("+ ", "• ")
            .replace("« ", "• ")
        )
        company_technologies = gpt_communicator(
            text, questions["company_technologies"].format(company=company)
        ).strip()

        yaml_text += "\n" + f'  - title: "{company_role}"'
        yaml_text += "\n" + f'    company: "{company}"'
        if company_start == "None":
            yaml_text += "\n" + f"    start: "
        else:
            yaml_text += "\n" + f'    start: "{company_start}"'
        if company_end == "None":
            yaml_text += "\n" + f"    end: "
        else:
            yaml_text += "\n" + f'    end: "{company_end}"'
        yaml_text += "\n" + f'    description: "{company_work}"'
        if company_technologies == "None":
            yaml_text += "\n" + f"    technologies: "
        else:
            yaml_text += "\n" + f'    technologies: "{company_technologies}"'
        yaml_text += "\n" + f"    visible: true"

    with open(f"{output_dir}/{output_file_name}.yml", "w") as text_file:
        text_file.write(yaml_text)

    return yaml_text
