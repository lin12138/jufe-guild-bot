def get_user(guild_id="17019816109928716791"):
    with open(f"./data/{guild_id}/trial_user.txt", 'r', encoding='utf-8') as f:
        return f.read()

def set_user(user: str, guild_id="17019816109928716791"):
    with open(f"./data/{guild_id}/trial_user.txt", 'w', encoding='utf-8') as f:
        f.write(user)
        f.close()