import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('token')

client = commands.Bot(command_prefix = ">")

path_list = ['1','2','3','4','5','6','7','8','9']
global path_not_available 
path_not_available = []
global count_step
count_step = 0
global current_players
current_players = []

def display(num):
    playboard = ""
    for i in num:
        playboard = playboard+str(i)+"\n"
        playboard = playboard.replace("', '"," | ")
        playboard = playboard.replace("']"," ")
        playboard = playboard.replace("['"," ")
    return playboard

def clear_board():
    global count_step, username, challenger, path_num, current_players, path_not_available
    count_step = 0
    global turn, turn_player
    del turn
    del turn_player
    del username
    del challenger
    del path_num
    current_players = []
    path_not_available = []

def player_response(pos, player, role):
    if pos in path_list:
        pass
    else:
        return "Invalid"
            
    if pos in path_not_available:
        return "Invalid"
    else:    
        for i in path_num:
            for j in i:
                if j == pos:
                    a = path_num.index(i)
                    b = i.index(j)
                    path_num[a][b] = role
                    path_not_available.append(pos)
                    if player == username:
                        return challenger
                    elif player == challenger:
                        return username
                    

def check_win(path_num):
    diag_win_1 = (path_num[0][0] == path_num[1][1] == path_num[2][2])
    diag_win_2 = (path_num[0][2] == path_num[1][1] == path_num[2][0])

    first_row = (path_num[0][0] == path_num[0][1] == path_num[0][2])
    second_row = (path_num[1][0] == path_num[1][1] == path_num[1][2])
    third_row = (path_num[2][0] == path_num[2][1] == path_num[2][2])


    first_col = (path_num[0][0] == path_num[1][0] == path_num[2][0])
    second_col = (path_num[0][1] == path_num[1][1] == path_num[2][1])
    third_col = (path_num[0][2] == path_num[1][2] == path_num[2][2])

    wpos = [diag_win_1, diag_win_2, first_row, second_row, second_row, third_row, first_col, second_col, third_col]

    if True in wpos:
        return False
    else:
        return True


@client.event
async def on_ready():
    print(f"{client.user} is online")

@client.command(brief='Start the game Tic-Tac-Toe using >tictactoe @<Mention Friend>')
async def tictactoe(message, challenge):
    global turn, turn_player
    turn = ""
    turn_player = ""
    
    global username
    uname = message.author.mention
    global current_players
    global challenger
    cname = challenge
    global path_num

    current_players.append(uname)
    current_players.append(cname)

    if len(current_players)>2 and (uname != current_players[0] or cname != current_players[1]):
        await message.send(f"Sorry {uname} wait for the current game to end.")
    else:
        username = current_players[0]
        challenger = current_players[1]

        if username.__contains__("!"):
            username = username.replace("!","")

        if challenger.__contains__("!"):
            challenger = challenger.replace("!","")
        await message.send(f"{username} challenged {str(challenger)} to a game of Tic-Tac-Toe")
        path_num = [['1','2','3'], ['4','5','6'], ['7','8','9']]
        board = discord.Embed(
            description = display(path_num)
        )
        await message.send(embed = board)

@client.command(brief = "move <position>")
async def move(message, pos):
    global turn, turn_player
    global count_step
    player_ = message.author.mention
    if player_.__contains__("!"):
        player_ = player_.replace("!","")
    if turn == "":
        turn = username
    else:
        if turn_player.__contains__("!"):
            turn_player = turn_player.replace("!","")
        turn = turn_player
        print(turn_player)

    if turn == player_ == username:
        turn_player = str(player_response(pos, username, role="X"))
        if turn_player == "Invalid":
            turn_player = username
            await message.send("Invalid move try again")
        else:    
            board = discord.Embed(
                description = display(path_num)
            )
            await message.send(embed = board)
            count_step = count_step + 1
            game = check_win(path_num)
            if game: 
                if count_step >= 9:
                    print(count_step)
                    board = discord.Embed(
                        description = "This game ended draw write >tictactoe to start new game"
                    )
                    await message.send(embed = board)
                    clear_board()
                else:
                    pass
            else:
                await message.send(f"{username} wins.")
                clear_board()

    
    elif turn == player_ == challenger:
        turn_player = str(player_response(pos, challenger ,role="O"))
        if turn_player == "Invalid":
            await message.send("Invalid move try again")
            turn_player = challenger
        else:    
            board = discord.Embed(
                description = display(path_num)
            )
            await message.send(embed = board)
            count_step = count_step + 1
            game = check_win(path_num)
            if game: 
                if count_step >= 9:
                    board = discord.Embed(
                        description = "This game ended draw write >tictactoe @friendname to start new game"
                    )
                    await message.send(embed = board)
                    clear_board()
                else:
                    pass
            else:
                await message.send(f"{challenger} wins.")
                clear_board()

    else:
        await message.send("It's not your turn")

@client.command(brief = "Quit Game")
async def quit(message):
    global username
    global challenger

    clear_user_name = message.author.mention

    if clear_user_name == username or clear_user_name == challenger:
        clear_board()
        await message.send("Bye!")
    else:
        await message.send("Maintain patience")

client.run(TOKEN)
