import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Application title
st.title('Calculus Visualizer')

# Sidebar configuration
st.sidebar.title('Configuration')

# Get the function from the user
function_input = st.sidebar.text_input('Function', 'x**3*(x*cos(x) + 4*sin(x))')

# Create the symbolic variable
x = sp.symbols('x')

# Create dictionary for sympy to recognize the string functions
sympy_dict = {'sin':sp.sin, 'cos':sp.cos, 'tan':sp.tan, 'exp':sp.exp, 'sqrt':sp.sqrt}

# Try to parse the entered function
try:
    function = sp.sympify(function_input, locals=sympy_dict)

    # Derivative explanation
    st.subheader('What is a Derivative?')
    st.write("""
    The derivative measures how a function changes as its input changes. 
    It's a fundamental concept in calculus. Loosely speaking, a derivative 
    can be thought of as how much one quantity is changing in response to 
    changes in some other quantity; for example, the derivative of the 
    position of a moving object with respect to time is the object's velocity, 
    and the derivative of velocity with respect to time is acceleration.
    """)

    # Integral explanation
    st.subheader('What is an Integral?')
    st.write("""
    The integral, on the other hand, is the accumulation of quantities. 
    It can be interpreted as the area under a curve. In a physical sense, 
    if the derivative of a position function gives a velocity function, 
    then the integral of a velocity function gives a position function.
    """)

    # Calculate derivative and integral
    derivative = sp.diff(function, x)
    integral = sp.integrate(function, x)

    # Generate the x values
    x_values = np.linspace(-10, 10, 400)

    # Generate the y values for the function, derivative, and integral
    y_values = np.real(sp.lambdify(x, function)(x_values))
    derivative_values = np.real(sp.lambdify(x, derivative)(x_values))
    integral_values = np.real(sp.lambdify(x, integral)(x_values))

    # Draw the function
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values, label=str(function))

    # Draw the derivative
    plt.plot(x_values, derivative_values, label='Derivative')

    # Draw the integral
    plt.plot(x_values, integral_values, label='Integral')

    # Choose a point to highlight on the plot
    point = st.sidebar.slider('Select a point in the range (-10,10)', -10.0, 10.0, 0.0)
    plt.plot(point, np.real(sp.lambdify(x, function)(point)), 'ro') # red point
    plt.text(point, np.real(sp.lambdify(x, function)(point)), '({}, {})'.format(point, np.real(sp.lambdify(x, function)(point))))

    plt.legend()
    st.pyplot(plt.gcf())

except sp.SympifyError:
    st.sidebar.error('Invalid function')
