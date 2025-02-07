from fuzzywuzzy import fuzz


def calculate_ats_score(resume_text, job_description):
    sections = ["projects", "experience", "summary", "skills"]
    extracted_sections = [section for section in sections if section in resume_text.lower()]
    filtered_resume_text = " ".join(extracted_sections)

    return fuzz.ratio(filtered_resume_text.lower(), job_description.lower())