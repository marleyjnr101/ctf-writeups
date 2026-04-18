def calculate_risk(likelihood, impact):
    score = likelihood * impact  
    if score >=   15:
        level = "Critical"
    elif score >= 10:
        level = "High"
    elif score >= 5:        
        
        level = "Medium"
    else:
        level = "Low"
    return score, level
    
# Test with actual risk register data
assets = [
    ("Customer Payment Database", 3, 5),
    ("Staff Email Accounts", 4, 4),
    ("Finance Staff",4,5),
    ("Staff Laptops", 2, 4),
]
for asset, likelihood, impact in assets:
    score, level = calculate_risk(likelihood, impact)
    print(f"{asset}: Score = {score}, Level = {level}")
    