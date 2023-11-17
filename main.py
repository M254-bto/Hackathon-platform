import streamlit as st
import requests
import pandas as pd
# import home, leaderboard, team

# Function to send requests with authorization header
def send_request(url, method='GET', data=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {st.session_state.get("key", "")}',
    }

    if method == 'GET':
        return requests.get(url, headers=headers).json()
    elif method == 'POST':
        return requests.post(url, json=data, headers=headers)

# Signup Function
def signup(username, email, password):
    url = "http://localhost:8000/register/"
    data = {'username': username, 'email': email, 'password': password}
    return requests.post(url, json=data)

# Login Function
def login(username, password):
    url = "http://localhost:8000/auth/login/"
    data = {'username': username, 'password': password}
    return requests.post(url, json=data)

# Create Team
def create_team(team_name, team_description):
    url = "http://localhost:8000/teams/"
    data = {'name': team_name, 'description': team_description}
    return send_request(url, method='POST', data=data)

# List Teams
def list_teams():
    url = "http://localhost:8000/teams/"
    return send_request(url)

# Join Team
def join_team(team_id):
    url = f"http://localhost:8000/teams/join/{team_id}/"
    return send_request(url, method='POST')

# Redirect to login after signup
# def redirect_to_login():
#     st.sidebar.success("User successfully registered!")
#     st.sidebar.radio("Choose a page", ["Login", "Main"])

# Redirect to main page after login


# def upload_file(file_content):
#     url = "http://localhost:8000/upload/"
#     files = {'file': ('dummy.txt', file_content)}
#     headers = {'Authorization': f'Token {st.session_state.get("key", "")}'}

#     response = requests.post(url, files=files, headers=headers)
#     return response

def upload_csv(filename, file_content):
    url = "http://localhost:8000/upload/"
    files = {'file': (filename, file_content)}
    headers = {'Authorization': f'Token {st.session_state.get("key", "")}',
               'Content-Disposition': f'inline ; filename={filename}'}

    response = requests.post(url, files=files, headers=headers)
    return response






# Main Function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Signup", "Login", "Main"])

    if page == "Signup":
        st.header("Signup")
        username = st.text_input("Username")
        email = st.text_input('Email')
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if username and password and email:
                signup(username, email, password)
                st.success("User successfully registered!")

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                response_data = login(username, password)
                if 'key' in response_data.content.decode():
                    st.success(f"Welcome back, {username}!")
                    st.session_state['key'] = response_data.content.decode().split('"')[3]
                    st.sidebar.radio("Choose a page", ["Home", "Leaderboard"])
                else:
                    st.error(f"Login failed: {response_data['detail']}")
    elif page == "Main":
        disp = st.sidebar.radio("Choose a page", ["Team", "Home", "Leaderboard"])
        if disp == "Team":
            st.title("This is a user dashboard")
            st.write("Here you can create a team or join a team")
            res = list_teams()
            for team in res:
                if st.button(team['name']):
                    join_team(team['id'])
                    st.success(f"Welcome to team {team['name']}!")
                    

            if st.button("create a team"):
                team_name = st.text_input("Team name")
                team_description = st.text_input("Team description")
                if st.button('Create'):
                    if team_name and team_description:
                        res = create_team(team_name, team_description)
                        st.write(res.content.decode())
                        st.success(f"Team {team_name} successfully created!")
                        
                    else:
                        st.error("Something went wrong.")

        elif disp == "Home":
            st.title("Upload submission file")
            st.write("Here you can upload your submission file")
            st.title("CSV File Upload Example")

            # CSV File Upload Widget
            csv_file_upload = st.file_uploader("Choose a CSV file", type=["csv"])

            # Upload Button
            if csv_file_upload is not None:
                if st.button("Upload CSV File"):
                    # Read the uploaded CSV file into a DataFrame
                    df = pd.read_csv(csv_file_upload)

                    # Convert DataFrame to CSV content
                    csv_content = df.to_csv(index=False)

                    # Send CSV file content to the DRF server
                    response = upload_csv(csv_file_upload.name, csv_content.encode('utf-8'))

                    # Display response
                    st.write(response.json())
        
   

if __name__ == "__main__":
    main()