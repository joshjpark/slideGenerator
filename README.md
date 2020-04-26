# slideGenerator
`slideGenerator` is an automation project for Google Slides, developed using Google Slides API. 

For detailed info about Google Slides, refer to [Google Slides manual](https://developers.google.com/slides/concepts/page-elements)
> The Google Slides API lets you create and modify Google Slides presentations. Apps can integrate with the Google Slides API to create beautiful slide decks automatically from user- and system-provided data. For example, you could use customer details from a database and combine them with predesigned templates and selected configuration options to create finished presentations in a fraction of the time it would take to create them manually. 

# Motivation
At UVic Bible club, we create Google Slides for our presentation on a weekly basis, and this involves routine tasks (fetch new Bible verses, change background images for slides, format text on slides, etc.) that add up to ~30 min/ week. I wanted to automate this process and reduce this task to a simple function call. 

# Structural Overview


API representation types and structure can be found on [here](https://developers.google.com/slides/concepts/page-elements). 


# Result
I effectively reduced the weekly slide preparation time from manual ~30 minutes to a function call that takes ~5 seconds. 


# Usage
----
In ```./src```, simply run: 
```
python3 start.py
``` 

Here is our console output:
```bash
Joshuas-MBP:slideGenerator joshua$ python3 start.py
** Init new slide deck & obtain object IDs
** title page created
** Silent Prayer slide created
** Creed slide created
** Representative prayer slide created
** Verses slides from Genesis 1:1-1:7 created
** Announcement slide created
** Prayer slide created
Joshuas-MBP:slideGenerator joshua$ 
```

Output slides are automatically stored to Google Drive. 
Here are some examples of its output:
[Output Demo 1](https://docs.google.com/presentation/d/1OSTpD9mweSyiZMSYRiq9Y9-DUTqFYkVKPHEiUD_IysU/edit?usp=sharing)
[Output Demo 2](https://docs.google.com/presentation/d/1OSTpD9mweSyiZMSYRiq9Y9-DUTqFYkVKPHEiUD_IysU/edit?usp=sharing)
[Output Demo 3](https://docs.google.com/presentation/d/1OSTpD9mweSyiZMSYRiq9Y9-DUTqFYkVKPHEiUD_IysU/edit?usp=sharing)