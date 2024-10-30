# Quizer
#### Video Demo:  <URL https://www.youtube.com/watch?v=U-CsjJF3ZOU>
#### Description:
Quizer is a website that allows multiple accounts to create and join quizes. When first visiting the website, it will require you to login into an account by typing in a username and password, or register for one. The register page prompts for a username, password and a confirmation password. The password should have at least one capital, one digit and at least 8 in length.
Once success, the user proceed to login and redirected to the index page. At the top of the index page, it will show "Your Quiz", which are the quizes you created, their unique code, and their following attempts(number of people taken the quiz) and their percentage correctness for each respective question. Below "Your Quiz", there is "Recently Taken", which are the quiz/quizes the user recently took, the quiz's unique code and their marks on that respecive quiz. If the user haven't created or joined any quizes, it will show a shaded text telling the user haven't created or joined any quiz.
To create a quiz, there is a navigation bar "Create" at the top left which redirects the user to the create page. In the create page, The page prompts for three questions and their following answers. Once filled, the user clicks the create button and their quiz is created. The user will be redirected to the index route and the quiz created should appear under "Your Quiz". To join a quiz, the navigation bar "Join" beside "Create" will redirect the user to the join page.
In the join page, the page shows the three questions in order with input boxes in between to prompt the user for the answer. Once the user answered all questions, the user should click submit. The user will be redirected to the index route and the quiz the user recently took should appear under "Recently Taken".
Note that all inputs prompted should be filled by the user else it will return an error message. Capitalisation is not a problem to check the answers.In the project, there is a falsk session folder to manage client logs, static folder for the css, templates folder to store all the html of the pages, app.py for the main python program, helpers.py to declare functions seperately, quizer.db database to store all datas including users, questions and answers, and requirements.txt to store information about all libraries.
In the database, table users store the username and password of every account. Table questions store the quiz code, a numbers, a questions, answer, creator, and corrrectness. Table answers stores the quiz code, taker and mark for each quiz. "Your Quiz" section mainly uses questions table and "Recently Taken" section uses answers table.