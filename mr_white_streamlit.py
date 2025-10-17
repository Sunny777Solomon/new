import streamlit as st
import random
import time

# --- Game Data (Common Word : Similar/Spy Word) ---
# Total of 200 pairs for high replayability.
WORD_SETS = {
    # 1. Nature/Geography
    "Ocean": "Sea",
    "River": "Stream",
    "Mountain": "Hill",
    "Desert": "Tundra",
    "Forest": "Woods",
    "Lake": "Pond",
    "Island": "Peninsula",
    "Rain": "Drizzle",
    "Snow": "Sleet",
    "Sun": "Star",
    "Moon": "Orbit",
    "Wave": "Tide",
    "Sand": "Gravel",
    "Mist": "Fog",
    "Canyon": "Gorge",
    "Volcano": "Geyser",
    "Swamp": "Marsh",
    "Cave": "Grotto",
    "Seed": "Spore",
    "Flower": "Blossom",
    "Ice": "Frost",
    "Horizon": "Sky",
    "Globe": "Map",
    "Oasis": "Well",
    "Jungle": "Savannah",
    "Boulder": "Pebble",
    # 2. Food/Drink
    "Apple": "Pear",
    "Bread": "Toast",
    "Cheese": "Butter",
    "Milk": "Cream",
    "Soup": "Broth",
    "Salad": "Coleslaw",
    "Noodle": "Spaghetti",
    "Pizza": "Calzone",
    "Steak": "Chop",
    "Muffin": "Scone",
    "Cookie": "Biscuit",
    "Juice": "Nectar",
    "Wine": "Grog",
    "Soda": "Fizzy",
    "Chili": "Curry",
    "Rice": "Quinoa",
    "Lemon": "Lime",
    "Tomato": "Pepper",
    "Oatmeal": "Cereal",
    "Sauce": "Gravy",
    "Sugar": "Honey",
    "Cake": "Pie",
    "Bacon": "Ham",
    "Fries": "Chips",
    "Ketchup": "Mustard",
    # 3. Objects/Tools
    "Hammer": "Mallet",
    "Screwdriver": "Wrench",
    "Saw": "Blade",
    "Clock": "Watch",
    "Chair": "Stool",
    "Table": "Desk",
    "Lamp": "Lantern",
    "Book": "Journal",
    "Pencil": "Crayon",
    "Scissors": "Shears",
    "Wire": "Cable",
    "Nail": "Screw",
    "Rope": "String",
    "Battery": "Cell",
    "Mirror": "Glass",
    "Key": "Lock",
    "Magnet": "Iron",
    "Ladder": "Step",
    "Helmet": "Cap",
    "Glove": "Mitt",
    "Radio": "Speaker",
    "Phone": "Tablet",
    "Wallet": "Purse",
    "Camera": "Lens",
    "Bucket": "Pail",
    # 4. Clothing/Accessories
    "Shirt": "Blouse",
    "Pants": "Trousers",
    "Shoe": "Boot",
    "Sock": "Stocking",
    "Scarf": "Shawl",
    "Hat": "Bonnet",
    "Jacket": "Coat",
    "Vest": "Waistcoat",
    "Belt": "Sash",
    "Tie": "Ascot",
    "Ring": "Band",
    "Necklace": "Pendant",
    "Bracelet": "Bangle",
    "Glasses": "Spectacles",
    "Zipper": "Button",
    "Pocket": "Cuff",
    "Hood": "Collar",
    "Denim": "Tweed",
    "Silk": "Satin",
    "Cape": "Cloak",
    "Wig": "Toupee",
    "Watch": "Bangle",
    "Jeans": "Overalls",
    "Sandal": "Flip-flop",
    "Towel": "Robe",
    # 5. Animals/Insects
    "Dog": "Wolf",
    "Cat": "Kitten",
    "Lion": "Tiger",
    "Bear": "Cub",
    "Eagle": "Hawk",
    "Shark": "Whale",
    "Snake": "Viper",
    "Frog": "Toad",
    "Bee": "Wasp",
    "Spider": "Tarantula",
    "Mouse": "Rat",
    "Goat": "Sheep",
    "Horse": "Pony",
    "Cow": "Bull",
    "Pig": "Boar",
    "Chicken": "Rooster",
    "Duck": "Goose",
    "Monkey": "Ape",
    "Rabbit": "Hare",
    "Deer": "Elk",
    "Snail": "Slug",
    "Ant": "Termite",
    "Fly": "Mosquito",
    "Lizard": "Newt",
    "Pelican": "Seagull",
    # 6. Concepts/Emotions
    "Joy": "Bliss",
    "Fear": "Dread",
    "Anger": "Rage",
    "Sadness": "Grief",
    "Love": "Affection",
    "Hate": "Dislike",
    "Truth": "Fact",
    "Lie": "Deceit",
    "Time": "Hour",
    "Space": "Void",
    "Idea": "Concept",
    "Dream": "Vision",
    "Wisdom": "Knowledge",
    "Fame": "Glory",
    "Power": "Might",
    "Wealth": "Riches",
    "Health": "Vigor",
    "Silence": "Quiet",
    "Noise": "Clatter",
    "Future": "Destiny",
    "Past": "History",
    "Chance": "Luck",
    "Humor": "Wit",
    "Aura": "Vibe",
    "Mystery": "Secret",
    # 7. Places/Buildings
    "House": "Cottage",
    "Apartment": "Flat",
    "School": "Academy",
    "Hospital": "Clinic",
    "Office": "Cubicle",
    "Store": "Shop",
    "Library": "Archives",
    "Church": "Chapel",
    "Castle": "Fortress",
    "Tower": "Spire",
    "Bridge": "Viaduct",
    "Tunnel": "Underpass",
    "Street": "Avenue",
    "Park": "Plaza",
    "Garden": "Nursery",
    "Museum": "Gallery",
    "Stadium": "Arena",
    "Hotel": "Inn",
    "Factory": "Mill",
    "Airport": "Hangar",
    "Bank": "Vault",
    "Dock": "Pier",
    "Farm": "Ranch",
    "Market": "Bazaar",
    "Theater": "Opera",
    # 8. Activities/Sports
    "Running": "Jogging",
    "Swimming": "Diving",
    "Jumping": "Leaping",
    "Throwing": "Pitching",
    "Writing": "Typing",
    "Reading": "Skimming",
    "Singing": "Humming",
    "Dancing": "Ballet",
    "Cooking": "Baking",
    "Driving": "Steering",
    "Sailing": "Rowing",
    "Fishing": "Angling",
    "Chess": "Checkers",
    "Poker": "Blackjack",
    "Basketball": "Netball",
    "Football": "Soccer",
    "Tennis": "Badminton",
    "Skiing": "Sledding",
    "Hiking": "Trekking",
    "Painting": "Sketching",
    "Whispering": "Murmuring",
    "Shouting": "Yelling",
    "Climbing": "Scrambling",
    "Listening": "Hearing",
    "Thinking": "Pondering",
    # Additional Diverse Pairs (200 total)
    "Metal": "Alloy",
    "Copper": "Bronze",
    "Fjord": "Inlet",
    "Chalet": "Cabin",
    "Novel": "Fable",
    "Poem": "Verse",
    "Camera": "Flash",
    "Engine": "Motor",
    "Gasoline": "Petrol",
    "Tire": "Rubber",
    "Wheel": "Axle",
    "Helmet": "Visor",
    "Shield": "Buckler",
    "Sword": "Dagger",
    "Armor": "Chainmail",
    "Soldier": "Trooper",
    "General": "Colonel",
    "Flag": "Banner",
    "Anthem": "Pledge",
    "Currency": "Coin",
    "Check": "Bill",
    "Debt": "Loan",
    "Profit": "Yield",
    "Taxes": "Tariff",
    "Court": "Jury",
    "Judge": "Magistrate",
    "Verdict": "Rulings",
    "Crime": "Felony",
    "Punish": "Jail",
    "Garden": "Hedge",
    "Bush": "Shrub",
    "Tree": "Sapling",
    "Branch": "Twig",
    "Root": "Stem",
    "Aroma": "Scent",
    "Perfume": "Cologne",
    "Soap": "Lather",
    "Shampoo": "Rinse",
    "Comb": "Brush",
    "Toothpaste": "Mouthwash",
    "Pillow": "Cushion",
    "Blanket": "Quilt",
    "Mattress": "Foam",
    "Candle": "Wick",
    "Stove": "Oven",
    "Microwave": "Toaster",
    "Coffee": "Espresso",
    "Latte": "Cappuccino",
    "Lemonade": "Cider",
    "Whiskey": "Bourbon",
    "Beer": "Ale",
    "Riddle": "Puzzle",
    "Maze": "Labyrinth",
    "Clue": "Hint",
    "Search": "Seek",
    "Find": "Discover",
    "Create": "Invent",
    "Destroy": "Ruin",
    "Grow": "Blossom",
    "Shrink": "Dwindle",
    "Speak": "Articulate",
    "Listen": "Heed",
    "Wander": "Stroll",
    "Sprint": "Dash",
    "Shine": "Glow",
    "Fade": "Dim",
    "Heavy": "Bulky",
    "Light": "Feather",
    "Warm": "Tepid",
    "Cold": "Chilly",
    "Smooth": "Sleek",
    "Rough": "Coarse",
    "Sharp": "Pointy",
    "Dull": "Blunt",
    "Sweet": "Syrup",
    "Sour": "Tart",
    "Bitter": "Acrid",
    "Salty": "Brine",
    "Wet": "Moist",
    "Dry": "Arid",
    "Vast": "Huge",
    "Tiny": "Micro",
    "Fast": "Rapid",
    "Slow": "Turtle",
    "Up": "Above",
    "Down": "Below",
    "Inside": "Within",
    "Outside": "Exterior",
    "Begin": "Initiate",
    "End": "Cease",
    "Day": "Dawn",
    "Night": "Dusk",
    "Friend": "Ally",
    "Enemy": "Foe",
    "Leader": "Captain",
    "Follower": "Aide",
    "Work": "Labor",
    "Rest": "Nod",
    "Help": "Assist",
    "Hurt": "Ache"
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
    if 'common_word' not in st.session_state:
        st.session_state.common_word = "" # Word given to Civilians
    if 'spy_word' not in st.session_state:
        st.session_state.spy_word = "" # Word given to The Spy
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
    """Assigns roles and the two secret words."""
    players = st.session_state.players
    num_players = len(players)
    
    if num_players < 3:
        st.error("You need at least 3 players to start the game.")
        return

    # 1. Randomly select the Common Word and the Similar/Spy Word
    # Check if we have enough words for the number of games played.
    if not WORD_SETS:
        st.error("Error: The word list is empty. Please add words to the WORD_SETS dictionary.")
        return

    st.session_state.common_word, st.session_state.spy_word = random.choice(list(WORD_SETS.items()))
    
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
    st.session_state.common_word = ""
    st.session_state.spy_word = ""
    st.session_state.reveal_name = None
    st.session_state.reveal_message = None

def get_role_message(player_name, role):
    """Constructs the personalized message for the player based on their role."""
    common_word = st.session_state.common_word
    spy_word = st.session_state.spy_word
    
    if role == "Mr. White":
        return "**Your Role: Mr. White** 🕵️‍♂️\n\n- **Your Word:** **[NONE]**\n\nYou are the imposter! Your goal is to figure out the **Common Word** and blend in by pretending you know it. Watch out for the Spy, who has a similar but different word!"
    elif role == "The Spy":
        return f"**Your Role: The Spy** 🤫\n\n- **Your Word:** **{spy_word}**\n\nYour word is SIMILAR to the common word ({common_word}), but DIFFERENT. Your mission is to deduce the **Common Word** that the Civilians have. Be vague to sound like a Civilian, but try to figure out the **Common Word**! (Private guess to the GM wins the game)."
    else: # Civilian
        return f"**Your Role: Civilian** 😇\n\n- **Your Word:** **{common_word}**\n\nYour mission is to find and vote out **Mr. White** (who has no word) and **The Spy** (who has a similar word). Discuss your word, but avoid saying it directly!"

def show_role(player_name):
    """Sets the state to display a specific player's role and forces a re-run."""
    role = st.session_state.roles.get(player_name)
    if role:
        st.session_state.reveal_name = player_name
        st.session_state.reveal_message = get_role_message(player_name, role)
        st.rerun()

def hide_role():
    """Hides the role message and forces a re-run."""
    st.session_state.reveal_name = None
    st.session_state.reveal_message = None
    st.rerun()

# --- Streamlit UI ---

st.set_page_config(layout="centered", page_title="Mr. White: Word Deduction", initial_sidebar_state="collapsed")
st.title("🕵️‍♂️ Mr. White: Word Deduction Game")
st.markdown("A simple, single-device game of word association, deduction, and deceit.")
initialize_game_state()

# --- Player Entry Phase ---
if not st.session_state.game_started:
    st.markdown(
        """
        ### 1. Add Players
        Enter the names of all players (hot-seat style).
        You need at least **3 players** (1 Mr. White, 1 The Spy, 1 Civilian).
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
            "🚀 Start Game and Assign Words", 
            on_click=start_game, 
            type="primary", 
            use_container_width=True
        )
    else:
        st.button(
            f"Start Game (Need {3 - len(st.session_state.players)} more player(s))", 
            disabled=True, 
            use_container_width=True
        )

# --- Game Started Phase ---
else:
    st.header("Game In Progress!")
    st.markdown(f"**Total Players:** {len(st.session_state.players)}")

    # 2. Role Reveal Section (Hot-Seat Mechanism)
    st.markdown("---")
    st.subheader("2. Player Word Check (Private)")
    st.info("⚠️ **Pass the device only to the selected player.** Click 'Hide Word' immediately after they read it.")

    # Dropdown to select player for role reveal
    player_to_reveal = st.selectbox(
        "Select Your Name to See Your Word:", 
        options=[""] + st.session_state.players,
        key="selected_player"
    )

    if st.session_state.reveal_name:
        # Currently revealing a role
        st.markdown(
            f"""
            <div style='background-color: #ff4b4b; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 1.2em;'>
                <h3 style='color: white; margin-top: 0;'>PRIVATE: {st.session_state.reveal_name}'s Role & Word</h3>
                <p style='font-size: 1.1em;'>{st.session_state.reveal_message.replace('\n', '<br>')}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.button("✅ Hide Word (Pass the Device)", on_click=hide_role, type="primary", use_container_width=True)

    elif player_to_reveal:
        # Player selected a name, prompt to show role
        st.button(
            f"👁️‍🗨️ Show Word for **{player_to_reveal}**", 
            on_click=lambda: show_role(player_to_reveal), 
            type="primary", 
            use_container_width=True
        )
        
    # 3. Gameplay Instructions (after all roles are known)
    if not st.session_state.reveal_name:
        st.markdown("---")
        st.subheader("3. Discussion Phase (Starts Now)")
        st.markdown(
            """
            The words have been assigned! Begin the discussion by describing your word vaguely.
            
            - **Civilians:** Collaborate to find the imposters.
            - **The Spy:** Try to sound like a Civilian while figuring out their Common Word.
            - **Mr. White:** Try to fool everyone!
            """
        )
        st.markdown("---")
        
        # Simplified Voting Panel (for manual voting after discussion)
        st.subheader("4. Voting Phase")
        st.warning("Once the discussion ends, choose a player to vote out. Their role will be revealed.")
        
        col_vote, col_reset = st.columns(2)
        with col_vote:
            vote_winner = st.selectbox(
                "Who do you suspect is an imposter (Mr. White or The Spy)?",
                options=[""] + st.session_state.players,
                index=0,
                key="final_vote"
            )

        if vote_winner:
            # Display final reveal
            st.markdown(f"#### The vote is cast against **{vote_winner}**.")
            
            final_role = st.session_state.roles.get(vote_winner, "Unknown")
            
            st.markdown(f"**{vote_winner}'s actual role was:** **{final_role}**")
            
            if final_role == "Mr. White":
                 st.balloons()
                 st.success(f"🎉 **Mr. White found!** The Civilians win! The common word was **{st.session_state.common_word}**.")
            elif final_role == "The Spy":
                 st.success(f"✅ **The Spy was eliminated!** The Civilians successfully defended their word! The common word was **{st.session_state.common_word}** (The Spy had **{st.session_state.spy_word}**).")
            else: # Civilian
                 st.error(f"😭 **You eliminated an innocent Civilian!** The common word was **{st.session_state.common_word}**. The game continues or Mr. White wins!")
            
            st.markdown("---")
        
        with col_reset:
            st.button("🔄 Reset Game", on_click=reset_game, use_container_width=True)
            
    st.markdown("---")
    st.caption("Game State (GM Reference - Hidden during play):")
    st.json({
        "Common Word (Civilian)": st.session_state.common_word,
        "Similar Word (The Spy)": st.session_state.spy_word,
        "Player Roles": st.session_state.roles
    })
    
    st.button("Complete Game Reset (Exit Phase)", on_click=reset_game, use_container_width=True)