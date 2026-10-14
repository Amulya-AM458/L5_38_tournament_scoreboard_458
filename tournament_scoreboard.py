"""Tournament scoreboard with basic league-table functionality."""

import secrets
import tempfile

POINTS = {"win": 3, "draw": 1, "loss": 0}
teams = {}
matches = []


def addTeam(teamName, players=None):
    """Add a team to the scoreboard."""
    if players is None:
        players = []
    teams[teamName] = {
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "gf": 0,
        "ga": 0,
        "players": players,
    }


def matchResult(homeGoals, awayGoals):
    """Return the result from the home team's perspective."""
    if homeGoals > awayGoals:
        return "home"
    if homeGoals < awayGoals:
        return "away"
    return "draw"


def recordMatch(home, away, homeGoals, awayGoals):
    """Record a match and update both teams' statistics."""
    result = matchResult(homeGoals, awayGoals)
    sides = ((home, homeGoals, awayGoals), (away, awayGoals, homeGoals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded
    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, homeGoals, awayGoals))


def points(teamName):
    """Calculate a team's league points."""
    stats = teams[teamName]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goalDifference(teamName):
    """Calculate a team's goal difference."""
    return teams[teamName]["gf"] - teams[teamName]["ga"]


def leagueTable():
    """Return teams ordered by points and goal difference."""
    return sorted(teams, key=lambda t: (points(t), goalDifference(t)), reverse=True)


def isTopTwo(teamName):
    """Check whether a team is in the top two."""
    table = leagueTable()
    return teamName in table[:2]


def tossCoin():
    """Simulate a coin toss."""
    return secrets.choice(["Heads", "Tails"])


def tableFilePath():
    """Create a securely named temporary file."""
    temporary_file = tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    )
    temporary_file.close()
    return temporary_file.name

def publishTable(server):
    """Return the intended publication destination."""
    return f"{server}:/var/www/"


def main():
    """Run the tournament scoreboard demonstration."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        addTeam(name)
    addTeam("Hill Warriors")
    print("Toss:", tossCoin())
    recordMatch("Royal Strikers", "City Rovers", 2, 1)
    recordMatch("Lake United", "Hill Warriors", 0, 0)
    recordMatch("City Rovers", "Lake United", 3, 2)
    recordMatch("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(leagueTable(), 1):
        stats = teams[name]
        print(
            pos,
            name,
            stats["played"],
            stats["won"],
            stats["drawn"],
            stats["lost"],
            points(name),
        )
    print("Is City Rovers in the top two?", isTopTwo("City Rovers"))
    print("Matches played:", len(matches))


if __name__ == "__main__":
    main()