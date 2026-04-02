import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    # password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Log in"):
        st.session_state.logged_in = True
        st.session_state.user_name = username
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.user_name = None
    st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "main.py", title="Dashboard", icon=":material/dashboard:", default=True
)
# bugs = st.Page("main.py", title="Bug reports", icon=":material/bug_report:")
# alerts = st.Page(
#     "main.py", title="System alerts", icon=":material/notification_important:"
# )

history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard],  # , bugs, alerts],
            "Tools": [ history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()