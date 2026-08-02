questions.json and questions.py done.
Tested and functioning properly

![test_questions](images/test_questions.png)

quiz.py done.
Tested and functioning

![quiz test](images/test_questions.png)

score.py done
Tested and functioninggg

![score test](images/test_quizzer.png)

integrated w Open Trivia DB API calls.
Tested and functioning

1st Aug
![completely functioning quiz](images/fullquiz.png)
So, we can now pick our category, difficulty level, question type and number of questions.

I'm gonna try to implement picking more than 1 category. 
And then after that, I'm going to make a full loop -- so that it goes back and allows the user to play again until the suer clicks exit.

Acc, I'll prolly do the second one first.

After it all, I'll do streamlit integration, ship, and then do UI with either Flask/Django, make it to a full webapp.

![loopapp](images/loop_app.png)
Be back in the evening! let's just say I wasn't trying on the last quiz run :P

---

I asked AI what else to implement, and it gave me an entitre list. I do wanna practice a lot w Python, so I'll probably acc try to add a lot of them.

So, I'll add different quiz styles.
A user can just do one where they just want to solve problems
like test prep more or less.
i'll also add timed quizzes
game mode - so from easy to medium, to hard. acc, I'll see what kindof tv show game or sumn, we can make this a cool game stylee.
Just keep solving.

So, that makes 5!
- Test Prep/Practice
- Timed quizzes
- Game Mode (call it sumn) Maybe jeopardy style??
- Exam Mode!
- Addicted/Endless mode

- Store stuff differently, and add stats!
- Allow pick mutiple questions.


for test prep (normal) - they'll ick their questions, answer them, and then  there'll be  a table to show what they missed at the end in addition to naswers being shown as they solve them

timed quiz would be a timer, and would also be the same review of answers a the end.

maybe one where they can go back to questions - so like test/exam simulation.

maybe once i do streamlit stuff, i'll add different users and habe them be displayed with their stats

store full question stats, not just score. topic.



we should also store scores and data abt the quizzes in the right ay. that's the way we'll be able to do analytics. so if we store the topic it was under, number of questions.

and we'll be ablte to adostats. best score, best topic, performance under a particular topic. average score under particular topics.

---

2nd Aug (12am btw)
![timer](images/timed_quiz.png)

Turns out the only way to implement the timer inteh CLI is just checking after each question, so after the timer ends, the user can finish answering their question even tho the timer just ended. there's another way to di that which I will attemot in the mornind and implement better stuff when we switch to GUI!