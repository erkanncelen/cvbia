from gpt_functions import pdf_reader, cv_text_to_yaml

cv_text = pdf_reader("gpt/test_files/john_smith_cv.pdf")
output_file_name = "john_smith_new_xebia_data_cv"

cv_text_to_yaml(
    cv_text=cv_text, output_dir="./gpt/yaml_output", output_file_name=output_file_name
)

# input_directory = "./gpt/pdf"
# for filename in os.listdir(input_directory):
#     try:
#         f = os.path.join(input_directory, filename)
#         print(f)
#         print(f"starting {filename}")
#         cv_text = pdf_reader(f)
#         output_file_name = filename.replace(".pdf", "")
#         cv_text_to_yaml(cv_text=cv_text, output_dir="./gpt/yaml_output", output_file_name=output_file_name)
#         now = datetime.now()
#         print(f"{filename} completed at {now}")
#     except:
#         print(f"{filename} FAILED at {now}")
#         continue
