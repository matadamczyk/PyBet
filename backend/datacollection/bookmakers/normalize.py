def normalize_team_name(team_name):
    if "nottingham" in team_name.lower():
        return "Nott'm Forest"
    if "utd" in team_name.lower():
        return "Man United"
    if "manchester" in team_name.lower():
        return team_name.replace("Manchester", "Man")
    if "wolverhampton" in team_name.lower():
        return "Wolves"
    return team_name

def normalize_identifier(identifier):
    if "nottingham" in identifier.lower():
        if "forest" in identifier.lower():
            identifier = identifier.replace(" Forest", "")
        return identifier.replace("Nottingham", "Nott'm Forest")
    if "utd" in identifier.lower():
        return identifier.replace("Manchester Utd", "Man United")
    if "manchester" in identifier.lower():
        return identifier.replace("Manchester", "Man")
    if "wolverhampton" in identifier.lower():
        return identifier.replace("Wolverhampton", "Wolves")
    return identifier