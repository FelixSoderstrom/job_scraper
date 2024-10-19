"""
This class should utilize OpenAI's Swarm package.

The class should take in a list created by BlocketScraper.
In my head, the process looks something like this:

We pass the description text of a job to Agent-A.
Agent-A then summarizes the description into 3-4 sentences.
The user reads the summarization and decides if this is a job for them.
If not, chuck it in the bin and go to the next one.
If yes, ask the user for their skills.
Agent-B recieves the skillset along with the full job description.
Agent-B generates a cover letter highlighting the users skillset yadda yadda.
A cover letter is returned.
### These steps below might be more suitable in the main file.
We package everything nicely together
(Job-Name, Company, Full description, Cover letter.)
and write it to a file.
"""


class JobCoach:
    pass
