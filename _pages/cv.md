---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Profile
======
Assistant Professor in Biomedical Engineering at Hospital Israelita Albert Einstein and researcher at its Brain Institute. My work focuses on human-robot interaction, robotic rehabilitation, assistive technologies, wearable sensing, and AI for healthcare.

Education
======
{% assign education = site.data.cv.education | sort: "endDate" | reverse %}
{% for edu in education %}
* **{{ edu.studyType }}**, {{ edu.institution }} ({{ edu.startDate }} - {{ edu.endDate }})
  * {{ edu.area }}{% if edu.thesis != "" %}
  * Thesis: {{ edu.thesis }}{% endif %}
{% endfor %}

Academic and Research Appointments
======
{% assign work = site.data.cv.work | sort: "startDate" | reverse %}
{% for item in work %}
* **{{ item.position }}**, {{ item.company }} ({{ item.startDate }} - {{ item.endDate }})
  * {{ item.summary }}
{% endfor %}

Selected Publications
======
{% assign publications = site.data.cv.publications | sort: "releaseDate" | reverse %}
{% for pub in publications %}
* **{{ pub.name }}**. {{ pub.publisher }}, {{ pub.releaseDate }}.
  * {{ pub.summary }}
  * [DOI / link]({{ pub.website }})
{% endfor %}

Selected Presentations
======
{% assign presentations = site.data.cv.presentations | sort: "date" | reverse %}
{% for talk in presentations %}
* **{{ talk.name }}**. {{ talk.event }}, {{ talk.date }}.
  * {{ talk.location }}
{% if talk.description != "" %}  * {{ talk.description }}
{% endif %}{% endfor %}

Teaching
======
{% assign teaching = site.data.cv.teaching | sort: "date" | reverse %}
{% for item in teaching %}
* **{{ item.course }}**, {{ item.institution }} ({{ item.date }})
  * {{ item.role }}
{% if item.description != "" %}  * {{ item.description }}
{% endif %}{% endfor %}

Languages
======
{% for language in site.data.cv.languages %}
* **{{ language.language }}**: {{ language.fluency }}
{% endfor %}
