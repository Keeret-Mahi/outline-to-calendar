from bs4 import BeautifulSoup

def extract_section_info(soup, target_section):
    # Extract course-wide data
    course_name = " ".join(soup.title.string.strip().split()) if soup.title else "N/A"
    course_code_el = soup.find(class_="outline-courses")
    course_term_el = soup.find(class_="outline-term")
    course_code = course_code_el.text.strip() if course_code_el else "N/A"
    course_term = course_term_el.text.strip() if course_term_el else "N/A"

    # Extract section-specific data
    rows = soup.select('table tbody tr')

    for row in rows:
        course_th = row.find('th')
        if not course_th:
            continue

        section_span = course_th.find('span', class_='section')
        if not section_span:
            continue

        section_num = section_span.text.strip().split()[0] 

        if section_num == target_section:
            class_type = section_span.find('span', class_='class-type').text.strip('[]')

            meet_days_div = row.find('td', class_='meet-days')
            lecture_days = ", ".join([
                span.text.strip().strip(',') for span in meet_days_div.select('.days-visual .present')
            ])

            term_span = meet_days_div.select_one('.date-range span')
            term_span = term_span.text.strip() if term_span else "N/A"

            time_str = row.find_all('td')[1].text.strip()
            start_time, end_time = time_str.split(' - ')

            location = row.find_all('td')[2].text.strip()

            return {
                "course_name": course_name,
                "course_code": course_code,
                "term": course_term,
                "section": section_num,
                "lecture_type": class_type,
                "lecture_days": lecture_days,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "term_span": term_span
            }

    raise ValueError(f"Section {target_section} not found in the outline. Please check section number.")
