import streamlit as st
import main, home, leaderboard

def teams():
    st.sidebar.radio("Choose a page", ["Home", "Leaderboard"])
    st.title("This is a user dashboard")
    st.write("Here you can create a team or join a team")
    res = main.list_teams()
    for team in res:
        if st.button(team['name']):
            main.join_team(team['id'])
            st.success(f"Welcome to team {team['name']}!")
            home.main()

    if st.button("create a team"):
        team_name = st.text_input("Team name")
        team_description = st.text_input("Team description")
        if st.button('Create'):
            if team_name and team_description:
                res = main.create_team(team_name, team_description)
                st.write(res.content.decode())
                st.success(f"Team {team_name} successfully created!")
                home.main()
            else:
                st.error("Something went wrong.")