import sys
from typing import Any

import feedparser
import re
from Home.models import RssUrls, RssData, RssSkills, SkillsJunction


def fetch_and_parse_rss(feeds):
    email_body = ''
    count = 0
    data = {"Data": []}

    for feed_url in feeds:
        try:
            print(f"Fetching and parsing RSS feed from: {feed_url}")
            feed_data = feedparser.parse(feed_url)

            for item in feed_data.entries:
                item_title = item.title
                item_link = item.link
                item_description = item.description
                item_pub_date = item.published

                count += 1
                email_body += f"""
                #{count}
                Title: {item_title}
                Link: {item_link}
                Published Date: {item_pub_date}\n"""

                description = item_description
                budget_start, budget_end, posted_on, country, category, skills_list = __regex(description)

                insert_rss_data(item_title, item_link, description, budget_start, budget_end, posted_on, category,
                                country, posted_on)

                latest_entry = RssData.objects.latest('id')
                latest_id = latest_entry.id
                for skill in skills_list:
                    try:
                        skill_id = RssSkills.get_or_create_skill(skill)
                        add_skills_junction_entry(rss_data_id=latest_id, rss_skills_id=skill_id)
                    except Exception as exc:
                        print("Exception in Skills", exc)

                data['Data'].append({
                    "Title": item_title,
                    "Link": item_link,
                    "Description": description,
                    "Budget_Start": budget_start,
                    "Budget_end": budget_end,
                    "Posted_on": posted_on,
                    "Category": category,
                    "Skills": skills_list,
                    "Country": country,
                    "Published Date": item_pub_date
                })
        except Exception as e:
            print(f"Error fetching or parsing RSS feed from {feed_url}: {e}\n")

    return data


def insert_rss_data(title, link, description, budget_start, budget_end, posted_on, category, country, published_date):
    existing_rss_data = RssData.objects.filter(title=title).first()

    if not existing_rss_data:
        latest_rss_url = RssUrls.objects.latest('id')
        print(latest_rss_url)

        new_rss_data = RssData.objects.create(
            title=title,
            link=link,
            description=description,
            budget_start=budget_start,
            budget_end=budget_end,
            posted_on=posted_on,
            category=category,
            country=country,
            published_date=published_date,
            id_rss_url_id=latest_rss_url.id
        )
        new_rss_data.save()
        print("New RSS data added")

    else:
        print("RSS data already exists")


def add_skills_junction_entry(rss_data_id, rss_skills_id):
    print("skills Junction")
    rss_data_instance = RssData.objects.get(id=rss_data_id)
    rss_skills_instance = RssSkills.objects.get(id=rss_skills_id)
    SkillsJunction.objects.create(rss_data_id=rss_data_instance, rss_skills_id=rss_skills_instance)


def __regex(desc: str) -> tuple[str | Any, str | Any, str | None | Any, str | None | Any, str | None | Any, list[str]]:
    budget_start, budget_end = 0, 0
    hourly_pattern = r'<b>Hourly Range<\/b>: (?:\$([\d,.]+)(?:-\$([\d,.]+))?)?'
    budget_pattern = r'<b>Budget<\/b>: \$([\d,.]+)(?:-\$([\d,.]+))?'
    posted_on_pattern = r'<b>Posted On<\/b>: (.*?)\sUTC'
    country_pattern = r'<b>Country<\/b>: (.*?)\n'
    category_pattern = r'<b>Category<\/b>: (.*?)<br'
    skills_pattern = r'<b>Skills<\/b>: (.*?)<br'

    posted_on, country, category, skills_list = None, None, None, []

    hourly_matches = re.search(hourly_pattern, desc)
    budget_matches = re.search(budget_pattern, desc)
    try:
        if hourly_matches:
            budget_start = hourly_matches.group(1)
            budget_end = hourly_matches.group(2)

            print("Budget Starts:", budget_start if budget_start is not None else "Not specified")
            print("Budget End:", budget_end if budget_end is not None else "Not specified")

        else:
            budget_start = budget_matches.group(1)
            budget_end = budget_matches.group(2)

            print("Budget Starts:", budget_start if budget_start is not None else "Not specified")
            print("Budget End:", budget_end if budget_end is not None else "Not specified")

        posted_on_matches = re.search(posted_on_pattern, desc)

        if posted_on_matches:
            posted_on = posted_on_matches.group(1)
            print("Posted On:", posted_on)
        else:
            print("No match found")

        country_matches = re.search(country_pattern, desc)

        if country_matches:
            country = country_matches.group(1)
            print("Country:", country)
        else:
            print("No match found")

        category_matches = re.search(category_pattern, desc)

        if category_matches:
            category = category_matches.group(1)
            print("Category:", category)
        else:
            print("No match found")

        skills_matches = re.search(skills_pattern, desc)

        if skills_matches:
            skills = skills_matches.group(1)
            skills = skills.strip()
            skills_list = [skill.strip() for skill in skills.split(',')]
            print("Skills:", skills_list)
        else:
            print("No match found")
    except Exception as e:
        print("exception in regex", e)

    return budget_start, budget_end, posted_on, country, category, skills_list


def get_skills_for_rss_data_id(rss_data_id):
    skills = SkillsJunction.objects.filter(rss_data_id=rss_data_id).values_list('rss_skills_id__skills', flat=True)
    print(f"Skills: {skills}", file=sys.stderr)
    return list(skills)
