import sys
import io
import contextlib

class CodeExecutor:
    @staticmethod
    def run_code(code_snippet):
        """
        Executes Python code string and captures standard output.
        Returns: (output: str, error: str)
        """
        # Create a buffer to capture 'print()' statements
        output_buffer = io.StringIO()
        error_message = None

        try:
            # Redirect stdout to the buffer
            with contextlib.redirect_stdout(output_buffer):
                # RESTRICTION: In a real production app, I will use Docker here.
                exec_globals = {"__builtins__": __builtins__} # Allow built-in functions
                exec(code_snippet, exec_globals)

        except Exception as e:
            # Capture runtime errors(Syntax, NameError, etc.)
            error_message = f"❌ Runtime Error: {str(e)}"


        # Get the standard output (print statements)
        execution_output = output_buffer.getvalue()

        return execution_output, error_message
    
# --- UNIT TEST ---
if __name__ == "__main__":
    test_code = """
def greet(name):
    print(f"Hello, {name}!")

greet("Vishal")
"""

    out, err = CodeExecutor.run_code(test_code)
    print(f"Output:\n{out}")
    if err: print(f"Error:\n{err}")