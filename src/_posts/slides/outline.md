---
layout: post
date: 2021-11-01
marp: true
theme: default
size: 16:9
title: Content Creation Workflow
style: |
  img {background-color: transparent!important;}
  a:hover, a:active, a:focus {text-decoration: none;}
  header a {color: #ffffff !important; font-size: 30px;}
  footer {color: #148ec8;}
header: '[&#9671;](#1, " ")'
footer: 'Slides by [Justin Bowen](#)'
---

![bg left:40%](https://res.cloudinary.com/tonsoffun/image/upload/w_1800,c_limit,q_80/v1666727172/RailsConfSelfie.jpg)

### Split backgrounds with specified size

---

<!-- 
backgroundImage:
backgroundColor:
color:
-->
---
### Intro header, to hook the reader (Why, How, What)
fdgd
---

# Why? 
## Why is this an issue worth solving
### Topical challenge statement
---
# How? 
## How should it be done? 
### How is it done?

```python
@app.route('/auth/linkedin', methods=['GET'])
def linkedin_auth():
    linkedin_auth_url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=123456&scope=profile%20email'
    return redirect(linkedin_auth_url)
```
---
# What? (maybe link to the final solution?)
## What is the solution?
## What is the conclusion?
# Conclusion
## What are the considerations? 
---
# Background header
## Experience to provide context
---
# Sitation
## Premise
## Considerations
---
# Task
## Requirements
---
# Action
## Example
---
# Result
## Solution
