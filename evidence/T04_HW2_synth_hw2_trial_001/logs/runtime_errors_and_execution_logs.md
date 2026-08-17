# Runtime Errors and Execution Logs

---------------------------------------------------------------------------
MissingOptionalLibraryError               Traceback (most recent call last)
/tmp/ipykernel_670/2500750226.py in <cell line: 0>()
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
