let team1 = 0;
let team2 = 0;

document.querySelector('#add1').onclick = function() {
    team1 = team1 + 1;
    document.querySelector('#score1').innerHTML = team1;
    if (team1 == 5) {
        // alert("Team 1 won!");
        document.querySelector('#result').innerHTML = "Team 1 Won!";
    }
}

document.querySelector('#add2').onclick = function() {
    team2 = team2 + 1;
    document.querySelector('#score2').innerHTML = team2;
    if (team2 == 5) {
        // alert("Team 1 won!");
        document.querySelector('#result').innerHTML = "Team 2 Won!";
    }
}
