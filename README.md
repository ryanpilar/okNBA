# 

# 🏀 okNBA

---

![image](https://user-images.githubusercontent.com/102194829/189457078-66494ba8-3aea-4e46-9cf4-00078ad9b3a6.png)



---

## 👋  Introduction

okNBA is coded in Python and was created to compare ESPN Fantaasy Basketball League's against eachother. 
Based on the user's predefined categories (FA%, 3's, GP, ...categories), okNBA calcutates the relative strength of their team in relation to their opponents. It accesses your ESPN Fantasy League's information and fetch's all relevent fantasty league data, free agent data being included.

Pandas to organize the player/team statistics and matplotlib to visually chart said data. 

## 🤷‍♂️  Who is this for? 

- It's for people that don't know a thing about basketball and don't want to end up last place in their fantasy pool

---

## 💪  Packages/Dependencies/Sources used 

beautifulsoup4 | pytz | random | requests | datetime | numpy | matplotlib | pandas | statistics | unicodedata | pickle  

- espn_api (https://github.com/cwendt94/espn-api) 
- basketball0reference.com

---

## 🖥  How to run

Navigate to ClassData_Center.py and input your ESPN credentials. 
Then, open BETA.ipynb and run/install dependencies that you do not have. BETA will:

1. create a data scructure that will hold all active players and their corresponding stats
2. rank order every stat for every player. There are 9 stats to consider
3. sign into your espn_fantasy league
4. get roster data for every fantasy team
5. rank order fantasy teams according to the metrics/categories
5. make analytic comparisons of players and teams

---

## 🔨  Improvements on the Application

- a dynamic and responsive UI. Integrate a charts library. 
- categories are currently hardcoded and need to be updated as per leauges changing. you can find them hardcoded in espn_scrapper.py
- finda an accurate singular data source.
- currently, there is no dependency architecture

## 🍪  Things to add

Obtain your ESPN cookies! ESPN_S2 and SWID cookie are values needed to authenticate your private fantasy sports leagues. Go find them!

 ---
 
 Have fun testing and improving it! 😎
