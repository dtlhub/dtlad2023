from dataclasses import dataclass
import sqlite3

@dataclass
class TeamInfo:
    teamname: str
    ecdsa_key: str
    rc4_key: str
    #1 on vulnerability, 0 if safe
    vulnerable_for_nonce_reuse: int
    vulnerable_for_fma_attack: int

non_patched_team = TeamInfo('', '1337', 'REDACTED', 1, 1)
non_patched_team_as_list = list(non_patched_team.__dict__.values())

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('users.db', check_same_thread=False)
        cur = self.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS teams(
            teamname TEXT UNIQUE,
            ecdsa_key TEXT,
            rc4_key TEXT,
            vulnerable_for_nonce_reuse INTEGER,
            vulnerable_for_fma_attack INTEGER
            )
                    """)
        self.connection.commit()
        cur.close()
    
    def __get_user_and_create_if_not_exists(self, teamname: str):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM teams WHERE teamname=(?)", [teamname])
        data = cur.fetchall()
        if len(data) = 0:
            team = non_patched_team_as_list.copy()
            team[0] = teamname
            cur.execute("INSERT INTO users(teamname,ecdsa_key,rc4_key,vulnerable_for_nonce_reuse,vulnerable_for_fma_attack) VALUES(?,?,?,?,?)", team)
        else:
            team = data[0]
        return TeamInfo(*team)


    def init_user(self, teamname: str) -> TeamInfo:
        return self.__get_user_and_create_if_not_exists(teamname)
    
    def update_user(self, team_info: TeamInfo):
        query = f'''
            UPDATE users
            SET teamname = ?,
            SET ecdsa_key = ?,
            SET rc4_key = ?,
            SET vulnerable_for_nonce_reuse = ?,
            SET vulnerable_for_fma_attack = ?
        '''
        cur = self.connection.cursor() 
        cur.execute(query, list(team_info.__dict__.values()))
        cur.close()

