import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Linear Equation Practice",
    page_icon="➗",
)

# Add a title
st.title("Linear Equation Solver")
st.subheader("Practice solving equations of the form: ax + b = c")

# Function to generate a random equation with integer solution
def generate_equation():
    # Generate a non-zero integer for 'a'
    a = random.randint(1, 10)
    if random.choice([True, False]):
        a = -a  # Make 'a' negative 50% of the time
    
    # First generate the solution (x) as an integer
    x = random.randint(-10, 10)
    
    # Generate a random value for 'b'
    b = random.randint(-20, 20)
    
    # Calculate 'c' to ensure the equation has the integer solution
    c = a * x + b
    
    # Store the values in session state
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.c = c
    st.session_state.solution = x
    
    # Return the equation as a string
    if b >= 0:
        return f"{a}x + {b} = {c}"
    else:
        return f"{a}x - {abs(b)} = {c}"

# Initialize session state if needed
if 'solution' not in st.session_state:
    st.session_state.solution = None
    st.session_state.attempts = 0
    st.session_state.feedback = ""
    st.session_state.show_solution = False
    st.session_state.can_show_solution = False
    st.session_state.user_input = None

# Button to generate a new equation
if st.button("Generate New Equation") or st.session_state.solution is None:
    equation = generate_equation()
    st.session_state.feedback = ""
    st.session_state.attempts = 0
    st.session_state.show_solution = False
    st.session_state.can_show_solution = False
    st.session_state.user_input = None

# Display the equation
if st.session_state.a >= 0:
    if st.session_state.b >= 0:
        equation_display = f"{st.session_state.a}x + {st.session_state.b} = {st.session_state.c}"
    else:
        equation_display = f"{st.session_state.a}x - {abs(st.session_state.b)} = {st.session_state.c}"
else:
    if st.session_state.b >= 0:
        equation_display = f"-{abs(st.session_state.a)}x + {st.session_state.b} = {st.session_state.c}"
    else:
        equation_display = f"-{abs(st.session_state.a)}x - {abs(st.session_state.b)} = {st.session_state.c}"

st.markdown(f"## Solve: {equation_display}")

# Input field for the answer
# Using an empty string for placeholder when value is None
placeholder = ""
if st.session_state.user_input is not None:
    user_answer = st.number_input("Enter your solution for x:", step=1, value=st.session_state.user_input)
else:
    # Use an empty container with text_input as a workaround for a blank number input
    col1, col2 = st.columns([3, 1])
    with col1:
        user_answer_str = st.text_input("Enter your solution for x:", placeholder="Enter a number...")
        if user_answer_str and user_answer_str.strip():
            try:
                user_answer = int(user_answer_str)
                st.session_state.user_input = user_answer
            except ValueError:
                st.error("Please enter a valid number")
                user_answer = 0
        else:
            user_answer = 0

# Check button
if st.button("Check Answer"):
    st.session_state.attempts += 1
    
    if user_answer == st.session_state.solution:
        st.success(f"Correct! x = {st.session_state.solution} is the right answer.")
        
        # Display solution steps
        st.markdown("### Solution Steps:")
        a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
        
        if b >= 0:
            st.markdown(f"1. Start with the equation: {a}x + {b} = {c}")
        else:
            st.markdown(f"1. Start with the equation: {a}x - {abs(b)} = {c}")
            
        st.markdown(f"2. Subtract {b} from both sides:")
        st.markdown(f"   {a}x = {c - b}")
        
        st.markdown(f"3. Divide both sides by {a}:")
        st.markdown(f"   x = {(c - b) / a} = {st.session_state.solution}")
    else:
        if st.session_state.attempts >= 2:
            st.warning(f"Not quite right. Try again! Hint: First isolate the x term, then solve for x.")
            st.session_state.can_show_solution = True
        else:
            st.error("That's not correct. Try again!")
            st.session_state.can_show_solution = False

# Show solution button - now outside the "Check Answer" button condition
if 'can_show_solution' not in st.session_state:
    st.session_state.can_show_solution = False
    
if st.session_state.can_show_solution and not st.session_state.show_solution:
    if st.button("Show Solution"):
        st.session_state.show_solution = True
            
# Show solution if requested
if st.session_state.show_solution:
    st.markdown("### Solution:")
    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    
    if b >= 0:
        st.markdown(f"1. Start with the equation: {a}x + {b} = {c}")
    else:
        st.markdown(f"1. Start with the equation: {a}x - {abs(b)} = {c}")
        
    st.markdown(f"2. Subtract {b} from both sides:")
    st.markdown(f"   {a}x = {c - b}")
    
    st.markdown(f"3. Divide both sides by {a}:")
    st.markdown(f"   x = {(c - b) / a} = {st.session_state.solution}")

# Add some tips
with st.expander("Need help solving linear equations?"):
    st.markdown("""
    ### Steps to solve linear equations of the form ax + b = c:
    
    1. Isolate the term with the variable (x) by moving all other terms to the opposite side
    2. Divide both sides by the coefficient of x
    
    Example:
    - For the equation 2x + 5 = 15:
    - Subtract 5 from both sides: 2x = 10
    - Divide both sides by 2: x = 5
    """) 