# Complete Unedited ChatGPT Transcript

I am completing HW2: QFT / Inverse QFT Hardware Recovery.

I uploaded the assignment materials. Please complete the assignment using this student ID:

synth_hw2_trial_004

Follow the assignment instructions exactly. Fill in any missing code cells and provide the required final answers.json content. Please include all required code and any required output files described in the assignment.

Completed HW2 for student ID synth_hw2_trial_004. The notebook includes the personalized seed/configuration, QFT + inverse QFT implementation, bit-order calculations, simulator results, transpiler statistics, reflections, and JSON export. The required JSON fields match the provided schema.

Key result: logical recovered state is 100, while the reversed measurement mapping makes the displayed Qiskit bitstring 001. The assignment specifically requires accounting for classical-bit display order this way.

Files:

Download completed HW2 notebook
Download answers.json

The answers.json passed validation against the supplied schema. The IBM hardware section was left as not attempted, which is allowed because hardware execution and the QPY export are optional.

Main submitted values are seed = 187642109893800, num_qubits = 3, input [0,0,1], reversed measurement map [[0,2],[1,1],[2,0]], counts = {"001": 2048}, dominant bitstring 001, original/transpiled depth 17, and simulator operations h:6, cp:6, barrier:3, measure:3, swap:2, x:1.

answers.json
Code
---------------------------------------------------------------------------

MissingOptionalLibraryError               Traceback (most recent call last)

/tmp/ipykernel_3961/2500750226.py in <cell line: 0>()
     30 
     31 # Quick visual check
---> 32 build_qft_circuit(config["num_qubits"], inverse=False).draw("mpl")



5 frames

/usr/local/lib/python3.12/dist-packages/qiskit/utils/lazy_tester.py in require_now(self, feature)
    220         if self:
    221             return
--> 222         raise MissingOptionalLibraryError(
    223             libname=self._name, name=feature, pip_install=self._install, msg=self._msg
    224         )


MissingOptionalLibraryError: "The 'pylatexenc' library is required to use 'MatplotlibDrawer'. You can install it with 'pip install pylatexenc'."

---------------------------------------------------------------------------
NOTE: If your import is failing due to a missing package, you can
manually install dependencies using either !pip or !apt.

To view examples of installing some common dependencies, click the
"Open Examples" button below.
---------------------------------------------------------------------------

That error is just from the visual circuit drawing, not from your QFT implementation.

Add this install cell before the cell that calls .draw("mpl"):

!pip install -q pylatexenc

Then rerun the import/setup cells and this line:

build_qft_circuit(config["num_qubits"], inverse=False).draw("mpl")

Alternatively, if you don’t care about the Matplotlib circuit image, replace:

.draw("mpl")

with:

.draw("text")

The assignment only requires you to implement and run the QFT/inverse-QFT workflow; the circuit image itself is just a visual check in that cell. The required submission items are the simulator result, depths/operation counts, reflections, and answers.json.

For Colab, I’d use:

!pip install -q qiskit qiskit-aer pylatexenc

near the very top of the notebook so you don’t hit another missing-library error later.
