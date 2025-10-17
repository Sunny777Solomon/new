import streamlit as st
import random
import time

# --- Game Data ---
# The KEY is the secret full location (Hidden), the VALUE is the single Clue Word (Given to Civilians/Spy).
LOCATIONS = {
    "A crowded museum gift shop": "Statue",
    "A high school cafeteria during lunch": "Tray",
    "A rainy night market": "Lantern",
    "A busy airport lounge": "Gate",
    "A submarine control room": "Periscope",
    "An outdoor music festival": "Wristband",
    "A medieval banquet hall": "Goblet"
}
ROLES = ["Mr. White", "The Spy"] # Civilians are calculated based on remaining slots

# --- Utility Functions ---

def initialize_game_state():
    """Initializes all necessary session state variables."""
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'roles' not in st.session_state:
        st.session_state.roles = {}
    if 'location' not in st.session_state:
        st.session_state.location = "" # Holds the full secret location string
    if 'clue_word' not in st.session_state:
        st.session_state.clue_word = "" # Holds the single clue word
    if 'reveal_name' not in st.session_state:
        st.session_state.reveal_name = None
    if 'reveal_message' not in st.session_state:
        st.session_state.reveal_message = None

def add_player():
    """Adds a player name to the list if it's non-empty and unique."""
    new_name = st.session_state.player_input.strip()
    if new_name and new_name not in st.session_state.players:
        st.session_state.players.append(new_name)
        st.session_state.player_input = "" # Clear the input after adding
        st.toast(f"{new_name} joined the game!")
    elif new_name in st.session_state.players:
        st.warning(f"Player {new_name} is already added!")

def start_game():
    """Assigns roles, location, and starts the game."""
    players = st.session_state.players
    num_players = len(players)
    
    if num_players < 3:
        st.error("You need at least 3 players to start the game.")
        return

    # 1. Randomly select location (full description) and the common single clue word
    st.session_state.location, common_clue_word = random.choice(list(LOCATIONS.items()))
    st.session_state.clue_word = common_clue_word # This is the only word Civilians/Spy get
    
    # 2. Randomly assign roles
    shuffled_players = random.sample(players, num_players)
    
    # Determine how many of each role (1 Mr. White, 1 Spy, rest Civilian)
    role_distribution = {
        "Mr. White": 1,
        "The Spy": 1,
        "Civilian": num_players - 2 
    }
    
    assigned_roles = {}
    role_pool = (
        ["Mr. White"] * role_distribution["Mr. White"] +
        ["The Spy"] * role_distribution["The Spy"] +
        ["Civilian"] * role_distribution["Civilian"]
    )
    
    random.shuffle(role_pool)
    
    for i, player in enumerate(shuffled_players):
        assigned_roles[player] = role_pool[i]

    st.session_state.roles = assigned_roles
    st.session_state.game_started = True

def reset_game():
    """Clears all state and resets the game to the player entry phase."""
    st.session_state.players = []
    st.session_state.game_started = False
    st.session_state.roles = {}
    st.session_state.location = ""
    st.session_state.clue_word = ""
    st.session_state.reveal_name = None
    st.session_state.reveal_message = None

def get_role_message(player_name, role):
    """Constructs the personalized message for the player."""
    clue_word = st.session_state.clue_word
    full_location = st.session_state.location # Stored only for the Spy's goal reference
    
    if role == "Mr. White":
        return "**Your Role: Mr. White** 🕵️‍♂️\n\nYou are the imposter! You have **NO CLUE** about the single word or the location. Listen carefully, blend in, and cause confusion. Your goal is to survive the vote until only one other player remains!"
    elif role == "The Spy":
        return f"**Your Role: The Spy** 🤫\n\n**The Clue Word is:** *{clue_word}*\n\nYour mission is to deduce the full location (**'{full_location}'**) from this word and the discussion. If you guess the full location correctly (by privately telling the GM) before you are voted out, The Spy wins!"
    else: # Civilian
        return f"**Your Role: Civilian** 😇\n\n**The Clue Word is:** *{clue_word}*\n\nYour mission is to find and vote out **Mr. White**! Discuss aspects of the location related to the Clue Word, but be vague enough so Mr. White can't figure out the full location."

def show_role(player_name):
    """Sets the state to display a specific player's role and forces a re-run."""
    role = st.session_state.roles.get(player_name)
    if role:
        st.session_state.reveal_name = player_name
        st.session_state.reveal_message = get_role_message(player_name, role)
        
        # CORRECTED: Use st.rerun() to immediately update the UI
        st.rerun()

def hide_role():
    """Hides the role message and forces a re-run."""
    st.session_state.reveal_name = None
    st.session_state.reveal_message = None
    # CORRECTED: Use st.rerun() to immediately update the UI
    st.rerun()

# --- Streamlit UI ---

st.set_page_config(layout="centered", page_title="Mr. White: Social Deduction", initial_sidebar_state="collapsed")
st.title("🕵️‍♂️ Mr. White: Social Deduction Game")
initialize_game_state()

# --- Player Entry Phase ---
if not st.session_state.game_started:
    st.markdown(
        """
        ### 1. Add Players
        Enter the names of all players (including yourself) who will be playing.
        You need at least **3 players** to start.
        """
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.text_input(
            "Player Name", 
            key="player_input", 
            on_change=add_player, 
            placeholder="Type name and press Enter"
        )
    with col2:
        st.button("Add Player", on_click=add_player, type="primary", use_container_width=True)

    # Display current player list
    if st.session_state.players:
        st.subheader("Current Players:")
        st.markdown(", ".join([f"**{p}**" for p in st.session_state.players]))
    else:
        st.info("No players added yet.")

    st.markdown("---")
    
    # Start Game Button
    if len(st.session_state.players) >= 3:
        st.button(
            "🚀 Start Game and Assign Roles", 
            on_click=start_game, 
            type="primary", 
            use_container_width=True
        )
    else:
        st.button(
            "Start Game (Need More Players)", 
            disabled=True, 
            use_container_width=True
        )

# --- Game Started Phase ---
else:
    st.header("Game In Progress!")
    st.markdown(f"**Total Players:** {len(st.session_state.players)}")

    # 2. Role Reveal Section (Hot-Seat Mechanism)
    st.markdown("---")
    st.subheader("2. Player Role Check (Private)")
    st.info("Pass the device to the player whose role needs to be revealed. Once they read it, click 'Hide Role' before passing it to the next person.")

    # Dropdown to select player for role reveal
    player_to_reveal = st.selectbox(
        "Select Your Name to See Your Role:", 
        options=[""] + st.session_state.players,
        key="selected_player"
    )

    if st.session_state.reveal_name:
        # Currently revealing a role
        st.markdown(
            f"""
            <div style='background-color: #ff4b4b; padding: 20px; border-radius: 10px; color: white;'>
                <h3 style='color: white; margin-top: 0;'>PRIVATE: {st.session_state.reveal_name}'s Role</h3>
                <p style='font-size: 1.1em;'>{st.session_state.reveal_message}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.button("✅ Hide Role (Pass the Device)", on_click=hide_role, type="primary", use_container_width=True)

    elif player_to_reveal:
        # Player selected a name, prompt to show role
        st.button(
            f"👁️‍🗨️ Show Role for {player_to_reveal}", 
            on_click=lambda: show_role(player_to_reveal), 
            type="primary", 
            use_container_width=True
        )
        
    # 3. Gameplay Instructions (after all roles are known)
    if not st.session_state.reveal_name:
        st.markdown("---")
        st.subheader("3. Discussion Phase (Starts Now)")
        st.markdown(
            f"""
            #### Everyone, start discussing the location!
            
            The secret common word is: **{st.session_state.clue_word}**
            
            - **Civilians and The Spy:** Know the word and must convince others they know the full location without giving it away.
            - **Mr. White:** Knows nothing and must deduce the word and location from the discussion.
            
            All players must take a turn describing an aspect of the location that relates to the Clue Word.
            """
        )
        st.markdown("---")
        
        # Simplified Voting Panel (for manual voting after discussion)
        st.subheader("4. Voting Phase")
        st.warning("When discussion ends, use this section to manually tally and resolve the votes.")
        
        col_vote, col_reset = st.columns(2)
        with col_vote:
            vote_winner = st.selectbox(
                "Who do you suspect is Mr. White?",
                options=[""] + st.session_state.players,
                index=0,
                key="final_vote"
            )

        if vote_winner:
            # Display final reveal
            st.markdown(f"#### The vote is cast against **{vote_winner}**.")
            
            # The reveal logic
            final_role = st.session_state.roles.get(vote_winner, "Unknown")
            
            st.markdown(f"**{vote_winner}'s actual role was:** {final_role}")

            if final_role == "Mr. White":
                 st.balloons()
                 st.success(f"🎉 **Mr. White found!** The Civilians win! The full secret location was **{st.session_state.location}**.")
            elif final_role == "The Spy":
                 st.error(f"❌ **The Spy was eliminated!** The Civilians lose, as The Spy had a separate win condition, OR the game continues! The full secret location was **{st.session_state.location}**.")
            else:
                 st.error(f"😭 **You eliminated an innocent Civilian!** The game continues or Mr. White wins! The full secret location was **{st.session_state.location}**.")
            
            st.markdown("---")
        
        with col_reset:
            st.button("🔄 Reset Game", on_click=reset_game, use_container_width=True)
            
    st.markdown("---")
    st.caption("Game State (GM Eyes Only):")
    st.json({
        "Full Secret Location": st.session_state.location,
        "Common Clue Word": st.session_state.clue_word,
        "Player Roles": st.session_state.roles
    })
    
    st.button("Complete Game Reset (Exit Phase)", on_click=reset_game, use_container_width=True)