from functions import *

def generate_cv(yaml_input:str=None, image=None):

    ## CLEANUP FILES
    cleanup_files(directories=['cv_pages', 'cv_images'])
    
    ## LOAD YAML
    if yaml_input:
        cv_data = yaml.safe_load(yaml_input)
    else:
        with open("cv_data.yaml", "r") as file:
            cv_data = yaml.safe_load(file)

    ## ASSERT MANDATORY FIELDS IN YAML
    yaml_checker(cv_data)
 
    ## REGISTER FONTS
    pdfmetrics.registerFont(TTFont('regular', 'fonts/ProximaNova-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('bold', 'fonts/ProximaNova-Semibold.ttf'))

## FIRST PAGE
    ## INITIATE CANVAS OBJECT
    c = canvas.Canvas("cv_pages/cv1.pdf", pagesize=landscape(A4))

    ## SET BACKGROUND
    draw_background(c, path='backgrounds/background1.jpg')

    ## SET PROFILE PICTURE
    if image:
        draw_picture(c, image=image)
    else:
        draw_picture(c, image=None, path='photos/tom_cruise.jpg')

    # NAME CARD
    y = 513
    x = 145
    if cv_data['first_name']:
        y = write(c, x, y, text=cv_data['first_name'], font='bold', punto=20, color='white', spacing=12)
    y -= 15
    if cv_data['last_name']:
        y = write(c, x, y, text=cv_data['last_name'], font='regular', punto=14, color='trans_white', spacing=12)
    y -= 22
    if cv_data['role']:
        y = write(c, x, y, text=cv_data['role'], font='regular', punto=12, color='trans_white', spacing=12)
    
    # ABOUT ME
    y = 394
    x = 40
    if cv_data["about me"]:
        y = write(c, x, y, text="About Me", font='bold', punto=12, color='white', spacing=12)
        y -= 25
        y = write(c, x, y, text=cv_data["about me"], font='regular', punto=8, color='trans_white', spacing=12)
    
    # EDUCATION
    y = 205
    x = 40
    if cv_data['education']:
        y = write(c, x, y, text="Education", font='bold', punto=12, color='white', spacing=12)
        y -= 25
        for edu in cv_data['education']:
            if edu['year']:
                y = write(c, x, y, text=edu['year'], font='bold', punto=8, color='white', spacing=12)
                y -= 12
            if edu['degree']:
                y = write(c, x, y, text=edu['degree'], font='bold', punto=8, color='white', spacing=12)
                y -= 12 
            if edu['institution']:    
                y = write(c, x, y, text=edu['institution'], font='regular', punto=8, color='trans_white', spacing=12)
                y -= 20

    # BIOGRAPHY
    y = 521
    x = 380
    if cv_data['biography']:
        y = write(c, x, y, text="Biography", font='bold', punto=12, color='purple', spacing=12)
        y -= 25
        y = write(c, x, y, text=cv_data['biography'], font='regular', punto=8, color='dark_grey', spacing=12)
    
    # ROLES
    y = 400
    x = 380
    if cv_data['roles']:
        write(c, x, y, text="Roles", font='bold', punto=12, color='purple', spacing=12)
        y -= 25
        for role in cv_data['roles']:
            if role['title']:
                y = write(c, x, y, text=role['title'], font='bold', punto=10, color='purple', spacing=12)
                y -= 15
            if role['description']:
                y = write(c, x, y, text=role['description'], font='regular', punto=8, color='dark_grey', spacing=12)
                y -= 8
    
    # CERTIFICATIONS
    if 'certifications' in cv_data and cv_data['certifications']:
        y -= 10
        y = write(c, x, y, text="Certifications", font='bold', punto=12, color='purple', spacing=12)
        y -= 20
        for certificate in cv_data['certifications']:
            if certificate['title']:
                y = write(c, x, y, text=certificate['title'], font='regular', punto=8, color='dark_grey', spacing=12)
                y -= 12

    # COMPETENCES
    y = 400
    x = 600
    if cv_data["competences"]:
        y = write(c, x, y, text="Competences", font='bold', punto=12, color='purple', spacing=12)
        y -= 25
        for comp in cv_data["competences"]:
            if comp['title']:
                y = write(c, x, y, text=comp['title'], font='bold', punto=10, color='purple', spacing=12)
                y -= 15
            if comp['description']:
                y = write(c, x, y, text=comp['description'], font='regular', punto=8, color='dark_grey', spacing=12)
                y -= 20

    c.save()

## EXPERIENCE PAGES
    c = canvas.Canvas("cv_pages/cv2.pdf", pagesize=landscape(A4))

    bg_image = "backgrounds/background2.jpg"
    c.drawImage(bg_image, 0, 0, width=A4[1], height=A4[0])

    # RECENT WORK EXPERIENCE HEADER
    y = 540
    x = 40
    y = write(c, x, y, text="Recent Work Experience", font='bold', punto=12, color='white', spacing=12)
    
    # RECENT WORK EXPERIENCE CONTENT: creates as many pages as necessary to fit all experience content
    y = 500
    x = 40
    page = 2
    for exp in cv_data['experience']:
        if page_end_checker(y, exp):
            c.save()
            page += 1
            c = canvas.Canvas(f"cv_pages/cv{page}.pdf", pagesize=landscape(A4))
            bg_image = "backgrounds/background2.jpg"
            c.drawImage(bg_image, 0, 0, width=A4[1], height=A4[0])
            y = 500
            x = 40
        if exp['title'] and exp['company']:
            y = write(c, x, y, text=f"{exp['title']} @ {exp['company']}", font='bold', punto=10, color='white', spacing=12)
            y -= 10
        if exp['start'] and exp['end']:
            y = write(c, x, y, text=f"{exp['start']} - {exp['end']}", font='bold', punto=8, color='white', spacing=12)
            y -= 20
        if exp['description']:
            y = write(c, x, y, text=exp['description'], font='regular', punto=8, color='trans_white', spacing=12)
            y -= 3
        if exp['technologies']:
            y = write(c, x, y, text=exp['technologies'], font='bold', punto=8, color='trans_white', spacing=12)
        y -= 25
    
    # CONTACT INFORMATION: only displayed on the last page
    y = 200
    x = 620
    y = write(c, x, y, text="Contact Information", font='bold', punto=10, color='purple', spacing=12)
    y -= 20
    if cv_data["email"]:
        y = write(c, x, y, text="Email:", font='bold', punto=8, color='light_grey', spacing=12)
        y = write(c, x+40, y, text=cv_data['email'], font='regular', punto=8, color='dark_grey', spacing=12)
        y -= 15
    if cv_data["phone"]:
        y = write(c, x, y, text="Phone:", font='bold', punto=8, color='light_grey', spacing=12)
        y = write(c, x+40, y, text=cv_data['phone'], font='regular', punto=8, color='dark_grey', spacing=12)
        y -= 15
    if cv_data["linkedin"]:
        y = write(c, x, y, text="Linkedin:", font='bold', punto=8, color='light_grey', spacing=12)
        y = write(c, x+40, y, text=cv_data['linkedin'], font='regular', punto=8, color='dark_grey', spacing=12)
        y -= 15
    if cv_data["github"]:
        y = write(c, x, y, text="Github:", font='bold', punto=8, color='light_grey', spacing=12)
        y = write(c, x+40, y, text=cv_data['github'], font='regular', punto=8, color='dark_grey', spacing=12)
        y -= 15
    
    c.save()

## MERGE PAGES INTO ONE PDF
    merge_pdfs()


if __name__ == "__main__":
    generate_cv()
