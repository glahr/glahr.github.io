---
permalink: /
title: "Gustavo Lahr"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am an Assistant Professor in Biomedical Engineering and a researcher at the Brain Institute of Hospital Israelita Albert Einstein, in Brazil.

My research sits at the intersection of robotics and healthcare, with a focus on human-robot interaction, robotic rehabilitation, assistive technologies, wearable sensing, and AI-driven clinical applications. I am particularly interested in making robotic systems more useful, adaptive, and practical in real-world care settings.

This website gathers my research, publications, talks, teaching, and ongoing projects.

# Biography

I work on robotics for healthcare, especially problems involving physical interaction, rehabilitation, assistive systems, and intelligent sensing. Before joining Einstein, I completed a postdoctoral fellowship at the Human-Robot Interfaces and Interaction Laboratory at the Istituto Italiano di Tecnologia, where I worked on dynamic manipulation and adaptive human-robot interaction. I received my Ph.D. and M.Sc. in Mechanical Engineering from the University of São Paulo, and my B.Sc. in Mechatronics Engineering from the same institution. During my doctorate, I was also a visiting researcher at KTH Royal Institute of Technology in Sweden.

# Education

{% assign education = site.data.cv.education | sort: "endDate" | reverse %}
{% for edu in education %}
- **{{ edu.studyType }}**, {{ edu.institution }} ({{ edu.startDate }} - {{ edu.endDate }}),
  {{ edu.area }}, "{{edu.thesis}}".
{% endfor %}

