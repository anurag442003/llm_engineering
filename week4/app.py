#!/usr/bin/env python
# coding: utf-8

# # Code Generator
# 
# The requirement: use a Frontier model to generate high performance C++ code from Python code
# 

# <table style="margin: 0; text-align: left;">
#     <tr>
#         <td style="width: 150px; height: 150px; vertical-align: middle;">
#             <img src="../resources.jpg" width="150" height="150" style="display: block;" />
#         </td>
#         <td>
#             <h2 style="color:#f71;">Reminder: fetch latest code</h2>
#             <span style="color:#f71;">I'm continually improving these labs, adding more examples and exercises.
#             At the start of each week, it's worth checking you have the latest code.<br/>
#             First do a <a href="https://chatgpt.com/share/6734e705-3270-8012-a074-421661af6ba9">git pull and merge your changes as needed</a>. Any problems? Try asking ChatGPT to clarify how to merge - or contact me!<br/><br/>
#             After you've pulled the code, from the llm_engineering directory, in an Anaconda prompt (PC) or Terminal (Mac), run:<br/>
#             <code>conda env update --f environment.yml --prune</code><br/>
#             Or if you used virtualenv rather than Anaconda, then run this from your activated environment in a Powershell (PC) or Terminal (Mac):<br/>
#             <code>pip install -r requirements.txt</code>
#             <br/>Then restart the kernel (Kernel menu >> Restart Kernel and Clear Outputs Of All Cells) to pick up the changes.
#             </span>
#         </td>
#     </tr>
# </table>

# <table style="margin: 0; text-align: left;">
#     <tr>
#         <td style="width: 150px; height: 150px; vertical-align: middle;">
#             <img src="../important.jpg" width="150" height="150" style="display: block;" />
#         </td>
#         <td>
#             <h1 style="color:#900;">Important Note</h1>
#             <span style="color:#900;">
#             In this lab, I use GPT-4o and Claude-3.5-Sonnet, which are the slightly higher priced models. The costs are still low, but if you'd prefer to keep costs ultra low, please make the suggested switches to the models (3 cells down from here).
#             </span>
#         </td>
#     </tr>
# </table>

# In[1]:


# imports

import os
import io
import sys
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
import gradio as gr
import subprocess
import google.generativeai as genai

# In[2]:


# environment

load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')


# In[3]:


GeminiModel=genai.configure(api_key=google_api_key)


# In[4]:


system_message = "You are an assistant that reimplements Python code in high performance C++ for an windows 11 OS. "
system_message += "Respond only with C++ code; use comments sparingly and do not provide any explanation other than occasional comments. "
system_message += "The C++ response needs to produce an identical output in the fastest possible time."


# In[5]:


def user_prompt_for(python):
    user_prompt = "Rewrite this Python code in C++ with the fastest possible implementation that produces identical output in the least time. "
    user_prompt += "Respond only with C++ code; do not explain your work other than a few comments. "
    user_prompt += "Pay attention to number types to ensure no int overflows. Remember to #include all necessary C++ packages such as iomanip.\n\n"
    user_prompt += python
    return user_prompt


# In[6]:


def messages_for(python):
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt_for(python)}
    ]


# In[7]:


def write_output(cpp):
    code = cpp.replace("```cpp","").replace("```","")
    with open("optimized.cpp", "w") as f:
        f.write(code)


# In[8]:


def optimize_gemini(python):
    stream=genai.GenerativeModel("gemini-1.5-flash")
    prompt=f"{system_message}\n\n{messages_for(python)}"
    response=stream.generate_content(prompt,stream=True)
    result=""
    for chunks in response:
        if chunks.text:
            result+=chunks.text
            print(chunks.text,end='',flush=True)
    write_output(result)
    


# In[11]:


pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(100_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
"""


# In[12]:


exec(pi)


# In[13]:


optimize_gemini(pi)


# In[14]:


exec(pi)


# # Compiling C++ and executing
# 
# This next cell contains the command to compile a C++ file on my M1 Mac.  
# It compiles the file `optimized.cpp` into an executable called `optimized`  
# Then it runs the program called `optimized`
# 
# You can google (or ask ChatGPT!) for how to do this on your platform, then replace the lines below.
# If you're not comfortable with this step, you can skip it for sure - I'll show you exactly how it performs on my Mac.

# In[15]:

try:
    subprocess.run(['g++', '-O3', '-std=c++17', '-o', 'optimized.exe', 'optimized.cpp'], check=True)
    subprocess.run(['./optimized.exe'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during compilation or execution: {e}")


# In[16]:


optimize_gemini(pi)


# In[20]:


python_hard = """
def lcg(seed, a=1664525, c=1013904223, m=2**32):
    value = seed
    while True:
        value = (a * value + c) % m
        yield value
        
def max_subarray_sum(n, seed, min_val, max_val):
    lcg_gen = lcg(seed)
    random_numbers = [next(lcg_gen) % (max_val - min_val + 1) + min_val for _ in range(n)]
    max_sum = float('-inf')
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += random_numbers[j]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum

def total_max_subarray_sum(n, initial_seed, min_val, max_val):
    total_sum = 0
    lcg_gen = lcg(initial_seed)
    for _ in range(20):
        seed = next(lcg_gen)
        total_sum += max_subarray_sum(n, seed, min_val, max_val)
    return total_sum

# Parameters
n = 10000         # Number of random numbers
initial_seed = 42 # Initial seed for the LCG
min_val = -10     # Minimum value of random numbers
max_val = 10      # Maximum value of random numbers

# Timing the function
import time
start_time = time.time()
result = total_max_subarray_sum(n, initial_seed, min_val, max_val)
end_time = time.time()

print("Total Maximum Subarray Sum (20 runs):", result)
print("Execution Time: {:.6f} seconds".format(end_time - start_time))
"""


# In[21]:


exec(python_hard)


# In[22]:


optimize_gemini(python_hard)


# In[23]:



try:
    subprocess.run(['g++', '-O3', '-std=c++17', '-o', 'optimized.exe', 'optimized.cpp'], check=True)
    subprocess.run(['./optimized.exe'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during compilation or execution: {e}")



# In[28]:


def write_output(cpp):
    code = cpp.replace("```cpp","").replace("```","")
    with open("optimized.cpp", "w") as f:
        f.write(code)


# In[29]:


def stream_gemini(python):
    stream=genai.GenerativeModel("gemini-1.5-flash")
    prompt=f"{system_message}\n\n{messages_for(python)}"
    response=stream.generate_content(prompt,stream=True)
    result=""
    for chunks in response:
        if chunks.text:
            result+=chunks.text
            print(chunks.text,end='',flush=True)
    write_output(result)
    return result
    


# In[32]:


def optimize(python, model):
    if model=="GEMINI":
        result = stream_gemini(python)
        return result
    else:
        raise ValueError("Unknown model")
    # for stream_so_far in result:
    #     yield stream_so_far        


# In[34]:


def execute_python(code):
        try:
            output = io.StringIO()
            sys.stdout = output
            exec(code)
        finally:
            sys.stdout = sys.__stdout__
        return output.getvalue()


# In[35]:


def execute_cpp(code):
    write_output(code)
    try:
        # Windows compilation and execution commands
        compile_cmd = ["g++", "-O3", "-std=c++17", "-o", "optimized.exe", "optimized.cpp"]
        compile_result = subprocess.run(compile_cmd, check=True, text=True, capture_output=True)
        run_cmd = ["optimized.exe"]
        run_result = subprocess.run(run_cmd, check=True, text=True, capture_output=True)
        return run_result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred:\n{e.stderr}"


# In[51]:


css = """
.container { margin: 15px; padding: 15px; }
.title { text-align: center; margin-bottom: 20px; }
.code-container { 
    background: #f5f5f5; 
    border-radius: 10px; 
    padding: 15px;
    height: 500px !important;  /* Fixed height */
    overflow-y: auto !important;  /* Enable vertical scrolling */
}
.button-row { gap: 10px; }
.convert-button { background: #4CAF50 !important; }
.run-button { background: #2196F3 !important; }
.output-container { 
    border-radius: 8px;
    padding: 10px;
    margin-top: 10px;
}
.python { background-color: #306998 !important; color: white !important; }
.cpp { background-color: #00599C !important; color: white !important; }

# /* Make sure the code editors take full height */
# .code-container > div {
#     height: 100% !important;
# }
# .code-container textarea {
#     height: 100% !important;
# }
"""


# In[52]:


with gr.Blocks(css=css) as ui:
    with gr.Column(elem_classes=["container"]):
        gr.Markdown("# 🔄 Python to C++ Converter", elem_classes=["title"])
        
        # Code input section
        with gr.Row(equal_height=True):
            with gr.Column():
                gr.Markdown("### Source Code")
                python = gr.Code(
                    label="Python Code",
                    value=python_hard,
                    language="python",
                    elem_classes=["code-container"]
                )
            with gr.Column():
                gr.Markdown("### Generated Code")
                cpp = gr.Code(
                    label="C++ Code",
                    language="cpp",
                    elem_classes=["code-container"]
                )
        
        # Controls section
        with gr.Row(elem_classes=["button-row"]):
            model = gr.Dropdown(
                ["GEMINI"], 
                label="Select Model",
                value="GEMINI",
                container=False
            )
            convert = gr.Button("🔄 Convert", elem_classes=["convert-button"])
        
        gr.Markdown("### Execution Results")
        with gr.Row(equal_height=True):
            with gr.Column():
                python_run = gr.Button("▶️ Run Python", elem_classes=["run-button"])
                python_out = gr.TextArea(
                    label="Python Output",
                    elem_classes=["output-container", "python"]
                )
            with gr.Column():
                cpp_run = gr.Button("▶️ Run C++", elem_classes=["run-button"])
                cpp_out = gr.TextArea(
                    label="C++ Output",
                    elem_classes=["output-container", "cpp"]
                )

    # Event handlers
    convert.click(fn=optimize, inputs=[python, model], outputs=cpp)
    python_run.click(fn=execute_python, inputs=[python], outputs=[python_out])
    cpp_run.click(fn=execute_cpp, inputs=[cpp], outputs=[cpp_out])

ui.launch(inbrowser=True)


# In[ ]:




