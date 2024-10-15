# Minesweeper via flask

My goal for this project was to expand the `Homepage` project from Week 8 into a fully-fledged web app. I have made a couple of games in Python prior to enrolling in cs50 and I want to be able to port those games to the web and make them accessible from my homepage.

Games are what first drew me to programming, when I started getting better at programming I got inspired to implement my own version of Minesweeper, as well as the card games Cribbage and 31.

My first goal of the project was to implement Minesweeper. I adjusted my existing Python code to work as the backend that could interact with flask. Then I created a new frontend using html, javascript, and css. While I had planned at first to implement multiple games, I ended up sticking with Minesweeper for the scope of this project as that gave me quite a bit of a challenge already. One plan I have for the future is to extend this project by pushing it to an actual server online so it can be accessed via the web. I also want it to have more games, as I have Python code written up for several other games, but I still need to translate the frontend to HTML/Javascript, as well as come up with an API for client/server communication.

I probably could have implemented the game logic almost totally in Javascript, but I wanted to keep the layout of the mines on the server so that someone would not be able to cheat by seeing where the mines are located via developer tools. The game board is created on the server, and information is provided to the client on a need-to-know basis. The server knows where all the mines are and which boxes should be revealed when given a user input. I used AJAX to send user input to the server and receive information on which squares to reveal, the numbers on the visible squares and whether the game is over. The client handles rendering the board and placing flags. I realized the server has no need to know where flags are since the goal of the game is simply to reveal all non-mines squares. Therefore flags are entirely handled on the client side.

In order to add an SQL element to the project, I decided to track players' stats, such as their fastest time, average time, the number of games they win or lose, and their win rate. In order to keep track of users, I implemented ways for a user to register, login, and change passwords, similar to the tasks from the Week 9 Finance project. I wanted to figure out a solution for using SQL without the SQL module from the cs50 library, so I used the native Python library sqlite3. The syntax was slightly different from the cs50 library but it seemed to work for the scope of the project.

<!-- #### Video Demo:  <URL HERE>
#### Description:
TODO -->
